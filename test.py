from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from rag.embedder import load_embeddings
from rag.vector_store import create_vectorestore 
from data.job_roles import docs
from rag.retriever import retrieve_role_info
'''
resume_text=extract_text_from_pdf("sample_resume.pdf")
cleand=clean_text(resume_text)
print("ORIGINAL\n",resume_text[:100])
print("CLEAND\n",cleand[:100])
'''

embeddings=load_embeddings() 
vectorstore=create_vectorestore(docs,embeddings)

role="Machine Learning Engineer"

results=retrieve_role_info(role,vectorstore)

print("Retrieved Role Requirements:\n")

for result in results:
    print(result.page_content)



