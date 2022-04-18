import os, sys

PYTHON_ABSOLUTE_PATH = sys.executable
CURRENT_ABSOLUTE_PATH = os.path.abspath('')


# INSTALLING DEPENDENCIES
os.system('pip install -r requirements.txt')
os.system('cls')


# CONFIG.ZEUS
with open('__VENDORS/config.zeus', 'w') as file:
    server_name = input('\nSERVER NAME: ')
    port_number = 8500 if server_name == 'demo' else 443
    file.write(f'https://{server_name}.zeustech.in:{port_number}/webapi/checkInOut/file/upload')


# MACHINE_LIST
no_of_machines = int(input('\nTotal Number of Machines: '))
print('\nType machine IP and number like this "192.168.88.201,12"')

machine_file_content = ''
for i in range(1, no_of_machines+1):
    machine_file_content += input(f'Machine {i}: ') + '\n'

with open('__VENDORS/machine_list', 'w') as file:
    file.write(machine_file_content)
os.system('cls')


# SCRIPT.BAT
print('==== Creating Executable Script ====')
with open('script.bat', 'w') as file:
    content = f'''cd /d "{CURRENT_ABSOLUTE_PATH}"\n{PYTHON_ABSOLUTE_PATH} {CURRENT_ABSOLUTE_PATH}\\upload_attendance.pyc'''
    file.write(content)
os.system('cls')


# WINDOWS CRON JOBS
print('==== Setting up CRON JOB ====\n')
print('Enter time in railway format - HH:MM\n')

cron_runtime = input('Run Daily at: ')
CRON_CMD = f'SCHTASKS /CREATE /SC DAILY /TN "ZEUSTECH\\auto-attendance-scheduler" /TR "{CURRENT_ABSOLUTE_PATH}\\upload_attendance.pyc" /ST {cron_runtime}'
os.system(CRON_CMD)


# Run update
if os.path.exists('update.py'):
    # While first setup run
    from update import main
    main()
elif os.path.exists('update.pyc'):
    # everytime else then the setup is run
    os.system(f'{CURRENT_ABSOLUTE_PATH}\\update.pyc')


print('\nSetup is successfully completed!\n')
os.system('pause')