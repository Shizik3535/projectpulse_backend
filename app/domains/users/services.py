from app.domains.users.dao import PositionDAO, RoleDAO



class UserService:
    @staticmethod
    async def get_all_positions():
        return await PositionDAO.find_all()

    @staticmethod
    async def get_all_roles():
        return await RoleDAO.find_all()
        