import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("AGG")


def create_img(df):

    tidy = pd.merge(
        left=df.melt(
        id_vars="trip_id", value_vars=["driving", "transit"], value_name="duration"
        ).rename(columns={"variable": "mode"}),
        right=df,
        how="inner",
        on="trip_id",
    ).sort_values(by=["distance"])
    sns.set_theme(style="whitegrid")

    plot = sns.catplot(
        data=tidy,
        kind="bar",
        x="trip_id",
        y="duration",
        hue="mode",
        color=2,
        palette="dark6",
        alpha=0.7,
        height=7,
        aspect=1.7,
    )

    plot.despine(left=True)
    plot.set_axis_labels("Distance in meters", "duration in seconds")
    plot.legend.set_title("")

    return plot
