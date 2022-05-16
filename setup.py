import os, sys, json

PYTHON_ABSOLUTE_PATH = sys.executable
CURRENT_ABSOLUTE_PATH = os.path.abspath('')


# INSTALLING DEPENDENCIES
os.system('pip install -r requirements.txt')
os.system('cls')


# CONFIG.ZEUS
configs = {}

server_name = input('\nSERVER NAME: ')
port_number = 8500 if server_name == 'demo' else 443

configs['SERVER_URL'] = f'https://{server_name}.zeustech.in:{port_number}/webapi/checkInOut/file/upload'
configs['MAX_RETRIES'] = int(input('Max retires (default: 5) : ')) or 5
configs['TIME_DELAY_FACTOR'] = int(input('Time delay in sec (default: 2): ')) or 2
configs['CRON_RUNTIME'] = (input('Run Daily at: '), int(input('Run every how many mins? (leave blank if NA): ')))

with open('__VENDORS/config.zeus', 'w') as config_file:
    json.dump(configs, config_file, indent=4)

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
print('==== Creating Executable Scripts ====')
with open('launch_bat.vbs', 'w') as file:
    content = f'''Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run chr(34) & "{CURRENT_ABSOLUTE_PATH}\script.bat" & Chr(34), 0\nSet WshShell = Nothing'''
    file.write(content)
with open('script.bat', 'w') as file:
    content = f'''cd /d "{CURRENT_ABSOLUTE_PATH}"\n{PYTHON_ABSOLUTE_PATH} {CURRENT_ABSOLUTE_PATH}\\startup.py'''
    file.write(content)
os.system('cls')

# Run startup functions
if os.path.exists('startup.py'):
    # While first setup run
    from startup import main
    main()


print('\nSetup is successfully completed!\n')
os.system('pause')