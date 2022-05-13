from auto_uploader_1 import (
    SERVER_URL, MAX_RETRIES, TIME_DELAY_FACTOR,
    read_config_file,
    get_machine_list,
    get_last_uploaded_log
)

def test__get_machine_list():
    machine_list = get_machine_list()
    print(machine_list)

def test__read_config_file():
    read_config_file()
    print(SERVER_URL, MAX_RETRIES, TIME_DELAY_FACTOR)

def test__get_last_uploaded_log():
    list_of_last_logs = get_last_uploaded_log()
    print(list_of_last_logs)

if __name__ == '__main__':
    # test__get_machine_list()
    # test__read_config_file()
    test__get_last_uploaded_log()