
from git import Repo
import datetime

now = datetime.datetime.now()
clean_now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
message = "Commit made on: "
full = message + clean_now

working_tree_dir = '/home/ec2-user/crontGit/coding-is-cool'

file = "coding-is-cool/activityTracker.txt"

COMMIT_MESSAGE = full


def alter_file(file):
    with open(file, "a") as f:
        f.write(full + "\n")


def git_push():
    try:
        repo = Repo('/home/ec2-user/crontGit/coding-is-cool')
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
	print('Some error occured while pushing the code')


print(full)

alter_file(file)

git_push()




