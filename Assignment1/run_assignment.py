import os
from pathlib import Path
from config import CONFIG

q1 = Path("./q1.py")
q2 = Path("./q2.py")

answer_loc = CONFIG["ANSWER_LOCATION"]
with open(answer_loc, "w") as f:
    f.write("")

os.system("python {}".format(q1))
os.system("python {}".format(q2))
