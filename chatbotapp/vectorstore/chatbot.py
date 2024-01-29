from llama_index import SimpleDirectoryReader, StorageContext
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import TokenTextSplitter
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index.text_splitter import SentenceSplitter
from llama_index.extractors import TitleExtractor
from llama_index.vector_stores import PGVectorStore
from llama_index.ingestion import IngestionPipeline, IngestionCache
from llama_index.embeddings import OpenAIEmbedding
from llama_index import Document
from llama_index.memory import ChatMemoryBuffer
from llama_index.llms  import ChatMessage
import textwrap
import openai
import sys
import os
import json
from datetime import datetime, timedelta


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ChatBot:
    def __init__(self,connection): 
        self.vector_store  = PGVectorStore.from_params(
                                database=connection.db_name,
                                host=connection.db_host,
                                password=connection.db_password,
                                port=connection.db_port,
                                user=connection.db_user,
                                table_name="pgdata",
                                embed_dim=1536,  # openai embedding dimension
                            ) 
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=1536)
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.memory,
        )
      
    def insert_vector_data(self):
        try: 
            parent_directory = os.getcwd()
            data_folder_path = os.path.join(parent_directory, "data")

            print("PathPlay",)
            if not os.path.exists(data_folder_path):
                documents = SimpleDirectoryReader(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/data").load_data()
                print("CCCCCC",documents)

            else: 
                 documents = SimpleDirectoryReader(parent_directory+"/data").load_data()
          
            pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(chunk_size=500, chunk_overlap=50),
                    TitleExtractor(),
                    OpenAIEmbedding(),
                ],
                vector_store=self.vector_store,
            ),
            nodes = pipeline[0].run(documents=documents)
            if nodes: 
                print(nodes)
                return True
        except Exception as e: 
            print(f"Error inserting the documents: {e}")
            return False

    def insert_vector_scrap_data(self):
        try: 
            parent_directory = os.getcwd()
            data_folder_path = os.path.join(parent_directory, "datascrap")

            print("PathPlay",)
            if not os.path.exists(data_folder_path):
                documents = SimpleDirectoryReader(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/datascrap").load_data()
                print("CCCCCC",documents)

            else: 
                 documents = SimpleDirectoryReader(parent_directory+"/datascrap").load_data()
          
            pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(chunk_size=500, chunk_overlap=50),
                    TitleExtractor(),
                    OpenAIEmbedding(),
                ],
                vector_store=self.vector_store,
            ),
            nodes = pipeline[0].run(documents=documents)
            if nodes: 
                print(nodes)
                return True
        except Exception as e: 
            print(f"Error inserting the documents: {e}")
            return False
        
    def delete_expired_user_history(self,connect,userid): 
        try: 
            current_date = datetime.now()
            formatted_date = (current_date - timedelta(days=10)).strftime('%Y-%m-%d')
            connect.execute(f"delete  FROM chat_history where userid='{userid}' and date<='{formatted_date}'")
            print("records Successfully Deleted")
        except Exception as e:
            print(f"Error deleting the records: {e}")


    def fetch_user_history_for_memory(self,userid,connect):
        try: 
            connect.execute(f"SELECT * FROM chat_history where userid='{userid}' limit 100")
            results = connect.fetchall()
            memory = []
            self.memory.chat_history.clear()
            if len(results)>0:
                for row in results:
                    print("User History",row)
                    message_user = ChatMessage(role="user", content=row[2])
                    message_system = ChatMessage(role="assistant", content=row[3])
                    memory.append(message_user)
                    memory.append(message_system)
                self.memory.chat_history = memory
        except Exception as e:
            print("Error storing the memory of user") 

    def chat_response(self,query,connect,userid):
        try: 
            current_date = datetime.now()
            formatted_date = current_date.strftime("%y-%m-%d")
            print("Query",query)
            prompt = query+"\n Answer should come from our vector database first."
            response = self.chat_engine.chat(query)
            print(response)
            connect.execute('ALTER TABLE chat_history ALTER COLUMN question TYPE VARCHAR(4096), ALTER COLUMN answer TYPE VARCHAR(4096)')
            connect.execute('INSERT INTO chat_history(userid, question, answer) VALUES (%s, %s, %s)', (userid, query, response.response))
        except Exception as e:
            print(f"Error getting answers {e}") 
        return response.response

