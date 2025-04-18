def second_lowest_grade(records):

    grades = sorted(list(set([grade for _, grade in records])))

    second_lowest = grades[1]

    students_with_second_lowest = [
        name for name, grade in records if grade == second_lowest
    ]
    students_with_second_lowest.sort()

    return students_with_second_lowest


if __name__ == "__main__":
    n = int(input())
    records = []
    for _ in range(n):
        name = input()
        grade = float(input())
        records.append([name, grade])

    result = second_lowest_grade(records)
    for student in result:
        print(student)
