import json
import redis
from datetime import datetime, timezone
from database.utils import getenv

REDIS_HOST = getenv('REDIS_HOST', 'todo-redis-service')
REDIS_PORT = getenv('REDIS_PORT', '8080')

token_blacklist = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=1)


def invalidate_jwt_token(token, exp):
    """
        Invalidate a current active OAuth2 token by putting it on a blacklist before its
        initial expiry date. Token is kept on the blacklist until its initial expiry date.

        :param token: current token to invalidate
        :param exp: expiry date of the current token
    """
    token_blacklist.set(f"jwt:{token}", json.dumps(datetime.now(tz=timezone.utc), default=str), ex=exp)


def get_jwt_token(token):
    """
        Get a token from the expired token blacklist.

        :param token: token to validate
        :returns: datetime of the expiry date of the invalidated token if present (else None)
    """
    return token_blacklist.get(f"jwt:{token}")
