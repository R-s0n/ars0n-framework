from celery import Celery
import subprocess

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379"
)

@celery_app.task
def test_scan():
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    subprocess.run(["sleep 10"], shell=True)
    print("running...")
    return "Task complete"

@celery_app.task
def test_amass():
    subprocess.run([f"python3 toolkit/fire-starter.py -S backend -P 8000 -d floqast.app"], shell=True)
    return "Amass Scan Complete"

@celery_app.task
def test_wildfire(command):
    subprocess.run([command], shell=True)
    return "Wildfire Scan Complete"