import pytest
from heart_rate_sentinel_no_mongo import tachycardic
from heart_rate_sentinel_no_mongo import heart_rate
from heart_rate_sentinel_no_mongo import heart_rate_average
from heart_rate_sentinel_no_mongo import new_patient_validation
from heart_rate_sentinel_no_mongo import new_heart_rate_validation
from heart_rate_sentinel_no_mongo import internal_average_validation


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


@pytest.mark.parametrize("candidate,expected", [
    ({
        "patient_id": "1",
        "attending_email": "mpostiglione17@gmail.com",
        "user_age": "50",
    }, True),
    ({
        "patient_id": 2,
        "user_age": 10,
    }, False),
    ({
        "attending_email": "mpostiglione17@gmail.com",
        "user_age": "50",
    }, False),
    ({
        "patient_id": 2,
        "attending_email": "mpostiglione17@gmail.com",
    }, False),



])
def test_new_patient(candidate, expected):
    response = new_patient_validation(candidate)
    assert response == expected


@pytest.mark.parametrize("candidate,expected", [
    ({
        "patient_id": "1",
        "heart_rate_average_since": "2018-11-10 13:00:36.372339",
    }, True),
    ({
        "patient_id": "1",
    }, False),
    ({
        "heart_rate_average_since": "2018-11-10 13:00:36.372339",
    }, False),



])
def test_heart_rate_interval_average(candidate, expected):
    response = internal_average_validation(candidate)
    assert response == expected


@pytest.mark.parametrize("candidate,expected", [
    ({
        "patient_id": "1",
        "heart_rate": 101,
    }, True),
    ({
        "patient_id": "1",
    }, False),
    ({
        "heart_rate": 101,
    }, False),



])
def test_add_heart_rate(candidate, expected):
    response = new_heart_rate_validation(candidate)
    assert response == expected
