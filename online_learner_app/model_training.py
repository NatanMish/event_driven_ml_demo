from river import linear_model, metrics
import pickle as pkl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


def main(messages):
    local_path = os.path.dirname(os.path.abspath(__file__))

    # check if model is available locally
    try:
        with open(os.path.join(local_path, "../temp_files/model.pkl"), "rb") as f:
            model = pkl.load(f)
        with open(os.path.join(local_path, "../temp_files/metric.pkl"), "rb") as f:
            metric = pkl.load(f)
        dataset = pd.read_csv(os.path.join(local_path, "../temp_files/dataset.csv"))
    except:
        model = linear_model.LinearRegression()
        metric = metrics.MAE()
        dataset = pd.DataFrame(columns=["x", "y"])

    for msg in messages:
        x = float(msg.split(",")[0])
        y = float(msg.split(",")[1])
        dataset = pd.concat(
            [
                dataset,
                pd.DataFrame(
                    [[x, y]],
                    columns=["x", "y"],
                ),
            ]
        )
        metric.update(y, model.predict_one({"x": x}))
        model.learn_one({"x": x}, y)

    with open(os.path.join(local_path, "../temp_files/model.pkl"), "wb") as f:
        pkl.dump(model, f)

    with open(os.path.join(local_path, "../temp_files/metric.pkl"), "wb") as f:
        pkl.dump(metric, f)

    dataset.to_csv(os.path.join(local_path, "../temp_files/dataset.csv"), index=False)

    # Plot the linear regression line
    sns.lmplot(
        x="x",
        y="y",
        data=dataset,
        ci=None,
        scatter_kws={"color": "blue"},
        line_kws={"color": "red"},
    )
    plt.savefig(os.path.join(local_path, "../temp_files/plot.png"))

    if len(dataset) == 0:
        return "No data points received yet, please generate some data points and try again!"
    else:
        print(f"Model's beta: {model.weights['x']}")
        print(f"Model's MAE: {metric.get()}")

    return f"Model's beta: {model.weights['x']}, Model's MAE: {metric.get()}, Dataset size: {len(dataset)}"


if __name__ == "__main__":
    main()
