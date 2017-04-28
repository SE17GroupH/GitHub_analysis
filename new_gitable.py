import urllib.request, urllib.error, urllib.parse
import json, csv, datetime, re, random

def get_url_json(url):
	"""get json data from a url"""
	#token = "22c5702a9526267cef83440a3c8c0e82d9bb43a6"
	request = urllib.request.Request(url)#, headers={"Authorization" : "token "+token})
	return json.loads(urllib.request.urlopen(request).read().decode())

def calc_duration(start_time, end_time):
	start_time = datetime.datetime(*list(map(int, re.split('[^\d]', start_time)[:-1])))
	end_time = datetime.datetime(*list(map(int, re.split('[^\d]', end_time)[:-1])))
	delta = end_time - start_time
	hours = int(delta.total_seconds()/3600)
	return hours

def process_issues(issues, issues_json):
	print("processing {} issues".format(len(issues_json)))
	for issue in issues_json:
		new_issue = {}
		new_issue['id'] = issue['number']
		new_issue['state'] = issue['state']
		new_issue["created_at"] = issue['created_at']
		
		if issue['state']=="closed":
			new_issue['closed_at'] = issue['closed_at']
			new_issue['duration'] = calc_duration(issue['created_at'], issue['closed_at'])
		else:
			new_issue['closed_at'] = "None"
			new_issue['duration'] = "None"

		new_issue['comments'] = issue['comments']
		new_issue["created_by"] = issue['user']['login']
		
		if issue['html_url'].find("/pull/")!=-1:
			new_issue["pull_request"] = "Yes"
		else:
			new_issue["pull_request"] = "No"

		if issue['assignees']:
			assignees = []
			for user in issue['assignees']:
				assignees.append(user['login'])
			new_issue["assignees"] = assignees
		else:
			new_issue["assignees"] = []
		
		if issue["milestone"]:
			new_issue["milestone"] = issue["milestone"]["due_on"]
		else:
			new_issue["milestone"] = "None"

		if issue["labels"]:
			new_issue["labels"] = len(issue["labels"])
		else:
			new_issue["labels"] = "None"

		issues[issue['number']] = new_issue
	

def get_issues(reponame):
	issue_url = "https://api.github.com/repos/{}/issues?state=all&page=".format(reponame)
	issue_url += "{}"
	page = 1
	issues = {}
	while(True):
		issues_json = get_url_json(issue_url.format(page))
		if not issues_json:
			break
		process_issues(issues, issues_json)
		page += 1
	
	return issues

def write_csv(data_dict_keys, data_dict, filename):
	with open(filename, 'w', newline='') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(data_dict_keys)
		for item in data_dict:
			row = []
			for key in data_dict_keys:
				row.append(data_dict[item][key])
			outputWriter.writerow(row)

repos = ["SE17GroupH/Zap"]

for index,reponame in enumerate(repos):
	issues = get_issues(reponame)
	filename = "{}_issues.csv".format(reponame.replace("/","_"))
	
	issue_keys = ["id", "state", "pull_request", "created_at", "closed_at", "duration", "created_by", "comments", "assignees", "milestone", "labels"]
	write_csv(issue_keys, issues, filename)