# Zeus-Uploader-Automation

## Setup
### For Development
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`
### For Production
 - `pip install -r requirements.txt`

## Usage
### Setting Up
 - run `setup.py`
 - enter SERVER NAME, MACHINE INFO, and TIME when to run task daily
### Set Auto-Update
 - Copy `update.py`
 - press `Win+R`, type `shell:startup`
 - press `Ctrl+Shift+V`
### Set CRON
 - Goto start, search `Task Scheduler`
 - In the left pane, expand `Task Scheduler Library`, and select `ZEUSTECH` folder
 - In the right pane, click on `Properties`
 - CHECK `Run with highest privilages`
 - Goto `Conditions` tab, UNCHECK `Start the task only if the computer is on AC power`

## Troubleshoot
Delete the `logs.csv` file and try again in case of anonymous errors.