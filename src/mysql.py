import aiomysql


DATABASES = {
    'host': '192.169.0.168',
    'port': 3306,
    'user': 'dev',
    'password': 'SoCarDev2017',
    'charset': 'utf8mb4',
    # 'database': 'autohome_article',
    # "max_allowed_packet": 64*1024*1024,
    "connect_timeout": 31536000,
    # "write_timeout": 300,
}


Pool = aiomysql.create_pool(**DATABASES)
