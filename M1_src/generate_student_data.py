import random
import csv
import math
from collections import Counter

# Set random seed for reproducibility
random.seed(42)

# Number of data points
n_samples = 100

# Function to generate data points with a normal-like distribution


def generate_bell_curve_data(mode, variance, min_val, max_val, n):
    """Generate integer data with a rough bell curve distribution around the mode"""
    std_dev = math.sqrt(variance)
    data = []
    for _ in range(n):
        # Use multiple uniform random values to approximate normal distribution (Central Limit Theorem)
        val = sum(random.random() for _ in range(12)) - \
            6  # Approximates standard normal
        val = val * std_dev + mode  # Scale and shift to desired mean and std dev
        val = round(val)  # Round to nearest integer
        val = max(min_val, min(max_val, val))  # Clip to range
        data.append(val)
    return data


# Generate StudyHours data (0-10, mode=7, variance=2)
study_hours = generate_bell_curve_data(7, 2, 0, 10, n_samples)

# Generate PrevExamScore data (0-100, mode=70, variance=20)
prev_exam_scores = generate_bell_curve_data(70, 20, 0, 100, n_samples)

# Determine Pass/Fail based on a weighted formula
# Students pass if they have enough combined points from study hours and previous exam
threshold = 65  # Threshold for passing
pass_fail = []
for i in range(n_samples):
    weighted_score = (study_hours[i] * 7) + (prev_exam_scores[i] * 0.3)
    pass_fail.append(1 if weighted_score >= threshold else 0)

# Create CSV file
csv_filename = 'student_data.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['StudyHours', 'PrevExamScore', 'Pass'])
    # Write data rows
    for i in range(n_samples):
        writer.writerow([study_hours[i], prev_exam_scores[i], pass_fail[i]])

# Print summary statistics
print(f"Generated {n_samples} student records and saved to {csv_filename}")

# Calculate and print some basic statistics
print("\nData Summary:")

# Study Hours statistics
print("StudyHours:")
study_hours_counter = Counter(study_hours)
study_hours_mean = sum(study_hours) / len(study_hours)
study_hours_mode = study_hours_counter.most_common(1)[0][0]
print(f"  Min: {min(study_hours)}")
print(f"  Max: {max(study_hours)}")
print(f"  Mean: {study_hours_mean:.2f}")
print(f"  Mode: {study_hours_mode}")

# Calculate standard deviation for StudyHours
study_hours_variance = sum((x - study_hours_mean) **
                           2 for x in study_hours) / len(study_hours)
study_hours_std = math.sqrt(study_hours_variance)
print(f"  Standard Deviation: {study_hours_std:.2f}")

# PrevExamScore statistics
print("\nPrevExamScore:")
prev_exam_mean = sum(prev_exam_scores) / len(prev_exam_scores)
prev_exam_mode = Counter(prev_exam_scores).most_common(1)[0][0]
print(f"  Min: {min(prev_exam_scores)}")
print(f"  Max: {max(prev_exam_scores)}")
print(f"  Mean: {prev_exam_mean:.2f}")
print(f"  Mode: {prev_exam_mode}")

# Calculate standard deviation for PrevExamScore
prev_exam_variance = sum((x - prev_exam_mean) **
                         2 for x in prev_exam_scores) / len(prev_exam_scores)
prev_exam_std = math.sqrt(prev_exam_variance)
print(f"  Standard Deviation: {prev_exam_std:.2f}")

# Pass/Fail statistics
print("\nPass/Fail:")
pass_count = sum(pass_fail)
fail_count = n_samples - pass_count
print(f"  Pass: {pass_count} ({pass_count/n_samples*100:.2f}%)")
print(f"  Fail: {fail_count} ({fail_count/n_samples*100:.2f}%)")

# Average Study Hours by Pass/Fail
pass_hours = [study_hours[i] for i in range(n_samples) if pass_fail[i] == 1]
fail_hours = [study_hours[i] for i in range(n_samples) if pass_fail[i] == 0]
pass_hours_mean = sum(pass_hours) / len(pass_hours) if pass_hours else 0
fail_hours_mean = sum(fail_hours) / len(fail_hours) if fail_hours else 0
print(f"\nAverage Study Hours for passing students: {pass_hours_mean:.2f}")
print(f"Average Study Hours for failing students: {fail_hours_mean:.2f}")

# Average Exam Scores by Pass/Fail
pass_scores = [prev_exam_scores[i]
               for i in range(n_samples) if pass_fail[i] == 1]
fail_scores = [prev_exam_scores[i]
               for i in range(n_samples) if pass_fail[i] == 0]
pass_scores_mean = sum(pass_scores) / len(pass_scores) if pass_scores else 0
fail_scores_mean = sum(fail_scores) / len(fail_scores) if fail_scores else 0
print(
    f"Average Previous Exam Score for passing students: {pass_scores_mean:.2f}")
print(
    f"Average Previous Exam Score for failing students: {fail_scores_mean:.2f}")
