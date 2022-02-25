import requests, json
from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('192.168.88.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    # connect to device
    conn = zk.connect()
    print('Connection was successful')

    for attendance in conn.get_attendance():
        if attendance is None:
            # implement here timeout logic
            print("attendance is", attendance)
            pass
        else:
            data = {"userId": attendance.user_id}

            print (attendance) # Attendance object
            print ("User ID:", attendance.user_id)
            print ("Punch:", attendance.punch)
            print ("Status:", attendance.status)
            print ("Timestamp:", attendance.timestamp)
            print ("UID:", attendance.uid)
            # print ("--------")

            print(conn.get_attendance())

            # response = requests.post('http://demo.zeustech.in:8082/webapi/checkInOut/punchin', data = json.dumps(data), headers={'Content-type': 'application/json'})
            # print(response)

except Exception as e:
    print ("Process terminate : {}".format(e))