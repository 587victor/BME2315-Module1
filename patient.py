import csv


class Patient:

    all_patients = []

    def __init__(self, donor_id, age_at_death, sex, cognitive_status,
                 age_onset, brain_injury, abeta40, abeta42, ttau, ptau):

        self.donor_id = donor_id
        self.age_at_death = age_at_death
        self.sex = sex
        self.cognitive_status = cognitive_status
        self.age_onset = age_onset
        self.brain_injury = brain_injury
        self.abeta40 = abeta40
        self.abeta42 = abeta42
        self.ttau = ttau
        self.ptau = ptau

        Patient.all_patients.append(self)

    def __repr__(self):
        return f"{self.donor_id}: ({self.age_at_death} | {self.sex} | {self.cognitive_status} | {self.age_onset} | {self.brain_injury} | {self.abeta40} | {self.abeta42} | {self.ttau} | {self.ptau})"

    def get_age_at_death(self):
        return self.age_at_death

    @classmethod
    def instantiate_from_csv(cls, filename):

        # Open the CSV and create a list containing all its rows.
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

        # Create one Patient object for each CSV row.
        for row in rows_of_patients:
            Patient(
                donor_id=row["Donor ID"],
                age_at_death=int(row["Age at Death"]),
                sex=row["Sex"],
                cognitive_status=row["Cognitive Status"],
                age_onset=row["Age of onset cognitive symptoms"],
                brain_injury=row["Known head injury"],
                abeta40=float(row["ABeta40 pg/ug"]),
                abeta42=float(row["ABeta42 pg/ug"]),
                ttau=float(row["tTAU pg/ug"]),
                ptau=float(row["pTAU pg/ug"])
            )

    @classmethod
    def filter(cls, list, donor_id="any", age_at_death="any", sex="any",
               cognitive_status="any", age_onset="any",
               brain_injury="any", abeta40="any", abeta42="any",
               ttau="any", ptau="any"):

        all_patients = list
        remove_list = []

        attr_list = (
            donor_id,
            age_at_death,
            sex,
            cognitive_status,
            age_onset,
            brain_injury,
            abeta40,
            abeta42,
            ttau,
            ptau
        )

        attr_name = (
            "donor_id",
            "age_at_death",
            "sex",
            "cognitive_status",
            "age_onset",
            "brain_injury",
            "abeta40",
            "abeta42",
            "ttau",
            "ptau"
        )

        for attr in range(len(attr_list)):
            if attr_list[attr] != "any":
                for patient in all_patients:
                    if getattr(patient, attr_name[attr]) != attr_list[attr]:
                        remove_list.append(patient)

                all_patients = [
                    patient for patient in all_patients
                    if patient not in remove_list
                ]

                remove_list.clear()

        return all_patients