# The Cocktail Advisor Chat 🍸
A smart chatbot that helps you discover and explore cocktail recipes based on your preferences.

# Technologies 💻
- `Python` 
- `Pandas` 
- `Langchain` 
- `FAISS` 
- `Fast API` 
- `Streamlit` 
- `OpenAI API`

# OpenAI API Key 🔐
To interact with the GPT models, an API key from OpenAI is required. This key enables your application to authenticate requests to OpenAI's services, ensuring that usage is secure and measured.

**Acquiring an API Key**
1. Create an account at OpenAI.
2. Navigate to the API section and generate a new API key.
3. Once you have your key, you will use it in your environment file to authenticate API requests from your application.

**Setting Up Your API Key**

In the root of your project:
1. Create a `.env` file.
2. Add the following line: `REACT_APP_OPENAI_API_KEY='your-api-key-here'`.
3. This will allow your application to authenticate its requests to OpenAI.


# Running the Project 🚦
To run the project in your local environment, follow these steps:

1. To start the FastAPI backend, run the following command in your terminal:
`uvicorn main:app --host 127.0.0.1 --port 8000 --reload`
2. Once the backend is running, open a new terminal window and start the Streamlit frontend:
`streamlit run streamlit_app.py`

### Usage:
1. Open your browser and go to `http://127.0.0.1:8000/docs` to access the FastAPI Swagger UI.
2. Open your browser and go to `http://localhost:8501` to view the Streamlit app.

### Example Requests:
- What are the 5 cocktails containing lemon?
- What are the 5 non-alcoholic cocktails containing sugar? 
- What are my favourite ingredients? 
- Recommend 5 cocktails that contain my favourite ingredients 
- Recommend a cocktail similar to “Hot Creamy Bush” 
- My favourite ingredients are lemon, mint, and honey. Can you suggest cocktails based on these?

# Summary

# Demo 📸
