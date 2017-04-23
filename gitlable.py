#  gitabel Python3 version by TeamH

"""
You will need to add your authorization token in the code.
Here is how you do it.
1) In terminal run the following command
curl -i -u <your_username> -d '{"scopes": ["repo", "user"], "note": "OpenSciences"}' https://api.github.com/authorizations
2) Enter ur password on prompt. You will get a JSON response. 
In that response there will be a key called "token" . 
Copy the value for that key and paste it on line marked "token" in the attached source code. 
3) Run the python file. 
		 python gitable.py
"""
 

import urllib.request, urllib.error, urllib.parse
import json, csv
import re, datetime
import sys, random, os


#global variables
#token = "22c5702a9526267cef83440a3c8c0e82d9bb43a6" #can set token here
token = "" #set your token here 
class L():
	"Anonymous container"
	def __init__(i,**fields) : 
		i.override(fields)
	def override(i,d): i.__dict__.update(d); return i
	def __repr__(i):
		d = i.__dict__
		name = i.__class__.__name__
		return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
										 for k in i.show()])+ '}'
	def show(i):
		lst = [str(k)+" : "+str(v) for k,v in i.__dict__.items() if v != None]
		return ',\t'.join(map(str,lst))
	
def secs(d0):
	d     = datetime.datetime(*list(map(int, re.split('[^\d]', d0)[:-1])))
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = d - epoch
	return delta.total_seconds()
 
def dump1(u,issues, mapping):
	"""
	requires github access token
	returns dictionary of labeled issues with its list of events.
	"""
	
	# if token == "22c5702a9526267cef83440a3c8c0e82d9bb43a6":
	# 	try:  
	# 		token = os.environ['GITHUB_TOKEN']
	# 	except KeyError: 
	# 		print("Please set the environment variable GITHUB_TOKEN")
	# 		print("In bash: GITHUB_TOKEN=<your_token>;export GITHUB_TOKEN")
	# 		sys.exit(1)
	
	request = urllib.request.Request(u, headers={"Authorization" : "token "+token})
	v = urllib.request.urlopen(request).read()
	w = json.loads(v.decode())
	if not w: 
		return False
	
	random.shuffle(w)
	
	for event in w:
		if not event.get('label'):
			# we don't want any issue with no label
			# cannot derive any useful insight from it
			# as we do not have the title/content of the issue
			continue

		issue_id = event['issue']['number']
		#created_at = secs(event['created_at'])
		created_at = event['created_at']
		action = event['event']
		label_name = event['label']['name']
		
		milestone = event['issue']['milestone']
		if milestone != None : 
			milestone = milestone['title']
		
		user = event['actor']['login']
		if not mapping.get(user):
			mapping[user] = "user{}".format(len(mapping)+1)
		user = mapping[user]

		eventObj = L(when=created_at,
					 action = action,
					 what = label_name,
					 user = user,
					 milestone = milestone)
		
		#issueObj = L(created=created_at)

		if not issues.get(issue_id): 
			issues[issue_id] = []
		issues[issue_id].append(eventObj)
	
	for issue,events in issues.items():
		events.sort(key=lambda event: event.when)

	return True

def dump(u,issues, mapping):
	try:
		return dump1(u, issues, mapping)
	except Exception as e: 
		print(e)
		print("Contact TA")
		return False



def extractGroupCommitData(url, token, alias):
	commit_data = {}
	request = urllib.request.Request(url, headers={"Authorization" : "token "+token})
	v = urllib.request.urlopen(request).read()
	j = json.loads(v.decode())
	if not j: 
		return False

	commit_data = {}

	for contributor in j:
		for week in contributor["weeks"]:
			week_time = week["w"]
			week_additions = week["a"]
			week_commits = week["c"]
			if week_time in commit_data:
				week_dict = commit_data[week_time]
				week_dict['commits'] += week_commits
				week_dict['additions'] += week_additions
				if week_dict['commits'] != 0:
					week_dict['additions_per_commit'] = week_dict['additions']/week_dict['commits']
				else:
					week_dict['additions_per_commit'] = 0
			else:
				week_dict = {}
				week_dict['commits'] = week_commits
				week_dict['additions'] = week_additions
				commit_data[week_time] = week_dict
				if week_dict['commits'] != 0:
					week_dict['additions_per_commit'] =week_dict['additions']/ week_dict['commits']
				else:
					week_dict['additions_per_commit'] = 0				

	#write data to csv file
		filename = alias+"_commit_data" + ".csv"
	with open(filename, 'w', newline='') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(["week", "commits", "additions", "additions_per_commit"])
		for x in commit_data:
			outputWriter.writerow([x, commit_data[x]['commits'], commit_data[x]['additions'], commit_data[x]['additions_per_commit']])



