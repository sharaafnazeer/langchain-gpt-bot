# **LangChain - ChatGPT - WhatsApp - BOT**

This project includes a minimal solution to ask questions on a document which is submitted to the platform.

## **Build Dependencies**

- [LangChain](https://docs.langchain.com/)
- [PineCone](https://www.pinecone.io/)
- [GreenAPI](https://green-api.com/en/)
- [Python3.9](https://www.python.org/downloads/release/python-390/)
- Code Editor/IDE

## **Installation and Setup**

Follow these steps to install and run the project:

- Clone the repository or download the repository as a zip file
- Create a OpenAPI account and copy the credentials
- Create a PineCone account and copy the credentials
- Create a GreenAPI account with a WhatsApp number and copy relevant credentials - This number will act as a BOT
- Create a **.env** file based on **.env.example** and update your credentials. You can provide any **APP_SECRET**
- Install the dependencies using the following command
    ```
    pip install -r requirements.txt
    ```
- Start the server using the following command
    ```
    python main.py
    ```
- Start the webhook using the following command
    ```
    python webhook.py
    ``` 
  
## **Generate Vectors to PineCone**
- Place the PDF documents inside the **docs** folder
- Execute the generate API - http://localhost:5000/generate
  - This will read your PDF document and upload it as a vector on the relevant PineCone instance
- Start asking questions from the BOT about the document

