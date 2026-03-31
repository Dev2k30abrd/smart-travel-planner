import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# ---------- Load Dataset ----------
df = pd.read_excel("Data_Train.xlsx")

# ---------- Keep Columns ----------
df = df[[
    "Airline",
    "Date_of_Journey",
    "Source",
    "Destination",
    "Duration",
    "Total_Stops",
    "Dep_Time",
    "Arrival_Time",
    "Route",
    "Price"
]]

# ---------- Duration Conversion ----------
def convert_duration(x):
    hours = 0
    minutes = 0

    if 'h' in x:
        hours = int(x.split('h')[0])

    if 'm' in x:
        parts = x.split('h')
        if len(parts) > 1:
            minutes = int(parts[1].replace('m', '').strip())
        else:
            minutes = int(x.replace('m', '').strip())

    return hours * 60 + minutes

df["Duration"] = df["Duration"].apply(convert_duration)

# ---------- Stops ----------
stop_map = {
    "non-stop": 0,
    "1 stop": 1,
    "2 stops": 2,
    "3 stops": 3,
    "4 stops": 4
}

df["Total_Stops"] = df["Total_Stops"].map(stop_map)
df["Total_Stops"] = df["Total_Stops"].fillna(df["Total_Stops"].mode()[0])

# ---------- Date Features ----------
df["Journey_Day"] = df["Date_of_Journey"].apply(lambda x: int(x.split('/')[0]))
df["Journey_Month"] = df["Date_of_Journey"].apply(lambda x: int(x.split('/')[1]))
df["Week_Group"] = df["Journey_Day"] % 7

# ---------- Time Features ----------
df["Dep_Hour"] = df["Dep_Time"].apply(lambda x: int(x.split(':')[0]))
df["Arrival_Hour"] = df["Arrival_Time"].apply(lambda x: int(x.split(':')[0]))

# ---------- Route ----------
df["Route"] = df["Route"].fillna("Unknown")
df["Route_Count"] = df["Route"].apply(lambda x: len(str(x).split('→')))

# ---------- Fuel ----------
df["Fuel_Index"] = (df["Duration"] * (df["Total_Stops"] + 1)) * 0.18

# ---------- Travel Features ----------
df["Hotel_Type"] = np.random.choice([0,1,2], len(df))
df["Season"] = np.random.choice([0,1,2], len(df))
df["User_Type"] = np.random.choice([0,1], len(df))
df["Days"] = np.random.randint(1,8, len(df))

# ---------- Encode ----------
le_airline = LabelEncoder()
le_source = LabelEncoder()
le_destination = LabelEncoder()

df["Airline"] = le_airline.fit_transform(df["Airline"])
df["Source"] = le_source.fit_transform(df["Source"])
df["Destination"] = le_destination.fit_transform(df["Destination"])

# ---------- Drop Unused ----------
df = df.drop([
    "Date_of_Journey",
    "Dep_Time",
    "Arrival_Time",
    "Route"
], axis=1)

# ---------- Features ----------
X = df.drop("Price", axis=1)
y = df["Price"]

# ---------- Split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------- Model ----------
model = RandomForestRegressor(
    n_estimators=700,
    max_depth=30,
    min_samples_split=3,
    random_state=42
)

model.fit(X_train, y_train)

# ---------- Evaluation ----------
y_pred = model.predict(X_test)

score = r2_score(y_test, y_pred)

print("Final Hybrid R2 Score:", score)