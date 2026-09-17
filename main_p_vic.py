from patient import Patient
import matplotlib.pyplot as plt
import numpy as np
import statistics


# Create Patient objects from the CSV file.
Patient.instantiate_from_csv(
    "Metadata and Protein Data for Module 1.csv"
)


# Sort patients from youngest to oldest by age at death.
Patient.all_patients.sort(
    key=Patient.get_age_at_death,
    reverse=False
)

print("Patients sorted by age at death:")

for patient in Patient.all_patients:
    print(patient)


# Filter using two attributes: Female and Dementia.
female_dementia_patients = Patient.filter(
    Patient.all_patients,
    sex="Female",
    cognitive_status="Dementia"
)

print("\nFemale patients with dementia:")

for patient in female_dementia_patients:
    print(patient)

print(
    f"Number of female patients with dementia = "
    f"{len(female_dementia_patients)}"
)


# Make lists of ABeta42 levels for female and male dementia patients.
abeta42_female_patients = []
abeta42_male_patients = []

for patient in Patient.filter(
        Patient.all_patients,
        sex="Female",
        cognitive_status="Dementia"):

    abeta42_female_patients.append(patient.abeta42)


for patient in Patient.filter(
        Patient.all_patients,
        sex="Male",
        cognitive_status="Dementia"):

    abeta42_male_patients.append(patient.abeta42)


# Find the means for the two bars.
x_female_bar = statistics.mean(
    abeta42_female_patients
)

x_male_bar = statistics.mean(
    abeta42_male_patients
)


# Find the standard deviations for the error bars.
abeta42_female_stdev = statistics.stdev(
    abeta42_female_patients
)

abeta42_male_stdev = statistics.stdev(
    abeta42_male_patients
)


# Print the means and standard deviations.
print(
    f"Female mean = {x_female_bar}, "
    f"standard deviation = {abeta42_female_stdev}"
)

print(
    f"Male mean = {x_male_bar}, "
    f"standard deviation = {abeta42_male_stdev}"
)


# Make the bar graph.
sex_cols = [
    "Female",
    "Male"
]

mean_abeta42 = [
    x_female_bar,
    x_male_bar
]

stdev_abeta42 = [
    abeta42_female_stdev,
    abeta42_male_stdev
]

yerr = [
    np.zeros(len(mean_abeta42)),
    stdev_abeta42
]

plt.bar(
    sex_cols,
    mean_abeta42,
    yerr=yerr,
    capsize=10,
    color=["purple", "blue"]
)

plt.title(
    "Average ABeta42 in Female vs. Male Patients with Dementia"
)

plt.xlabel("Sex")
plt.ylabel("Average ABeta42 (pg/ug)")

plt.savefig("abeta42_bar_graph.png")
plt.show()


# Make two lists for the scatter plot.
patient_age_at_death = []
patient_abeta42 = []

for patient in Patient.all_patients:
    patient_age_at_death.append(
        patient.age_at_death
    )

for patient in Patient.all_patients:
    patient_abeta42.append(
        patient.abeta42
    )


# Age at death is the independent variable.
X = patient_age_at_death

# ABeta42 is the dependent variable.
y = patient_abeta42


# Make the scatter plot.
plt.scatter(
    X,
    y,
    color="green"
)

plt.xlabel("Age at Death")
plt.ylabel("ABeta42 (pg/ug)")

plt.title(
    "Scatter Plot of ABeta42 vs. Age at Death"
)

plt.savefig("abeta42_scatter_plot.png")
plt.show()