import boto3
import json
import typing

from src.config import Config
from src.models import CertificateInfo
from src.constants import (
    CERTIFICATES_TABLE_NAME_OLD,
    CERTIFICATES_TABLE_KEY_SCHEMA_OLD, 
    CERTIFICATES_TABLE_ATTRIBUTE_DEFINITIONS_OLD,
)
from src.constants import (
    DOMAINS_TABLE_NAME,
    DOMAINS_TABLE_KEY_SCHEMA, 
    DOMAINS_TABLE_ATTRIBUTE_DEFINITIONS,
)


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

    def create_table(self, table_name: str, key_schema, attribute_definitions):
        table = self._resource.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()

        return table
    
    def get_table(self, 
            table_name: str,
            key_schema,
            attribute_definitions):
        
        tables = self._client.list_tables()['TableNames']
        if table_name not in tables:
            table = self.create_table(
                table_name,
                key_schema,
                attribute_definitions
            )
            
            return table
        else:
            return self._resource.Table(table_name)

    def upsert_domains(self, parent_domain: str, domains: typing.List[str]):
        table = self.get_table(
            f'${DOMAINS_TABLE_NAME}',
            key_schema=DOMAINS_TABLE_KEY_SCHEMA,
            attribute_definitions=DOMAINS_TABLE_ATTRIBUTE_DEFINITIONS
        )
        with table.batch_writer() as batch:
            for domain in domains:
                batch.put_item(
                    Item={
                        'domain': domain,
                        'parent_domain': parent_domain
                    }
                )

    def upsert_certificates(self, domain: str, certificates: typing.List[CertificateInfo]):
        table = self.get_table(
            f'${CERTIFICATES_TABLE_NAME_OLD}/{domain}',
            key_schema=CERTIFICATES_TABLE_KEY_SCHEMA_OLD,
            attribute_definitions=CERTIFICATES_TABLE_ATTRIBUTE_DEFINITIONS_OLD
        )
        with table.batch_writer() as batch:
            for cert in certificates:
                _cert = cert.dict()
                _cert['domains'] = json.dumps(cert.domains)
                batch.put_item(
                    Item=_cert
                )
