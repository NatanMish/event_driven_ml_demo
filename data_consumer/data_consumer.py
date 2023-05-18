from kafka import KafkaConsumer


def consume_data_points(
    consumer_timeout_ms=10000, topic="data_points", group_id="my-group"
):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: x.decode("utf-8"),
        consumer_timeout_ms=consumer_timeout_ms,
    )

    messages = []
    for message in consumer:
        message = message.value
        messages.append(message)
        print("RECEIVED {}".format(message))
        yield message

    consumer.close()
    print(f"messages received: {len(messages)}")


def main():
    print("Consuming data points...")
    messages = consume_data_points()
    print("Consumed {} data points".format(len([x for x in messages])))


if __name__ == "__main__":
    main()
