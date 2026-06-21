# 💨 GIOŚ - analiza jakości powietrza

## 🔎 Intro

Niniejsze repozytorium skupia się na projekcie analizy danych pochodzących z API Głównego Inspektoriatu Ochrony Środowiska. Projekt ten można podzielić na cztery główne elementy:

- **Krok 1:** Pobranie cogodzinnych danych ze strony [powietrze.gios.gov.pl](https://powietrze.gios.gov.pl/pjp/content/api) przy użyciu skryptu Pythona - [api_request.py](pliki_python/api_request.py).

- **Krok 2:** Czyszczenie i zapis danych do plików CSV w Pandas w pliku [pipeline.py](pliki_python/pipeline.py).

- **Krok 3:** Automatyzacja pliku [pipeline.py](pliki_python/pipeline.py) w Github Actions za pomocą pliku [automation.yml](.github\workflows/automation.yml) (co 8 godzin).

- **Krok 4:** Analiza i wizalizacja danych w Excelu - [analiza.xlsx](analiza.xlsx).

Pozwala to na codzienne automatyczne pobieranie danych za pomocą API (wraz z usuwaniem duplikatów i czyszczeniem danych), zapis na chmurze (Github Actions) i automatycznym pobieraniem tych danych w Excelu (Power Query).

Źródło danych: GIOŚ - EKOINFONET https://powietrze.gios.gov.pl/pjp/content/api

## ⚙️ How to Run

Pyły zawieszone (PM 2.5 i PM 10)

PM 2.5: To mikroskopijne cząstki o wielkości do 2,5 mikrometra. Z powodu swoich minimalnych rozmiarów są niezwykle niebezpieczne – potrafią bezpośrednio przenikać do układu krwionośnego. Przekroczenie określonych dla nich norm skutkuje ogłoszeniem alarmu smogowego.

PM 10: To zawiesina cząsteczek o średnicy nieprzekraczającej 10 mikrometrów. Ich szkodliwość wynika z obecności substancji rakotwórczych, takich jak metale ciężkie, dioksyny, furany czy benzopireny. Ten rodzaj pyłu atakuje przede wszystkim ludzki układ oddechowy.

Źródło danych: https://airly.org/pl/pyl-zawieszony-czym-jest-pm10-a-czym-pm2-5-aerozole-atmosferyczne/

Dwutlenek azotu (NO2)

Jest to gaz o wysokiej reaktywności i silnych właściwościach utleniających. Odgrywa kluczową rolę w formowaniu się smogu oraz innych niebezpiecznych substancji (np. ozonu czy cząstek stałych). Może powstawać wtórnie w wyniku reakcji chemicznych w atmosferze. Dalsze procesy utleniania NO2 prowadzą do powstania kwasu azotowego (HNO3), który opada na glebę w formie kropli lub cząsteczek azotanów. Wysokie stężenie tego gazu zagraża głównie dzieciom, astmatykom oraz osobom z problemami kardiologicznymi i oddechowymi.

Źródło danych: https://www.iqair.com/pl/newsroom/nitrogen-dioxide


Dwutlenek siarki (SO2)

To bardzo toksyczny gaz o charakterystycznej, duszącej woni. Trafia do powietrza głównie przez cały rok z powodu działalności przemysłowej, a w sezonie grzewczym – w wyniku spalania węgla w domowych piecach. Związki siarki mają silne właściwości zakwaszające, co prowadzi m.in. do powstawania kwaśnych opadów. Zjawisko to niszczy środowisko: obniża żyzność i jakość gleb, hamuje rozwój roślinności, a nawet doprowadza do jej usychania.

Źródło danych: https://smoglab.pl/dwutlenek-siarki-w-polsce-zle-na-balkanach-gorzej-czym-truje-nas-smog-4/

Ozon troposferyczny (O3)
W przeciwieństwie do ozonu w wyższych partiach Ziemi, ten występujący blisko powierzchni (w troposferze) jest szkodliwym zanieczyszczeniem wtórnym. Tworzy się w wyniku reakcji tlenków azotu i lotnych związków organicznych, które zachodzą pod wpływem słońca i upałów. Z tego powodu jego najwyższe stężenia notuje się wiosną i latem. Ozon łatwo przemieszcza się na dalekie dystanse, stąd jego ilość w Polsce zależy często od mas powietrza z południa i południowego zachodu Europy.
Dla człowieka jest toksyczny – wywołuje podrażnienia oczu, infekcje dróg oddechowych, zmniejsza wydolność płuc i nasila astmę. Broniący się przed nim organizm ogranicza pobór tlenu, co obciąża układ krążenia. Powoduje też bóle głowy, senność, zmęczenie oraz spadek ciśnienia. Ponadto niszczy rośliny i przyspiesza niszczenie (korozję) materiałów.

Źródło danych: https://powietrze.gios.gov.pl/pjp/content/show/1000577