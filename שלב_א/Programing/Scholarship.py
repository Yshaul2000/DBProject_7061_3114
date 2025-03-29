import random

scholarship_names = [
    "Excellence Scholarship", "Merit Scholarship", "Athletic Scholarship", "Community Service Scholarship",
    "STEM Scholarship", "Arts Scholarship", "Leadership Scholarship", "Diversity Scholarship",
    "Academic Achievement Scholarship", "Financial Aid Scholarship", "Research Grant",
    "International Student Scholarship",
    "Women in Technology Scholarship", "Minority Scholarship", "Science Scholarship", "Music Scholarship",
    "Creative Writing Scholarship", "Sports Scholarship", "Innovation Scholarship", "Healthcare Scholarship"
]


def generate_scholarship_records(num_records):
    with open("Scholarship_Insert.sql", "w", encoding="utf-8") as file:
        for i in range(1, num_records + 1):
            name = random.choice(scholarship_names)
            amount = random.randint(1000, 10000)  # סכום המלגה (בין 1,000 ל-10,000)
            annual_hours = random.randint(20, 200)  # שעות שנתיות נדרשות (בין 20 ל-200)

            sql_command = f"INSERT INTO Scholarship (Scholarship_ID, Name, Amount, AnnualHours) VALUES ({i}, '{name}', {amount}, {annual_hours});\n"
            file.write(sql_command)


if __name__ == "__main__":
    generate_scholarship_records(400)
