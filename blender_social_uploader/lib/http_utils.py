import ssl
import certifi
import aiohttp

async def fetch_json_with_ssl(url: str, **kwargs) -> dict:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()
