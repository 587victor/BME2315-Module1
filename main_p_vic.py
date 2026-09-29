import matplotlib.pyplot as pit
from scipy import stats
import numpy as np
import statistics
import pandas as pd
from sklearn.linear_model import LinearRegression


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

t_stat, p_val= stats.ttest_ind(
    abeta42_female_patients,
    abeta42_male_patients
)
print(f't_stat = {t_stat}, p_val = {p_val}')


plt.bar(
    sex_cols,
    mean_abeta42,
    yerr=yerr,
    capsize=10,
    color=["green", "blue"]
)

plt.title(
    "Average ABeta42 in Female vs. Male Patients with Dementia"
)

plt.xlabel("Sex")
plt.ylabel("Average ABeta42 (pg/ug)")

#t-test labels
y_max= max(mean_abeta42) + max(stdev_abeta42)
plt.text(
    0.5,
    y_max -40,
    f"t= {t_stat:.2f}\np = {p_val:.3e}",
    ha="center",
    va="bottom"
)

plt.savefig("abeta42_bar_graph.png")
plt.show()


# Make two lists for the scatter plot.
patient_age_at_death = []
patient_abeta42 = []

for patient in Patient.all_patients:
    patient_age_at_death.append(patient.age_at_death)
    patient_abeta42.append(patient.abeta42)


# Age at death is the independent variable.
X = patient_age_at_death
X=np.array(patient_age_at_death).reshape(-1,1)
# ABeta42 is the dependent variable.
y = patient_abeta42
y = np.array(patient_abeta42)


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

#Linear regression
model = LinearRegression()
model.fit(X,y)
slope = model.coef_[0]
intercept = model.intercept_
r_squared = model.score(X,y)

equation = f"y = {slope:.2f}x + {intercept:.2f}"

plt.plot(
    X,
    model.predict(X)
)
plt.text(
    max(patient_age_at_death) -15,
    max(patient_abeta42) -60,
    f"{equation}\nR^2 = {r_squared:.2f}"
)


plt.savefig("abeta42_scatter_plot.png")
plt.show()

#outlier IQR rule
q1= np.percentile(patient_abeta42, 25)
q3= np.percentile(patient_abeta42, 75)

iqr = q3- q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

#identifying outlier

for patient in Patient.all_patients:
    if (
        patient.abeta42 < lower_bound
        or patient.abeta42 > upper_bound
    ): 
        print(
            "outlier:",
            patient.age_at_death,
            patient.abeta42
        )
#regression plot without outliers vs with
model_all = LinearRegression()
model_all.fit(X, y)

print("WITH OUTLIERS")
print("Slope =", model_all.coef_[0])
print("Intercept =", model_all.intercept_)
print("R^2 =", model_all.score(X, y))


# Remove IQR outliers
age_no_outliers = []
abeta42_no_outliers = []

for patient in Patient.all_patients:
    if (
        patient.abeta42 >= lower_bound
        and patient.abeta42 <= upper_bound
    ):
        age_no_outliers.append(patient.age_at_death)
        abeta42_no_outliers.append(patient.abeta42)


X_no = np.array(age_no_outliers).reshape(-1, 1)
y_no = np.array(abeta42_no_outliers)


# Regression without outliers
model_no = LinearRegression()
model_no.fit(X_no, y_no)

print("\nWITHOUT OUTLIERS")
print("Slope =", model_no.coef_[0])
print("Intercept =", model_no.intercept_)
print("R^2 =", model_no.score(X_no, y_no))
# Plot regression WITH outliers
plt.scatter(
    X,
    y,
    color="green",
    label="All data"
)

plt.plot(
    X,
    model_all.predict(X),
    label="Regression with outliers"
)


# Plot regression WITHOUT outliers
plt.scatter(
    X_no,
    y_no,
    color="blue",
    label="Data without outliers"
)

plt.plot(
    X_no,
    model_no.predict(X_no),
    label="Regression without outliers"
)


plt.xlabel("Age at Death")
plt.ylabel("ABeta42 (pg/ug)")

plt.title(
    "ABeta42 vs. Age at Death: Outlier Comparison"
)

plt.legend()

plt.show()