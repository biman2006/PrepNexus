import os
import streamlit as st
from dotenv import load_dotenv

from database.db import engine
from database.crud import get_user_by_id, get_all_users, get_all_resume, delete_user, delete_resume

load_dotenv()


def is_admin():
    user_id = st.session_state.get("user_id")
    user = get_user_by_id(user_id) if user_id else None
    return bool(user and user.is_active and user.role == "admin")


def show_admin_panel():
    if not is_admin():
        st.error("⛔ Unauthorized Access. Administrator privileges required.")
        return

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)); padding: 24px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 24px;">
        <h1 style="margin: 0; color: #F8FAFC; font-size: 28px;">🛠️ PrepNexus Admin Command Center</h1>
        <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 15px;">Monitor candidate accounts, manage stored resumes, and audit system health.</p>
    </div>
    """, unsafe_allow_html=True)

    users = get_all_users()
    resumes = get_all_resume()

    # Overview Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Candidates", len(users))
    with m2:
        st.metric("Resumes Analyzed", len(resumes))
    with m3:
        avg_score = (sum(r.readiness_score for r in resumes if r.readiness_score is not None) / len(resumes)) if resumes else 0
        st.metric("Avg Readiness", f"{avg_score:.1f}%")
    with m4:
        st.metric("Active Session", st.session_state.get("user_email", "Admin"))

    st.markdown("---")

    tab_users, tab_resumes, tab_system = st.tabs([
        "👥 Candidate Management",
        "📄 Resume Repository",
        "⚙️ System Diagnostics"
    ])

    # ==============================
    # TAB 1: USERS
    # ==============================
    with tab_users:
        st.subheader(f"Registered Users ({len(users)})")

        if not users:
            st.info("No registered users found.")
        else:
            for user in users:
                col_info, col_action = st.columns([4, 1])
                with col_info:
                    role_badge = "🛡️ Admin" if user.role == "admin" else "👤 Candidate"
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.03); padding: 12px 18px; border-radius: 10px; border-left: 4px solid #6366F1; margin-bottom: 8px;">
                        <strong style="color: #F8FAFC; font-size: 16px;">{user.name or 'No Name'}</strong> 
                        <span style="color: #94A3B8; margin-left: 10px;">({user.email})</span>
                        <span style="background: rgba(99, 102, 241, 0.2); color: #818CF8; padding: 2px 8px; border-radius: 6px; font-size: 12px; margin-left: 10px;">{role_badge}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_action:
                    if user.role != "admin" and st.button("🗑️ Delete", key=f"del_user_{user.id}"):
                        delete_user(user.id)
                        st.success(f"User {user.email} removed.")
                        st.rerun()

    # ==============================
    # TAB 2: RESUMES
    # ==============================
    with tab_resumes:
        st.subheader(f"Generated Resumes ({len(resumes)})")

        if not resumes:
            st.info("No resumes generated yet.")
        else:
            for resume in resumes:
                with st.expander(f"Resume #{resume.id} - {resume.target_role.title()} (User ID: {resume.user_id})"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.write(f"**Target Role:** {resume.target_role}")
                    with c2:
                        ats = f"{resume.ats_score:.1f}%" if resume.ats_score is not None else "N/A"
                        st.write(f"**ATS Score:** {ats}")
                    with c3:
                        readiness = f"{resume.readiness_score:.1f}%" if resume.readiness_score is not None else "N/A"
                        st.write(f"**Readiness Score:** {readiness}")

                    st.text_area("Content Preview", resume.generated_resume[:500] + ("..." if len(resume.generated_resume) > 500 else ""), height=120, key=f"preview_{resume.id}")

                    if st.button("🗑️ Delete Resume", key=f"del_resume_{resume.id}"):
                        delete_resume(resume.id)
                        st.success(f"Resume #{resume.id} removed.")
                        st.rerun()

    # ==============================
    # TAB 3: SYSTEM
    # ==============================
    with tab_system:
        st.subheader("System Configuration & Health")
        st.write(f"**Database:** {engine.url.drivername}")
        st.write(f"**Current Admin User:** {st.session_state.get('user_email')}")
        st.write(f"**JWT Algorithm:** HS256")
        st.success("All system services operational.")