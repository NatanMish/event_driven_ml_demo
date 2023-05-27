import streamlit as st
from online_learner_app.data_producer.data_producer import (
    generate_dataset,
    send_dataset_to_kafka,
)
from online_learner_app.data_consumer.data_consumer import consume_data_points
import datetime
import pandas as pd
import pickle as pkl
import requests


def main():
    st.title("Online Model Training App")
    st.image("app_diagram.png")
    topic = "data_points"  # Replace with your Kafka topic name

    st.header("Recently Received Data Points")
    time_placeholder = st.empty()
    messages_placeholder = st.empty()
    example_messages_placeholder = st.empty()

    st.header("Online Linear Regression")
    image_placeholder = st.empty()
    dataset_size_placeholder = st.empty()
    beta_placeholder = st.empty()
    mae_placeholder = st.empty()

    st.header("Dataset Generator")
    st.write(
        "Enter the parameters below and click 'Generate Dataset' to create a dataset and send it to Kafka."
    )

    st.latex(r"""y = \beta x + \epsilon""")
    st.latex(r"""\epsilon \sim \mathcal{N}(0, \sigma^2)""")

    # Parameters input
    beta = st.number_input("Beta", value=1)
    n = st.number_input("n", value=20)
    std_dev = st.number_input("Standard Deviation", value=0.1)

    if st.button("Generate Dataset"):
        # Generate the dataset
        simulated_batch = generate_dataset(beta, n, std_dev)

        # Send the dataset to Kafka
        send_dataset_to_kafka(topic, simulated_batch)

        st.success("Dataset generated and sent to Kafka!")

        timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        time_placeholder.write(f"Kafka receiving messages at: {timenow}")

        messages = consume_data_points(
            topic=topic, group_id="streamlit_app", consumer_timeout_ms=10000
        )

        messages_consumed = [x for x in messages]
        messages_placeholder.write(f"Received {len(messages_consumed)} messages")
        example_messages_placeholder.write(
            [
                f"x: {x.split(',')[0]}, y: {x.split(',')[1]}"
                for x in messages_consumed[:5]
            ]
        )

        result = requests.post(
            "http://127.0.0.1:50814/data_points", json={"messages": messages_consumed}
        )
        print(result.text)

        dataset_size_placeholder.write(
            f"Dataset size: {len(pd.read_csv('./temp_files/dataset.csv'))}"
        )

        with open("./temp_files/model.pkl", "rb") as f:
            model = pkl.load(f)
        beta_placeholder.write(
            f"River Linear Regression model's beta: {model.weights['x']}"
        )

        with open("./temp_files/metric.pkl", "rb") as f:
            metric = pkl.load(f)

        mae_placeholder.write(f"River Linear Regression model's MAE: {metric.get()}")
        image_placeholder.image("./temp_files/plot.png")

    # insert some space here
    st.write("")

    if st.button("Clear dataset and model weights"):
        with open("./temp_files/model.pkl", "wb") as f:
            f.write(b"")
        with open("./temp_files/dataset.csv", "wb") as f:
            f.write(b"")
        with open("./temp_files/metric.pkl", "wb") as f:
            f.write(b"")
        messages_placeholder.write(f"Received 0 messages")
        example_messages_placeholder.write(f"Example messages: []")
        beta_placeholder.write(f"River Linear Regression model's beta: ")
        mae_placeholder.write(f"River Linear Regression model's MAE: ")
        dataset_size_placeholder.write("Dataset size: 0")
        st.success("Dataset and model weights cleared!")
        image_placeholder = st.empty()


if __name__ == "__main__":
    main()
