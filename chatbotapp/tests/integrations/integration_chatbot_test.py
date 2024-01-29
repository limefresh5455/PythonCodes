import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from vectorstore.chatbot import ChatBot

# Replace 'your_module' with the actual name of the module where ChatBot is defined

@pytest.fixture
def mock_connection():
    db_user =  os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'testpassword')
    db_host = os.getenv('DB_HOST', '172.17.0.2')
    db_port = int(os.getenv('DB_PORT', '5432'))
    db_name = os.getenv('DB_NAME', 'postgres')
    return Mock(db_name=db_name, db_host=db_host, db_password=db_password,
                db_port=db_port, db_user=db_user)

@patch('llama_index.SimpleDirectoryReader.load_data')
@patch('llama_index.ingestion.IngestionPipeline.run')
@patch('llama_index.retrievers.VectorIndexRetriever')
@patch('llama_index.get_response_synthesizer')
@patch('llama_index.query_engine.RetrieverQueryEngine')
@pytest.mark.integration
def test_integration_functionality(mock_query_engine, mock_response_synthesizer, mock_retriever, mock_run, mock_load_data, mock_connection):
    mock_load_data.return_value = ["mock_document1", "mock_document2"]
    mock_run.return_value = ["mock_node1", "mock_node2"]
    mock_query_engine.return_value = Mock(response="mock_response")

    chatbot = ChatBot(mock_connection)

    # Integration test logic here
    result = chatbot.insert_vector_data()
    assert result is True

    response = chatbot.chat_response("mock_query")
    assert response