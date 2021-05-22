import requests;
import json
import logging
import time;

path = '.\log\map_annotation.txt'
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(path,encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

applyCount = None
state = None

def scount():
    global applyCount
    global state
    url = 'https://bm.gd-pa.cn/api/student/bmStudentApply/getApplyStatistics?_t=1621332046&batchId=1390147840566681602'



    headers = {
        'Referer':'https://bm.gd-pa.cn/wsbm/student/statistics/currentBatch',
        'X-Access-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjEzNDUzOTcsInVzZXJuYW1lIjoiMjc2MjM1NTA2In0.M-Le8XzIGiRxyuoDUvDBaFfkEiVupkLKVM0brrbkL5s'
    }

    req = requests.get(url, headers=headers, verify=False).json()

    applyCountT = req['result']['applyCount']
    stateT = req['result']['state']

    if stateT != state or applyCountT != applyCount:
        applyCount = applyCountT
        state = stateT
        logger.info(state + ':' + str(applyCount))


while True:
    scount()
    time.sleep(5)