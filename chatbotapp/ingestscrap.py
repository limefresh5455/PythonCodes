from vectorstore.chatbot import ChatBot
from db.connection import DBConnection

class VStore(ChatBot): 
    def __init__(self): 
        self.connection =  DBConnection(connection=False)
        super().__init__(self.connection)

    def store_vectors(self):
        is_connection = self.connection.connect_db()
        if is_connection: 
            self.insert_vector_scrap_data()
        
if __name__ == '__main__': 
    vstore  = VStore()
    vstore.store_vectors()