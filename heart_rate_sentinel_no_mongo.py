from flask import Flask, jsonify, request
from validate_email import validate_email
import datetime
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
users = [{

}, {
             "patient_id": "1",
             "attending_email": "mike@gmail.com",
             "age": 50,
             "heart_rate": [60, 100, 102],
             "timestamps": [datetime.now(), datetime.now(),
                            "2018-11-10 14:59:25.974534"],
             "tach": True,
}, {
             "patient_id": "2",
             "attending_email": "tom@gmail.com",
             "age": 50,
             "heart_rate": [60, 100, 99],
             "timestamps": [datetime.now(), datetime.now(),
                            "2018-11-10 14:59:25.974534"],
             "tach": False,
}] * 100


@app.route("/api/status/<patient_id>", methods=["GET"])
def tachycardic(patient_id):
    """
              Returns if patient is tachycardic

    :param patient_id: string
                Must be the patient id number of an existing patient
    :return: string
            tells the user if the patient is tachycardic
            and when they became tachycardic
    """
    patient_id_int = int(patient_id)
    user = users[patient_id_int]
    id = user.get("patient_id")
    timestamps = user.get("timestamps")
    time = timestamps[len(timestamps)-1]
    if user.get("tach"):
        string = "Patient" + str(id) + " is tachycardic as of " + str(time)
        # me = "mpostiglione17@gmail.com"
        # you = str(user.get("attending_email"))
        # s = smtplib.SMTP("0.0.0.0", 5000)
        # s.sendmail(me, [you], string)
        # s.quit()
    else:
        string = "Patient" + str(id) + " is not tachycardic as of " + str(time)
    print(string)
    return string


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate(patient_id):
    """
                  Returns all heart rate measurements of the patient

        :param patient_id: string
                    Must be the patient id number of an existing patient
        :return: string
                returns string that has all heart rate measurements
                for the patient
        """
    patient_id_int = int(patient_id)
    user = users[patient_id_int]
    return str(user.get("heart_rate"))


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_average(patient_id):
    """
              Returns the average heart rate of the patient

    :param patient_id: string
                Must be the patient id number of an existing patient
    :return: string
            string that contains the
            average heart rate of the patient
    """
    patient_id_int = int(patient_id)
    user = users[patient_id_int]
    rate = user.get("heart_rate")
    average_rate = sum(rate)/len(rate)
    return str(average_rate)


@app.route("/api/new_patient", methods=['POST'])
def new_patient():
    """
                  adds new patient to users list

        :return: json
                returns the information stored for the new
                patient
        """
    # try:
    r = request.get_json()
    s1 = r.get("patient_id")
    s2 = r.get("attending_email")
    s3 = r.get("user_age")
    check1 = validate_email(s2)
    check2 = isinstance(int(s1), int)
    check3 = isinstance(float(s3), float)
    u = {
        "patient_id": s1,
        "attending_email": s2,
        "age": s3,
        "heart_rate": [],
        "timestamps": [],
        "tach": False,
        }
    if check1 and check2 and check3:
        users[int(s1)] = u
        return jsonify(u)

    return jsonify({"message": "Error occurred, check your inputs"}), 500
    # except:
    # return jsonify({"message": "Error occurred, check your inputs"}), 500


@app.route("/api/heart_rate", methods=['POST'])
def add_heart_rate():
    """
                     adds a new heart rate reading to the
                     patient's info and updates the
                     tachcardia status flag

           :return: json
                   returns the information stored for the new
                   patient
           """
    # try:
    r = request.get_json()
    s1 = r.get("patient_id")
    s1_int = int(s1)
    s2 = r.get("heart_rate")
    s2_float = float(s2)
    check1 = isinstance(s1_int, int)
    check2 = isinstance(s2_float, float)
    if check1 & check2:
        user = users[s1_int]
        user_heartrate = user.get("heart_rate")
        user_heartrate.append(s2_float)
        user["heart_rate"] = user_heartrate
        user_timestamps = user.get("timestamps")
        user_timestamps.append(datetime.now())
        user["timestamps"] = user_timestamps
        if s2_float > 159 and (float(user.get("age"))*365) <= 2:
            user["tach"] = True
        elif s2_float > 166 and (float(user.get("age"))*365) > 2 \
                and (float(user.get("age"))*365) <= 6:
            user["tach"] = True
        elif s2_float > 182 and (float(user.get("age"))*365) > 6 \
                and (float(user.get("age"))*365) <= 21:
            user["tach"] = True
        elif s2_float > 179 and (float(user.get("age"))*365) > 21 \
                and (float(user.get("age"))*365) <= 62:
            user["tach"] = True
        elif s2_float > 186 and (float(user.get("age"))*365) > 62 \
                and (float(user.get("age"))*365) <= 155:
            user["tach"] = True
        elif s2_float > 169 and (float(user.get("age"))*365) > 155 \
                and (float(user.get("age"))*365) <= 341:
            user["tach"] = True
        elif s2_float > 151 and float(user.get("age")) >= 1 \
                and float(user.get("age")) <= 2:
            user["tach"] = True
        elif s2_float > 137 and float(user.get("age")) > 2 \
                and float(user.get("age")) <= 4:
            user["tach"] = True
        elif s2_float > 133 and float(user.get("age")) > 4 \
                and float(user.get("age")) <= 7:
            user["tach"] = True
        elif s2_float > 130 and float(user.get("age")) > 7 \
                and float(user.get("age")) <= 11:
            user["tach"] = True
        elif s2_float > 119 and float(user.get("age")) > 11 \
                and float(user.get("age")) <= 15:
            user["tach"] = True
        elif s2_float > 100 and float(user.get("age")) > 15:
            user["tach"] = True
        users[s1_int] = user
        return jsonify(user)

    return jsonify({"message": "Error occurred, check your inputs"}), 500
    # except:
    # return jsonify({"message": "Error occurred, check your inputs"}), 500


@app.route("/api/heart_rate/interval_average", methods=['POST'])
def interval_average():
    """
                     returns the average heart rate of a
                     patient up to a certain date

           :return: json
                   returns the information stored for the new
                   patient
           """
    # try:
    r = request.get_json()
    s1 = r.get("patient_id")
    s1_int = int(s1)
    s2 = r.get("heart_rate_average_since")
    date_time_obj = datetime.strptime(str(s2), "%Y-%m-%d %H:%M:%S.%f")
    check1 = isinstance(s1_int, int)
    if check1:
        user = users[s1_int]
        times = user.get("timestamps")
        index = 0
        for x in range(len(times)):
            if times[x].date() > date_time_obj.date():
                index = x
                break
            if times[x].date() == date_time_obj.date() \
                    and times[x].time() > date_time_obj.time():
                index = x
                break
            index = x
        heartrates = user.get("heart_rate")
        if index == 0:
            average = 0
        else:
            sum = 0
            for i in range(index+1):
                sum = sum + heartrates[i]
                average = sum/(index+1)
        return jsonify({"average": average,
                        "Time:": date_time_obj})

    return jsonify({"message": "Error occurred, check your inputs"}), 500
    # except:
    # return jsonify({"message": "Error occurred, check your inputs"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
