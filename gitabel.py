#  gitabel Python3 version
#  the world's smallest project management tool
#  reports relabelling times in github (time in seconds since epoch)
#  thanks to dr parnin
#  todo:
#    - ensure events sorted by time
#    - add issue id
#    - add person handle

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
	requires github access token as environment variable named GITHUB_TOKEN
	returns dictionary of labeled issues with its list of events.
	"""
	try:  
		token = os.environ['GITHUB_TOKEN']
	except KeyError: 
		print("Please set the environment variable GITHUB_TOKEN")
		print("In bash: GITHUB_TOKEN=<your_token>;export GITHUB_TOKEN")
		sys.exit(1)
	
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


launchDump()