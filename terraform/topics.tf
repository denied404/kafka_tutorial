resource "kafka_topic" "source" {
  name = "source"
  replication_factor = var.kafka_topic_default_replication_factor
  partitions = var.kafka_topic_default_partitions
}

resource "kafka_topic" "response" {
  name = "response"
  replication_factor = var.kafka_topic_default_replication_factor
  partitions = var.kafka_topic_default_partitions
}
