import pytest
from heart_rate_sentinel_no_mongo import tachycardic
from heart_rate_sentinel_no_mongo import heart_rate
from heart_rate_sentinel_no_mongo import heart_rate_average
import requests


@pytest.mark.parametrize("candidate,expected", [
    ('1', "Patient1 is tachycardic as of 2018-11-10 14:59:25.974534"),
    ('2', "Patient2 is not tachycardic as of 2018-11-10 14:59:25.974534")



])
def test_tachycardic(candidate, expected):
    response = tachycardic(candidate)
    assert response == expected


@pytest.mark.parametrize("candidate,expected", [
    ('1', "[60, 100, 102]"),
    ('2', "[60, 100, 99]")



])
def test_heart_rate(candidate, expected):
    response = heart_rate(candidate)
    assert response == expected


@pytest.mark.parametrize("candidate,expected", [
    ('1', "87.33333333333333"),
    ('2', "86.33333333333333"),



])
def test_heart_rate_average(candidate, expected):
    response = heart_rate_average(candidate)
    assert response == expected


def test_new_patient():
    resp = requests.post("http://0.0.0.0:5000/api/new_patient", json={
        "patient_id": "1",
        "attending_email": "suyash.kumar@duke.edu",
        "user_age": "50",
    })
    assert resp.status_code == 200


def test_heart_rate_interval_average():
    resp = requests.post(
        "http://0.0.0.0:5000/api/heart_rate/interval_average", json={
                            "patient_id": "1",
                            "heart_rate_average_since":
                            "2018-11-10 13:00:36.372339",
        })
    print(resp.text)
    assert resp.status_code == 200


def test_add_heart_rate():
    resp = requests.post("http://0.0.0.0:5000/api/heart_rate", json={
        "patient_id": "1",
        "heart_rate": 60,
    })
    print(resp.text)
    assert resp.status_code == 200
