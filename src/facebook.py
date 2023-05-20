import aiohttp
import pydantic
import typing
import urllib.parse

from src.config import Config
from src.models import FacebookCertificateResponse, CertificateInfo


class FacebookGraph(object):
    _base_url: str
    _config: Config

    def __init__(self, base_url: str, config: Config) -> None:
        self._base_url = base_url
        self._config = config

    async def __aenter__(self):
        await self.connect()

        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def connect(self):
        connector = aiohttp.TCPConnector(force_close=True)
        self._session = aiohttp.ClientSession(
            base_url=self._base_url,
            connector=connector,
            headers={
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate'
            }
        )

    async def _get_resource(self, url: str) -> FacebookCertificateResponse:
        
        async with self._session.get(url) as response:
            if response.ok:
                data = await response.json()
                data = pydantic.parse_obj_as(FacebookCertificateResponse, data)

                return data
            else:
                print(response)
                return None
        
    async def get_certificates(self, domain: str) -> typing.List[CertificateInfo]:
        query = {
            'query': domain,
            'access_token': f'{self._config.FACEBOOK_CLIENT_ID}|{self._config.FACEBOOK_CLIENT_SECRET}',
            'fields': ','.join([
                'cert_hash_sha256',
                'domains',
                'issuer_name',
                'subject_name'
            ]),
            'limit': 100
        }
        resource_path = f'/certificates?{urllib.parse.urlencode(query)}'
        certificates: typing.List[CertificateInfo] = list()

        while resource_path:
            response = await self._get_resource(resource_path)
            certificates.extend(response.data)
            after = response.paging.cursors.after if response.paging and response.paging.cursors and response.paging.cursors.after else None
            query['after'] = after
            resource_path = f'/certificates?{urllib.parse.urlencode(query)}' if after else None

        return certificates

    async def subscribe(self, domains: typing.List[str]):
        URL = f'/{self._config.FACEBOOK_CLIENT_ID}/subscribe_domains'
        body = {
            'subscribe': ','.join(domains),
            'access_token': self._config.FACEBOOK_CLIENT_SECRET
        }
        async with self._session.post(URL, body=body) as response:
            if response.ok:
                return True
            else:
                print(response)
                return False
    
    async def unsubscribe(self, domains: typing.List[str]):
        URL = f'/{self._config.FACEBOOK_CLIENT_ID}/subscribe_domains'
        body = {
            'unsubscribe': ','.join(domains),
            'access_token': self._config.FACEBOOK_CLIENT_SECRET
        }
        async with self._session.post(URL, body=body) as response:
            if response.ok:
                return True
            else:
                print(response)
                return False
            
    async def get_subscribed_domains(self):
        query = {
            'fields': 'domain',
            'access_token': self._config.FACEBOOK_CLIENT_SECRET
        }
        URL = f'/{self._config.FACEBOOK_CLIENT_ID}/subscribe_domains{urllib.parse.urlencode(query)}'
        async with self._session.get(URL) as response:
            # TODO: there are pagination
            ...
            # Example:
            """
            {"data":[{"domain":"example.com","id":"1584179144975746"}],"paging":{"cursors":{"before":"QVFIU...","after":"QVFIU..."}}}
            """

        return None
    
    