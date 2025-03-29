import random

first_names = [
    "David", "Sarah", "John", "Emily", "Michael", "Rachel", "Daniel", "Jessica",
    "James", "Sophia", "Matthew", "Olivia", "Andrew", "Emma", "Joshua", "Isabella",
    "Joseph", "Mia", "Benjamin", "Amelia", "Samuel", "Harper", "Ethan", "Lily"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
    "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez",
    "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez"
]

domains = ["gmail.com", "yahoo.com", "outlook.com", "mail.com"]


def random_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"


def generate_student_records(num_records):
    with open("Student_Insert.sql", "w", encoding="utf-8") as file:
        for i in range(1, num_records + 1):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = random_email(first_name, last_name)

            sql_command = f"INSERT INTO Student (StudentID, FirstName, LastName, Email) VALUES ({i}, '{first_name}', '{last_name}', '{email}');\n"
            file.write(sql_command)


if __name__ == "__main__":
    generate_student_records(400)
