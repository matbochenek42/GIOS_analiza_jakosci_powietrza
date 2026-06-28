# 💨 GIOŚ - analiza jakości powietrza

## 🔎 Intro

Niniejsze repozytorium skupia się na projekcie analizy danych pochodzących z API Głównego Inspektoriatu Ochrony Środowiska. Projekt ten można podzielić na cztery główne elementy:

![schemat](screeny/schemat.png)

- **Krok 1:** Pobranie cogodzinnych danych ze strony [powietrze.gios.gov.pl](https://powietrze.gios.gov.pl/pjp/content/api) przy użyciu skryptu Pythona - [api_request.py](pliki_python/api_request.py).

- **Krok 2:** Czyszczenie i zapis danych do plików CSV w Pandas w pliku [pipeline.py](pliki_python/pipeline.py).

- **Krok 3:** Automatyzacja pliku [pipeline.py](pliki_python/pipeline.py) w Github Actions za pomocą pliku [automation.yml](.github\workflows/automation.yml) (co 8 godzin).

- **Krok 4:** Analiza i wizualizacja danych w Excelu - [analiza.xlsx](analiza.xlsx).

Pozwala to na automatyczne pobieranie danych za pomocą API (wraz z usuwaniem duplikatów i czyszczeniem danych), zapis na chmurze (Github Actions) i automatycznym pobieraniem tych danych w Excelu (Power Query).

**Źródło danych:** [GIOŚ - EKOINFONET](https://powietrze.gios.gov.pl/pjp/content/api)

**Uwaga:** informacje o danych (rodzaje zanieczyszczenia powietrza) użytych w projekcie znajdziesz [tutaj](dane/dane.md). 

## 🧱 Schemat repozytorium

| Folder / Plik | Opis |
|----------------|-------------|
| **.github/workflows** | Folder w którym znajduje się skrypt automatyzujący pobieranie danych w Github Actions w formacie .yml |
| **dane/** | Folder zawierający dane źródłowe pobierane przez API w formacie CSV |
| **pliki_python/** | Folder zawierający skrypty Pythona pozwalające na pobieranie i czyszczenie danych |
| **screeny/** | Folder zawierający screeny projektu |
| **.gitignore** | Wskazanie plików, które powinny być ignorowane na Github |
| **analiza.xlsx** | ... |
| **README.md** | Opis repozytorium |
| **requirements.txt** | Plik zawierający dodatkowe biblioteki Pythona, które Github musi pobrać w celu automatyzacji pliku pipeline.py |


## 📊 Wizualizacja

![Dashboard](screeny/dashboard.gif)

Dashboard możesz zobaczyć i pobrać [tutaj](analiza.xlsx)

## 💡 Wnioski

## 🖥️ Szczegóły techniczne
- **Narzędzia wykorzystane w projekcie:** Python, Pandas, Github Actions, Excel, Power Query
- **Źródło danych:** [Generalny Inspektoriat Ochrony Środowiska](https://powietrze.gios.gov.pl/pjp/current) 
    - Link do API: https://api.gios.gov.pl/pjp-api/swagger-ui/index.html
    - Dokumentacja API: https://powietrze.gios.gov.pl/pjp/content/api


## ✒️ Autor

- **Autor:** Mateusz Bochenek
- **E-mail:** matbochenek42@gmail.com
- **Profil GitHub:** https://github.com/matbochenek42
- **Profil LeetCode:** https://leetcode.com/u/SmO7BWmsiz/