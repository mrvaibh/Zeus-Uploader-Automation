import os, sys, requests, csv, webbrowser
from datetime import datetime
from zk import ZK

os.chdir('__VENDORS')

def log_errors(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()

    with open('error_log.txt', 'a') as error_log:
        error_log.write(f'''[ {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} ]
    ===ERROR=== {str(error)}
    ===TYPE=== {str(exc_type)}
    ===LINENO=== {str(exc_tb.tb_lineno)}\n''')
    print ("Process terminate : {}".format(error))

def upload_punches(IP, sensor_id, last_log):
    conn = None
    # create ZK instance
    zk = ZK(IP, port=4370, timeout=60, password=0, force_udp=False, ommit_ping=False)

    try:
        # connect to device
        conn = zk.connect()

        attendances = []

        try:
            last_attendance_time_obj = datetime.strptime(last_log, '%d-%m-%Y %H:%M:%S')
        except:
            last_attendance_time_obj = datetime.strptime('01-01-1990 00:00:00', '%d-%m-%Y %H:%M:%S')

        for attendance in conn.get_attendance():
            if attendance is None:
                continue

            if attendance.timestamp >= last_attendance_time_obj:
                attendances.append({
                    'Badgenumber': attendance.user_id.zfill(5),
                    'blank1': '',
                    'Checktime': datetime.strftime(attendance.timestamp, '%d-%m-%Y %H:%M'),
                    'blank2': '',
                    'Sensorid': sensor_id
                })

        current_machine_time = conn.get_time().strftime("%d-%m-%Y %H:%M:%S")
        machine_status = True

    except Exception as error:
        log_errors(error)

        attendances = []
        try:
            # validating last log time
            last_attendance_time_obj = datetime.strptime(last_log, '%d-%m-%Y %H:%M:%S')
            current_machine_time = last_log
        except:
            current_machine_time = '01-01-1990 00:00:00'

        machine_status = False
        print ("Error in upload_punch() : {}".format(error))

    finally:
        if conn:
            conn.disconnect()

    return {
        'attendances': attendances,
        'current_machine_time': current_machine_time,
        'machine_status': machine_status,
    }



# Code starts here
try:
    SERVER_URL = 'http://demo.zeustech.in:8082/webapi/checkInOut/file/upload'

    # setting up configurations
    if os.path.exists('config.zeus'):
        with open('config.zeus', 'r') as file:
            lines = file.read().splitlines()

            SERVER_URL = lines[0]

    # open and get machine list
    file = open('machine_list', 'r')
    machine_list = file.read().splitlines()
    file.close()


    # create log file if doesn't exist
    if not os.path.exists('logs.csv'):
        with open('logs.csv', 'w') as csv_file:
            IP_list = [each_line.split(',')[0] for each_line in machine_list]
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(IP_list)


    # open log file and getting last row
    with open('logs.csv', 'r') as log_file:
        data = log_file.readlines()
    list_of_last_log = data[-1].replace('\n', '').split(',')


    total_data = []
    logs = []
    machines_status_html = '<h1>Last Updated: ' + datetime.now().strftime('%d/%m/%Y, %H:%M:%S') + '</h1><hr>'

    # Fetching data from all machines one by one
    # and appending to `total_data`
    for (index, each_line) in enumerate(machine_list):
        [IP, sensor_id] = each_line.split(',')

        last_log = list_of_last_log[index]

        returned_data = upload_punches(IP, sensor_id, last_log)
        total_data += returned_data['attendances']

        logs.append(returned_data['current_machine_time'])

        if returned_data['machine_status']:
            machines_status_html += f'''<h2 style="color:green;">Machine {IP} -- is OK -- Data Uploaded.</h2>\n'''
        else:
            machines_status_html += f'''<h2 style="color:red;">Machine {IP} -- is DOWN -- Connection Failed.</h2>\n'''

    with open('machine_status.html', 'w') as file:
        file.write(machines_status_html)

    # open machine_status file in the default web browser
    url = os.path.abspath("machine_status.html")
    webbrowser.open(url, new=2)

    if not total_data:
        print('No new punches found')
        exit()

    print(f'Total {len(total_data)} punches found')


    # creating CSV out of `total_data`
    with open('mytable.csv', 'w') as csv_file:
        field_names = ['Badgenumber', 'blank1', 'Checktime', 'blank2', 'Sensorid']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', lineterminator='\n') # default field-delimiter is ","
        csv_writer.writerows(total_data)


    # send entire data to the server at once
    with open('mytable.csv', 'r') as csv_file:
        data = csv_file.read()
        response = requests.post(SERVER_URL, data=data, headers={'Content-type': 'application/text'}, verify=False, allow_redirects=True)
        print("Data uploaded. Response status:", response.status_code)

    # Deleting the file immediately
    os.remove('mytable.csv')


    # append logs
    with open('logs.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        csv_writer.writerow(logs)

except Exception as error:
    log_errors(error)
