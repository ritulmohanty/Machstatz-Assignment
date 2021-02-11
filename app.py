from flask import Flask, request, jsonify, render_template
from datetime import datetime
import time
import json

app = Flask(__name__)

'''
	Util functions
'''
def utc_to_local(utc_time):  
	now = time.time()
	offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
	return utc_time + offset


def display_time(time_in_seconds):
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{hours}h:{minutes}m:{seconds}s'

def find_index_in_array_of_object(arr, key):
	if len(arr) == 0:
		return -1

	for idx, i  in enumerate(arr):
		if i["id"] == key:
			return idx;

	return -1

def average(lst): 
    return sum(lst) / len(lst) 


'''
	routes
'''

# index route
@app.route('/') 
def index():
	return render_template('index.html')


@app.route('/question1', methods=["GET"])
def question1():

	#getting the query variables 
	start_time = request.args.get("start_time")
	end_time = request.args.get("end_time")

	if(start_time == None or end_time == None):
		return "Please send start_time and end_time as query string in the format: %Y-%m-%dT%H:%M:%SZ"

	# parsing string time to UTC
	start_time = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
	end_time = datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")

	#converting utc to local
	start_time  = utc_to_local(start_time)
	end_time  = utc_to_local(end_time)


	#loading json data
	f = open("./json/sample_json_1.json")
	data = json.load(f)

	output = {
		"shiftA" : {
			"production_A_count" : 0,
			"production_B_count" : 0
		},
		"shiftB" : {
			"production_A_count" : 0,
			"production_B_count" : 0
		},
		"shiftC" : {
			"production_A_count" : 0,
			"production_B_count" : 0
		}
	}


	A_starttime = datetime.strptime("06:00:00","%H:%M:%S").strftime("%H:%M:%S")
	A_endtime = datetime.strptime("13:59:59","%H:%M:%S").strftime("%H:%M:%S")

	B_starttime = datetime.strptime("14:00:00","%H:%M:%S").strftime("%H:%M:%S")
	B_endtime = datetime.strptime("19:59:59","%H:%M:%S").strftime("%H:%M:%S")

	C_starttime = datetime.strptime("20:00:00","%H:%M:%S").strftime("%H:%M:%S")
	C_endtime = datetime.strptime("05:59:59","%H:%M:%S").strftime("%H:%M:%S")


	for obj in data:
		objtime = datetime.strptime(obj["time"],"%Y-%m-%d %H:%M:%S")

		if(objtime >= start_time and objtime <= end_time):

			hour = objtime.strftime("%H:%M:%S")

			if(hour >= A_starttime and hour <= A_endtime):
				if(obj["production_A"] == True):
					output["shiftA"]["production_A_count"]+=1
				if(obj["production_B"] == True):
					output["shiftA"]["production_B_count"]+=1

			if(hour >= B_starttime and hour <= B_endtime):
				if(obj["production_A"] == True):
					output["shiftB"]["production_A_count"]+=1
				if(obj["production_B"] == True):
					output["shiftB"]["production_B_count"]+=1

			if(hour >= C_starttime or hour <= C_endtime):
				if(obj["production_A"] == True):
					output["shiftC"]["production_A_count"]+=1
				if(obj["production_B"] == True):
					output["shiftC"]["production_B_count"]+=1


	return jsonify(output)


@app.route('/question2', methods=["GET"])
def question2():
	#getting the query variables 
	start_time = request.args.get("start_time")
	end_time = request.args.get("end_time")

	if(start_time == None or end_time == None):
		return "Please send start_time and end_time as query string in the format: %Y-%m-%dT%H:%M:%SZ"

	# parsing string time to UTC
	start_time = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
	end_time = datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")

	#converting utc to local
	start_time  = utc_to_local(start_time)
	end_time  = utc_to_local(end_time)


	#loading json data
	f = open("./json/sample_json_2.json")
	data = json.load(f)

	output = {
        "runtime": 0,
        "downtime": 0,
        "utilisation": 0
    }

	for obj in data:
		objtime = datetime.strptime(obj["time"],"%Y-%m-%d %H:%M:%S")

		if(objtime>=start_time and objtime<=end_time):

			if(obj["runtime"]<1021):
				output["runtime"] += obj["runtime"]
				output["downtime"] +=  obj["downtime"]
			else:
				output["runtime"] += 1021
				output["downtime"] += (obj["runtime"] - 1021)


	if (output["runtime"] + output["downtime"] > 0):
		output["utilisation"] = (output["runtime"]/(output["runtime"]+output["downtime"]))*100

	output["downtime"] = display_time(output["downtime"])
	output["runtime"] = display_time(output["runtime"])

	return jsonify(output)


@app.route('/question3')
def question3():
	#getting the query variables 
	start_time = request.args.get("start_time")
	end_time = request.args.get("end_time")

	if(start_time == None or end_time == None):
		return "Please send start_time and end_time as query string in the format: %Y-%m-%dT%H:%M:%SZ"

	# parsing string time to UTC
	start_time = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
	end_time = datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")

	#converting utc to local
	start_time  = utc_to_local(start_time)
	end_time  = utc_to_local(end_time)


	#loading json data
	f = open("./json/sample_json_3.json")
	data = json.load(f)

	output = []

	for obj in data:
		objtime = datetime.strptime(obj["time"],"%Y-%m-%d %H:%M:%S")

		if(objtime>=start_time and objtime<=end_time):
			_id = int(obj["id"][2:])

			found_id = find_index_in_array_of_object(output, _id);

			if found_id >= 0:
				if obj["state"]:
					output[found_id]["b2"].append(obj["belt2"])
				else:
					output[found_id]["b1"].append(obj["belt1"])
			else:
				if obj["state"]:
					temp = {"id": _id, "b2":[], "b1": []}
					temp["b2"].append(obj["belt2"])
					output.append(temp)

				else:
					temp = {"id": _id, "b2":[], "b1": []}
					temp["b1"].append(obj["belt1"])
					output.append(temp)


	for obj in output:
		obj["avg_belt1"] = 0
		obj["avg_belt2"] = 0

		if len(obj["b1"]):
			obj["avg_belt1"] = average(obj["b1"])

		if len(obj["b2"]):
			obj["avg_belt2"] = average(obj["b2"])

		del obj['b1']
		del obj['b2']

	output = sorted(output, key=lambda x: x["id"], reverse=False)

	return jsonify(output)


if __name__ == '__main__':
	app.run(use_reloader=True)