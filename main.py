import requests
from prettytable import PrettyTable

API_KEY = '94bf55895d4dc4befdaa831a389ef988'
BASE_URL = 'https://api.themoviedb.org/3'
NOW_PLAYING_URL = f'{BASE_URL}/movie/now_playing'
SEARCH_MOVIE_URL = f'{BASE_URL}/search/movie'


def obtenir_cinemes(ciutat):
    params = {
        'api_key': API_KEY,
        'region': ciutat
    }
    try:
        response = requests.get(NOW_PLAYING_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f'Error en fer la sol·licitud a l\'API: {e}')
        return []


def obtenir_info_pelicula(id_pelicula):
    url = f'{BASE_URL}/movie/{id_pelicula}'
    params = {
        'api_key': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f'Error en fer la sol·licitud a l\'API: {e}')
        return None


def imprimir_info_pelicula(pelicula):
    table = PrettyTable()
    table.field_names = ['Títol', 'Data de Publicació', 'Resum']
    table.add_row([pelicula.get('title', ''), pelicula.get('release_date', ''), pelicula.get('overview', '')])

    # Estableix l'amplada màxima per a cada columna
    table.max_width['Títol'] = 30
    table.max_width['Data de Publicació'] = 12
    table.max_width['Resum'] = 50

    print(table)


def imprimir_cinemes(cinemes):
    if cinemes:
        for cinema in cinemes:
            imprimir_info_pelicula(cinema)
    else:
        print('No s\'han trobat resultats.')


def buscar_pelicula(nom_pelicula):
    params = {
        'api_key': API_KEY,
        'query': nom_pelicula
    }
    try:
        response = requests.get(SEARCH_MOVIE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f'Error en fer la sol·licitud a l\'API: {e}')
        return []


def menu_principal():
    print('1. Consultar la cartellera d\'una ciutat')
    print('2. Llistar la cartellera de Girona')
    print('3. Buscar si una pel·lícula està en cartellera')
    print('4. Sortir')


def seleccionar_ciutat():
    ciutat = input('Introdueix el nom de la ciutat: ')
    return ciutat


def seleccionar_pelicula():
    pelicula = input('Introdueix el nom de la pel·lícula: ')
    return pelicula


def mostrar_cinemes():
    ciutat = seleccionar_ciutat()
    cinemes = obtenir_cinemes(ciutat)
    imprimir_cinemes(cinemes)


def mostrar_pelicules_girona():
    cinemes = obtenir_cinemes('Girona')
    imprimir_cinemes(cinemes)


def buscar_pelicula_en_cartellera():
    nom_pelicula = seleccionar_pelicula()
    pelicules = buscar_pelicula(nom_pelicula)
    if pelicules:
        pelicula = pelicules[0]  # Obtenir la primera pel·lícula de la llista
        print('La pel·lícula està en cartellera:')
        imprimir_info_pelicula(pelicula)
    else:
        print('La pel·lícula no està en cartellera.')


def main():
    menu_principal()
    opcio = input('Selecciona una opció: ')
    if opcio == '1':
        mostrar_cinemes()
    elif opcio == '2':
        mostrar_pelicules_girona()
    elif opcio == '3':
        buscar_pelicula_en_cartellera()
    elif opcio == '4':
        print('¡Fins aviat!')
        exit()
    else:
        print('Opció invàlida. Torna-ho a intentar.')

    print("\nPrem ENTER per continuar...")
    input()
    main()


if __name__ == '__main__':
    main()
