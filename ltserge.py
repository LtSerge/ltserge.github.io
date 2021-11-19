from git import Repo
import datetime
import time
from datetime import date, timedelta
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
print('--------------')
print(COMMIT_MESSAGE)
print('Unix Code: ')
print(unix_time)
# creating the date object of today's date
todays_date = date.today()
# print('Today Date: ' + todays_date)

value = 0
value_raw = 0
# insert your API key here
API_KEY = '20yrbsOgJltKYbi4xNzPWrkR9WT'

# make API request
try:
    res = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_funding_rate_perpetual_all',
                   params={'a': 'BTC', 'api_key': API_KEY, 'f': 'JSON', 'i': '24h', 's': unix_time})
except  requests.ConnectionError:
    print('The Value from Glassnode did not arrive')
    
json_str = json.loads(res.text)
value_raw = json_str[0]['o']['mean']
value_raw = value_raw * 100
value = round(value_raw, 3)
print('Daily Perp Funding All Exch: ')
print(value)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

day = yesterday.day
year = yesterday.year
month = yesterday.month


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
        print('--------------')
    except:
        print('Some error occured while pushing the code')
        print('--------------')


alter_file(file)

git_push()
