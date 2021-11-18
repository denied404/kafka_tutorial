resource "schemaregistry_subject" "source" {
  subject = "source-value"
  schema = file("schemas/source.avro.json")
}

resource "schemaregistry_subject" "response" {
  subject = "response-value"
  schema = file("schemas/response.avro.json")
}
