import os
from datetime import datetime
currenttime = datetime.now().strftime('%Y-%m-%d-%H')
path = os.getcwd()
print('cur dir',path)
print('par dir',os.path.abspath(os.path.join(path,os.pardir)))
print('cur dir after print the parent dir',os.getcwd())
print(currenttime)