from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from celery_worker import test_scan, test_amass, test_wildfire
import logging
import subprocess
import psutil
import os
import signal

app = FastAPI()

logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Scan:
    def __init__(self):
        self.scan_running = False
        self.scan_step = 0
        self.scan_complete = 0
        self.scan_step_name = "N/a"
        self.scan_target = "N/a"
        self.core_module = "N/a"

scan_obj = Scan()

def start_scan(fire_starter, fire_cloud, fire_scanner, domain_count, core_module):
    global scan_obj
    scan_obj.scan_running = True
    scan_obj.scan_step = 1
    counter = 0
    if fire_starter:
        counter += 14
    if fire_cloud:
        counter += 8
    if fire_scanner:
        counter += 12
    scan_obj.scan_complete = counter * domain_count
    scan_obj.core_module = core_module
    scan_obj.scan_step_name = "Starting..."
    scan_obj.scan_target = "Sorting..."

def stop_scan():
    global scan_obj
    scan_obj.scan_running = False
    scan_obj.scan_step = 0
    scan_obj.scan_complete = 0
    scan_obj.scan_step_name = "Not Running"
    scan_obj.core_module = "N/a"
    scan_obj.scan_target = "N/a"

def cancel_subprocesses():
    current_pid = os.getpid()
    all_processes = psutil.process_iter(attrs=['pid', 'ppid', 'cmdline'])
    for process in all_processes:
        pid = process.info['pid']
        ppid = process.info['ppid']
        cmdline = process.info['cmdline']
        if ppid == current_pid and pid != current_pid:
            print(f"Terminating subprocess {pid}: {' '.join(cmdline)}")
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print(f"Process {pid} not found.")

@app.get('/terminate-subprocesses')
async def terminate_subprocesses():
    try:
        cancel_subprocesses()
        return JSONResponse(status_code=200, content={'message': 'Subprocesses terminated successfully'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})

@app.get('/ping')
async def ping():
    return JSONResponse(status_code=200, content={"message": "pong!"})

@app.get('/status')
async def status():
    global scan_obj
    if scan_obj.scan_running:
        return JSONResponse(status_code=200, content={
            "scan_running": True,
            "scan_step": scan_obj.scan_step,
            "scan_complete": scan_obj.scan_complete,
            "scan_step_name": scan_obj.scan_step_name,
            "scan_target": scan_obj.scan_target,
            "core_module": scan_obj.core_module
        })
    else:
        return JSONResponse(status_code=200, content={
            "scan_running": False,
            "scan_step": scan_obj.scan_step,
            "scan_complete": scan_obj.scan_complete,
            "scan_step_name": scan_obj.scan_step_name,
            "scan_target": scan_obj.scan_target
        })

@app.post('/update-scan')
async def update_scan(request: Request):
    global scan_obj
    if scan_obj.scan_running:
        data = await request.json()
        scan_obj.scan_step += 1
        scan_obj.scan_step_name = data.get('stepName', scan_obj.scan_step_name)
        scan_obj.scan_target = data.get('target_domain', scan_obj.scan_target)
        return JSONResponse(status_code=200, content={
            "scan_running": scan_obj.scan_running,
            "scan_step": scan_obj.scan_step,
            "scan_step_name": scan_obj.scan_step_name,
            "target_domain": scan_obj.scan_target
        })
    else:
        return JSONResponse(status_code=400, content={"message": "ERROR: Scan Not Currently Running..."})

@app.get('/amass/status/{task_id}')
async def get_task_status(task_id: str):
    result = test_amass.AsyncResult(task_id)
    return JSONResponse(status_code=200, content={"status": str(result.state)})

@app.get('/amass')
async def amass(request: Request):
    print("testing Amass via celery worker...")
    domain = request.query_params.get("d")
    task = test_amass.apply_async(args=(domain,))
    return JSONResponse(status_code=200, content={"taskId": str(task.id)})
