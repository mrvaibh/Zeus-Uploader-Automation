import sys, requests, csv
from datetime import datetime
from zk import ZK, const


def upload_punches(IP, sensor_id):
    conn = None
    # create ZK instance
    zk = ZK('192.168.88.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

    # connect to device
    conn = zk.connect()

    with open('.log', 'r') as log_file:
        last_attendance = log_file.read()[-16:]
        if last_attendance:
            last_attendance_time_obj = datetime.strptime(last_attendance, '%d-%m-%Y %H:%M')
        else:
            last_attendance_time_obj = datetime.strptime('01-01-1990 00:00', '%d-%m-%Y %H:%M')

    export = []

    for attendance in conn.get_attendance():
        if attendance is None:
            continue

        attendance_time = attendance.timestamp.strftime("%d-%m-%Y %H:%M")
        attendance_time_obj = datetime.strptime(attendance_time, '%d-%m-%Y %H:%M')

        if attendance_time_obj > last_attendance_time_obj:
            export.append({
                'Badgenumber': attendance.user_id.zfill(5),
                'blank1': '',
                'Checktime': attendance_time,
                'blank2': '',
                'Sensorid': sensor_id
            })

    print(export)

    if not export:
        return

    # creating CSV out of `export`
    with open('mytable.csv', 'w') as csv_file:
        field_names = ['Badgenumber', 'blank1', 'Checktime', 'blank2', 'Sensorid']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', lineterminator='\n') # default field-delimiter is ","
        csv_writer.writerows(export)

    # send file to the server
    response_code = None
    with open('mytable.csv', 'r') as csv_file:
        data = csv_file.read()
        # response = requests.post('http://demo.zeustech.in:8082/webapi/checkInOut/punchin', data=data, headers={'Content-type': 'application/text'})
        # response_code = response.status_code

    # Deleting the file immediately
    # os.remove('mytable.csv')

    with open('.log', 'a') as log_file:
        log_file.write('[' + datetime.now().strftime("%d-%m-%Y %H:%M") + '] -- IP: ' + IP + ' -- ' + ' MID: ' + sensor_id + ' -- ' + export[-1]['Checktime'])

try:
    machine_list = open('.machine_list', 'r').read().splitlines()

    for each_line in machine_list:
        [IP, sensor_id] = each_line.split(',')

        upload_punches(IP, sensor_id.replace('\n', ''))
    
except Exception as e:
    print ("Process terminate : {}".format(e))