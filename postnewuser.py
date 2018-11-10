import requests


def main():
    r2 = requests.post("http://0.0.0.0:5000/api/new_patient", json={
        "patient_id": "1",
        "attending_email": "suyash.kumar@duke.edu",
        "user_age": "50",
    })
    print(r2.text)

    r1 = requests.post("http://0.0.0.0:5000/api/heart_rate", json={
        "patient_id": "1",
        "heart_rate": 60,
    })
    print(r1.text)

    r3 = requests.post("http://0.0.0.0:5000/api/heart_rate", json={
        "patient_id": "1",
        "heart_rate": 101,
    })
    print(r3.text)

    r = requests.post(
        "http://0.0.0.0:5000/api/heart_rate/interval_average", json={
            "patient_id": "1",
            "heart_rate_average_since": "2018-11-10 13:00:36.372339",
        })
    print(r.text)


if __name__ == "__main__":
    main()
