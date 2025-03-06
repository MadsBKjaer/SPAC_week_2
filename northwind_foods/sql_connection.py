import sqlalchemy as sql
from sqlalchemy import create_engine
from environs import Env
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def create_connection_string(
    host: str, port: str, user: str, password: str, database: str
) -> str:
    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"


def create_sql_engine(database: str) -> sql.Engine:
    env = Env()
    env.read_env()
    return create_engine(create_connection_string(**env.dict(database)))


if __name__ == "__main__":
    sns.set_theme()
    with create_sql_engine("northwind_db").connect() as connection:

        # Total price by country
        total_price_country_df = pd.read_sql(
            "select * from orders join orderdetails using (orderid)",
            con=connection,
        )
        total_price_country_df["TotalPrice"] = (
            total_price_country_df["UnitPrice"] * total_price_country_df["Quantity"]
        )
        total_price_country_df.groupby(["ShipCountry"])["TotalPrice"].sum().plot(
            kind="bar", rot=40, title="Total price by country"
        )
        plt.show()

        # Total quantity by shipper
        quantity_shipper_df = pd.read_sql(
            "select * from "
            "orders join orderdetails using (orderid) "
            "join shippers on orders.shipvia = shippers.shipperid",
            con=connection,
        )
        quantity_shipper_df.groupby(["ShipperID"])["Quantity"].sum().plot(
            kind="bar", rot=0, title="Total quantity by shipper"
        )
        plt.show()

        # Mean packing time (ShippedDate - OrderDate) grouped in 100 freight intervals
        packing_time_freight_df = pd.read_sql(
            "select OrderDate, ShippedDate, Freight from orders", con=connection
        )
        packing_time_freight_df["PackingTime"] = (
            packing_time_freight_df["ShippedDate"]
            - packing_time_freight_df["OrderDate"]
        )
        freight_df = packing_time_freight_df["Freight"]
        grouped = (
            packing_time_freight_df[["Freight", "PackingTime"]]
            .groupby(
                pd.cut(freight_df, np.arange(0, freight_df.max() + 100, 100)),
                observed=True,  # Too avoid deprecated warning since default value is changing in coming update.
            )
            .mean()["PackingTime"]
            .dropna()
            .plot(kind="bar", rot=20, title="Mean packing time by freight")
        )
        plt.show()
