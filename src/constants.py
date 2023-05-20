# NEW
DOMAINS_TABLE_NAME = 'domains'
DOMAINS_TABLE_KEY_SCHEMA = [
    {
        'AttributeName': 'domain',
        'KeyType': 'HASH'
    }
]
DOMAINS_TABLE_ATTRIBUTE_DEFINITIONS = [
    {
        'AttributeName': 'domain',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'parent_domain',
        'AttributeType': 'S'
    }
]

# OLD

CERTIFICATES_TABLE_NAME_OLD = 'certificates'      # Таблица, в которой храним найденные сертификаты
CERTIFICATES_TABLE_KEY_SCHEMA_OLD = [             # Схема ключей таблицы certificates/<domain_name>
    {
        'AttributeName': 'cert_hash_sha256',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'subject_name',
        'KeyType': 'RANGE'
    }
]
CERTIFICATES_TABLE_ATTRIBUTE_DEFINITIONS_OLD = [  # Схема столбцов таблицы certificates/<domain_name>
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
]