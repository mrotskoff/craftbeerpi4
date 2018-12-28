import asyncio
import time

import aiosqlite
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from core.craftbeerpi import CraftBeerPi
from cbpi_api.config import ConfigType

class ConfigTestCase(AioHTTPTestCase):


    async def get_application(self):
        self.cbpi = CraftBeerPi()
        self.cbpi.setup()
        return self.cbpi.app


    @unittest_run_loop
    async def test_get(self):

        assert await self.cbpi.config2.get("CBPI_TEST_1", 1) == "22"

    @unittest_run_loop
    async def test_set_get(self):
        value = str(time.time())

        await self.cbpi.config2.set("CBPI_TEST_2", value)

        assert await self.cbpi.config2.get("CBPI_TEST_2", 1) == value

    @unittest_run_loop
    async def test_add(self):
        value = str(time.time())
        key = "CBPI_TEST_3"
        async with aiosqlite.connect("./craftbeerpi.db") as db:
            await db.execute("DELETE FROM config WHERE name = ? ", (key,))
            await db.commit()

        await self.cbpi.config2.add(key, value, type=ConfigType.STRING, description="test")

    @unittest_run_loop
    async def test_http_set(self):
        value = str(time.time())
        key = "CBPI_TEST_3"
        await self.cbpi.config2.set(key, value)
        assert await self.cbpi.config2.get(key, 1) == value

        resp = await self.client.request("POST", "/config/%s/" % key, json={'value': '1'})
        assert resp.status == 204
        assert await self.cbpi.config2.get(key, -1) == "1"

    @unittest_run_loop
    async def test_http_get(self):
        resp = await self.client.request("GET", "/config/")
        assert resp.status == 200
        #print(await eresp.json())
