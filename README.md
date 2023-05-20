# CloudFunction for Facebook Graph API to get Certificate Transparency (CT) logs

- [How CT works](https://certificate.transparency.dev/howctworks/).
- [How get credentials for Facebok Graph API](https://appsecurity.gitbook.io/devops/v/ppc/tech/api/famous-api/facebook-api)
- [YDB Docs](https://ydb.tech/en/docs)
- [Facebook CT Log Monitor Web](https://developers.facebook.com/tools/ct/search/)

# Getting started

Facebook Graph API `.env` (find your credentials on the [Facebook App page](https://developers.facebook.com/apps).):

```
FACEBOOK_CLIENT_ID=
FACEBOOK_CLIENT_SECRET=
```

DynamoDB `.env`:

```
DOCUMENT_API_ENDPOINT=
REGION_NAME=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

# Prepare code for YCloud

```
git archive --format zip -o cf-ct-facebook.zip main
```