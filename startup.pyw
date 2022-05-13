import os, requests

os.chdir(os.path.dirname(__file__))

BASE_URL = 'https://raw.githubusercontent.com/mrvaibh/Zeus-Uploader-Automation/main/'


def needs_update():
    response = requests.get(BASE_URL + 'RELEASE')
    latest_version = response.content.decode().split('.')
    local_version = None

    with open('RELEASE') as file:
        local_version = file.readline().split('.')

    # comparing PATCH, MINOR, MAJOR versions respectively
    for v1, v2 in zip(reversed(latest_version), reversed(local_version)):
        if v1 > v2:
            return True
    return False


def update_file(filename):
    # getting latest content from API
    print(f'Updating {filename}...')
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
    'startup.pyw',
]

def main():
    # updating all files
    if needs_update():
        for file in FILES_TO_UPDATE:
            update_file(file)

def run_uploader():
    import subprocess
    subprocess.call('python upload_attendance.py', shell=True)


if __name__ == '__main__':
    main()


    # TASK SCHEDULER
    import time, schedule

    with open('__VENDORS/config.zeus') as file:
        (railtime, everytime) = file.readlines()[3].split(',')

    if not everytime: schedule.every().day.at(railtime).do(run_uploader)
    else: schedule.every(int(everytime)).hours.at(railtime).do(run_uploader)
    
    while True:
        schedule.run_pending()
        time.sleep(1)