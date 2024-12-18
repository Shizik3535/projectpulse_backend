from app.base.dao import BaseDAO
from app.domains.auth.models import BlackListToken


class BlackListTokenDAO(BaseDAO):
    model = BlackListToken
