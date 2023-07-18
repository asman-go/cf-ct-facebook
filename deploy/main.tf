data "archive_file" "cf-archive" {
  type = "zip"
  source_dir = "${path.module}/../"
  output_path = "${path.module}/../cf-ct-facebook.zip"
}

resource "yandex_function" "cf-ct-facebook" {
  name = "cf-ct-facebook"
  description = "Получение CTLog от Facebook Graph API"
  user_hash = data.archive_file.cf-archive.output_base64sha256 # uuid()  # Должна меняться, иначе версия функции не создастся
  runtime = "python311"
  entrypoint = "main.event_handler"
  memory = "128"  # 128 MB
  execution_timeout = "10"  # 10 seconds
  service_account_id = var.service-account-id  # Service Account нужен для доступа к секретам

  environment = {
    DOCUMENT_API_ENDPOINT = var.document_api_endpoint
    REGION_NAME = var.region_name
  }

  secrets {
    id = var.facebook-graph-api-secrets.secret_id
    version_id = var.facebook-graph-api-secrets.id
    key = "client_id"
    environment_variable = "FACEBOOK_CLIENT_ID"
  }
  secrets {
    id = var.facebook-graph-api-secrets.secret_id
    version_id = var.facebook-graph-api-secrets.id
    key = "client_secret"
    environment_variable = "FACEBOOK_CLIENT_SECRET"
  }
  secrets {
    id = var.aws-static-access-key.secret_id
    version_id = var.aws-static-access-key.id
    key = "client_id"
    environment_variable = "AWS_ACCESS_KEY_ID"
  }
  secrets {
    id = var.aws-static-access-key.secret_id
    version_id = var.aws-static-access-key.id
    key = "client_secret"
    environment_variable = "AWS_SECRET_ACCESS_KEY"
  }

  content {
    zip_filename = data.archive_file.cf-archive.output_path
  }
}