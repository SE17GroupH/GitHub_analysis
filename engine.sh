#!/bin/bash
# Team H
echo "---------Github Heuristics Engine----------"
echo "Needs git and git_stats (gem install git_stats)"
echo "Enter a Github repo path username/reponame"
read -p 'Username: ' username
read -p 'Reponame: ' reponame
git clone "https://github.com/$username/$reponame"
cd $reponame
######################################################
# Anonymize
echo 
echo "Anonymizing git repo using git filter-branch.."
git log --all --format='%cE' | sort -u | grep -v "noreply@github.com" > /tmp/authors.txt
file=/tmp/authors.txt
i=1
while IFS= read -r line; do
  str='
	WRONG_EMAIL=foobar
	NEW_NAME=usershoofar
	NEW_EMAIL=barfoo@example.com

	if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
	then
	    export GIT_COMMITTER_NAME="$NEW_NAME"
	    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
	fi
	if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
	then
	    export GIT_AUTHOR_NAME="$NEW_NAME"
	    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
	fi
	'
	result_string="${str/foobar/$line}"
	result_string="${result_string/shoofar/$i}"
	result_string="${result_string/barfoo/$i}"
	echo "replacing $line with user$i"
	i=$((i+1))
	#echo "$result_string"
	git filter-branch --env-filter "$result_string" --tag-name-filter cat -- --branches --tags > /dev/null
	rm -rf .git/refs/original/
done < "$file"
######################################################
# Generate stats
git_stats generate --silent
echo "Git_stats report generated at $(pwd)/git_stats/index.html"