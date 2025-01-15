import os

def get_command():
    return input(">>> ")

while True:
    try:
        os.system(get_command())
    except Exception as e:
        print(e)