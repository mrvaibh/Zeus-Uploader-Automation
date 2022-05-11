import os, sys, requests, csv, webbrowser, time, logging, traceback
from datetime import datetime
from zk import ZK

os.chdir(os.path.dirname(__file__))                                                                     
os.chdir('__VENDORS')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

###### CONSTANTS 
MAX_RETRIES = 5
TIME_DELAY_FACTOR = 2
SERVER_URL = 'https://demo.zeustech.in:8500/webapi/checkInOut/file/upload'


def log_errors(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    
    logger.error(f'''[ {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} ]
    ===ERROR=== {str(error)}
    ===TYPE=== {str(exc_type)}
    ===LINENO=== {str(exc_tb.tb_lineno)}\n''')
    logger ("Process terminate : {}".format(error))


def upload_punches_to_server(device_code, punches, script_start_time):

    logger.info(f"uploading punches for device - {device_code} with {len(punches)} punches")
    file_name = f'data_uploaded-{script_start_time}-device_{device_code}.csv'
    with open(file_name, 'w') as csv_file:
        field_names = ['Badgenumber', 'blank1', 'Checktime', 'blank2', 'Sensorid']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', lineterminator='\n') # default field-delimiter is ","
        csv_writer.writerows(punches)

    retries = 0
    response = None
    upload_successful = False
    while retries < MAX_RETRIES:
        try:
            time.sleep(TIME_DELAY_FACTOR ** retries)
            with open(file_name, 'r') as csv_file:
                data = csv_file.read()
                response = requests.post(SERVER_URL, data=data, headers={'Content-type': 'application/text'}, verify=False, allow_redirects=True)
                logger.info(f"Upload Request response -  device_code {device_code} Response status:{response.status_code} and response message {response.content}")
                upload_successful = True if response.status_code == 200 else False
            break
        except:
            logger.error(f"Exception in uploading to server for device_code {device_code}", traceback.format_exc())
            retries += 1

    if(upload_successful):
        logger.info("Upload Successful!")
    else:
        logger.error("Upload not sucessful|")

def save_all_punches_for_debugging(device_code, punches, script_start_time):
    file_name = f'raw_punches_{script_start_time}-{device_code}.csv'
    with open(file_name, 'w') as csv_file:
        field_names = ['Badgenumber', 'blank1', 'Checktime', 'blank2', 'Sensorid']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', lineterminator='\n') # default field-delimiter is ","
        csv_writer.writerows(punches)

def parse_punches(device_punches, sensor_id, last_attendance_time_obj):
    attendances = []
    all_punches = []
    latest_attendance_timestamp = datetime(1999, 1, 1, 0, 0)
    for attendance in device_punches:
        if attendance is None:
            continue
        checktime = datetime.strftime(attendance.timestamp, '%d-%m-%Y %H:%M')
        punch = {
            'Badgenumber': attendance.user_id.zfill(5),
            'blank1': '',
            'Checktime':checktime,
            'blank2': '',
            'Sensorid': sensor_id
        }
        all_punches.append(punch)
        if attendance.timestamp >= last_attendance_time_obj:
            attendances.append(punch)
        if attendance.timestamp >= latest_attendance_timestamp:
            latest_attendance_timestamp = attendance.timestamp
    logger.info(f"received total punche = {len(all_punches)},  new punches = {len(attendances)} and latest timestamp - {latest_attendance_timestamp}")
    return (attendances, all_punches)

def fetch_punches_from_device(IP, sensor_id, last_log):
    conn = None
    zk = ZK(IP, port=4370, timeout=60, password=0, force_udp=False, ommit_ping=False)
    retries = 0
    while retries < MAX_RETRIES:
        try:
            time.sleep(TIME_DELAY_FACTOR ** retries)
            logger.info(f'Machine: {IP} -- Attempt {retries + 1}/{MAX_RETRIES}')
            # connect to device
            if(not conn):
                conn = zk.connect()
            current_machine_time = conn.get_time().strftime("%d-%m-%Y %H:%M:%S")
            attendances = []
            all_punches = []
            last_attendance_time_obj = datetime.strptime(last_log, '%d-%m-%Y %H:%M:%S')
            logger.info(f"last_log_time {last_attendance_time_obj} and current_machine_time {current_machine_time}")
            device_raw_punches = conn.get_attendance()
            parsed_punches_tuple = parse_punches(device_raw_punches, sensor_id, last_attendance_time_obj)
            machine_status = True
            exceptional_error = None
            break
        except Exception as error:
            logger.error(f"Not able to get punches from device {sensor_id}", traceback.format_exc())
            attendances = []
            current_machine_time = last_log
            machine_status = False
            exceptional_error = error
            retries += 1

    if conn:
        conn.disconnect()

    return {
        'conn': conn,
        'exceptional_error': exceptional_error,
        'attendances': parsed_punches_tuple[0],
        'all_punches': parsed_punches_tuple[1],
        'current_machine_time': current_machine_time,
        'machine_status': machine_status,
    }

def read_config_file():
    # setting up configurations
    if os.path.exists('config.zeus') == False:
        logger.error("config.zeus does not exist. Falling back to defaults")
        return
    with open('config.zeus', 'r') as file:
        lines = file.read().splitlines()
        SERVER_URL = lines[0]
        MAX_RETRIES = int(lines[1])
        TIME_DELAY_FACTOR = int(lines[2])

def get_machine_list() :
    # open and get machine list q
    with open('machine_list', 'r') as file:
        return file.read().splitlines()

def create_machine_log_file():
    machine_list = get_machine_list()
    # create log file if doesn't exist
    if not os.path.exists('logs.csv'):
        with open('logs.csv', 'w') as csv_file:
            IP_list = [each_line.split(',')[0] for each_line in machine_list]
            default_last_log_time = ["01-01-1990 00:00:00" for each_line in machine_list]
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(IP_list)

def get_last_uploaded_time():
    create_machine_log_file()
    # open log file and getting last row
    with open('logs.csv', 'r') as log_file:
        last_row = log_file.readlines()[-1]
    list_of_last_log = last_row.replace('\n', '').split(',')
    return list_of_last_log

def process_device(IP, sensor_id, last_log, script_start_time):
    returned_data = fetch_punches_from_device(IP, sensor_id, last_log)
    last_log = returned_data['current_machine_time']
    machine_status = returned_data['machine_status']
    new_punches = returned_data['attendances']
    all_punches = returned_data['all_punches']
    if not returned_data['conn']:
        logger.error("Error in upload_punch() : {}".format(returned_data['exceptional_error']))
        return (last_log, False)

    process_successful = False
    upload_punches_to_server(sensor_id, new_punches, script_start_time)
    save_all_punches_for_debugging(sensor_id, all_punches, script_start_time)
    process_successful = True
    return (last_log, process_successful)

#Code starts here. 
def init():
    try: 
        script_start_time = datetime.now().strftime("%d-%m-%Y %H %M")
        logger.info(f"starting auto upload at {script_start_time}")
        read_config_file()
        machine_list = get_machine_list()
        list_of_last_log = get_last_uploaded_time()
        #Updated latest uploaded timestamp for each device
        logs = []
        machines_status_html = '<h1>Last Updated: ' + script_start_time + '</h1><hr>\n'

        logger.info("Device IPs and their last updated timestamp")
        logger.info(machine_list)
        logger.info(list_of_last_log)

        # Fetching data from all machines one by one
        for (index, each_line) in enumerate(machine_list):
            [IP, sensor_id] = each_line.split(',')
            last_log = list_of_last_log[index]
            logger.info(f"starting process for {IP} with last_upload_time {last_log}")
            process_result = process_device(IP, sensor_id, last_log, script_start_time)
            logger.info(f"device processed with result {process_result}")
            last_log = process_result[0]
            logs.append(last_log)
            machines_status_html += (f'''<h2 style="color:green;">Machine {IP} -- is OK -- Data Uploaded.</h2>\n''' 
                                    if process_result[1] else
                                    f'''<h2 style="color:red;">Machine {IP} -- is DOWN -- Connection Failed.</h2>\n''')


        with open('logs.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(logs)

        with open('machine_status.html', 'w') as file:
            file.write(machines_status_html)

        # open machine_status file in the default web browser
        url = os.path.abspath("machine_status.html")
        webbrowser.open(url, new=2)

    except Exception as error:
        log_errors(error)


init()