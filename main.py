# Импортируем список ID компаний, функции для создания базы данных и таблиц
from companies_list import list_companies
from db_creator import create_database, create_companies_table, create_vacancies_table, insert_vacancies
# Импортируем класс DBManager который взаимодействует и управляет базой данных
from db_manager import DBManager

def main():
    """
    Основная функция программы, которая управляет созданием базы данных,
    вставкой вакансий и взаимодействием с пользователем через меню
    """
    db_name = 'courswork_5_gogol_maksim'

    # Создание базы данных и таблиц
    create_database(db_name)
    create_companies_table(db_name)
    create_vacancies_table(db_name)

    # Вставка вакансий в базу данных
    insert_vacancies(db_name, list_companies)

    # Создание экземпляра DBManager для работы с базой данных
    db_manager = DBManager(db_name)

    # Основное меню для взаимодействия с пользователем
    while True:
        print("1. Получить список компаний и количество вакансий")
        print("2. Получить все вакансии")
        print("3. Получить среднюю зарплату")
        print("4. Получить вакансии с зарплатой выше средней")
        print("5. Получить вакансии с ключевым словом")
        print("6. Выход")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            # Получаем список компаний и количество вакансий от каждой компании
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            for company, vacancy_count in companies_and_vacancies:
                print(f"Компания: {company}, Количество вакансий: {vacancy_count}")
        elif choice == "2":
            # Получаем все вакансии
            all_vacancies = db_manager.get_all_vacancies()
            for vacancy in all_vacancies:
                try:
                    print(
                        f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")
                except UnicodeEncodeError:
                    # Обработка ошибки, если возникнет проблема с кодировкой
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}".replace('\u2060', '' ))
        elif choice == "3":
            # Получаем среднюю з/п
            avg_salary = db_manager.get_avg_salary()[0]
            print(f"Средняя зарплата: {avg_salary}")
        elif choice == "4":
            # Получаем все вакансии чья з/п выше средней
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in higher_salary_vacancies:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}, Обязанности: {vacancy[3]}, Компания: {vacancy[4]}")
        elif choice == "5":
            # Получаем вакансии и данные по ним по ключевому слову
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in keyword_vacancies:
                print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Ссылка: {vacancy[2]}, Компания: {vacancy[3]}")
        elif choice == "6":
            # Выход из цикла while
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")
    # Закрываем соединение с базой данных
    db_manager.close()

if __name__ == "__main__":
    main()
