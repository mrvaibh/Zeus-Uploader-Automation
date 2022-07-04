import os, webbrowser
from logger import logger, log_traces
from zk import ZK

def get_status(IP):
    logger.info(f'Checking Machine status: {IP}')
    conn = None
    # create ZK instance
    zk = ZK(IP, port=4370, timeout=60, password=0, force_udp=False, ommit_ping=False)

    try:
        # connect to device
        conn = zk.connect()
        machine_status = True
    except Exception as error:
        log_traces(error)
        machine_status = False
    finally:
        if conn:
            conn.disconnect()
    return {'machine_status': machine_status}


# Code starts here
try:

    # open and get machine list
    file = open('machine_list', 'r')
    machine_list = file.read().splitlines()
    file.close()

    # Write first line of HTML
    if os.path.exists('machine_status.html'):
        with open('machine_status.html') as html_file:
            machines_status_html = html_file.readline()
    else:
        machines_status_html = '<h1>Last Updated: NEVER</h1><hr>\n'

    # Checking status of all machines one by one
    for each_line in machine_list:
        IP = each_line.split(',')[0]

        returned_data = get_status(IP)

        if returned_data['machine_status']:
            machines_status_html += f'''<h2 style="color:green;">Machine {IP} -- is OK -- Connection Successful</h2>\n'''
        else:
            machines_status_html += f'''<h2 style="color:red;">Machine {IP} -- is DOWN -- Connection Failed.</h2>\n'''

    # Write entire HTML
    logger.info('Writing status file...')
    with open('machine_status.html', 'w') as file:
        file.write(machines_status_html)

    # open machine_status file in the default web browser
    logger.info('Opening in browser')
    url = os.path.abspath("machine_status.html")
    webbrowser.open(url, new=2)

except:
    log_traces()