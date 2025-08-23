import requests
from sqlalchemy import text,MetaData
from config import EURI_API_KEY,EURI_API_URL,MODEL_NAME,DATABASE_URI


##to provide the metadata so as to connect to the database with llm models
##if we not pass the schema information, the llm models won't know how to interact with the database

##connection between the database schema and the llm models
def get_db_schema(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    schema = ""
    for table in meta.tables.values():
        schema += f"\nTable: {table.name}\nColumns: {', '.join([col.name + ' (' + str(col.type) + ')' for col in table.columns])}\n"
    return schema.strip()


##This function sends your text prompt to an LLM API and returns the model’s generated reply as a clean string.



def call_euri_llm(prompt):
    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    response = requests.post(EURI_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # raise exception on error
    return response.json()["choices"][0]["message"]["content"].strip()

##This function lets you run any SQL query on your database via SQLAlchemy and gives back both the data and the column names in a Python-friendly format.

def execute_sql(engine, query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall(), result.keys()

