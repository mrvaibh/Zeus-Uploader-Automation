import requests, json
from zk import ZK, const

import pickle

conn = None
# create ZK instance
zk = ZK('192.168.88.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)


try:
    # connect to device
    conn = zk.connect()
    print('Connection was successful')

    # def get_user_details(user_id):
    #     all_users = conn.get_users()
    #     for user in all_users:
    #         print(user.user_id == user_id)
    #         if user.user_id is user_id:
    #             return user
    #     return

    # data = {
    #     'user_list': [user for user in conn.get_users()],
    #     'fingerprints': [fingerprint for fingerprint in conn.get_templates()]
    # }

    # file = open('data.pickle', 'wb')
    # pickle.dump(data, file)
    # print('Dumped data')


    # file = open('data.pickle', 'rb')
    # data = pickle.load(file)

    # for user in data['user_list']:
    #     conn.set_user(uid=user.uid, name=user.name, privilege=user.privilege, password=user.password, group_id=user.group_id, user_id=user.user_id, card=user.card)

    #     for fingerprint in data['fingerprints']:
    #         if fingerprint.uid == user.uid:
    #             conn.save_user_template(user, fingerprint)
    # print('Loaded data')

    print(conn.get_users())
    print(conn.get_templates())

    exit()
    

    for attendance in conn.get_attendance():
        if attendance is None:
            # implement here timeout logic
            print("attendance is", attendance)
            pass
        else:
            data = {"userId": attendance.user_id }  
            # response = requests.post('http://demo.zeustech.in:8082/webapi/checkInOut/punchin', data = json.dumps(data), headers={'Content-type': 'application/json'})
            # print(response)
            # print (attendance) # Attendance object
            # print ("User ID:", attendance.user_id)
            # print ("Punch:", attendance.punch)
            # print ("Status:", attendance.status)
            # print ("Timestamp:", attendance.timestamp)
            # print ("UID:", attendance.uid)
            # print ("--------")

except Exception as e:
    print ("Process terminate : {}".format(e))