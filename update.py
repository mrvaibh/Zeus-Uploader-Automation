import os, requests

os.chdir(os.path.dirname(__file__))

BASE_URL = 'https://raw.githubusercontent.com/mrvaibh/Zeus-Uploader-Automation/main/'

response = requests.get(BASE_URL + 'RELEASE')

latest_version = response.content.decode()
local_version = None

with open('RELEASE') as file:
    local_version = file.readline()

if __name__ == '__main__' and latest_version == local_version:
    exit()


def update_file(filename):
    # getting latest content from API
    response = requests.get(BASE_URL + filename)
    latest_file_content = response.content.decode()

    # writing into .py file
    with open(filename, 'w') as file:
        file.write(latest_file_content)

FILES_TO_UPDATE = [
    'upload_attendance.py',
    'upload_attendance_fast.py',
    'machine_status.py',
    'setup.py',
    'RELEASE',
    'update.py',
]

def main():
    for file in FILES_TO_UPDATE:
        update_file(file)

if __name__ == '__main__':
    main()