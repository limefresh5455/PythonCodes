## PG Vector Db Loading

To Load Image of pgVector, run the command `docker pull anakane/pgvector` to connect with pgvector run this command `sudo docker run -d   --name mypos    -p 5432:5432   -e POSTGRES_PASSWORD=testpassword   ankane/pgvector`, check the container host address `docker container inspect containerID` and use ip address in the DATABASE_URL in place of example ip 172.17.0.3

Set the Environment Variables.
DATABASE_URL
postgresql://postgres:testpassword@172.17.0.3:5432/postgres
ip should be the ip of docker container and details from VectorStore.py file

OPENAI_API_KEY
set API key as OPENAI_API_KEY in env
#6d93bc44e840d605014d113212910290fa6ca2d60fc539272b986d321b80f552
COLLECTION_NAME
set the table name as COLLECTION_NAME in env

cd in to project folder and also change the ip address in vectorStore.py file as well like the Environment variable

run the following command to insert the collection name and vector extention.
python3 vectorStore.py

after creating a vector extension using above command
run the following command to run project
uvicorn app:app --reload --port 8001

the project will run on port
http://127.0.0.1:8001/

To store the documents in vector Data put the documents txt files in documents folder and visit the following route
http://127.0.0.1:8001//kintsugi-platform-vector

the documents will store in pgvector and we can ask questions in chatbot running on
http://127.0.0.1:8001/


