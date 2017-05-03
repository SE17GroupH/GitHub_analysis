import urllib.request, urllib.error, urllib.parse
import json, csv, datetime, re, random


#global variable
users_global = {}

def get_url_json(url):
	"""get json data from a url"""
	token = "49d551586219d7a7fac856977577c6c4fd994dac"
	request = urllib.request.Request(url, headers={"Authorization" : "token "+token})
	return json.loads(urllib.request.urlopen(request).read().decode())

def calc_duration(start_time, end_time):
	start_time = datetime.datetime(*list(map(int, re.split('[^\d]', start_time)[:-1])))
	end_time = datetime.datetime(*list(map(int, re.split('[^\d]', end_time)[:-1])))
	delta = end_time - start_time
	hours = int(delta.total_seconds()/3600)
	return hours

def process_issues(issues_json):
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
		#new_issue["created_by"] = issue['user']['login']
		########
		user = issue['user']['login']
		if not users_global.get(user):
			users_global[user] = "user{}".format(len(users_global)+1)
		########
		new_issue["created_by"] = users_global[user]
		if issue['html_url'].find("/pull/")!=-1:
			new_issue["pull_request"] = "Yes"
		else:
			new_issue["pull_request"] = "No"

		if issue['assignees']:
			assignees = []
			for user in issue['assignees']:
				#assignees.append(user['login'])
				########
				if not users_global.get(user['login']):
					users_global[user['login']] = "user{}".format(len(users_global)+1)
				########
				assignees.append(users_global[user['login']])
			new_issue["assignees"] = assignees
		else:
			new_issue["assignees"] = []
		
		if issue["milestone"]:
			new_issue["milestone"] = issue["milestone"]["due_on"]
		else:
			new_issue["milestone"] = "None"

		if issue["labels"]:
			new_issue["labels"] = len(issue["labels"])
			new_issue["bug"] = "False"
			for label in issue["labels"]:
				if label["name"] == "bug":
					new_issue["bug"] = "True"
					break
			
		else:
			new_issue["labels"] = "None"
			new_issue["bug"] = "False"

		issues.append(new_issue)
	return issues
	

def get_issues(reponame):
	issue_url = "https://api.github.com/repos/{}/issues?state=all&page=".format(reponame)
	issue_url += "{}"
	page = 1
	issues = []
	while(True):
		issues_json = get_url_json(issue_url.format(page))
		if not issues_json:
			break
		issues.extend(process_issues(issues_json))
		page += 1
	return issues

def calc_date_timestamp(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_contributors(reponame):
	commit_url = "https://api.github.com/repos/{}/stats/contributors".format(reponame)
	contributors = []
	contributors_json = get_url_json(commit_url)
	for contr in contributors_json:
		user = contr["author"]["login"]
		if not users_global.get(user):
			users_global[user] = "user{}".format(len(users_global)+1)
		user_dict = {}
		user_dict["name"] = users_global[user]
		user_dict["total_commits"] = contr["total"]
		total_loc = 0
		user_dict["week1_date"] = calc_date_timestamp(int(contr["weeks"][0]["w"]))
		for index,week in enumerate(contr["weeks"]):
			user_dict["week"+str(index+1)] = week["c"]
			user_dict["week"+str(index+1)+"_loc"] = week["a"]+week["d"]
			total_loc += week["a"]+week["d"]
		user_dict["total_loc"] = total_loc
		
		contributors.append(user_dict)

	index = len(contributors_json[0]["weeks"])-1
	while index>0:
		week = "week"+str(index+1)
		commits = 0
		for user in contributors:
			commits+=user[week]
		if commits==0:
			del contributors[0][week]
			del contributors[0][week+"_loc"]
		else:
			break
		index-=1
	
	return contributors


def write_csv(dict_keys, list_of_dict, filename):
	with open(filename, 'w', newline='') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(dict_keys)
		for item in list_of_dict:
			row = []
			for key in dict_keys:
				row.append(item[key])
			outputWriter.writerow(row)

def write_issues_csv(groupname, reponame):
	issues = get_issues(reponame)
	filename = "{}_issues.csv".format(groupname)
	keys = ["id", "state", "pull_request", "created_at", "closed_at", "duration", "created_by", "comments", "assignees", "milestone", "labels", "bug"]
	write_csv(keys, issues, filename)

def write_contributors_csv(groupname, reponame):
	contributors = get_contributors(reponame)
	filename = "{}_contributors_commits.csv".format(groupname)
	keys = ["name","total_commits", "week1_date"]
	for i in range((len(contributors[0])-4)//2):
		keys.append("week"+str(i+1))
	write_csv(keys, contributors, filename)

	filename = "{}_contributors_loc.csv".format(groupname)
	keys = ["name","total_loc","week1_date"]
	for i in range((len(contributors[0])-4)//2):
		keys.append("week"+str(i+1)+"_loc")
	write_csv(keys, contributors, filename)


if __name__ == '__main__':
	#repos = ["SidHeg/se17-teamD"]#"NCSU-SE-Spring-17/SE-17-S", "SE17GroupH/ZapServer", "SE17GroupH/Zap"]
	#repos = ["NCSU-SE-Spring-17/SE-17-S"]
	#repos = ["SE17GroupH/ZapServer"]
	repos = ["SE17GroupH/Zap"]
	for index,reponame in enumerate(repos):
		groupname = "{}".format(reponame.replace("/","-"))
		#write_issues_csv(groupname, reponame)
		write_contributors_csv(groupname, reponame)
		print(users_global)
		users_global = {}