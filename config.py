class Config(object):
    """
    Main Configuration for Message In A Bottle API Gateway
    """
    DEBUG = False
    TESTING = False

    # configuring microservices endpoints
    import os

    REQUESTS_TIMEOUT_SECONDS = float(os.getenv("REQUESTS_TIMEOUT_SECONDS", 5))

    # configuring redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis_cache')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', '0')
    REDIS_URL = 'redis://%s:%s/%s' % (
        REDIS_HOST,
        REDIS_PORT,
        REDIS_DB
    )

    # users microservice
    USERS_MS_PROTO = os.getenv('USERS_MS_PROTO', 'http')
    USERS_MS_HOST = os.getenv('USERS_MS_HOST', 'localhost')
    USERS_MS_PORT = os.getenv('USERS_MS_PORT', 5001)
    USERS_MS_URL = '%s://%s:%s' % (USERS_MS_PROTO, USERS_MS_HOST, USERS_MS_PORT)

    # messages microservice
    MESSAGES_MS_PROTO = os.getenv('MESSAGES_MS_PROTO', 'http')
    MESSAGES_MS_HOST = os.getenv('MESSAGES_MS_HOST', 'localhost')
    MESSAGES_MS_PORT = os.getenv('MESSAGES_MS_PORT', 5002)
    MESSAGES_MS_URL = '%s://%s:%s' % (MESSAGES_MS_PROTO, MESSAGES_MS_HOST, MESSAGES_MS_PORT)

    # blacklist microservice
    BLACKLIST_MS_PROTO = os.getenv('BLACKLIST_MS_PROTO', 'http')
    BLACKLIST_MS_HOST = os.getenv('BLACKLIST_MS_HOST', 'localhost')
    BLACKLIST_MS_PORT = os.getenv('BLACKLIST_MS_PORT', 5003)
    BLACKLIST_MS_URL = '%s://%s:%s' % (BLACKLIST_MS_PROTO, BLACKLIST_MS_HOST, BLACKLIST_MS_PORT)


    # Configuring sessions
    SESSION_TYPE = 'redis'

    # secret key
    SECRET_KEY = os.getenv('APP_SECRET', b'isreallynotsecretatall')


class DebugConfig(Config):
    """
    This is the main configuration object for application.
    """
    DEBUG = True
    TESTING = False


class DevConfig(DebugConfig):
    """
    This is the main configuration object for application.
    """
    pass


class TestConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = True

    import os
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


class ProdConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = False
    DEBUG = False

    import os
    SECRET_KEY = os.getenv('APP_SECRET', os.urandom(24))


