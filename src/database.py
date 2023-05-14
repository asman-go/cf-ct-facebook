import boto3
import json
import typing

from src.config import Config
from src.models import CertificateInfo


class DocumentAPI(object):

    def __init__(self, config: Config) -> None:
        self._client = boto3.client(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

        self._resource = boto3.resource(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    
    def get_table(self, domain: str):
        CERTIFICATE_TABLE_NAME = f'certificates/{domain}'
        tables = self._client.list_tables()['TableNames']
        if CERTIFICATE_TABLE_NAME not in tables:
            table = self._resource.create_table(
                TableName=CERTIFICATE_TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'cert_hash_sha256',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'subject_name',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'cert_hash_sha256',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'domains',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'issuer_name',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'subject_name',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            
            return table
        else:
            return self._resource.Table(CERTIFICATE_TABLE_NAME)

    def upsert(self, domain: str, certificates: typing.List[CertificateInfo]):
        table = self.get_table(domain)
        with table.batch_writer() as batch:
            for cert in certificates:
                _cert = cert.dict()
                _cert['domains'] = json.dumps(cert.domains)
                batch.put_item(
                    Item=_cert
                )
