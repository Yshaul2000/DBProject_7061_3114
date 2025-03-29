import random
import datetime

# הגדרת קובץ ה-SQL
filename = 'insert_employees.sql'

names = [
    'Yinon Shaul', 'David Cohen', 'Sarah Levy', 'John Doe', 'Michael Green', 'Tamar Sasson',
    'Yael Perez', 'Daniel Miller', 'Noa Goldstein', 'Eitan Shapiro', 'Amit Weiss', 'Ronen Azulay',
    'Nadav Koren', 'Tal Ben-David', 'Avi Rosen', 'Lior Katz', 'Barak Stern', 'Maya Friedman',
    'Shira Avrahami', 'Rachel Cohen', 'Itamar Levi', 'Eli Gazit', 'Hila Mor', 'Alon Tamir',
    'Yossi Nahmias', 'Keren Solomon', 'Nitzan Gold', 'Guy Shaked', 'Ziv Doron', 'Gil Lavi'
]


def generate_random_id():
    """
    יוצר מספר רנדומלי בן 9 ספרות (כמו תעודת זהות)
    """
    return random.randint(100000000, 999999999)


with open(filename, 'w') as file:
    file.write('INSERT INTO Employees (employee_id, name, salary, hire_date, department_id) VALUES\n')

    for department_id in range(1, 401):
        employee_id = generate_random_id()
        name = random.choice(names)
        salary = round(random.uniform(30000, 100000), 2)
        hire_date = datetime.date(2000, 1, 1) + datetime.timedelta(days=random.randint(0, 9000))

        line = f"({employee_id}, '{name}', {salary}, '{hire_date}', {department_id})"

        if department_id < 400:
            line += ','
        line += '\n'

        file.write(line)

    file.write(';')

print(f"SQL file '{filename}' has been created successfully.")
