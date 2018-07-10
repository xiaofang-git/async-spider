from models import Price
import asyncio
import aiomysql


DATABASES = {
    'host': ""
    'port': 3306,
    'user': ""
    'password': ""
    'charset': 'utf8mb4',
    # 'database': 'autohome_article',
    # "max_allowed_packet": 64*1024*1024,
    "connect_timeout": 31536000,
    # "write_timeout": 300,
}


def run():
    loop = asyncio.get_event_loop()

    # # 获取数据库连接池
    task = aiomysql.create_pool(**DATABASES)
    pool = loop.run_until_complete(asyncio.gather(task))
    Price.pool = pool[0]

    # 获取任务

    tasks = loop.run_until_complete(asyncio.gather(Price.get_tasks()))
    print(tasks)

    # 生成任务
    my_func_list = (Price(name).save() for name in tasks)
    loop.run_until_complete(asyncio.gather(*my_func_list))

