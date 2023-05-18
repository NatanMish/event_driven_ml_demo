from kafka import KafkaProducer
import random


def generate_dataset(beta, n, std_dev):
    x_values = [round(random.random(), 2) for _ in range(n)]
    y_values = [beta * x + round(random.gauss(0, std_dev), 2) for x in x_values]
    return x_values, y_values


def send_dataset_to_kafka(topic, dataset):
    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    for x, y in zip(*dataset):
        message = f"{x},{y}".encode("utf-8")
        producer.send(topic, value=message)

    producer.flush()
    producer.close()


def main(beta=2.5, n=100, std_dev=0.1):

    # Generate the dataset
    dataset = generate_dataset(beta, n, std_dev)

    # Send the dataset to Kafka
    send_dataset_to_kafka("data_points", dataset)


if __name__ == "__main__":
    main()
