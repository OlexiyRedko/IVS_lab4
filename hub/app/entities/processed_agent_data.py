from pydantic import BaseModel, model_validator
from app.entities.agent_data import AgentData


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

    # @model_validator(mode='before')
    # @classmethod
    # def proc_ag_data_valid(cls, data):
    #     if "agent_data" in data.keys():
    #             return data
    #     else:
    #         data["agent_data"]={'user_id':data["user_id"],'accelerometer':data["accelerometer"],'gps':data["gps"], 'timestamp':data["timestamp"]}
    #         if isinstance(data["parking"]["empty_count"], float):
    #             if data["parking"]["empty_count"]>=100:
    #                 data["road_state"]="good"
    #             else:
    #                 data["road_state"]="bad"
    #         elif isinstance(data["parking"]["empty_count"], str):
    #             data["road_state"]=data["parking"]["empty_count"]
    #         else:
    #             raise ValueError(
    #                 "Invalid road_state format. Expected float or string"
    #             )
    #         return data
            