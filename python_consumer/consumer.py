from time import time
from uuid import uuid4
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient

SCHEMA_REGISTRY_URL="http://localhost:8081"
KAFKA_BROKERS="localhost:9092"

class TestMessage(object):
    def __init__(self, name, passed, ts):
        self.name = name
        self.passed = passed
        self.ts=ts

def dict_to_test_message(obj, ctx):
    if obj is None:
        return None

    return TestMessage(name=obj['name'],
                       passed=obj['passed'],
                       ts=obj['ts'])


if __name__ == "__main__":
    schema_registry_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY_URL})
    with open('../terraform/schemas/test-topic.avro.json') as fp:
        schema_str = fp.read()
    value_deserializer = AvroDeserializer(schema_registry_client=schema_registry_client,
                                          schema_str=schema_str,
                                          from_dict=dict_to_test_message)

    consumer = DeserializingConsumer({
        'bootstrap.servers': KAFKA_BROKERS,
        'value.deserializer': value_deserializer,
        'group.id': 1
        })
    consumer.subscribe(['test-topic'])

    while True:
        try:
            # Timeout for polling is 1 sec
            msg = consumer.poll(1)

            if msg is None:
                continue
            
            val = msg.value()
            if val is not None:
                print("Name: {}, passed: {}, timestamp: {}".format(val.name,
                                                                   val.passed,
                                                                   val.ts))
        except KeyboardInterrupt:
            break

    consumer.close()
