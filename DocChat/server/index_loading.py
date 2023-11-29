import flask
from flask import jsonify
from llama_index import GPTSimpleVectorIndex, MockLLMPredictor, MockEmbedding, ServiceContext
import os

def run_mock(question, indexFilePath):

    index = GPTSimpleVectorIndex.load_from_disk(indexFilePath)
    llm_predictor = MockLLMPredictor(max_tokens=256)
    embed_model = MockEmbedding(embed_dim=1536)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, embed_model=embed_model)
    """
    response = index.query(
        question,
        service_context=service_context,
        mode="embedding"
    )
    """
    response = index.query(
        question,
        service_context=service_context,
        mode="default"
    )

    response = flask.make_response('ran a mock query to count tokens or debug. question was: ' + question)
    response.status_code = 200
    return response

def run(question, indexFilePath):

    if os.path.exists(indexFilePath):
        index = GPTSimpleVectorIndex.load_from_disk(indexFilePath)
        # !!!!! API CALL HAPPENS HERE (index.query) CAREFUL.
        #responseEmbeddings = index.query(question, mode="embedding")
        responseDefault = index.query(question, mode="default")
        print('here')

        return flask.make_response(jsonify(responseDefault), 200)


def load_and_query(question, indexFilePath, environment):

    if environment.mock:
        run_mock(question, indexFilePath)
    else:
        run(question, indexFilePath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    environment = {'mock' : True}
    load_and_query("what commitments have organizations made to help with recycling efforts?", "results/index.json", environment)
    #a = str(sys.argv[1])
    #b = str(sys.argv[2])
    #main(a,b)

