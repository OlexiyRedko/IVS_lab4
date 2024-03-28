import asyncio
import json
from typing import Set, Dict, List, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.orm import registry
from datetime import datetime
from pydantic import BaseModel, field_validator
from config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)

# FastAPI app setup
app = FastAPI()
# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("user_id", Integer),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
)

class PracessedAgentDataToPost:
    pass
mapper_registry = registry()
mapper_registry.map_imperatively(PracessedAgentDataToPost, processed_agent_data)

SessionLocal = sessionmaker(bind=engine)
metadata.create_all(bind=engine)


# SQLAlchemy model
class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str
    user_id: int
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime


# FastAPI models
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData


# WebSocket subscriptions
subscriptions: Dict[int, Set[WebSocket]] = {}


# FastAPI WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in subscriptions:
        subscriptions[user_id] = set()
    subscriptions[user_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions[user_id].remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(user_id: int, data):
    if user_id in subscriptions:
        for websocket in subscriptions[user_id]:
            await websocket.send_json(json.dumps(data))


# FastAPI CRUDL endpoints


@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    # Insert data to database
    # Send data to subscribers
    for data_inst in data:
        with SessionLocal() as session:
            currdata = PracessedAgentDataToPost(
                road_state = data_inst.road_state,
                user_id = data_inst.agent_data.user_id,
                x = data_inst.agent_data.accelerometer.x,
                y = data_inst.agent_data.accelerometer.y,
                z = data_inst.agent_data.accelerometer.z,
                latitude = data_inst.agent_data.gps.latitude,
                longitude = data_inst.agent_data.gps.longitude,
                timestamp = data_inst.agent_data.timestamp
            )
            session.add(currdata)
            session.commit()
        


@app.get(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def read_processed_agent_data(processed_agent_data_id: int):
    # Get data by id
    with SessionLocal() as session:
        RecivedAgentData = session.get(PracessedAgentDataToPost, processed_agent_data_id)
        return RecivedAgentData


@app.get("/processed_agent_data/", response_model=list[ProcessedAgentDataInDB])
def list_processed_agent_data():
    # Get list of data
    with SessionLocal() as session:
        statement = select(PracessedAgentDataToPost)
        RecivedAgentData = session.scalars(statement).all()
        return RecivedAgentData
    


@app.put(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    # Update data
    with SessionLocal() as session:
        RecivedAgentData = session.execute(select(PracessedAgentDataToPost).filter_by(id=processed_agent_data_id)).scalar_one()
        RecivedAgentData.road_state = data.road_state
        RecivedAgentData.user_id = data.agent_data.user_id
        RecivedAgentData.x = data.agent_data.accelerometer.x
        RecivedAgentData.y = data.agent_data.accelerometer.y
        RecivedAgentData.z = data.agent_data.accelerometer.z
        RecivedAgentData.latitude = data.agent_data.gps.latitude
        RecivedAgentData.longitude = data.agent_data.gps.longitude
        RecivedAgentData.timestamp = data.agent_data.timestamp
        session.commit()
        RecivedAgentData = session.execute(select(PracessedAgentDataToPost).filter_by(id=processed_agent_data_id)).scalar_one()
        return RecivedAgentData




@app.delete(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB,
)
def delete_processed_agent_data(processed_agent_data_id: int):
    # Delete by id
    with SessionLocal() as session:
        RecivedAgentData = session.execute(select(PracessedAgentDataToPost).filter_by(id=processed_agent_data_id)).scalar_one()
        session.delete(RecivedAgentData)
        session.commit()
        return RecivedAgentData

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
