# Импортируем библеотеку psycopg2 для работы с базой данных
import psycopg2
# Импортируем функции get_employer_info и get_vacancies которые дают нам данные от api.
from api_hh import get_employer_info, get_vacancies
# Импортируем config
from config import config

def create_database(db_name):
    """
    Создаем базу данных.
    :param db_name: Имя базы данных.
    """
    # Подключаемся к серверу PostgreSQL
    conn = psycopg2.connect(
        host=config()['host'],
        database='',
        user=config()['user'],
        password=config()['password']
    )
    # Включаем автокоммит для создания базы данных
    conn.autocommit = True
    cur = conn.cursor()
    # Удаляем базу данных, если она существует
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    # Создаем новую базу данных
    cur.execute(f"CREATE DATABASE {db_name}")
    # Закрываем соединение
    conn.close()

def create_companies_table(db_name):
    """  Создает таблицу компаний в указанной базе данных. """
    conn = psycopg2.connect(
        host=config()['host'],
        database=db_name,
        user=config()['user'],
        password=config()['password']
    )
    cur = conn.cursor()
    # Создаем таблицу компаний, если она не существует
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL UNIQUE,
            company_url VARCHAR(255) NOT NULL
        );
    """)
    # Подверждаем изменения
    conn.commit()
    # Закрываем соединение
    conn.close()

def create_vacancies_table(db_name):
    """ Создаем таблицу вакансий в указанной базе данных. """
    conn = psycopg2.connect(
        host=config()['host'],
        database=db_name,
        user=config()['user'],
        password=config()['password']
    )
    cur = conn.cursor()
    # Создаем таблицу вакансий, если она не существует
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            vacancy_name VARCHAR(255) NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            company_id INTEGER REFERENCES companies(company_id),
            salary_from INTEGER,
            salary_to INTEGER,
            snippet_requirements VARCHAR(255),
            snippet_responsibilities VARCHAR(255),
            vacancy_url VARCHAR(255) NOT NULL
        );
    """)
    # Подверждаем изменения
    conn.commit()
    # Закрываем соединение
    conn.close()

def insert_vacancies(db_name, list_companies):
    """ Вставляет вакансии в таблицу вакансий на основе информации о компаниях. """
    conn = psycopg2.connect(
        host=config()['host'],
        database=db_name,
        user=config()['user'],
        password=config()['password']
    )
    with conn.cursor() as cur:
        # Проходим по списку компаний
        for company_id in list_companies:
            # Получаем информацию о работодателе
            employer_info = get_employer_info(company_id)
            # Получаем вакансии для компании
            vacancies = get_vacancies(company_id)
            if employer_info:
                # Название компании
                company_name = employer_info.get('name', 'Неизвестная компания')
                # Ссылка на компанию
                company_url = employer_info.get('alternate_url', '')
                # Вставляем информацию о компании в таблицу
                cur.execute("""
                    INSERT INTO companies (company_name, company_url)
                    VALUES (%s, %s)
                    ON CONFLICT (company_name) DO NOTHING
                    RETURNING company_id
                """, (company_name, company_url))

                # Получаем ID компании, если вставка успешна
                company_id = cur.fetchone()
                if company_id:
                    company_id = company_id[0]
                    # Проходим по списку вакансий для компании
                    for vacancy in vacancies:
                        vacancy_name = vacancy['name'] # Название вакансии
                        salary_from = vacancy['salary']['from'] if vacancy['salary'] else None # Минимальная зарпалата
                        salary_to = vacancy['salary']['to'] if vacancy['salary'] else None # Максимальная зарплата
                        snippet_requirements = vacancy['snippet']['requirement'] if 'snippet' in vacancy else '' # Требования, навыки, знания для вакансии
                        snippet_responsibilities = vacancy['snippet']['responsibility'] if 'snippet' in vacancy else '' # Обязанности
                        vacancy_url = vacancy['alternate_url']

                        # Вставляем информацию о вакансии в таблицу
                        cur.execute("""
                            INSERT INTO vacancies (vacancy_name, company_id, company_name, salary_from, salary_to, snippet_requirements, snippet_responsibilities, vacancy_url)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            vacancy_name, company_id, company_name, salary_from, salary_to,
                            snippet_requirements, snippet_responsibilities, vacancy_url
                        ))
        # Подтверждаем изминения
        conn.commit()
    # Закрываем соединение
    conn.close()