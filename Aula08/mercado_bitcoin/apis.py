from abc import ABC, abstractmethod
import datetime
import os
import requests
import logging
from typing import List
import json
import time
import ratelimit
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from schedule import repeat, every, run_pending


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



class MercadoBitcoinApi(ABC):
    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"
    
    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass
    


    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls = 29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries = 10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint:{endpoint}")
        resposta =  requests.get(endpoint)
        resposta.raise_for_status()
        resposta = resposta.json()
        return resposta

#Metodo Day Summary
class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


#Metodo Trades
class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date:datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None ) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            if date_from > date_to:
                raise RuntimeError("Date_from cannot be greater than date_to")
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to   = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"
        return endpoint
