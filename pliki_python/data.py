# %% [markdown]
# # Import danych

# %% [markdown]
# Import funkcji z pliku [api_request.py](api_request.py)

# %%
import pandas as pd
import time
from api_request import stations, api_request

# %%
df_stations = stations()
id_stations = df_stations["Identyfikator stacji"].unique().tolist() # lista z id stacji, potrzebne do innych url API

# %% [markdown]
# ### Stanowiska pomiarowe
# 
# lista stanowisk pomiarowych dostępnych na wybranej stacji pomiarowej

# %%
df_sensors = api_request("station/sensors/", id_stations, "Lista stanowisk pomiarowych dla podanej stacji") 
id_sensors = df_sensors["Identyfikator stanowiska"].unique().tolist() # lista z id stanowisk, potrzebne do innych url API

# %% [markdown]
# ### Dane pomiarowe 
# 
# dane pomiarowe na podstawie podanego identyfikatora stanowiska pomiarowego

# %%
df_measures = api_request("data/getData/", id_sensors, "Lista danych pomiarowych", item_id = "id_stacji", add_id=True) 

# %% [markdown]
# ### Indeks jakości powietrza
# 
# indeksy jakości powietrza na podstawie podanego identyfikatora stacji pomiarowej

# %%
df_air = api_request("aqindex/getIndex/", id_stations, "AqIndex")

# %% [markdown]
# # 📊 Przegląd danych

# %% [markdown]
# ### Stacje pomiarowe

# %%
print(f"\nLiczba wierszy w df_stations: {len(df_stations)}\n")
time.sleep(2) 

# %%
print(df_stations.sample(5))
time.sleep(2) 

# %% [markdown]
# ### Stanowiska pomiarowe

# %%
len(df_sensors)

# %%
df_sensors.sample(5)

# %% [markdown]
# ### Dane pomiarowe

# %%
len(df_measures)

# %%
df_measures.sample(5)

# %%
df_measures.info()

# %% [markdown]
# ### Indeks jakości powietrza

# %%
len(df_air)

# %%
df_air.sample(5)

# %% [markdown]
# ## 🧹 Czyszczenie danych 

# %%
# zmiana nazw kolumn
df_stations.rename(columns={
    "WGS84 φ N": "Szerokość geograficzna (N)",
    "WGS84 λ E": "Długość geograficzna (N)"
}, inplace=True)

# %%
# zmiana nazw kolumn (kod wygenerowany przez czat GPT)

df_air = df_air.rename(columns={
    'Identyfikator stacji pomiarowej': 'id_stacji',
    'Data wykonania obliczeń indeksu': 'data_obliczenia',
    'Wartość indeksu': 'wartosc_indeksu',
    'Nazwa kategorii indeksu': 'kategoria_indeksu',

    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st': 'data_zrodlowa',

    'Data wykonania obliczeń indeksu dla wskaźnika SO2': 'so2_data_obliczenia',
    'Wartość indeksu dla wskaźnika SO2': 'so2_wartosc',
    'Nazwa kategorii indeksu dla wskażnika SO2': 'so2_kategoria',
    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika SO2': 'so2_data_zrodlowa',

    'Data wykonania obliczeń indeksu dla wskaźnika NO2': 'no2_data_obliczenia',
    'Wartość indeksu dla wskaźnika NO2': 'no2_wartosc',
    'Nazwa kategorii indeksu dla wskażnika NO2': 'no2_kategoria',
    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika NO2': 'no2_data_zrodlowa',

    'Data wykonania obliczeń indeksu dla wskaźnika PM10': 'pm10_data_obliczenia',
    'Wartość indeksu dla wskaźnika PM10': 'pm10_wartosc',
    'Nazwa kategorii indeksu dla wskażnika PM10': 'pm10_kategoria',
    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM10': 'pm10_data_zrodlowa',

    'Data wykonania obliczeń indeksu dla wskaźnika PM2.5': 'pm25_data_obliczenia',
    'Wartość indeksu dla wskaźnika PM2.5': 'pm25_wartosc',
    'Nazwa kategorii indeksu dla wskażnika PM2.5': 'pm25_kategoria',
    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM2.5': 'pm25_data_zrodlowa',

    'Data wykonania obliczeń indeksu dla wskaźnika O3': 'o3_data_obliczenia',
    'Wartość indeksu dla wskaźnika O3': 'o3_wartosc',
    'Nazwa kategorii indeksu dla wskażnika O3': 'o3_kategoria',
    'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika O3': 'o3_data_zrodlowa',

    'Status indeksu ogólnego dla stacji pomiarowej': 'status_stacji',
    'Kod zanieczyszczenia krytycznego': 'krytyczne_zanieczyszczenie'
})

# %%
# usuwanie ewentualnych pustych wierszy

df_stations.dropna(subset=["Identyfikator stacji"], inplace=True)
df_sensors.dropna(subset=["Identyfikator stanowiska", "Identyfikator stacji"], inplace=True) 
df_measures.dropna(subset=["Kod stanowiska"], inplace=True)
df_air.dropna(subset=["id_stacji"], inplace=True) 

# %%
# usuwanie ewentualnych duplikatów

df_stations.drop_duplicates(inplace=True, subset=["Identyfikator stacji"])
df_sensors.drop_duplicates(inplace=True, subset=["Identyfikator stanowiska", "Identyfikator stacji"])
df_measures.drop_duplicates(inplace=True, subset=["Kod stanowiska", "Data"])
df_air.drop_duplicates(inplace=True, subset=["id_stacji", "data_obliczenia"])

# %%
# usuwanie drukowanych liter
df_stations["Województwo"] = df_stations["Województwo"].str.capitalize()

# %%
df_stations.sample(3)

# %%
# konwersja wartości float na int

df_air["id_stacji"] = df_air["id_stacji"].astype(int)

cols = ["wartosc_indeksu", "so2_wartosc", "no2_wartosc", "pm10_wartosc", "pm25_wartosc", "o3_wartosc"]

df_air[cols] = df_air[cols].astype("Int64")

# %%
df_air.sample(3)


