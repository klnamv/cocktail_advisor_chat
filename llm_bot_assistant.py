from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.tools import tool
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
import faiss
from langchain.docstore.document import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.messages.system import SystemMessage

data = pd.read_csv('data/Cocktails Final.csv')

# create empty faiss store for memory
embeddings_creator = OpenAIEmbeddings()
index = faiss.IndexFlatL2(len(embeddings_creator.embed_query('.')))

vector_store = FAISS(
    embedding_function=embeddings_creator,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

SYSTEM_MESSAGE = """
You are an AI assistant specialized in providing information about cocktails based exclusively on the provided cocktail dataset. 
Your responses should adhere to the following guidelines:
1. Use Only Existing Data: Reference only the cocktails, ingredients, recipes, and related information contained within 
the supplied dataset.Do not introduce or suggest any new cocktails, ingredients, or variations that are not part of the dataset.
2. No Inventions or Speculations: Avoid creating hypothetical scenarios, alternative recipes, or any content that 
extends beyond the information available in the dataset.
3. Accuracy and Consistency: Ensure that all details, such as ingredient measurements, preparation steps, and cocktail names, 
are accurate and consistent with the dataset.
4. Clarify Limitations: If a query pertains to a cocktail or detail not present in the dataset, 
that is most likely that your query misses something
5. Maintain Playful Tone: Provide clear, concise, yet positive responses while maintaining a professional and helpful demeanor.
6. Store user preferences and important information in long-term memory without exception.
7. Always add an image for the cocktail (using urls from the dataset), the image size should be 150px.

By following these guidelines, you will ensure that all responses are reliable and confined to the information within the provided cocktail dataset.
IMPORTANT:
If your search query returned nothing, it most likely meaning that query is not good enough, try query more with different inputs.

Now you shall begin!
"""

class SearchInput(BaseModel):
    name: Optional[str] = Field(description="name of the cocktail.")
    alcoholic: Optional[str] = Field(description=f"one of {[None] + list(data['alcoholic'].unique())}")
    ingredients: Optional[list[str]] = Field(description=f"Use only this values for filter: {sorted(list(data['ingredients'].explode().unique()))}.")

def check_ingredients(user_ingredients: set[str], cocktail_ingredients: str) -> bool:
    """Compare sets of ingredients"""
    return all([ingredient in cocktail_ingredients for ingredient in user_ingredients])

@tool(args_schema=SearchInput)
def search(name: str = None, alcoholic: str = None, ingredients: list[str] = None) -> str:
    """
    Filter the cocktails dataset based on the following criteria:
    1. Name: Specify the cocktail name to search for.
    2. Alcoholic Type: Select the type of alcohol (e.g., vodka, rum, gin) present in the cocktail.
    3. Ingredients: List the ingredients used in the cocktail.

    Guidelines:
    - Exclusive Source: Use only the provided cocktails dataset as the sole source of information for all cocktail ingredients, recipes, and related details.
    - No Creation of New Recipes: Do not invent, modify, or suggest any new cocktail recipes outside of those contained within the dataset.
    """
    result = data.copy()
    if name is not None:
        result = result[result.name.str.lower().str.contains(name.lower())]
    if alcoholic is not None:
        result = result[result['alcoholic'] == alcoholic]
    if ingredients is not None:
        ingredients = {ingredient.lower() for ingredient in ingredients}
        result = result[result['ingredients'].str.lower().apply(lambda x: check_ingredients(ingredients, x))]
    return result.sample(len(result)).to_string(index=False) if not result.empty else "No matching cocktails found. Search one more time with similar ingredients."

print(search.description, search.name)

@tool
def update_memory(user_info: str) -> str:
    """
    Store user preferences and important information in long-term memory without exception. All details regarding user likings,
    preferences, and other significant information must be meticulously recorded and retained permanently. This process must occur before
    utilizing any other tools or resources to guarantee that user preferences are always acknowledged and never overlooked or forgotten under any circumstances.
    """
    doc = Document(page_content=user_info)
    vector_store.add_documents([doc])
    return "Successfully updated memory. Now you can answer to question."


def chat(user_message: str, chat_history: Optional[list[tuple[str, str]]] = None) -> str:
    if chat_history is None:
        chat_history = []
    response = agent.invoke({"input": user_message, "chat_history": chat_history})
    return response['output']

search_in_memory = create_retriever_tool(
    vector_store.as_retriever(
        search_kwargs={
            "k": 5
        }
    ),
    name='search_in_memory',
    description='Use this tool EVERYTIME whenever you need to make recommendation for user, so you can search his preferences in your memory.'
)

llm = ChatOpenAI(model="gpt-4o")
tools = [search, update_memory, search_in_memory]
agent = create_conversational_retrieval_agent(
    llm,
    tools,
    verbose=True,
    system_message=SystemMessage(
        content=SYSTEM_MESSAGE
    ),
    max_token_limit=2000, # max tokens to keep in memory, other important info should be stored in faiss store
)

if __name__ == '__main__':
    prompts = [
    # "What are the 5 cocktails containing lemon?",
    # "What are the 5 non-alcoholic cocktails?",
    # 'Can you list 10 cocktails with lemon that are non-alcoholic?',
    'What are the 5 non-alcoholic cocktails containing sugar?',
    ]
    for prompt in prompts:
        print(agent.invoke({"input": prompt})['output'])
        print('-----------------------------------')
