import pydantic
import typing


class Cursor(pydantic.BaseModel):
    after: str = ""
    before: str = ""


class Paginator(pydantic.BaseModel):
    cursors: Cursor
    next: str = ""


class CertificateInfo(pydantic.BaseModel):
    cert_hash_sha256: str
    domains: typing.List[str]
    issuer_name: str
    subject_name: str
    id: str


class FacebookCertificateResponse(pydantic.BaseModel):
    data: typing.List[CertificateInfo]
    paging: typing.Optional[Paginator]