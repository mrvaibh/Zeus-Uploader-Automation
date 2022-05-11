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

    max_retries = input('Max retires (default: 5) : ') or '5'
    time_delay = input('Time delay in sec (default: 2): ') or '2'

    cron_runtime = input('Run Daily at: ') + ',' + input('Run every how many hrs? (leave blank if NA): ')

    file.writelines([
        f'https://{server_name}.zeustech.in:{port_number}/webapi/checkInOut/file/upload' + '\n',
        max_retries + '\n',
        time_delay + '\n',
        cron_runtime
    ])

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
    content = f'''cd /d "{CURRENT_ABSOLUTE_PATH}"\n{PYTHON_ABSOLUTE_PATH} {CURRENT_ABSOLUTE_PATH}\\upload_attendance.py'''
    file.write(content)
os.system('cls')

# Run startup functions
if os.path.exists('startup.py'):
    # While first setup run
    from startup import main
    main()


print('\nSetup is successfully completed!\n')
os.system('pause')