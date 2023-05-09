import pydantic
import typing


class Config(pydantic.BaseSettings):
    # Find your credentials on the [Facebook App page](https://developers.facebook.com/apps).
    FACEBOOK_CLIENT_ID: str = "<client-id>"
    FACEBOOK_CLIENT_SECRET: str = "<client-secret>"
    # YDB: via cli — ydb config profile get db1
    DOCUMENT_API_ENDPOINT: str = "https://example.com/path/to/your/db"
    REGION_NAME: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "<key-id>"
    AWS_SECRET_ACCESS_KEY: str = "<secret-access-key>"
