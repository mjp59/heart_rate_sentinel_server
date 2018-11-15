[![Build Status](https://travis-ci.com/mjp59/heart_rate_sentinel_server.svg?branch=master)](https://travis-ci.com/mjp59/heart_rate_sentinel_server)

VCM: vcm-7314.vm.duke.edu:5000 , Ip address: 152.3.53.153

The working server is in the file heart_rate_sentinel_no_mongo.py. This python file contains a working flask server that stores user information in local ram. The patient information is stored in a dictonary structure, that contains fields for:

patient id
attending_email
heart_rate
timestamps
tachyardia status flag

The server performs six functions, 3 get request that returns info on the patient and 3 post requests that add info to the patient information, minus the average post command.

The first function can be reached with /api/status/<patient_id>. This call works by returning if the patient is tachycardic by looking at the status flag for the patient. 

The second funcion can be reached with /api/heart_rate/<patient_id>. This call works by returning the list of heart rate mesurements for the patient. 

The thrid function can be reached with /api/heart_rate/average/<patient_id>. This call works by adding all the heart rate measurements in the list and divdiing by the length of the list. Then this value is returned as an average. 

The fourth function can be reached with /api/new_patient. This function takes in a json that contains new patient information. The function then addes the new patient to the local storage of patients.

The fifth function can be reached with /api/heart_rate. This function takes in a json that contains a new patient heart rate. It checks if the heart_rate for the patient is tachyradia. This can be done for all age ranges down to a few days of age. If it is tachycardic then the users status flag is changed to true and an alert email is sent to the attending email. The new heart rate is also added to the patient data.

The sixth function can be reached with /api/heart_rate/interval_average. This function takes in json with the patient id and a datetime string. The average is then calculated for all heart rates that occur before this datetime. The correct heart rates are found by string comparing the timestamp list to the given datatime. Then we get the index of this list that coresspinds to the given datatime. Then that index is used to navigate the heartrate list to create the correct average. The average is then returned.

Extras:
tachycarida detection down to 0-5 days. Can take in floats as age.
attempted monog script but mongomodel was breaking. But this script is close to fully functional as well. 


# heart_rate_sentinel_server
