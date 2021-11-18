from time import time
from uuid import uuid4
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient

SCHEMA_REGISTRY_URL="http://localhost:8081"
KAFKA_BROKERS="localhost:9092"

class TestMessage(object):
    def __init__(self, name, passed):
        self.name = name
        self.passed = passed 
        self.ts=round(time() * 1000)

def test_message_to_dict(msg, ctx):
    return dict(name=msg.name,
                passed=msg.passed,
                ts=msg.ts)


if __name__ == "__main__":
    schema_registry_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY_URL})
    schema_str = """
    {
      "type":"record",
      "name":"testRecord",
      "namespace":"usatu",
      "fields":[
        {
          "name":"name",
          "type":"string"
        },
        {
          "name":"last_name",
          "type":["null", "string"],
          "default": null
        },
        {
          "name":"passed",
          "type":[
            "null",
            {
              "type":"enum",
              "name":"YesNo",
              "symbols":[
                "Y",
                "N"
              ]
            }
          ],
          "default": null
        },
        {
          "name":"ts",
          "type":{
            "type": "long",
            "logicalType": "timestamp-millis"
          }
        }
      ]
    }
    """

    value_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                      schema_str=schema_str,
                                      to_dict=test_message_to_dict)

    producer = SerializingProducer({
        'bootstrap.servers': KAFKA_BROKERS,
        'value.serializer': value_serializer 
        })

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print("Delivery failed because, well, {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    message = TestMessage("Boris Brejca", "Y")
    producer.produce(topic='test-topic', value=message, key=str(uuid4()), on_delivery=delivery_report)
    producer.flush()
