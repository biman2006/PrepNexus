


import streamlit as st

class AdminUI:

    @staticmethod
    def login_page():
        st.title("ADMIN PANEL")

        username=st.text_input("Admin Username")

        password=st.text_input("Admin Password",
                               type="password")
        
        if st.button("Login"):

            from admin.admin_auth import AdminAuth

            if AdminAuth.login(username,password):
                st.session_state.admin_logged_in=True

                st.success("Admin login successful")

                st.rerun()

            else:
                st.error("Invalid credentials")




    @staticmethod
    def dashboard():
        st.title("Admin Dashboard")
        from admin.admin_dashboard import AdminDashboard

        stats = AdminDashboard.get_stats()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Users",
                stats.get("total_users", 0)
            )

        with col2:
            st.metric(
                "Total Resume Analysis",
                stats.get("total_resume", 0)
            )
            

        st.markdown("---")

        st.subheader("Users")
        from admin.admin_service import AdminService

        users=AdminService.get_users()


        for user in users:
            st.write(f"{user.email}")
