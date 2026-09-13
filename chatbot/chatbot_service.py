class MemoryManager:
    def __init__(self):

        self.memory=[]



    def add_message(self,role,content):

        self.memory.append({
            "role":role,
            "content":content
        })


    def get_memory_context(self):

        context=""

        for message in self.memory:

            context+=(
                f"{message['role']}:"
                f"{message['content']}\n"
            )


        return context
    

import faiss 
import numpy as np

from sentence_transformers import SentenceTransformer



class RAGEngine:

    def __init__(self):

        self.embedding_model=(SentenceTransformer("all-MiniLM-L6-v2"))


        self.documents=[]


        self.index=faiss.IndexFlatL2(384)


    def chunk_text(self,text,chunk_size=300):

            chunks=[]

            for i in range(0,len(text),chunk_size):

                chunks.append(text[i:i+chunk_size])


            return chunks
        



    def add_document(self,text):

            chunks=self.chunk_text(text)

            self.documents.extend(chunks)

            embeddings=self.embedding_model.encode(chunks)

            self.index.add(embeddings)



    def retrieve_context(self,query,top_k=3):

            if len(self.documents)==0:
                return ""
            

            query_embedding=(
                self.embedding_model.encode([query])
            )


            query_embedding=np.array(query_embedding).astype("float32")


            distance,indices=(self.index.search(query_embedding,top_k))


            retrieved_chunks=[]

            for idx in indices[0]:

                if idx<len(self.documents):

                    retrieved_chunks.append(self.documents[idx])


            return "\n".join(retrieved_chunks)


class PromptBuilder:

    def build_chat_prompt(self,user_message,memory_context="",rag_context=""):


        prompt=f"""


        You are PrepNexus AI,
        an expert AI career Assistant.

        Your responsibilities:
        - Career guidence
        -Resume optimization
        -ATS improvement
        -Skill recomendations
        -Learning roadmap
        -Interview preparation
        -Project suggestions 


    Previous Conversations:
    {memory_context}


    Retrieved Knowledge:
    {rag_context}


    User Question:
    {user_message}


    Instructions:

    - Give professional answers
    - Keep answers beginner-friendly 
    - Be practical
    - Use structured responses
    - Use bullet points with helpful





               """
        
        return prompt



from utils.structured_output import call_gemini_structured, ChatbotStructuredResponse


class PrepNexusChatbot:

    def __init__(self, model):
        self.model = model
        self.prompt_builder = PromptBuilder()
        self.memory_manager = MemoryManager()
        self.rag_engine = RAGEngine()

    def add_document(self, text):
        self.rag_engine.add_document(text)

    def get_response(self, user_message):
        try:
            memory_context = self.memory_manager.get_memory_context()
            rag_context = self.rag_engine.retrieve_context(user_message)
            final_prompt = self.prompt_builder.build_chat_prompt(user_message, memory_context, rag_context)

            if self.model is None:
                return f"🤖 **PrepNexus AI**: Thanks for your question about *{user_message}*! Configure your GEMINI_API_KEY to unlock full personalized career guidance."

            # Structured Output generation
            structured_prompt = f"""
            {final_prompt}

            Return JSON matching this schema:
            {{
              "summary": "Direct concise answer...",
              "key_takeaways": ["Takeaway 1", "Takeaway 2"],
              "action_plan": ["Action 1", "Action 2"],
              "recommended_resources": ["Resource or tool 1"],
              "followup_questions": ["Question 1"]
            }}
            """

            structured = call_gemini_structured(self.model, structured_prompt, schema_class=ChatbotStructuredResponse)

            if structured and isinstance(structured, dict) and structured.get("summary"):
                lines = []
                lines.append(f"### 🎯 Summary\n{structured['summary']}")

                if structured.get("key_takeaways"):
                    lines.append("\n### 💡 Key Takeaways")
                    for pt in structured["key_takeaways"]:
                        lines.append(f"- {pt}")

                if structured.get("action_plan"):
                    lines.append("\n### 🚀 Action Plan")
                    for idx, step in enumerate(structured["action_plan"], 1):
                        lines.append(f"{idx}. {step}")

                if structured.get("recommended_resources"):
                    lines.append("\n### 📚 Recommended Resources")
                    for res in structured["recommended_resources"]:
                        lines.append(f"- {res}")

                if structured.get("followup_questions"):
                    lines.append("\n---\n*Suggested next question:* " + structured["followup_questions"][0])

                bot_response = "\n".join(lines)
            else:
                response = self.model.generate_content(final_prompt)
                bot_response = getattr(response, "text", "I'm sorry, I couldn't process your request.")

            self.memory_manager.add_message("assistant", bot_response)
            return bot_response

        except Exception as e:
            return f"❌ Error generating response: {str(e)}"