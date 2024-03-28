from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData
import logging
import json


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    # Implement it
    data={}
    data["agent_data"]={'accelerometer':agent_data.accelerometer,'gps':agent_data.gps, 'timestamp':agent_data.timestamp, 'user_id':agent_data.user_id}
    if isinstance(agent_data.accelerometer.z, float):
        if agent_data.accelerometer.z<10000:
            data["road_state"] ="pit"
        else:
            data["road_state"] = "good"
    else:
        raise ValueError(
            "Invalid accelerometer format. Expected float or string"
        )
    return ProcessedAgentData.model_validate(data )   
