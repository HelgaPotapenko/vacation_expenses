#this module contains global parameters for application

import logging
from datetime import datetime, date
import json
import uuid
import sqlite3
from typing import List, TypeVar
from abc import ABC
from dataclasses import dataclass

__all__ = ['db_name', 'log_file_name', 'log_format', 'logging', 
           'datetime', 'date', 
           'sqlite3', 
           'uuid', 
           'ABC', 
           'dataclass', 
           'TypeVar']

db_name = 'vacation_expenses_db.sqlite3'

log_file_name = f'{date.today()}.log'
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
