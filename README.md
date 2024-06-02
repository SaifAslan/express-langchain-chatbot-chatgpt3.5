# Express Chatbot

This project is a chatbot that uses the LangChain library to generate responses to user queries. It uses the Pinecone vector store to retrieve relevant documents and the OpenAI embeddings model to convert documents to vectors.

## Requirements

* Python 3.12
* LangChain
* BeautifulSoup4
* Black
* OpenAI
* Pinecone-client
* Unstructured
* NLTK
* FastAPI
* Jinja2
* Uvicorn
* Streamlit
* Streamlit-chat
* TQDM
* LangChain-Pinecone
* LangChain-Community
* LangChain-OpenAI

## Installation

To install the required packages, run the following command:
pipenv install

## Usage

To run the chatbot, run the following command:
pipenv shell
streamlit run frontend.py

This will start the Streamlit app, and you can interact with the chatbot by entering your queries in the text input field.

## Tests

To run the tests, run the following command:
pipenv shell
python -m unittest tests/test_document_loader.py

This will run the tests for the document loader.

## Environment Variables

The following environment variables are required:

* `OPENAI_API_KEY` = OpenAI API key
* `INDEX_NAME` = Pinecone index name
* `INDEX_HOST`= Pinecone index host
* `PINECONE_API_KEY`= Pinecone API key
* `PINECONE_ENVIROMENT_REGION`= Pinecone host region

You can set these environment variables in a `.env` file or by using the `dotenv` library.

## License

This project is licensed under the MIT License.