import os, requests

BASE_URL = 'https://raw.githubusercontent.com/mrvaibh/Zeus-Uploader-Automation/main/'

response = requests.get(BASE_URL + 'RELEASE')

latest_version = response.content.decode()
local_version = None

with open('RELEASE') as file:
    local_version = file.readline()

if latest_version == local_version:
    exit()


def update_file(filename):
    # getting latest content from API
    response = requests.get(BASE_URL + filename)
    latest_file_content = response.content.decode()
    print(latest_file_content)
    
    # writing into .py file
    with open(filename, 'w') as file:
        file.write(latest_file_content)
    
    # compile .py to .pyc
    if filename[-3:] == '.py':
        os.system(f'python -m compileall -b {filename}')
        os.remove(filename)

update_file('upload_attendance.py')
update_file('upload_attendance_fast.py')
update_file('machine_status.py')
update_file('update.py')
update_file('RELEASE')