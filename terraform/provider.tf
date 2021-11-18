provider "schemaregistry" {
  uri = var.schema_registry_url
}

provider "kafka" {
  bootstrap_servers = var.kafka_bootstrap_servers
  tls_enabled = false
}
