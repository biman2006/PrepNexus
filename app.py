import streamlit as st
import tempfile 
import os 
from PIL import Image

from utils.pdf_parser import extract_text_from_pdf 
from utils.text_cleaner import clean_text 
from utils.skill_extractor import extract_skill 
from utils.readiness_scorer import calculate_readiness

from rag.embedder import load_embeddings 
from rag.retriever import retrieve_role_info 
from rag.vector_store import create_vectorestore 

from data.all_skills import all_skills 
from data.job_roles import docs 
from data.role_weights import role_skill_weights 


Icon=Image.open("icon.png")


st.set_page_config(
    page_title="PrepNexus",
    page_icon=Icon,
    layout="wide"
)

logo=Image.open("logo.png")


col1,col2,col3=st.columns([1,2,1])

with col2:
    st.image(
        logo,
        width=620
    )

st.title("🚀 PrepNexus Interview Preparation Platform")

st.subheader(
    "Analyze your resume, compare with job roles, "
    "identify missing skills, and measure your career readiness."
)


## LOAD VECTORSTORE 

@st.cache_resource
def load_vectorstore():
    embeddings=load_embeddings()

    vectorstore=create_vectorestore(
        docs,
        embeddings
    )

    return vectorstore

vectorstore=load_vectorstore() 


## SIDEBAR 

st.sidebar.image(
    logo,
    width=220
)

st.sidebar.markdown("## 🚀PrepNexus")

st.sidebar.markdown(
    "Career Intelligence Platform"
)

#INPUT SECTION 

st.markdown("---")

st.markdown("## 📄 Upload Your Resume ")

upload_file=st.file_uploader(
    "Upload PDF Resume",
    type=["pdf"]
)

st.markdown("## 🎯 Select Your Target Job Role ")

available_roles=sorted(
    list(role_skill_weights.keys())
)

target_role=st.selectbox(
    "choose your desired role",
    available_roles
)

analyze=st.button(
    "🔍 Analyze Resume"
)

# MAIN ANALYSIS 

if analyze:

    if upload_file is None:
        st.warning("Please upload your resume PDF first")

    else:


        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:
            
            tmp_file.write(
                upload_file.read()
            )

            temp_pdf_path=tmp_file.name


        # RESUME PROCESSING 

        resume_text=extract_text_from_pdf(
            temp_pdf_path
        )

        cleaned_resume=clean_text(
            resume_text
        )

        resume_skills=set(
            extract_skill(
                cleaned_resume,
                all_skills
            )
        )

        #ROLE RETRIEVAL 

        retrieved_docs=retrieve_role_info(
            target_role,
            vectorstore
        )

        role_text=retrieved_docs[0].page_content

        role_skills=set(
            extract_skill(
                role_text,
                all_skills
            )
        )


        #BASIC MATCH SCORE 

        matched_skills=role_skills.intersection(resume_skills)

        missing_skills=(
            role_skills-resume_skills
        )

        if len(role_skills)>0:

            basic_match_score=(
                len(matched_skills)/len(role_skills)
            )*100

        else:
            basic_match_score=0


        weighted_result=calculate_readiness(
            resume_skills,
            role_skill_weights[target_role]
        )

        readiness_score=weighted_result[
            "readiness_score"
        ]


        if readiness_score>=85:
            status="Highly Job Ready"

        elif readiness_score>=70:
            status="Job Ready"

        elif readiness_score>=50:
            status="Moderate Readiness"

        else:
            status="Significant Skill Gap"



        #RESULT DASHBOARD 

        st.markdown("---")

        st.success(
            "Resume Analysis Complete"
        )


        col1,col2,col3=st.columns([1,1,1])

        with col1:
            st.metric(
                "ATS Match Score",
                f"{basic_match_score:.2f}%"
            )

        with col2:
            st.metric(
                "Interview Readiness Score",
                f"{readiness_score:.2f}%"
            )

        with col3:
            st.metric(
                "Candidate Status",
                status
            )


            st.subheader(
                "📊 Performance Dashboard"
            )

            st.write("ATS Match Score")
            st.progress(
                int(basic_match_score)
            )

            st.write("Career Readiness Score")
            st.progress(
                int(readiness_score)
            )


            st.subheader(
                "🎯 Retrieved Job Role Description"
            )

            st.write(role_text)


            st.subheader("🧠 Your Resume Skills")
            st.write(
                sorted(resume_skills)
            )

            st.subheader("📌 Required Skills")
            st.write(
                sorted(role_skills)
            )

            st.subheader("✅ Matched Skills")
            st.write(
                sorted(matched_skills)
            )

            st.subheader("❌ Missing Skills")
            st.write(
                sorted(missing_skills)
            )


            st.subheader(
                "🚀 Advanced Readiness Breakdown"
            )

            col4,col5,col6=st.columns(3)

            with col4:
                st.markdown(
                    "### Core Skills"
                )

                st.write(
                    "Matched:",
                    sorted(weighted_result["core_matched"])
                )

                st.write(
                    "Missing:",
                    sorted(
                        weighted_result["missing_core"]
                    )
                )


                with col5:
                    st.markdown(
                        "### Secondary Skills"
                    )

                    st.write("Matched:",
                             sorted(weighted_result["secondary_matched"]))
                    

                    st.write("Missing:",
                             sorted(weighted_result["missing_secondary"]))
                    

                    with col6:
                        st.markdown(
                            "### Advanced Skills"
                        )

                        st.write(
                            "Matched:",
                            sorted(
                                weighted_result["advanced_matched"]
                            )
                        )

                        st.write(
                            "Missing:",
                            sorted(
                                weighted_result["missing_advanced"]
                            )

                        )




                        st.subheader("📈 Career Recommendation")

                        if readiness_score>=85:

                            st.success(
                                "You are highly competitive for this role "
                                "Focus on projects, portfolio, and interview mastery"
                            )

                        elif readiness_score>=70:
                            st.info(
                                "You are job-ready. Imporoving secondary "
                                "and advanced skills will increase competitiveness"
                            )

                        elif readiness_score>=50:
                            st.warning(
                                "You have moderate readiness."
                                "Focus on missing core skills first"
                            )

                        else:

                            st.error(
                                """
                                 Significant skill gap detected.
                                 Prioritize foundational core skill development.
                                
                                """
                            )
                           

                            st.markdown("---")

                            st.caption("PrepNexus © AI-Powered Interview Preparation Platform")


                            os.remove(
                                temp_pdf_path
                            )

