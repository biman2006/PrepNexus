from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from rag.embedder import load_embeddings
from rag.vector_store import create_vectorestore 
from data.job_roles import docs
from rag.retriever import retrieve_role_info
from utils.skill_extractor import extract_skill
from data.all_skills import all_skills

resume_text=extract_text_from_pdf("sample_resume.pdf")
cleand=clean_text(resume_text)
resume_skills=set(extract_skill(cleand,all_skills))


embeddings=load_embeddings() 
vectorstore=create_vectorestore(docs,embeddings)

target_role=input("Enter your target job role:")

retrieved_docs=retrieve_role_info(target_role,vectorstore)

role_text=retrieved_docs[0].page_content


role_skills=set(extract_skill(role_text,all_skills))

matched_skills=role_skills.intersection(resume_skills)

missing_skills=role_skills-resume_skills

if len(role_skills)>0:
    match_score=(len(matched_skills)/len(role_skills))*100

else:
    match_score=0


print("\n"+ "="*100)

print("Target Role:")
print(target_role)

print("\nRole Required Skills:")
print(role_skills)

print("\nYour Resume Skills:")
print(resume_skills)

print("\nMatched Skills:")
print(matched_skills)

print("\nMissing Skills:")
print(missing_skills)

print(f"\nMatch Score: {match_score:.2f}%")


