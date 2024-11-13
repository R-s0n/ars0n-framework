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

@app.get('/debug')
async def amass(request: Request):
    # flags = request.query_params.get("flags")
    # domain = request.query_params.get("domain")
    # print(domain)
    # print(flags)
    # subprocess.run([f"python3 toolkit/fire-starter.py -S backend -P 8000 -d {domain} {flags}"], shell=True)
    print("testing celery worker...")
    task = test_scan.apply_async()
    return JSONResponse(status_code=200, content={"taskId": str(task.id)})

@app.get('/debug/amass')
async def amass(request: Request):
    print("testing Amass via celery worker...")
    task = test_amass.apply_async()
    return JSONResponse(status_code=200, content={"taskId": str(task.id)})

@app.get('/debug/status/{task_id}')
async def get_task_status(task_id: str):
    result = test_scan.AsyncResult(task_id)
    return JSONResponse(status_code=200, content={"status": str(result.state)})

@app.post('/wildfire')
async def wildfire(request: Request):
    global scan_obj
    if not scan_obj.scan_running:
        data = await request.json()
        fire_starter = data.get('fireStarter')
        fire_cloud = data.get('fireCloud')
        fire_scanner = data.get('fireScanner')
        fqdn = data.get('fqdn', '')
        scan_single_domain = data.get('scanSingleDomain', False)
        domain_count = data.get('domainCount', 1)
        start_flag = " --start" if fire_starter else ""
        cloud_flag = " --cloud" if fire_cloud else ""
        scan_flag = " --scan" if fire_scanner else ""
        fqdn_flag = f" --fqdn {fqdn}" if scan_single_domain else ""
        scanSingle_flag = " --scanSingle" if scan_single_domain else ""
        scan_obj.core_module = "Wildfire.py"
        start_scan(fire_starter, fire_cloud, fire_scanner, domain_count, scan_obj.core_module)
        command = f"python3 wildfire.py{start_flag}{cloud_flag}{scan_flag}{fqdn_flag}{scanSingle_flag} -S backend"
        task = test_wildfire.apply_async(args=(command,))
        stop_scan()
        return JSONResponse(status_code=200, content={"taskId": str(task.id)})
    else:
        return JSONResponse(status_code=400, content={"message": "ERROR: Scan Running..."})

@app.post('/collect_screenshots')
async def collect_screenshots():
    subprocess.run(["python3 wildfire.py --screenshots"], shell=True)
    return JSONResponse(status_code=200, content={"message": "Done!"})