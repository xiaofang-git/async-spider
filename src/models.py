from log import logging
import aiohttp
from scrapy.selector import Selector
# from mysql import Pool
import math


class Price:

    URL = "http://luochejia.yiche.com/{}/price/?page={}"

    def __init__(self, name: str, cid: int = 1):
        self.name = name
        self.cid = cid
        self.price = []

    @property
    async def __compared(self):
        # 从首页获取总共的页数，每页数量10   p1 * 10
        # 从数据库获取当前车型价格的总数量    p2
        # 需要抓取的数量                  p1 * 10 - p2
        # 需要抓取的页数                  (p1 * 10 - p2) / 10  向上取整

        from_db = 0
        from_html = int(await self.__pages_num) * 10
        need = math.ceil((from_html - from_db) / 10)
        return need

    async def bare_car_price(self, page=1):
        # 从网络获取信息
        try:
            async with aiohttp.ClientSession(conn_timeout=5) as request:
                async with request.get(Price.URL.format(self.name, page)) as r:
                    return await r.text()
        except Exception as e:
            logging.error(e)

    @classmethod
    def get_tasks(cls):

        # conn = Pool.get()
        # with conn.cursor() as cur:
        #     cur.execute("show databases;")
        #     value = cur.fetchone()
        #     print(value)
        # # async with conn.cursor() as cur:
        # #     await cur.execute("show databases;")
        # #     value = await cur.fetchone()
        # #     print(value)
        # # async with Pool.get() as conn:
        # #     async with conn.cursor() as cur:
        # #         await cur.execute("show databases;")
        # #         value = await cur.fetchone()
        # #         print(value)
        # # 获取所有车型别名
        tasks = [
            "benben", "aodia5", "aodia1", "aodir8", "aerfaluomioustelvio",
            "zagato", "jilidihaogs"
        ]

        try:
            pass
        except Exception as e:
            logging.error(e)
        finally:
            return tasks

    async def __parse(self):
        # 解析出价格信息
        pages = int(await self.__compared)
        for page in range(pages):
            text = await self.bare_car_price(page + 1)
            dom = Selector(text=text)
            mnames = dom.xpath(
                "//div[@class='big-img-box']//div[@class='title']/text()"
            ).extract()
            results = dom.xpath(
                "//div[@class='big-img-box']//em/text()").extract()

            item = [{
                'mnane': mname,
                'price': result,
                'cname': self.name,
                'cid': self.cid
            } for mname, result in zip(mnames, results)]
            self.price.append(item)

    @property
    async def __pages_num(self):
        # 获取总页数
        pages = 1
        text = await self.bare_car_price()
        dom = Selector(text=text)
        num = dom.xpath("//div[@class='pagination mbt20']//a[last()-1]/@href"
                        ).extract_first()
        if num:
            number = num.split("=")[1].split("&")[0]
            pages = number if number else 1
        return pages

    async def save(self):
        # 获取并储存结果
        print(Price.pool)
        await self.__parse()
        print(self.price)
