import os, requests, json
from logger import logger, log_traces

###### coming back to current dir
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)

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
    'auto_uploader.py',
    'upload_attendance.py',
    'machine_status.py',
    'setup.py',
    'RELEASE',
    'startup.py',
]

def main():
    # updating all files
    if needs_update():
        for file in FILES_TO_UPDATE:
            update_file(file)

def run_uploader():
    logger.info('Running uploader')
    import subprocess
    subprocess.call('python auto_uploader.py', shell=True)


if __name__ == '__main__':
    try:
        main()


        # TASK SCHEDULER
        import time, schedule

        with open('__VENDORS/config.zeus', 'rb') as config_file:
            (railtime, everytime) = json.load(config_file)['CRON_RUNTIME']

        if not everytime: schedule.every().day.at(railtime).do(run_uploader)
        else: schedule.every(int(everytime)).minutes.do(run_uploader)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        log_traces()