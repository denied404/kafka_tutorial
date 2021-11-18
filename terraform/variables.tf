variable "schema_registry_url" {
  type = string
  description = "A URL to the schema registry host"
}

variable "kafka_bootstrap_servers" {
  type = list
  description = "An array of kafka brokers"
}

variable "kafka_topic_default_replication_factor" {
  type = number
  description = "Default kafka topic replication factor"
  default = 1
}

variable "kafka_topic_default_partitions" {
  type = number
  description = "Default kafka topic partitions count"
  default = 1
}

