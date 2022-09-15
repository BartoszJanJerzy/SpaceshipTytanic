import pandera as pa
from pandera.typing import Series
import pickle
import os

path = os.path.join("models", "values.pickle")
with open(path, "rb") as file:
    values = pickle.load(file)

mins = values["min"]
maxes = values["max"]


class RawData(pa.SchemaModel):
    is_g: Series[bool] = pa.Field(alias="is_g734s", check_name=True)
    cryo_sleep: Series[bool] = pa.Field(alias="CryoSleep", check_name=True)
    vip: Series[bool] = pa.Field(alias="VIP", check_name=True)
    europa: Series[bool] = pa.Field(alias="Europa", check_name=True)
    mars: Series[bool] = pa.Field(alias="Mars", check_name=True)
    pso: Series[bool] = pa.Field(alias="PSO J318.5-22", check_name=True)
    trappist: Series[bool] = pa.Field(alias="TRAPPIST-1e", check_name=True)
    age: Series[int] = pa.Field(
        alias="Age", check_name=True,
        in_range={"min_value": mins["Age"], "max_value": maxes["Age"]}
    )
    room_service: Series[int] = pa.Field(
        alias="RoomService",
        check_name=True,
        in_range={"min_value": mins["RoomService"], "max_value": maxes["RoomService"]},
    )
    food: Series[int] = pa.Field(
        alias="FoodCourt", check_name=True,
        in_range={"min_value": mins["FoodCourt"], "max_value": maxes["FoodCourt"]}
    )
    shopping: Series[int] = pa.Field(
        alias="ShoppingMall",
        check_name=True,
        in_range={"min_value": mins["ShoppingMall"], "max_value": maxes["ShoppingMall"]},
    )
    spa: Series[int] = pa.Field(
        alias="Spa", check_name=True,
        in_range={"min_value": mins["Spa"], "max_value": maxes["Spa"]}
    )
    vrdeck: Series[int] = pa.Field(
        alias="VRDeck", check_name=True,
        in_range={"min_value": mins["VRDeck"], "max_value": maxes["VRDeck"]}
    )


class PreprocessedData(pa.SchemaModel):
    is_g: Series[int] = pa.Field(alias="is_g734s", check_name=True)
    cryo_sleep: Series[int] = pa.Field(alias="CryoSleep", check_name=True)
    vip: Series[int] = pa.Field(alias="VIP", check_name=True)
    europa: Series[int] = pa.Field(alias="Europa", check_name=True)
    mars: Series[int] = pa.Field(alias="Mars", check_name=True)
    pso: Series[int] = pa.Field(alias="PSO J318.5-22", check_name=True)
    trappist: Series[int] = pa.Field(alias="TRAPPIST-1e", check_name=True)
    age: Series[float] = pa.Field(alias="Age", check_name=True)
    room_service: Series[float] = pa.Field(alias="RoomService", check_name=True)
    food: Series[float] = pa.Field(alias="FoodCourt", check_name=True)
    shopping: Series[float] = pa.Field(alias="ShoppingMall", check_name=True)
    spa: Series[float] = pa.Field(alias="Spa", check_name=True)
    vrdeck: Series[float] = pa.Field(alias="VRDeck", check_name=True)
