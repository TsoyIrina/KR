import requests

url = 'http://127.0.0.1:8080/'


def take_airports():
    url_airs = url + 'airports'
    list_airports = []
    res = requests.get(url_airs).json()
    for i in res:
        list_airports.append((i['code'], i["name"]))
    return list_airports


def take_flights(air_from, air_to, stops):
    url_line = url + f'routes/{air_from}/{air_to}?max_stops={stops}'
    res = requests.get(url_line).json()
    return res


def take_flight(id_flight):
    url_flight = url + 'flights'
    flights = requests.get(url_flight).json()
    res_flight = next(flight for flight in flights if flight['id'] == id_flight)
    return res_flight


# take_flights('FNJ', 'TRC', 2)
# print(take_flight(1))

# [{'num_stops': 1,
# 'flights': [
# {'id': 1002, 'from_airport': {'id': 3, 'code': 'ENA', 'name': 'Kenai Municipal Airport'},
# 'to_airport': {'id': 4, 'code': 'LKN', 'name': 'Leknes Airport'},
# 'airline': {'id': 1, 'code': 'IN', 'name': 'NAM Air'}, 'price': 100},
# {'id': 1003, 'from_airport': {'id': 4, 'code': 'LKN', 'name': 'Leknes Airport'},
# 'to_airport': {'id': 5, 'code': 'KLF', 'name': 'Grabtsevo Airport'},
# 'airline': {'id': 1, 'code': 'IN', 'name': 'NAM Air'},
# 'price': 100}],
# 'total_price': 200}]


# [{'num_stops': 0,
# 'flights': [
# {'id': 6, 'from_airport': {'id': 247, 'code': 'FNJ', 'name': 'Pyongyang Sunan International Airport'},
#      'to_airport': {'id': 223, 'code': 'TRC', 'name': 'Francisco Sarabia International Airport'},
#      'airline': {'id': 186, 'code': 'D7', 'name': 'AirAsia X'},
#      'price': 2293.97}],
#      'total_price': 2293.97}]
