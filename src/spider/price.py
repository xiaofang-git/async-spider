from models import Price
import asyncio


def run():
    loop = asyncio.get_event_loop()
    tasks = Price.get_tasks()
    my_func_list = (Price(name).save() for name in tasks)
    loop.run_until_complete(asyncio.gather(*my_func_list))
