import requests


def main():
    r2 = requests.post("http://0.0.0.0:5000/api/new_patient", json={
        "patient_id": "1",  # usually this would be the patient MRN
        "attending_email": "suyash.kumar@duke.edu",
        "user_age": "50",  # in years
    })
    print(r2.text)


if __name__ == "__main__":
    main()
