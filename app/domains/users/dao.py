from app.base.dao import BaseDAO
from app.domains.users.models import User, Role, Position


class UserDAO(BaseDAO):
    model = User

class RoleDAO(BaseDAO):
    model = Role

class PositionDAO(BaseDAO):
    model = Position
