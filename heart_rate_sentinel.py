from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields
from validate_email import validate_email
import datetime
from datetime import datetime



app = Flask(__name__)

connect("mongodb://localhost:27017/example")


class User:
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField
    age = fields.IntegerField()
    heart_rate = fields.ListField
    timestamps = fields.ListField
    tach = fields.BooleanField


@app.route("/api/status/<patient_id>", methods=["GET"])
def tachycardic(patient_id):
    """
   Returns whether the patient is tachycardic

   parameter: patient id- int, patient who's records we are examining

   return: string- string, that contains the output
    """
    user = User.objects.raw({"_id": patient_id}).first()
    id = user.patient_id
    timestamps = user.timestamps
    time = timestamps[len(timestamps)-1]
    if user.tach:
        string = "Patient" + str(id) + "is tachycardic as of" + time
    else:
        string = "Patient" + str(id) + "is not tachycardic as of" + time
    return string


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate(patient_id):
    """
   Returns all heart rate data from a patient

   parameter: patient id- int, patient who's records we are examining

   return: list gives a list that contains all heart rate measurments for a patient
    """
    user = User.objects.raw({"_id": patient_id}).first()
    return user.heart_rate


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_average(patient_id):
    """
   Returns all heart rate data from a patient

   parameter: patient id- int, patient who's records we are examining

   return: list gives a list that contains all heart rate measurments for a patient
    """
    user = User.objects.raw({"_id": patient_id}).first()
    rate = user.heart_rate
    average_rate = sum(rate)/len(rate)
    return average_rate


@app.route("/api/new_patient", methods=['POST'])
def new_patient():
    try:
        r = request.get_json()
        s1 = int(r.get("patient_id"))
        s2 = r.get("attending_email")
        s3 = int(r.get("user_age"))
        check1 = validate_email(s2)
        check2 = isinstance(s1, int)
        check3 = isinstance(s3, int)
        u = User(patient_id=s1, attending_email=s2, age=s3, heart_rate=[], timestamps=[], tach=False)
        if check1 and check2 and check3:
            u.save()
            return jsonify({"user": u})

        return jsonify({"message": "Error occurred, check your inputs"}), 500
    except:
        return jsonify({"message": "Error occurred, check your inputs"}), 500


@app.route("/api/heart_rate", methods=['POST'])
def add_heart_rate():
    try:
        r = request.get_json()
        s1 = r.get("patient_id")
        s1_int = int(s1)
        s2 = float(r.get("heart_rate"))
        check1 = isinstance(s1_int, int)
        check2 = isinstance(s2, float)
        if check1 & check2:
            user = User.objects.raw({"_id": s1}).first()
            user.heart_rate.append(s2)
            user.timestamps.append(datetime.now())
            user.save()
            return jsonify({"user": user})

        return jsonify({"message": "Error occurred, check your inputs"}), 500
    except:
        return jsonify({"message": "Error occurred, check your inputs"}), 500


@app.route("/api/heart_rate/interval_average", methods=['POST'])
def interval_average():
    try:
        r = request.get_json()
        s1 = r.get("patient_id")
        s1_int = int(s1)
        s2 = r.get("heart_rate")

        date_time_obj = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S.%f')
        print('Date:', date_time_obj.date())
        print('Time:', date_time_obj.time())
        print('Date-time:', date_time_obj)
        check1 = isinstance(s1_int, int)
        if check1:
            user = User.objects.raw({"_id": s1}).first()
            times = user.timestamps
            index = 0
            for x in range(len(times)):
                if times[x].date() >= date_time_obj.date():
                    index = x
                    break
            heartrates = user.heart_rate
            sum = 0
            for i in range(index+1):
                sum = sum + heartrates[i]
            average = sum/(index+1)
            return jsonify({"average": average,
                            "Time:": date_time_obj})

        return jsonify({"message": "Error occurred, check your inputs"}), 500
    except:
        return jsonify({"message": "Error occurred, check your inputs"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0")