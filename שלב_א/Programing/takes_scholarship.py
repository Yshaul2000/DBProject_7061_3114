import random
from datetime import datetime, timedelta


def random_date():
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2025-03-25', '%Y-%m-%d')
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')


def generate_takes_scholarship_records(num_records, num_students=400, num_scholarships=400):
    with open("Takes_Scholarship_Insert.sql", "w", encoding="utf-8") as file:
        unique_pairs = set()  # כדי להימנע מכפילויות

        for _ in range(num_records):
            while True:
                student_id = random.randint(1, num_students)
                scholarship_id = random.randint(1, num_scholarships)

                if (student_id, scholarship_id) not in unique_pairs:
                    unique_pairs.add((student_id, scholarship_id))
                    break

            approval_date = random_date()
            sql_command = f"INSERT INTO takes_scholarship (StudentID, Scholarship_ID, approval_date) VALUES ({student_id}, {scholarship_id}, '{approval_date}');\n"
            file.write(sql_command)


if __name__ == "__main__":
    generate_takes_scholarship_records(400)
