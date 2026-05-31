"""
Ten plik ma za zadanie pobrać dane (za pomocą API) i załadować je do DataFrame
Dokumentacja API: https://powietrze.gios.gov.pl/pjp/content/api
"""

import pandas as pd
import requests

def stations(): # Stacje pomiarowe
    
    print("Trwa ładowanie danych z API do DataFrame...\n")

    results = [] # pusta lista, która ma służyć do zapisu danych i konwersji do DataFrame
    url_stations = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll" # API url

    # sprawdzanie czy udało się nawiązać połączenie z API
    try:
        response_stations = requests.get(url_stations, timeout=10) 
        response_stations.raise_for_status() 
        
        data_stations = response_stations.json()

        station = data_stations.get("Lista stacji pomiarowych", [])
        results.extend(station) # dodawanie danych do listy

    except requests.exceptions.RequestException as e:
        print(f"Nie udało się połączyć z API ❌")
        # print(e)

    if results:
        print("Poprawno załadowano dane ✅")
        return pd.DataFrame(results) # DataFrame
    else:
        print("Połączono z API, ale nie zwróciło żadnych danych ⚠️")
        return pd.DataFrame()


# poniższa funkcja działa podobnie jak ww. funkcja stations(), natomiast zawiera ona element iteracji przez ID z innych dataframe'ów 

def api_request(api_url, id_list, column_name, base_url = "https://api.gios.gov.pl/pjp-api/v1/rest/", item_id = None, add_id = False): # opcjonalnie dodać add_date = False
    
    print("Trwa ładowanie danych z API do DataFrame...\n")

    results = []
    no_output = []
    item_count = 1

    with requests.Session() as session:
        for i in id_list:
            url = f"{base_url}{api_url}{i}"

            item_count += 1

            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()

                data_json = response.json()

                api_data = data_json.get(column_name)

                if api_data is None:
                    no_output.append(i)
                    continue
                
                # now = pd.Timestamp("now")

                if isinstance(api_data, list):
                    if add_id: # dodanie id stacji dla API: df_measures = api_request("data/getData/", id_sensors, "Lista danych pomiarowych", add_id=True) 
                        api_data = [{**item, item_id: i} for item in api_data]
                    results.extend(api_data)

                elif isinstance(api_data, dict): # specjalny warunek dla: df_air = api_request("aqindex/getIndex/", id_stations, "AqIndex")
                    """
                    if add_id:
                        api_data[item_id] = i
                        api_data["data_dodania"] = now
                    """
                    results.append(api_data)

            except requests.exceptions.RequestException as e: # liczenie iteracji dla którego nie nawiązano połączenia
                no_output.append(i)

        if no_output:
            print(f"Nie udało się połączyć z API dla '{column_name}'. {len(no_output)} z {item_count} wszystkich wartości nie dodano do DataFrame ❌")
        else:
            print(f"Wszystkie wartości dla '{column_name}' zostały załadowane ✅")

        return pd.DataFrame(results)

"""
# Stacje pomiarowe
df_stations = stations()
id_stations = df_stations["Identyfikator stacji"].unique().tolist() # lista z id stacji, potrzebne do innych url API

# Stanowiska pomiarowe
df_sensors = api_request("station/sensors/", id_stations, "Lista stanowisk pomiarowych dla podanej stacji") # lista stanowisk pomiarowych dostępnych na wybranej stacji pomiarowej
id_sensors = df_sensors["Identyfikator stanowiska"].unique().tolist() # lista z id stanowisk, potrzebne do innych url API

# Dane pomiarowe 
df_measures = api_request("data/getData/", id_sensors, "Lista danych pomiarowych", item_id = "id_stacji", add_id=True) # dane pomiarowe na podstawie podanego identyfikatora stanowiska pomiarowego

# Indeks jakości powietrza
df_air = api_request("aqindex/getIndex/", id_stations, "AqIndex") # indeksy jakości powietrza na podstawie podanego identyfikatora stacji pomiarowej
"""