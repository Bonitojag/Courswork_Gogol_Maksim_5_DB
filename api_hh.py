# Импортируем бибдеотеку requests для работы с API
import requests

def get_employer_info(employer_id):
    """
    Получает информацию о работодателе по его идентификатору.
    :param employer_id: Идентификатор работодателя.
    :return: Словарь с информацией о работодателе, если запрос успешен; иначе пустой словарь.
    """
    api_endpoint = f"https://api.hh.ru/employers/{employer_id}"  # Формируем URL для запроса
    response = requests.get(api_endpoint)  # Отправляем GET-запрос
    if response.status_code == 200:  # Проверяем успешность запроса
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(
            f"Ошибка при получении информации о работодателе {employer_id}: {response.status_code}")  # Выводим сообщение об ошибке
        return {}  # Возвращаем пустой словарь в случае ошибки


def get_vacancies(employer_id):
    """
    Получает список вакансий для указанного работодателя.
    :param employer_id: Идентификатор работодателя.
    :return: Список вакансий (каждая вакансия представлена в виде словаря), если запрос успешен; иначе пустой список.
    """
    api_endpoint = f"https://api.hh.ru/vacancies"  # Формируем URL для запроса
    params = {"employer_id": employer_id}  # Параметры запроса
    response = requests.get(api_endpoint, params=params)  # Отправляем GET-запрос с параметрами
    if response.status_code == 200:  # Проверяем успешность запроса
        return response.json().get('items', [])  # Возвращаем список вакансий
    else:
        print(
            f"Ошибка при получении вакансий для работодателя {employer_id}: {response.status_code}")  # Выводим сообщение об ошибке
        return []  # Возвращаем пустой список в случае ошибки


def get_vacancies_from_api(employer_id):
    """
    Получает вакансии для работодателя, используя функцию get_vacancies.
    :param employer_id: Идентификатор работодателя.
    :return: Список вакансий для указанного работодателя.
    """
    return get_vacancies(employer_id)  # Вызываем функцию для получения вакансий




