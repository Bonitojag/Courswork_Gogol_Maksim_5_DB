from typing import Any
# Импортируем библеотеку psycopg2 для работы с базой данных
import psycopg2
# Импортирум функцию config
from config import config

class DBManager:
    """Класс для управления базой данных вакансий."""
    def __init__(self, db_name):
        """
        Инициализация базы данных.
        :param db_name: Имя базы данных.
        :raises Exception: Если не удалось подключиться к базе данных.
        """
        self.conn = psycopg2.connect(
        host=config()['host'],
        database=db_name,
        user=config()['user'],
        password=config()['password']
    )
        self.cur = self.conn.cursor()
        if not self.conn:
            raise Exception("Failed to connect to database")

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """
        Получить список компаний и количество вакансий у каждой компании.
        :return: Список кортежей, где каждый кортеж содержит имя компании и количество вакансий.
        """
        self.cur.execute("""
            SELECT companies.company_name, COUNT(vacancies.vacancy_id) AS vacancy_count 
            FROM companies  
            LEFT JOIN vacancies ON companies.company_id = vacancies.company_id 
            GROUP BY companies.company_name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """
        Получить все вакансии с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: Список кортежей, где каждый кортеж содержит информацию о вакансии.
        """
        self.cur.execute("""
            SELECT companies.company_name AS company_name, 
               vacancies.vacancy_name, 
               vacancies.salary_from,
               vacancies.salary_to,
               vacancies.vacancy_url
               FROM vacancies
               LEFT JOIN companies  ON vacancies.company_id = companies.company_id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> tuple[Any, ...] | None:
        """
        Получить среднюю зарплату по вакансиям.
        :return: Средняя зарплата
        """
        self.cur.execute("""
            SELECT AVG(vacancies.salary_to) AS avg_salary 
            FROM vacancies 
            WHERE vacancies.salary_to IS NOT NULL
        """)
        return self.cur.fetchone()

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """
        Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Список кортежей с информацией о вакансиях.
        """

        avg_salary = self.get_avg_salary()[0]
        self.cur.execute("""
            SELECT vacancies.vacancy_name, vacancies.salary_to, vacancies.vacancy_url, vacancies.snippet_responsibilities, vacancies.company_name
            FROM vacancies 
            LEFT JOIN companies  ON vacancies.company_id = companies.company_id 
            WHERE vacancies.salary_to IS NOT NULL AND vacancies.salary_to > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> list[tuple[Any, ...]]:
        """
        Получить список всех вакансий, в названии которых содержатся переданные в метод слова.
        :param keyword: Ключевое слово для поиска в названии вакансии.
        :return: Список кортежей с информацией о вакансиях.
        """
        self.cur.execute("""
            SELECT vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url, vacancies.company_name 
            FROM vacancies 
            LEFT JOIN companies c ON vacancies.company_id = c.company_id 
            WHERE vacancies.vacancy_name LIKE %s
        """, (f"%{keyword}%",))
        return self.cur.fetchall()

    def close(self) -> None:
        """Закрыть соединение с базой данных."""
        self.conn.close()
