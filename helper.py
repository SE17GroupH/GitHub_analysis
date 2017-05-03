import urllib.request, datetime
import json, csv, re

def get_json(url):
	"""
	get json data(list) from a Github api url
	url -> str : ex - https://api.github.com/..
	"""
	token = "31ac0df1ade9e3b993823aa9f45c30231490ea75"
	request = urllib.request.Request(url, headers={"Authorization" : "token "+token})
	return json.loads(urllib.request.urlopen(request).read().decode())

def calc_duration(start_time, end_time):
	"""
	function to return duration(int) in hours between 2 time formats
	start_time -> str : date format string, ex - "2017-02-20T07:19:22Z"
	end_time -> str : date format string, should be ahead of start_time
	"""
	start_time = datetime.datetime(*list(map(int, re.split('[^\d]', start_time)[:-1])))
	end_time = datetime.datetime(*list(map(int, re.split('[^\d]', end_time)[:-1])))
	delta = end_time - start_time
	hours = int(delta.total_seconds()/3600)
	return hours

def write_csv(data_dict_keys, data_dict, filename):
	"""
	function to write data from dictionary to a csv file
	data_dict_keys -> list : columns of csv file, should be keys in data_dict
	data dict -> dict : dictionary containing data values
	filename -> str : desired output name of the csv file
	"""
	with open(filename, 'w', newline='') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(data_dict_keys)
		for item in data_dict:
			row = []
			for key in data_dict_keys:
				row.append(data_dict[item][key])
			outputWriter.writerow(row)