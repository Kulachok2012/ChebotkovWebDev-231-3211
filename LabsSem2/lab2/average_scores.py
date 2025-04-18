def compute_average_scores(scores):

    num_students = len(scores[0])
    average_scores = []

    for i in range(num_students):
        student_scores = [scores[j][i] for j in range(len(scores))] #все оценки конкретного студента по всем предметам
        average_score = sum(student_scores) / len(student_scores)
        average_scores.append(average_score)

    return average_scores


if __name__ == "__main__":
    n, x = map(int, input().split())
    scores = []
    for _ in range(x):
        subject_scores = list(map(float, input().split()))
        scores.append(subject_scores)

    average_scores = compute_average_scores(scores)

    for score in average_scores:
        print(f"{score:.1f}")

#5 3
#89 90 78 93 80
#90 91 85 88 86
#91 92 83 89 90.5

