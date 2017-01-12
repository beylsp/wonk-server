from flask_redis import FlaskRedis
from mockredis import MockRedis


class MockRedisWrapper(MockRedis):
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


def create_db(app):
    if app.testing:
        db = FlaskRedis.from_custom_provider(MockRedisWrapper)
    else:
        db = FlaskRedis()
    return db
