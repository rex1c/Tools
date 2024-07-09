import os , time

os.system("python3 watch.py")
os.system("python3 watch.py")

while True:
    os.system("python3 watch.py > alert")
    time.sleep(600)
