from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import logic
from database import engine



# DBMS: This command tells the engine to create the tables 
# defined in your models.py if they don't exist.
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="SentinelCloud API")

# Alert System Instance (DSA: Queue)
alert_manager = logic.AlertManager()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SentinelCloud is Active", "status": "Secure"}

# REST API: HTTP POST (Creating data)
@app.post("/servers/")
def create_server(hostname: str, ip: str, db: Session = Depends(get_db)):
    # Logic: Sanitizing inputs
    clean_ip = logic.format_ip_safely(ip)
    new_server = models.Server(hostname=hostname, ip_address=clean_ip)
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

# REST API: HTTP GET (Retrieving data)
@app.get("/alerts/next")
def get_alert():
    # DSA: Pop from Queue logic
    return {"alert": alert_manager.get_next_alert()}

# REST API: POST Metric (The 'Heartbeat' endpoint)
@app.post("/metrics/{server_id}")
def add_metric(server_id: int, cpu: float, ram: float, db: Session = Depends(get_db)):
    # 1. Store in DBMS
    new_metric = models.Metric(server_id=server_id, cpu_usage=cpu, ram_usage=ram)
    db.add(new_metric)
    db.commit()
    
    # 2. Check for alerts (Programming Logic + DSA)
    server = db.query(models.Server).filter(models.Server.id == server_id).first()
    if server:
        alert_manager.trigger_alert(server.hostname, cpu)
    
    return {"status": "Metric Logged"}