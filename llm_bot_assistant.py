from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.tools import tool
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional

data = pd.read_csv('data/Cocktails Final.csv')
data['ingredients'] = data['ingredients'].str.strip("[]").str.replace("'", "").str.split(', ')

class SearchInput(BaseModel):
    name: Optional[str] = Field(description="name of the cocktail.")
    alcoholic: Optional[str] = Field(description=f"one of {list(data['alcoholic'].unique())}")
    # category: Optional[str] = Field(description=f"one of {list(data['category'].unique())}")
    ingredients: Optional[list[str]] = Field(description=f"list with one of {list(data['ingredients'].explode().unique())}")

@tool
def search_by_name(name: str) -> str:
    """Search for cocktails by their name."""
    result = data[data['name'].str.contains(name, case=False, na=False)]
    return result.to_string(index=False) if not result.empty else "No matching cocktails found."

@tool
def search_by_alcoholic(alcohol_type: str) -> str:
    """Search for alcoholic or non-alcoholic cocktails. Accepts 'alcoholic' or 'non alcoholic' as input."""
    alcohol_type = alcohol_type.lower()
    filter_value = 'Alcoholic' if alcohol_type == 'alcoholic' else 'Non alcoholic'
    result = data[data['alcoholic'].str.lower() == filter_value.lower()]
    return result.to_string(index=False) if not result.empty else "No matching cocktails found."

@tool
def search_by_category(category: str) -> str:
    """Search for cocktails by category, such as 'Cocktail' or 'Shot'."""
    result = data[data['category'].str.contains(category, case=False, na=False)]
    return result.to_string(index=False) if not result.empty else "No matching cocktails found."

@tool
def search_by_ingredient(ingredient: str) -> str:
    """Find cocktails containing a specific ingredient, such as 'lemon' or 'sugar'."""
    result = data[data['ingredients'].str.contains(ingredient, case=False, na=False)]
    return result.to_string(index=False) if not result.empty else "No matching cocktails found."

description = f"""
    Filter cocktails dataset by name, alcoholic type, category and ingredients.
    :param name:
    :param alcoholic: one of {list(data['alcoholic'].unique())}
    :param category: one of {list(data['category'].unique())}
    :param ingredients: list with one of {list(data['ingredients'].explode().unique())}
    :return: filtered cocktails dataset
    """

def check_ingredients(user_ingredients: set[str], cocktail_ingredients: set[str]) -> bool:
    return user_ingredients.issubset(cocktail_ingredients)

@tool(args_schema=SearchInput)
def search(name: str = None, alcoholic: str = None, ingredients: list[str] = None) -> str:
    """Filter cocktails dataset by name, alcoholic type and ingredients."""
    result = data.copy()
    if name is not None:
        result = result[result.name.str.lower().str.contains(name)]
    if alcoholic is not None:
        result = result[result['alcoholic'] == alcoholic]
    # if category is not None:
    #     result = result[result['category'] == category]
    if ingredients is not None:
        result = result[result['ingredients'].apply(lambda x: check_ingredients(set(ingredients), x))]
    return result.sample(len(result)).to_string(index=False) if not result.empty else "No matching cocktails found."



llm = ChatOpenAI(model="gpt-4o-mini")

# tools = [search_by_name, search_by_alcoholic, search_by_category, search_by_ingredient]
print(search.description)
tools = [search]
agent = create_conversational_retrieval_agent(
    ChatOpenAI(model='gpt-4o-mini'),
    tools,
    verbose=True
)

prompts = [
# "What are the 5 cocktails containing lemon?",
# "What are the 5 non-alcoholic cocktails?",
# 'Can you list 10 cocktails with lemon that are non-alcoholic?',
'What are the 5 non-alcoholic cocktails containing sugar?',
]
for prompt in prompts:
    print(agent.invoke(prompt)['output'])
    print('-----------------------------------')
