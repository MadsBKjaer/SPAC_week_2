import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()


def inspect_dataframe(df: pd.DataFrame, head: int = 10) -> None:
    print(df.columns)
    print(df.head(head))

    housing_price_by_region: pd.DataFrame = housing_price.groupby(["region"])
    print(housing_price_by_region[["purchase_price"]].mean())


def plot_grouping(
    df: pd.DataFrame, x_axis: str, y_axis: str, group: str, plot_type: str = "bar"
) -> None:
    grouped_df: pd.DataFrame = (
        df.groupby([x_axis, group])[y_axis]
        .mean()
        .reset_index()
        .pivot(index=x_axis, columns=group, values=y_axis)
    )
    # print(grouped_df)
    grouped_df.plot(kind=plot_type, ylabel=y_axis)
    plt.show()


if __name__ == "__main__":
    housing_price: pd.DataFrame = pd.read_csv(
        path.join("Data", "DKHousingPricesSample100k.csv")
    )
    inspect_dataframe(housing_price)
    plot_grouping(housing_price, "no_rooms", "purchase_price", "region", "line")
    plot_grouping(housing_price, "house_type", "purchase_price", "region")
    plot_grouping(
        housing_price,
        "quarter",
        "sqm_price",
        "house_type",
        "line",
    )
