class AdminDashboard:

    @staticmethod
    def get_stats():

        from admin.admin_service import AdminService
        stats={
            "total_users": AdminService.total_user(),
            "total_resume": AdminService.total_resume()
        }


        return stats