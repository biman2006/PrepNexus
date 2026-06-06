import os
import streamlit as st
from dotenv import load_dotenv

from database.db import engine

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def is_admin():

    if "user_email" not in st.session_state:
        return False

    if not ADMIN_EMAIL:
        return False

    current_user = st.session_state["user_email"].strip().lower()

    return current_user == ADMIN_EMAIL.strip().lower()


def show_admin_panel():

    # ==============================
    # SECURITY CHECK
    # ==============================

    if not is_admin():
        st.error("⛔ Unauthorized Access")
        return

    # ==============================
    # HEADER
    # ==============================

    st.title("🛠️ PrepNexus Admin Dashboard")

    st.success(
        f"Logged in as Admin: {st.session_state.user_email}"
    )

    # ==============================
    # DATABASE INFO
    # ==============================

    st.subheader("🗄️ Database Information")

    st.code(str(engine.url))

    # ==============================
    # USER SECTION
    # ==============================

    from database.crud import get_all_users

    users = get_all_users()

    st.markdown("---")
    st.subheader("👥 Users")

    st.metric(
        "Total Users",
        len(users)
    )

    if not users:
        st.info("No users found.")
    else:

        for user in users:

            with st.expander(
                f"{user.name} ({user.email})"
            ):

                st.write(f"User ID: {user.id}")
                st.write(f"Email: {user.email}")

                if st.button(
                    "🗑️ Delete User",
                    key=f"user_{user.id}"
                ):
                    
                    from database.crud import Delete_user

                    Delete_user(user.id)

                    st.success(
                        f"Deleted user {user.email}"
                    )

                    st.rerun()

    # ==============================
    # RESUME SECTION
    # ==============================

    from database.crud import get_all_resume

    resumes = get_all_resume()

    st.markdown("---")
    st.subheader("📄 Resumes")

    st.metric(
        "Total Resumes",
        len(resumes)
    )

    if not resumes:
        st.info("No resumes found.")
    else:

        for resume in resumes:

            with st.expander(
                f"Resume #{resume.id}"
            ):

                st.write(
                    f"User ID: {resume.user_id}"
                )

                st.write(
                    f"Target Role: {resume.target_role}"
                )

                st.write(
                    f"ATS Score: {resume.ats_score}"
                )

                st.write(
                    f"Readiness Score: {resume.readiness_score}"
                )

                if st.button(
                    "🗑️ Delete Resume",
                    key=f"resume_{resume.id}"
                ):
                    
                    from database.crud import delete_resume

                    delete_resume(
                        resume.id
                    )

                    st.success(
                        f"Deleted Resume #{resume.id}"
                    )

                    st.rerun()

    # ==============================
    # SYSTEM INFO
    # ==============================

    st.markdown("---")
    st.subheader("⚙️ System Information")

    st.write(
        "Current User:",
        st.session_state.user_email
    )

    st.write(
        "Admin Email:",
        ADMIN_EMAIL
    )