import json
import shutil
import sqlite3
import os

DB_FOLDER = "databases"
ADMIN_PASSWORD = "admin"

USERS_FILE = "users.json"
GUESTS_FILE = "guests.json"

def authenticate_admin():
    password_attempt = input("Введите пароль: ")
    return password_attempt == ADMIN_PASSWORD

def authenticate_user():
    users = load_data(USERS_FILE)
    password_attempt = input("Введите пароль: ")
    for user in users:
        if user["password"] == password_attempt:
            return True
    return False

def guest():
    password_attempt = input("Введите пароль: ")
    return "" == password_attempt

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)
def create_admin_database(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            salary INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def view_all_data(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM people')
    all_data = cursor.fetchall()

    conn.close()

    if all_data:
        print("Вся информация из БД:")
        for row in all_data:
            print(row)
    else:
        print("База данных пуста.")

def view_name(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM people')
    all_data = cursor.fetchall()

    conn.close()

    if all_data:
        print("Вся информация из БД:")
        for row in all_data:
            print(row)
    else:
        print("База данных пуста.")

def insert_person(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    name = input("Введите имя человека: ")
    age = int(input("Введите возраст человека: "))
    salary = int(input("Введите зарплату человека: "))

    cursor.execute('INSERT INTO people (name, age, salary) VALUES (?, ?, ?)', (name, age, salary))

    conn.commit()
    conn.close()

def edit_person(db_name):
    db_path = os.path.join(DB_FOLDER, f"{db_name}.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    person_id = int(input("Введите ID человека для редактирования: "))

    cursor.execute('SELECT * FROM people WHERE id = ?', (person_id,))
    person = cursor.fetchone()

    if person:
        print(f"Текущая информация: ID={person[0]}, Имя={person[1]}, Возраст={person[2]}, Зарплата={person[3]}")

        new_name = input("Введите новое имя (оставьте пустым, чтобы не изменять): ")
        new_age = input("Введите новый возраст (оставьте пустым, чтобы не изменять): ")
        new_salary = input("Введите новую зарплату (оставьте пустым, чтобы не изменять): ")

        if new_name:
            cursor.execute('UPDATE people SET name = ? WHERE id = ?', (new_name, person_id))
        if new_age:
            cursor.execute('UPDATE people SET age = ? WHERE id = ?', (new_age, person_id))
        if new_salary:
            cursor.execute('UPDATE people SET salary = ? WHERE id = ?', (new_salary, person_id))

        print(f"Информация о человеке с ID={person_id} успешно обновлена.")
    else:
        print(f"Сотрудник с ID={person_id} не найден.")

    conn.commit()
    conn.close()

def delete_database(db_name):
    if authenticate_admin():
        db_path = os.path.join(DB_FOLDER, f"{db_name}.db")
        try:
            os.remove(db_path)
            print(f"База данных '{db_name}' успешно удалена!")
        except FileNotFoundError:
            print(f"Базы данных '{db_name}' не существует.")

def delete_all_databases():
    if authenticate_admin():
        db_path = os.path.join(DB_FOLDER)

        try:
            shutil.rmtree(db_path)
            print(f"Папка с базами данных успешно удалена!")
        except FileNotFoundError:
            print(f"Папка с базами данных не удаётся удалить!")
    else:
        print("Неверный пароль администратора.")


def add_user():
    users = load_data(USERS_FILE)

    username = input("Введите имя пользователя: ")
    password = input("Введите пароль пользователя: ")

    users.append({"username": username, "password": password})
    save_data(users,USERS_FILE)

    print(f"Пользователь {username} успешно добавлен.")

def add_quest():
    users = load_data(GUESTS_FILE)

    username = input("Введите имя нового пользователя: ")
    users.append({"username": username})
    save_data(users, GUESTS_FILE)

    print(f"Гость {username} успешно добавлен.")
def main():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    while True:
        if authenticate_admin():
            command = input("Вы зашли под ролью админа. Выберите команду:\n"
                            "1 - Создать БД\n"
                            "2 - Просмотреть всю информацию из БД\n"
                            "3 - Добавить информацию о человеке\n"
                            "4 - Редактировать информацию о человеке\n"
                            "5 - Удалить определённую БД\n"
                            "6 - Удалить все БД\n"
                            "7 - Добавить пользователя\n"
                            "8 - Добавить гостя\n"
                            "9 - Выйти\n")
            match command:
                case "1":
                    admin_db_name = input("Введите имя базы данных: ")
                    create_admin_database(admin_db_name)
                    print("БД успешно создана")
                case "2":
                    admin_db_name = input("Введите имя базы данныха: ")
                    view_all_data(admin_db_name)
                case "3":
                    admin_db_name = input("Введите имя базы данных: ")
                    insert_person(admin_db_name)
                    print("Информация о человеке добавлена успешно")
                case "4":
                    admin_db_name = input("Введите имя базы данных: ")
                    edit_person(admin_db_name)
                case "5":
                    delete_db_name = input("Введите имя базы данных для удаления: ")
                    delete_database(delete_db_name)
                    print("БД успешно удалена!")
                case "6":
                    delete_all_databases()
                    print("Все базы данных удалены!")
                case "7":
                    add_user()
                case "8":
                    add_quest()
                case "9":
                    exit()
        elif authenticate_user():
            command = input("Вы зашли как обычный пользователь. Выберите команду:\n"
                            "1 - Просмотреть всю информацию из БД\n"
                            "2 - Добавить информацию о человеке\n"
                            "3 - Редактировать информацию о человеке\n"
                            "4 - Выйти\n")
            match command:
                case "1":
                    admin_db_name = input("Введите имя базы данныха: ")
                    view_all_data(admin_db_name)
                case "2":
                    admin_db_name = input("Введите имя базы данных: ")
                    insert_person(admin_db_name)
                case "3":
                    admin_db_name = input("Введите имя базы данных: ")
                    edit_person(admin_db_name)
                case "4":
                    exit()
        elif guest():
            command = input("Вы зашли как гость. Выберите команду:\n"
                            "1 - Просмотреть информацию из БД\n"
                            "2 - Выйти\n")
            match command:
                case "1":
                    admin_db_name = input("Введите имя базы данныха: ")
                    view_name(admin_db_name)
                case "2":
                    exit()

        else:
            print("Неверные учетные данные.")

if __name__ == "__main__":
    main()