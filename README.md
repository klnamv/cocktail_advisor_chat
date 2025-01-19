# The Cocktail Advisor Chat 🍸
A smart chatbot that helps you discover and explore cocktail recipes based on your preferences.


<img width="1800" alt="image" src="https://github.com/user-attachments/assets/a6752cf2-9c62-4cf4-9e2e-2f7fe00fe70d" />

# Technologies 💻
- `Python` 
- `Pandas` 
- `Langchain` 
- `FAISS` 
- `Fast API` 
- `Streamlit` 
- `OpenAI API`
- `Docker`

# OpenAI API Key 🔐
To interact with the GPT models, an API key from OpenAI is required. This key enables your application to authenticate requests to OpenAI's services, ensuring that usage is secure and measured.

**Acquiring an API Key**
1. Create an account at OpenAI.
2. Navigate to the API section and generate a new API key.
3. Once you have your key, you will use it in your environment file to authenticate API requests from your application.

**Setting Up Your API Key**

In the root of your project:
1. Create a `.env` file.
2. Add the following line: `OPENAI_API_KEY=your-api-key-here`.

# Running the Project 🚦
To run the project in your local environment, follow these steps:

1. Run `Docker`
2. In terminal run `docker build -t my-streamlit-fastapi-app . `
3. And the final `docker run -p 8000:8000 -p 8501:8501 --env-file .env my-streamlit-fastapi-app`
4. This will run UI on [http://0.0.0.0:8501/](http://0.0.0.0:8501/) and API on [http://0.0.0.0:8000/](http://0.0.0.0:8000/docs)

### Example Requests:
- What are the 5 cocktails containing lemon?
- What are the 5 non-alcoholic cocktails containing sugar? 
- What are my favourite ingredients? 
- Recommend 5 cocktails that contain my favourite ingredients 
- Recommend a cocktail similar to “Hot Creamy Bush” 
- My favourite ingredients are lemon, mint, and honey. Can you suggest cocktails based on these?

# Problems - solutions 🐛
**Problem:** Model couldn't filter on multiple columns, because it had 5 different tools for each column.

*Solution: created one tool that could filter on any column (even multiple at once) instead of 5 different tools* ✅<br />

<br />

**Problem:** The model didn't want to save information to memory about the user's preferences.

*Solution: stricter system prompt, created `update_memory` to save all user preferences* ✅

<br />

**Problem:** The model incorrectly filtered the search by ingredient, pretending that such an ingredient did not exist.

*Solution: change approach for filtering ingredients and more examples for model on how to filter on this column* ✅

<br />

**Problem:** The model invented new cocktail recipes and photos of which did not exist when she could not find the necessary information.

*Solution: add guidance in system prompt for model to use only information from knowledge base using existing tools* ✅

<br />

**Problem:** Sometimes the whole dataset can be returned after filtering, causing model for token input/output exceed.

*Solution:  add limit on the number of returned strings to the server function at the end* 💡

  

# Summary



# Demo 📸

[demo](https://github.com/user-attachments/assets/fee34b25-fd7f-435a-9e84-e517329214a3)


