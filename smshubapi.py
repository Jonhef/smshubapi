URL="http://smshub.org/stubs/handler_api.php"
import aiohttp
import urllib.parse
import json
import requests

class SmsHub:
    class Status:
        @staticmethod
        @property
        def Sent():
            return 1
        @staticmethod
        @property
        def Repeat():
            return 3
        @staticmethod
        @property
        def Successed():
            return 6
        @staticmethod
        @property
        def Cancel():
            return 8
        @staticmethod
        @property
        def Wait():
            return 0
    def __init__(self, apikey: str):
        self.api_key = str(apikey)
    async def getNumbersStatus(self, country: int = None, operator: str = None):
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "getNumbersStatus"
            }
            if country:
                data["country"] = str(country)
            if operator:
                data["operator"] = str(operator)
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                return json.loads(await response.text())
    async def getBalance(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "getBalance"
            }
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                return (await response.text()).split(":")[1]
    """Returning tuple (ID, NUMBER)"""
    async def getNumber(self, service: str, operator: str = None, country: int = None):
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "getBalance",
                "service": service,
            }
            if operator:
                data["operator"] = operator
            if country:
                data["country"] = country
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                try:
                    resp = (await response.text()).split(":")
                except:
                    text = await response.text()
                    raise Exception(text)
                return (resp[1], resp[2])
    async def setStatus(self, id: int, status: Status):
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "setStatus",
                "status": status,
                "id": id
            }
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                return (await response.text())
    async def getStatus(self, id: int) -> tuple:
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "getStatus",
                "id": id
            }
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                resp = (await response.text()).upper()
                if resp == "STATUS_WAIT_CODE":
                    return (SmsHub.Status.Wait, None)
                if resp == "STATUS_CANCEL":
                    return (SmsHub.Status.Cancel, None)
                if resp.split(":")[0] == "STATUS_WAIT_RETRY":
                    return (SmsHub.Status.Repeat, resp.split(":")[1])
                if resp.split(":")[0] == "STATUS_OK":
                    return (SmsHub.Status.Sent, resp.split(":")[1])
    async def getPrices(self, service: str, country: int = None):
        async with aiohttp.ClientSession() as session:
            data = {
                "api_key": self.api_key,
                "action": "getPrices"
            }
            if service:
                data["service"] = service
            if country:
                data["country"] = country
            _data = "&".join([f"{key}={urllib.parse.quote(str(value))}" for key, value in data.items()])
            url_to_req = f"{URL}?{_data}"
            async with session.get(url=url_to_req) as response:
                text =  (await response.text())
                return json.loads(text)