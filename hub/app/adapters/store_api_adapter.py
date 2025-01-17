import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        logging.info("size of data "+ str(len(processed_agent_data_batch)))
        for i in processed_agent_data_batch:
            logging.info(i)
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        # Implement it
        data = [json.loads(item.json()) for item in processed_agent_data_batch]

        responce = requests.post(f"{self.api_base_url}/processed_agent_data", json=data)
        return responce.status_code == requests.codes.ok
