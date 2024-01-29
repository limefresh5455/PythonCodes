
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'testpassword')

class DBConnection:
    def __init__(self,connection=None): 
        self.db_user =  os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', 'testpassword')
        self.db_host = os.getenv('DB_HOST', '172.17.0.2')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'postgres')
        self.connection = connection
        self.cursor = None
    def connect_db(self): 
        try: 
            self.connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
            if self.cursor: 
                try: 
                    self.cursor.execute("CREATE EXTENSION vector")
                    self.cursor.execute("CREATE TABLE IF NOT EXISTS pgdata (id SERIAL PRIMARY KEY, data_vector vector);")                
                    self.cursor.execute("CREATE TABLE IF NOT EXISTS chat_history(id SERIAL PRIMARY KEY,userid varchar(255),question varchar(255),answer varchar(255),date DATE)")
                except: 
                    print("Extension Already exists")
        except Exception as e:
            print(f"Error connecting to the database: {e}") 
            raise e 
        return self.cursor

       

