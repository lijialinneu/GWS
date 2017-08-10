# !/usr/bin/env python

import subprocess
import datetime

'''
function: auto push to github
author: lijialin
2017-08-10
'''
subprocess.call(["git", "add", "."])
subprocess.call(["git", "commit", "-m", "auto push at " + str(datetime.datetime.now())])
subprocess.call(["git", "push", "github_origin", "master"])


