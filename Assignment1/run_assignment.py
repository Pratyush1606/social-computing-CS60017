import os
from pathlib import Path

q1 = Path("./q1.py")
q2 = Path("./q2.py")

os.system("python {}".format(q1))
os.system("python {}".format(q2))
