variable "document_api_endpoint" {
  description = "Адрес YDB (DynamoDB), куда класть результаты из Yandex Forms"
  type = string
}

variable "region_name" {
  description = "Нужен для корректной работы с S3 API к DynamoDB"
  type = string
  default = "ru-central1"
}

variable "facebook-graph-api-secrets" {
  description = "Секреты для подключения к Facebook Graph API"
  sensitive = true
}

variable "aws-static-access-key" {
  description = "Доступ к DynamoDB по токену от сервис-аккаунта"
  sensitive = true
}

variable "service-account-id" {
  description = "Сервисный аккаунт для доступа к секретам"
}