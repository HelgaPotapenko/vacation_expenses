from params import *

#custom logger for app
class CustomLogger():
    def __init__(self) -> None:
        self.uid = uuid.uuid4()
        self.logger = logging.getLogger(__name__)
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

#DB processing

class SQLiteDBTool():
    def __init__(self, db_name: str)-> None : 
        self.db = db_name
        
    def sql_modify_data (self, sql_rq_text) -> None:
        try:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;') 
            cursor.execute(sql_rq_text)
            connection.commit() 
        except Exception as e:
            raise e
        finally:
            connection.close()
        return result
    
    def sql_get_data(self, sql_rq_text) -> None:
        data = []
        error_msg = 0
        state = 0
        try:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            rows = cursor.execute(sql_rq_text).fetchall()
            for row in rows:
                data.append(dict(zip([column[0] for column in cursor.description], row)))       
        except Exception as e:
            raise e
        finally:
            connection.close()    
        return data

#classes for dictonary values

class DictonaryValue(ABC):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.descr = kwargs.get('descr')
        
        self.id_column_name = 'id'
        self.db_dictonary_table_name = ''
        self.db_descr_column_name = ''
        
        self.log = kwargs.get('log')
        self.log.write(f'object {type(self).__name__} "{self.descr}" created', 'debug')
        
    @property
    def as_dict(self) -> dict:
        return {'id': self.id, 'descr': self.descr}
        
        
    @property
    def get_enrich_sql(self) -> str:
        return """select {} from {}  where {} = '{}'""".format(self.id_column_name,
                                                  self.db_dictonary_table_name,
                                                  self.db_descr_column_name,
                                                  self.descr
                                                   )

    def enrich(self):
        if self.id is None:
            self.log.write(self.get_enrich_sql, 'debug')
            db_tool = SQLiteDBTool(db_name)
            db_tool = SQLiteDBTool(db_name)
            sql_rq = self.get_enrich_sql
            result = db_tool.sql_get_data(sql_rq)
            if len(result) == 0:
                raise RuntimeError(f'{sql_rq} returned 0 records')
            else:
                self.id = result[0].get(self.id_column_name)
                self.log.write(f'object {type(self).__name__} enriched', 'debug')
    
        
class PayerValue(DictonaryValue):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_dictonary_table_name = 'payers'
        self.db_descr_column_name = 'payer_name'
        
        self.enrich()
        
        
class ExpenseCategoryValue(DictonaryValue):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_dictonary_table_name = 'expense_categories'
        self.db_descr_column_name = 'expense_category_name'
        
        self.enrich()

class VacationValue(DictonaryValue):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_dictonary_table_name = 'vacations'
        self.db_descr_column_name = 'description'
        
        self.enrich()


class ExpenseItem():
    @dataclass
    class ExpenseItemData:
        id: str = ''
        expense_date: str = ''
        description: str = ''
        vacation: VacationValue = None
        expense_category: ExpenseCategoryValue = None
        payer: PayerValue = None
            
        @property    
        def as_dict(self):
            result = self.__dict__.copy()
            result['vacation'] =self.vacation.as_dict
            result['expense_category'] = self.expense_category.as_dict
            result['payer'] = self.payer.as_dict
            print (result)
            return result
    
    def __init__(self, **kwargs) -> None:
        self.log = CustomLogger()
        self.log.write(f'START creating object {type(self).__name__}', 'info')
        try:
            params = {}
            params['id'] = kwargs.get('id')
            params['description'] = kwargs.get('description')
            params['expense_date'] = kwargs.get('expense_date')
            params['vacation'] = VacationValue(descr = kwargs.get('vacation'), log=self.log)
            params['expense_category'] = ExpenseCategoryValue(descr = kwargs.get('expense_category'), log=self.log)
            params['payer'] = PayerValue(descr = kwargs.get('payer'), log=self.log)
            self.data = self.ExpenseItemData(**params)
            self.log.write(f'object {type(self).__name__} "" created', 'debug')
            self.log.write(str(self.as_dict), 'debug')
            self.log.write(f'FINISH creating object {type(self).__name__}', 'info')
        except Exception as e:
            self.log.write(e, 'error')
            self.log.write(f'FINISH creating object {type(self).__name__}', 'info')
            self.log.close()
        #self.log.close()
    
    @property    
    def as_dict(self):  
        return self.data.as_dict
            
    def __del__(self):
        self.log.write(f'object {type(self).__name__} destroyd', 'debug')
        self.log.close()    


