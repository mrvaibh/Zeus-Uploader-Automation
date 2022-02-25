import requests, json
from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
    # connect to device
    conn = zk.connect()
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            data = {"userId": attendance.user_id }
            response = requests.post('http://demo.zeustech.in:8082/webapi/checkInOut/punchin', data = json.dumps(data), headers={'Content-type': 'application/json'})
            print(response)
            print (attendance) # Attendance object

except Exception as e:
    print ("Process terminate : {}".format(e))
