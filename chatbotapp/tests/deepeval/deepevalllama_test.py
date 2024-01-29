from llama_index.response.schema import Response
from typing import List
from llama_index.schema import Document
from deepeval.metrics import HallucinationMetric
from llama_index import download_loader
from llama_index.vector_stores import PGVectorStore
from llama_index.query_engine import RetrieverQueryEngine
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index import get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index import  StorageContext
from llama_index.evaluation import ResponseEvaluator
import os
class HallucinationResponseEvaluator:
    def get_context(self, response: Response) -> List[Document]:
        """Get context information from given Response object using source nodes.

        Args:
            response (Response): Response object from an index based on the query.

        Returns:
            List of Documents of source nodes information as context information.
        """
        context = []

        for context_info in response.source_nodes:
            context.append(Document(text=context_info.node.get_content()))

        return context

    def evaluate(self, response: Response) -> str:

        # Evaluate factual consistency metrics
        answer = str(response)
        metric = HallucinationMetric()
        context = self.get_context(response)
        context = " ".join([d.text for d in context])
        test_case = LLMTestCase(input="This is an example input", context=context, actual_output=answer)
        score = metric.measure(test_case=test_case)
        if metric.is_successful():
            return "YES"
        else:
            return "NO"
        
db_user =  os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'testpassword')
db_host = os.getenv('DB_HOST', '172.17.0.2')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'postgres')
evaluator = HallucinationResponseEvaluator()

vector_store  = PGVectorStore.from_params(
                                database=db_name,
                                host=db_host,
                                password=db_password,
                                port=db_port,
                                user=db_user,
                                table_name="pgdata",
                                embed_dim=1536,  # openai embedding dimension
                            )
storage_context = StorageContext.from_defaults(vector_store=vector_store)
evaluator_gpt4 = ResponseEvaluator(service_context=storage_context)
print("Evolution GPT:",evaluator_gpt4)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=3,
        )
        # configure response synthesizer
response_synthesizer = get_response_synthesizer()
# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

query = "What is the minimum sales tax in Texas in 2023"
response = query_engine.query(query)
print("Query Response",response)
eval_result = evaluator.evaluate(response)
print("Response Evolution: ",eval_result)