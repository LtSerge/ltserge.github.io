from git import Repo
import datetime
import time
from datetime import date
import json
import requests

now = datetime.datetime.now()
clean_now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
message = "Commit made on: "
full = message + clean_now

working_tree_dir = '/home/ec2-user/crontGit/ltserge.github.io'

file = "ltserge.github.io/pf24h.txt"

COMMIT_MESSAGE = full

# unix time for api
unix_time = int(time.time())
print(unix_time)
# creating the date object of today's date
todays_date = date.today()
print(todays_date)
year = todays_date.year
month = todays_date.month
day = todays_date.day
value = 0

# insert your API key here
API_KEY = '20yrbsOgJltKYbi4xNzPWrkR9WT'

# make API request
res = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_funding_rate_perpetual_all',
                   params={'a': 'BTC', 'api_key': API_KEY, 'f': 'JSON', 'i': '24h', 's': unix_time})

json_str = json.loads(res.text)
print(json_str[0]['o']['mean'])
value = json_str[0]['o']['mean']


def alter_file(file):
    with open(file, "r") as in_file:
        buf = in_file.readlines()

    with open(file, "w") as out_file:
        for line in buf:
            if line == "//Include Above\n":
                line = f"d := t == timestamp({year}, {month}, {day}, 0, 0, 0) ? {value} : d\n" + line
            out_file.write(line)


def git_push():
    try:
        repo = Repo('/home/ec2-user/crontGit/ltserge.github.io')
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')


print(full)

alter_file(file)

git_push()
