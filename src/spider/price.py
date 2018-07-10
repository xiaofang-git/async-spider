from models import Price
import asyncio
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


def run():
    loop = asyncio.get_event_loop()
    tasks = Price.get_tasks()
    # # 获取数据库连接池
    task = aiomysql.create_pool(**DATABASES)
    pool = loop.run_until_complete(asyncio.gather(task))
    Price.pool = pool

    my_func_list = (Price(name).save() for name in tasks)
    loop.run_until_complete(asyncio.gather(*my_func_list))

