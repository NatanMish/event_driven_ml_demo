from river import linear_model, metrics
from data_consumer.data_consumer import consume_data_points
import pickle as pkl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    messages = [
        x
        for x in consume_data_points(
            topic="data_points",
            group_id="online_learner_app",
            consumer_timeout_ms=10000,
        )
    ]

    # check if model is available locally
    try:
        with open("./temp_files/model.pkl", "rb") as f:
            model = pkl.load(f)
        with open("./temp_files/metric.pkl", "rb") as f:
            metric = pkl.load(f)
        dataset = pd.read_csv("./temp_files/dataset.csv")
    except:
        model = linear_model.LinearRegression()
        metric = metrics.MAE()
        dataset = pd.DataFrame(columns=["x", "y"])

    for msg in messages:
        dataset = pd.concat(
            [
                dataset,
                pd.DataFrame(
                    [[float(msg.split(",")[0]), float(msg.split(",")[1])]],
                    columns=["x", "y"],
                ),
            ]
        )
        metric.update(
            float(msg.split(",")[1]), model.predict_one({"x": float(msg.split(",")[0])})
        )
        model.learn_one({"x": float(msg.split(",")[0])}, float(msg.split(",")[1]))

    # save model locally
    with open("./temp_files/model.pkl", "wb") as f:
        pkl.dump(model, f)

    # save metric locally
    with open("./temp_files/metric.pkl", "wb") as f:
        pkl.dump(metric, f)

    # save dataset locally
    dataset.to_csv("./temp_files/dataset.csv", index=False)

    # Plot the linear regression line
    sns.lmplot(
        x="x",
        y="y",
        data=dataset,
        ci=None,
        scatter_kws={"color": "blue"},
        line_kws={"color": "red"},
    )
    plt.savefig("./temp_files/plot.png")

    if len(dataset) == 0:
        return "No data points received yet, please generate some data points and try again!"
    else:
        print(f"Model's beta: {model.weights['x']}")
        print(f"Model's MAE: {metric.get()}")

    return f"Model's beta: {model.weights['x']}, Model's MAE: {metric.get()}, Dataset size: {len(dataset)}"


if __name__ == "__main__":
    main()
