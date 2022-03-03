#imports
from abc import ABC, abstractmethod
import datetime
import os
import requests
import logging
from typing import List
import json
import time

from mercado_bitcoin.apis import DaySummaryApi, TradesApi
from mercado_bitcoin.writers import DataWriter


from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from schedule import repeat, every, run_pending




#Ingestor
class DataIngestor(ABC):
    def __init__(self, writer,  coins: List[str], default_start_date: datetime.date) -> None: 
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()
        #super().__init__()
    
    @property
    def _filename_checkpoint(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._filename_checkpoint, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._filename_checkpoint, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.default_start_date

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()


    @abstractmethod
    def ingest(self, **kwargs) -> None:
        pass

class DaysummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        date =  self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))



