import os, sys

PYTHON_ABSOLUTE_PATH = sys.executable
CURRENT_ABSOLUTE_PATH = os.path.abspath('')


# INSTALLING DEPENDENCIES
os.system('pip install -r requirements.txt')
os.system('cls')


# CONFIG.ZEUS
with open('__VENDORS/config.zeus', 'w') as file:
    server_name = input('\nSERVER NAME: ')
    file.write(f'https://{server_name}.zeustech.in/webapi/checkInOut/file/upload')


# MACHINE_LIST
no_of_machines = int(input('\nTotal Number of Machines: '))
print('\nType machine IP and number like this "192.168.1.2,12"')

machine_file_content = ''
for i in no_of_machines:
    machine_file_content += input(f'Machine {i}: ') + '\n'

with open('__VENDORS/machine_list', 'w') as file:
    file.write(machine_file_content)
os.system('cls')


# SCRIPT.BAT
print('==== Creating Executable Script ====')
with open('script.bat', 'w') as file:
    content = f'''cd /d "{CURRENT_ABSOLUTE_PATH}"\n{PYTHON_ABSOLUTE_PATH} {CURRENT_ABSOLUTE_PATH}\\upload_attendance.pyc'''
    file.write(content)


# WINDOWS CRON JOBS
print('==== Setting up CRON JOB ====\n')
print('Your attendances will be uploaded automatically everyday')
print('(Enter time in railway format [HH:MM])\n')

cron_runtime = input('Run Daily at: ')
CRON_CMD_1 = f'SCHTASKS /CREATE /SC DAILY /TN "ZEUSTECH\\auto-attendance-scheduler" /TR "{CURRENT_ABSOLUTE_PATH}\\upload_attendance.pyc" /ST {cron_runtime}'
CRON_CMD_2 = f'SCHTASKS /CREATE /SC ONSTART /TN "ZEUSTECH\\update-auto-attendance" /TR "{CURRENT_ABSOLUTE_PATH}\\update.pyc"'
os.system(CRON_CMD_1)
os.system(CRON_CMD_2)


os.system('cls')

print('Setup is successfully completed!\n')
os.system('pause')

if os.path.exists('update.py'):
    os.system(f'{CURRENT_ABSOLUTE_PATH}\\update.py')