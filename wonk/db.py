from flask_redis import FlaskRedis


def create_db(app):
    if app.testing:
        from mockredis import MockRedis

        class MockRedisWrapper(MockRedis):
            @classmethod
            def from_url(cls, *args, **kwargs):
                return cls()
        db = FlaskRedis.from_custom_provider(MockRedisWrapper)
    else:
        db = FlaskRedis()
    return db
