import sqlite3
import os

class Database:
  def __init__(self):
    self.database_name = "QRCodes.db"
    self.table_name = "QRCodes"

    if not os.path.exists(self.database_name):
        self.create_database(self.database_name)
        self.create_table(self.database_name, self.table_name)

  def create_database(self, database_name):
    self.conn = sqlite3.connect(database_name)
  
  def create_table(self,database_name, table_name):
    self.conn = sqlite3.connect(database_name)
    self.cursor = self.conn.cursor()
    try:
      self.cursor.execute("CREATE TABLE "+ table_name+" (Filename VARCHAR(255), Details VARCHAR(255), Time VARCHAR(255))")
      self.conn.commit()
    except:
      self.conn.rollback()
    finally:
      self.conn.close()
  
  def insert_data(self, filename, details, time):
    self.conn = sqlite3.connect(self.database_name)
    self.cursor = self.conn.cursor()
    self.cursor.execute("INSERT INTO "+ self.table_name+" (Filename, Details, Time) VALUES (?,?,?)",(filename, details, time))
    self.conn.commit()
    self.conn.close()

    #print(self.get_data())
  def get_data(self):
    self.conn = sqlite3.connect(self.database_name)
    self.cursor = self.conn.cursor()
    self.cursor.execute("SELECT * FROM "+self.table_name)
    result = self.cursor.fetchall()
    
    self.conn.commit()
    self.conn.close()
    
    return result




