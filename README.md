# Zeus-Uploader-Automation

## Setup
### PIPENV (recommended)
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`
### Globally
 - `pip install -r requirements.txt`

## Usage
 - create a file `machine_list` and add IP and Machine ID per line. For example:
 ```
192.168.88.201,11
192.168.88.202,12
192.168.88.203,13
192.168.88.204,14
192.168.88.205,15
```
__Note: MID must me unique and always the same once created__
 - create `config.zeus` and add URL of server endpoint. For example: `http://demo.zeustech.in:8082/webapi/checkInOut/punchin`

## Cron
 - Make use if `script.bat` to setup CRON