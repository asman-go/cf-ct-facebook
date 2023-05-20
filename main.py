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

    # 1. Get information from Facebook Graph API
    async with FacebookGraph("https://graph.facebook.com", config) as fb_client:
        async def get_certificates(domain: str):
            result[domain] = await fb_client.get_certificates(domain)

        await asyncio.gather(*[get_certificates(domain) for domain in domains])
    
    # 2. If it is new domain we'll subscribe for updates
        await fb_client.subscribe(domains)

    # 2. Send result to DynamoDB
    dynamodb = DocumentAPI(config)
    for parent_domain in result:
        domains = []
        certificates = result[parent_domain]
        for certificate in certificates:
            domains.extend[certificate.domains]

        domains = list(set(domains))
        dynamodb.upsert_domains(parent_domain, domains)
        dynamodb.upsert_certificates(parent_domain, certificates)

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
