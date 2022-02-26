import os, sys, requests, csv
from datetime import datetime
from zk import ZK, const


def upload_punches(IP, sensor_id, last_log):
    conn = None
    # create ZK instance
    zk = ZK(IP, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

    # connect to device
    conn = zk.connect()

    attendances = []

    for attendance in conn.get_attendance():
        if attendance is None:
            continue

        try:
            last_attendance_time_obj = datetime.strptime(last_log, '%d-%m-%Y %H:%M:%S')
        except:
            last_attendance_time_obj = datetime.strptime('01-01-1990 00:00:00', '%d-%m-%Y %H:%M:%S')

        if attendance.timestamp >= last_attendance_time_obj:
            attendances.append({
                'Badgenumber': attendance.user_id.zfill(5),
                'blank1': '',
                'Checktime': datetime.strftime(attendance.timestamp, '%d-%m-%Y %H:%M'),
                'blank2': '',
                'Sensorid': sensor_id
            })

    return [
        attendances,
        conn.get_time().strftime("%d-%m-%Y %H:%M:%S")
    ]

# Main logic
try:
    SERVER_URL = 'http://demo.zeustech.in:8082/webapi/checkInOut/punchin'

    if os.path.exists('config.zeus'):
        with open('config.zeus', 'r') as file:
            lines = file.read().splitlines()

            SERVER_URL = lines[0]

    file = open('machine_list', 'r')
    machine_list = file.read().splitlines()
    file.close()


    # create log file if doesn't exist
    if not os.path.exists('logs.csv'):
        with open('logs.csv', 'w') as csv_file:
            IP_list = [each_line.split(',')[0] for each_line in machine_list]
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(IP_list)

    total_data = []
    logs = []

    # Fetching data from all machines one by one
    for (index, each_line) in enumerate(machine_list):
        [IP, sensor_id] = each_line.split(',')

        with open('logs.csv', 'r') as log_file:
            data = log_file.readlines()

        list_of_last_log = data[-1].replace('\n', '').split(',')
        last_log = list_of_last_log[index]

        [attendances, machine_time] = upload_punches(IP, sensor_id, last_log)
        total_data += attendances

        logs.append(machine_time)


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
        response = requests.post(SERVER_URL, data=data, headers={'Content-type': 'application/text'})
        print("Data uploaded. Response status:", response.status_code)

    # Deleting the file immediately
    os.remove('mytable.csv')


    # append logs
    with open('logs.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        csv_writer.writerow(logs)


except Exception as error:
    exc_type, exc_obj, exc_tb = sys.exc_info()

    with open('error_log.txt', 'a') as error_log:
        error_log.write(f'''[ {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} ]
    ===ERROR=== {str(error)}
    ===TYPE=== {str(exc_type)}
    ===LINENO=== {str(exc_tb.tb_lineno)}\n''')

    print ("Process terminate : {}".format(error))