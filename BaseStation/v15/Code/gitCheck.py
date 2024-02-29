import threading
import consts
import platform
import sys
import git

def checkGit(a):
    try:
        if platform.system() == "Windows":
            repo = git.Repo("../../../Player_YOLO")
            repo.remotes.origin.pull()
            sha = repo.head.object.hexsha
        else:
            sha = "LINUX_COMMIT"
        consts.gitHash = {
            "playerYolo": str(sha[:7])
        }
    except:
        pass

args = 0
t1 = threading.Thread(target=checkGit)