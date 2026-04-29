from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from rag.embedder import load_embeddings
from rag.vector_store import create_vectorestore 
from data.job_roles import docs
from rag.retriever import retrieve_role_info
from utils.skill_extractor import extract_skill
from data.all_skills import all_skills
from utils.readiness_scorer import calculate_readiness
from data.role_weights import role_skill_weights



resume_text=extract_text_from_pdf("sample_resume.pdf")
cleand=clean_text(resume_text)
resume_skills=set(extract_skill(cleand,all_skills))


embeddings=load_embeddings() 
vectorstore=create_vectorestore(docs,embeddings)

target_role=input("Enter your target job role:").strip().lower()

retrieved_docs=retrieve_role_info(target_role,vectorstore)

role_text=retrieved_docs[0].page_content


role_skills=set(extract_skill(role_text,all_skills))

matched_skills=role_skills.intersection(resume_skills)

missing_skills=role_skills-resume_skills

if len(role_skills)>0:
    basic_match_score=(len(matched_skills)/len(role_skills))*100

else:
    basic_match_score=0



## READINESS ANALYSIS:
role_key=target_role
weighted_result=None 

if role_key in role_skill_weights:
    weighted_result=calculate_readiness(resume_skills,role_skill_weights[role_key])


print("\n"+ "="*100)

print("Target Role:")
print(target_role)

print("Retrieved Role Description:")
print(role_text)

print("\nRole Required Skills:")
print(role_skills)

print("\nYour Resume Skills:")
print(resume_skills)

print("\nMatched Skills:")
print(matched_skills)

print("\nMissing Skills:")
print(missing_skills)

print(f"\nMatch Score: {basic_match_score:.2f}%")



## ADVANCED WEIGHTED OUTPUT 

if weighted_result:
    print("\n" + "="*100)
    print("ADVANCED ROLE_BASED READINESS ANALYSIS")
    print("="*100)

    #core skills 

    print("\ncore skills Matched:")
    print(weighted_result["core_matched"])

    print("\nMissing Core Skills:")
    print(weighted_result["missing_core"])


    print(
        f"\ncore score contribution:"
        f"{weighted_result['core_score']}/60"
    )

    #Secondary skills 

    print("\nSecondary Skills Matched:")
    print(weighted_result["secondary_matched"])

    print("\nMissing Secondary Skills:")
    print(weighted_result["missing_secondary"])

    print(f"\nsecondary score contribution:"
          f"{weighted_result['secondary_score']}/30")
    

    #Advanced Skills 

    print("\nAdvanced Skills Matched:")
    print(weighted_result["advanced_matched"])

    print("\nMissing advanced Skills:")
    print(weighted_result["missing_advanced"])

    print(f"\nadvanced score contribution:"
          f"{weighted_result['advanced_score']}/10")
    


    readiness_score = weighted_result[
        "readiness_score"
    ]

    print(
        f"\nFinal Career Readiness Score: "
        f"{readiness_score:.2f}%"
    )

    # -------------------------
    # Candidate Classification
    # -------------------------
    if readiness_score >= 85:
        status = "Highly Job Ready"

    elif readiness_score >= 70:
        status = "Job Ready"

    elif readiness_score >= 50:
        status = "Moderate Readiness"

    else:
        status = "Significant Skill Gap"

    print(f"\nCandidate Status: {status}")

    



    print("\nCareer Recommendation:")

    if readiness_score >= 85:
        print(
            "You are highly competitive for this role. "
            "Focus on portfolio, projects, and interview preparation."
        )

    elif readiness_score >= 70:
        print(
            "You are job-ready. Strengthening secondary "
            "and advanced skills can improve competitiveness."
        )

    elif readiness_score >= 50:
        print(
            "You have foundational readiness, but significant "
            "upskilling is recommended before aggressively applying."
        )

    else:
        print(
            "You currently have major skill gaps. "
            "Prioritize core skills first."
        )


print("\n" + "=" * 100)
print("END OF REPORT")
print("=" * 100)
    


    

    




    


