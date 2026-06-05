


class AdminService:
    
    @staticmethod
    def total_user():
        from database.crud import get_all_users

        users=get_all_users()

        return len(users)

    @staticmethod
    def total_resume():
        from database.crud import get_all_resume
        resumes=get_all_resume()

        return len(resumes) 
    
    @staticmethod
    def get_users():
        from database.crud import get_all_users
        return get_all_users()
    

    @staticmethod
    def get_resumes():
        from database.crud import get_all_resume
        return get_all_resume()
    
