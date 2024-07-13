import requests

def fetch_radio_stations_by_country(country):
    url = f'http://www.radio-browser.info/webservice/json/stations/bycountryexact/{country}'
    response = requests.get(url)
    return response.json()

def fetch_radio_stations_by_genre(genre):
    url = f'http://www.radio-browser.info/webservice/json/stations/bytag/{genre}'
    response = requests.get(url)
    return response.json()

def fetch_radio_stations_by_language(language):
    url = f'http://www.radio-browser.info/webservice/json/stations/bylanguage/{language}'
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    country = 'United States'
    genre = 'pop'
    language = 'English'
    
    print("Fetching radio stations by country...")
    stations_by_country = fetch_radio_stations_by_country(country)
    print(stations_by_country[:5])  # Print first 5 stations for brevity
    
    print("Fetching radio stations by genre...")
    stations_by_genre = fetch_radio_stations_by_genre(genre)
    print(stations_by_genre[:5])  # Print first 5 stations for brevity
    
    print("Fetching radio stations by language...")
    stations_by_language = fetch_radio_stations_by_language(language)
    print(stations_by_language[:5])  # Print first 5 stations for brevity
