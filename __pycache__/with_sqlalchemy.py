from sqlalchemy import MetaData
from sqlalchemy import Integer, String, Column, Table, Date, ForeignKey
from sqlalchemy.orm import sessionmaker,  relationship
from sqlalchemy import  create_engine, select
from sqlalchemy.orm import declarative_base
from abc import ABC
from sqlalchemy.inspection import inspect
from params import *


db_name = 'sqlite:///vacation_expenses_db.sqlite3'

#custom logger for app
class CustomLogger():
    def __init__(self) -> None:
        self.uid = uuid.uuid4()
        self.logger = logging.getLogger(str(self.uid))
        self.logger.setLevel(logging.DEBUG)

        self.handler = logging.FileHandler(log_file_name, mode='a')
        formatter = logging.Formatter(log_format)

        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
    
    def write(self, message, level:str = 'debug') -> None:
        allowed_levels = ['debug', 'info', 'warning', 'error']
        if level in (allowed_levels):
            function = getattr(self.logger, level)
            function (f'{self.uid}: {message}')
            
    def close(self) -> None:
        self.logger.removeHandler(self.handler)

#declare db structure
Base = declarative_base()

class Vacation(Base):
    __tablename__ = 'vacations'
    id = Column(Integer, primary_key=True)
    date_start = Column(Date)
    date_end = Column(Date)
    description = Column(String)
    
    expence = relationship('Expenses', back_populates='vacation')
    
class Payer(Base):    
    __tablename__ = 'payers'
    id = Column(Integer, primary_key=True)
    payer_name = Column(String)
    
    expence = relationship('Expenses', back_populates='payer')
    
class ExpenseCategories(Base):    
    __tablename__ = 'expense_categories'
    id = Column(Integer, primary_key=True)
    expense_category_name = Column(String)   
    
    expence = relationship('Expenses', back_populates='expense_category')

class Expenses(Base):    
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    description = Column(String)   
    expense_category_id = Column(Integer, ForeignKey('expense_categories.id'))
    expense_date = Column(Date)
    payer_id = Column(Integer, ForeignKey('payers.id'))
    vacation_id = Column(Integer, ForeignKey('vacations.id'))
    
    payer = relationship('Payer', back_populates='expence')
    expense_category = relationship('ExpenseCategories', back_populates='expence')
    vacation = relationship('Vacation', back_populates='expence')

#classes for get lists of dictonary values
class DictonaryValues(ABC):        
    def get_list(self) -> list:
        engine = create_engine(db_name, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        all_values = session.query(self.table).all()
        return all_values
    
    @property
    def as_json(self):
        return json.dumps({'data' : self.get_list()}, ensure_ascii=False)
    
        
class VacationValues(DictonaryValues):
    def __init__(self):
        self.table = Vacation
        self.string_value_column = 'description'
    
    def get_list(self) -> list:
        all_values = super().get_list()
        result = ['{}, {} - {}'.format(x.description, x.date_start, x.date_end) for x in all_values]
        return result
    
#class for work with expenses items
class ExpenseValue():
    def __init__(self, **kwargs) -> None:
        self.log = CustomLogger()
        self.log.write(f'START creating object {type(self).__name__}', 'info')  
        self.log.write(f'FINISH creating object {type(self).__name__}', 'info')
    
    def __del__(self):
        self.log.write(f'object {type(self).__name__} destroyd', 'debug')
        self.log.close()              

engine = create_engine(db_name, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
expenses = session.query(Expenses).first()
print("payer:", expenses.payer.payer_name)
print("vacation:", expenses.vacation.description)
