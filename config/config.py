class Config:
    """基础配置"""
    BASE_URL = "http://localhost:8000"
    TIMEOUT = 10

class TestConfig(Config):
    """多环境扩展"""
    pass

class ProdConfig(Config):
    """多环境扩展"""
    pass

config = TestConfig()