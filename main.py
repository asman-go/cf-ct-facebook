import asyncio
import functions_framework
import itertools
import typing

from src.database import DocumentAPI
from src.config import Config
from src.facebook import FacebookGraph
from src.models import CertificateInfo


async def task(domains: typing.List[str], config: Config) -> typing.List[str]:
    result: typing.Dict[str, typing.List[CertificateInfo]] = dict()

    async with FacebookGraph("https://graph.facebook.com", config) as fb_client:
        async def get_certificates(domain: str):
            result[domain] = await fb_client.get_certificates(domain)

        await asyncio.gather(*[get_certificates(domain) for domain in domains])

        dynamodb = DocumentAPI(config)
        for domain in result:
            dynamodb.upsert(domain, result[domain])

    return result.keys()


def event_handler(event, context):
    config = Config()
    if 'request' in event and 'domains' in event['request']:
        domains: typing.List[str] = event['request']['domains']

        data = asyncio.run(task(domains, config))
        data = list(data)

        return {
            'response': {
                'count': len(data),
                'data': data
            }
        }

    return {
        'response': {
            'text': 'Where are domains?'
        }
    }


@functions_framework.http
def gcp_http_handler(request):
    event = request.get_json(silent=True)
    print('Event', event)
    config = Config()
    if 'request' in event and 'domains' in event['request']:
        domains: typing.List[str] = event['request']['domains']

        data = asyncio.run(task(domains, config))
        data = list(data)

        return {
            'response': {
                'count': len(data),
                'data': data
            }
        }

    return {
        'response': {
            'text': 'Where are domains?'
        }
    }


# if __name__ == '__main__':
#    print(handler({}, {}))
