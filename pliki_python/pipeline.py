# plik eksportowany z overview_danych.ipynb

import pandas as pd
import os
from datetime import datetime
from api_request import stations, api_request

def run_pipeline():
    """
    zapis danych do dataframe, czyszczenie danych, usuwanie duplikatów, zapis do pliku csv
    """
    # Stacje pomiarowe                       # tu by się przydało dać obsługę wyjątków?
    df_stations = stations()
    id_stations = df_stations["Identyfikator stacji"].unique().tolist() # lista z id stacji, potrzebne do innych url API

    # Stanowiska pomiarowe
    df_sensors = api_request("station/sensors/", id_stations, "Lista stanowisk pomiarowych dla podanej stacji") 
    id_sensors = df_sensors["Identyfikator stanowiska"].unique().tolist() # lista z id stanowisk, potrzebne do innych url API

    # Dane pomiarowe 
    df_measures = api_request("data/getData/", id_sensors, "Lista danych pomiarowych", item_id = "id_stacji", add_id=True) 

    # Indeks jakości powietrza
    df_air = api_request("aqindex/getIndex/", id_stations, "AqIndex")

    # 🧹 Czyszczenie danych 

    # zmiana nazw kolumn
    df_stations.rename(columns={
        "WGS84 φ N": "Szerokość geograficzna (N)",
        "WGS84 λ E": "Długość geograficzna (E)"
    }, inplace=True)


    # zmiana nazw kolumn 
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

    # usuwanie ewentualnych pustych wierszy
    df_stations.dropna(subset=["Identyfikator stacji"], inplace=True)
    df_sensors.dropna(subset=["Identyfikator stanowiska", "Identyfikator stacji"], inplace=True) 
    df_measures.dropna(subset=["Kod stanowiska"], inplace=True)
    df_air.dropna(subset=["id_stacji"], inplace=True) 

    # usuwanie ewentualnych duplikatów
    df_stations.drop_duplicates(inplace=True, subset=["Identyfikator stacji"])
    df_sensors.drop_duplicates(inplace=True, subset=["Identyfikator stanowiska", "Identyfikator stacji"])
    df_measures.drop_duplicates(inplace=True, subset=["Kod stanowiska", "Data"])
    df_air.drop_duplicates(inplace=True, subset=["id_stacji", "data_obliczenia"])

    # usuwanie drukowanych liter
    df_stations["Województwo"] = df_stations["Województwo"].str.capitalize()

    # konwersja wartości float na int
    df_air["id_stacji"] = df_air["id_stacji"].astype(int)
    cols = ["wartosc_indeksu", "so2_wartosc", "no2_wartosc", "pm10_wartosc", "pm25_wartosc", "o3_wartosc"]
    df_air[cols] = df_air[cols].astype("Int64")

    # tworzenie ścieżek i folderów
    main_folder = "dane"
    measures_folder = f"{main_folder}/pomiary"
    air_folder = f"{main_folder}/powietrze"

    os.makedirs(main_folder, exist_ok=True)
    os.makedirs(measures_folder, exist_ok=True)
    os.makedirs(air_folder, exist_ok=True)

    df_stations.to_csv(f"{main_folder}/stacje_pomiarowe.csv", mode="w", index=False, encoding="utf-8-sig")
    df_sensors.to_csv(f"{main_folder}/stanowiska_pomiarowe.csv", mode="w", index=False, encoding="utf-8-sig")

    # partycjonowanie plików wg. aktualnego miesięca i roku
    now = datetime.now()
    current_month = now.strftime("%Y_%m")

    measures_path = f"{measures_folder}/dane_pomiarowe_{current_month}.csv"
    air_path = f"{air_folder}/jakosc_powietrza_{current_month}.csv"
    
    # usuwanie potencjalnych duplikatów między nowym df a istniejącymi już danymi w pliku csv
    if os.path.exists(measures_path):
        existing_measures_keys = pd.read_csv(measures_path, usecols=["Kod stanowiska", "Data"]) # odczyt tylko istotnych kolumn
        
        # dopasowanie kluczy 
        # zostają tylko wiersze unikalne dla nowych wierszy
        merged_measures = df_measures.merge(existing_measures_keys, on=["Kod stanowiska", "Data"], how="left", indicator=True)
        df_measures = merged_measures[merged_measures["_merge"] == "left_only"].drop(columns=["_merge"])

    # zapis do csv jeśli są nowe wiersze
    if not df_measures.empty:
        df_measures.to_csv(measures_path, mode="a", index=False, encoding="utf-8-sig", header=not os.path.exists(measures_path))

    if os.path.exists(air_path):
        existing_air_keys = pd.read_csv(air_path, usecols=["id_stacji", "data_obliczenia"])
        
        # existing_air_keys["id_stacji"] = existing_air_keys["id_stacji"].astype(int)
        
        merged_air = df_air.merge(existing_air_keys, on=["id_stacji", "data_obliczenia"], how="left", indicator=True)
        df_air = merged_air[merged_air["_merge"] == "left_only"].drop(columns=["_merge"])


    if not df_air.empty:
        df_air.to_csv(air_path, mode="a", index=False, encoding="utf-8-sig", header=not os.path.exists(air_path))

    # encoding="utf-8-sig" -> żeby nie było błędów w Power Query
    # header=not os.path.exists("jakosc_powietrza.csv") -> jeśli plik nie istnieje dodaj też nazwy kolumn, jeśli istnieje to nie dodawaj nazw kolumn

if __name__ == "__main__":
    run_pipeline()
