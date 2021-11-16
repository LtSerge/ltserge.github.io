from git import Repo
import datetime

now = datetime.datetime.now()
clean_now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
message = "Commit made on: "
full = message + clean_now

working_tree_dir = '/home/ec2-user/crontGit/ltserge.github.io'

file = "ltserge.github.io/pf24h.txt"

COMMIT_MESSAGE = full


def alter_file(file):
    with open(file, "r") as in_file:
        buf = in_file.readlines()

    with open(file, "w") as out_file:
        for line in buf:
            if line == "; Include this text\n":
                line = line + "Include below\n"
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