def dumpMilestone(url, milestones, token):
	request = urllib.request.Request(url, headers={"Authorization" : "token "+token})
	v = urllib.request.urlopen(request).read()
	w = json.loads(v.decode())
	if not w or ('message' in w and w['message'] == "Not Found"): return False
	
	milestone = w
	identifier = milestone['id']
	milestone_id = milestone['number']
	milestone_title = milestone['title']
	milestone_description = milestone['description']

	# created_at = secs(milestone['created_at'])
	# due_at_string = milestone['due_on']

	# due_at = secs(due_at_string) if due_at_string != None else due_at_string
	# print(due_at)
	# closed_at_string = milestone['closed_at']
	# closed_at = secs(closed_at_string) if closed_at_string != None else closed_at_string
	
	created_at = milestone['created_at']
	due_at = milestone['due_on']
	closed_at = milestone['closed_at']

	user = milestone['creator']['login']
	open_issues = milestone['open_issues']
	closed_issues = milestone['closed_issues']
	milestoneObj = L(ident=identifier,
	           m_id = milestone_id,
	           m_title = milestone_title,
	           m_description = milestone_description,
	           created_at=created_at,
	           due_at = due_at,
	           closed_at = closed_at,
	           user = user,
	           open_issues = open_issues,
	           closed_issues = closed_issues)

	milestones.append(milestoneObj)
	return True

def extractGroupMilestoneData(url, token, alias):
	milestones = []
	page = 1
	while(True):

		milestone_url = url + "/" + str(page)
		print(url)
		doNext = False
		try:
			doNext = dumpMilestone(milestone_url, milestones, token)
		except Exception as e:
			print("Exception")
			doNext = False

		print("milestone "+ str(page))
		page = page + 1
		if not doNext: 
			break

	#write data to csv file
	file = alias+"_milestone_data" + ".csv"
	with open(file, 'w', newline='') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(["id", "opened_at", "closed_at", "due_on", "closed_issues", "open_issues"])
		for m in milestones:
			outputWriter.writerow([m.m_id, m.created_at, m.due_at, m.closed_at, m.closed_issues, m.open_issues])


def launchDump():
	repos = ['karanjadhav2508/kqsse17',
			'SE17GroupH/Zap', 
			'SE17GroupH/ZapServer',
			'Rushi-Bhatt/SE17-Team-K',
			'zsthampi/SE17-Group-N', 
			'rnambis/SE17-group-O', 
			'genterist/whiteWolf', 
			'harshalgala/se17-Q', 
			'NCSU-SE-Spring-17/SE-17-S', 
			'SidHeg/se17-teamD', 
			'syazdan25/SE17-Project'
			]

	with open("private_mappings.csv", 'w', newline='') as file:
		outputWriter = csv.writer(file)
		outputWriter.writerow(['original', 'alias'])
		
	random.shuffle(repos)

	for index,reponame in enumerate(repos):
		page = 1
		issues, mapping = {}, {}
		
		repo_url = 'https://api.github.com/repos/{}/issues/events?page='.format(reponame)+'{}'
		print(repo_url);
		while(dump(repo_url.format(page), issues, mapping)):
			page += 1
		
		group_id = "group{}".format(index+1)
		with open("private_mappings.csv", 'a', newline='') as file:
			outputWriter = csv.writer(file)
			outputWriter.writerow([reponame, group_id])
			for username, user_id in mapping.items():
				outputWriter.writerow([username, user_id])

		filename = group_id+".csv"
		with open(filename, 'w', newline='') as outputFile:
			outputWriter = csv.writer(outputFile)
			outputWriter.writerow(["issue_id", "when", "action", "what", "user", "milestone"])
			for issue, events in issues.items():
				for event in events: 
					outputWriter.writerow([issue, event.when, event.action, event.what, event.user, event.milestone])


		#commit
		commit_repo = 'https://api.github.com/repos/{}/stats/contributors'.format(reponame)
		extractGroupCommitData(commit_repo, token, group_id)

		#milestone
		milestone_repo = 'https://api.github.com/repos/{}/milestones'.format(reponame)
		extractGroupMilestoneData(milestone_repo, token, group_id)


launchDump()

