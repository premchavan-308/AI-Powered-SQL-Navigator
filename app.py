from fastapi import FastAPI
from pydantic import BaseModel
from query_generator import generate_sql_query, execute_query
from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/test_db"
engine = create_engine(DATABASE_URL)
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/generate_sql/")
async def generate_sql(data: dict):
    nl_query = data.get("query")
    sql = generate_sql_query(nl_query) # This calls your generator
    return {"sql": sql} # The UI looks for this "sql" key
from fastapi import Request

@app.post("/execute_sql/")
async def execute_sql(request: Request):
    # Get the raw JSON body
    data = await request.json()
    # Safely extract the 'sql' key
    query = data.get("sql")
    
    # Check if query is actually a string
    if not isinstance(query, str):
        return {"results": [], "error": f"Invalid query format: expected string, got {type(query)}"}

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            results = [dict(row) for row in result.mappings()]
            return {"results": results}
    except Exception as e:
        return {"results": [], "error": str(e)}
    
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1", port=8000)