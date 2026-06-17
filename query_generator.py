import os
import sqlparse
import re
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine, get_schema
import google.generativeai as genai
import os
from dotenv import load_dotenv
from database import get_schema

# Load the API key from your .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-3.5-flash')

def clean_sql_output(response_text):
    """Removes markdown formatting and extracts the raw SQL query."""

    clean_query = re.sub(r"```sql\n(.*?)\n```", r"\1", response_text, flags=re.DOTALL)

    sql_match = re.search(r"SELECT .*?;", clean_query, re.DOTALL | re.IGNORECASE)

    return sql_match.group(0) if sql_match else clean_query.strip()

def validate_sql_query(sql_query):
    """Validates the SQL Query syntax before execution."""
    try:
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            return False, "Invalid SQL syntax."
        return True, None
    except Exception as e:
        return False, str(e)
    
def generate_sql_query(nl_query):
    """Converts Natural Language query to an optimized SQL query."""
    schema = get_schema()

    schema_text = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in schema.items()])

    prompt = f"""
    You are an SQL expert. Convert the following natural language query into an optimized MySQL query.
    
    Database Schema: {schema_text}
    
    User Request: {nl_query}

    SQL Query:
    """
    try:
        response = model.generate_content(prompt)
        raw_sql_query = response.text.strip()

        clean_query = clean_sql_output(raw_sql_query)
        return clean_query
    
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def suggest_index(sql_query):
    """Suggests indexes for the executed SQL query."""
    try:
        with engine.connect() as connection:
            explain_query = f"Explain {sql_query}"
            result = connection.execute(text(explain_query))
            execution_plan = result.fetchall()

        print("\nQuery Execution Plan: ")
        for row in execution_plan:
            print(row)

        return "Considering adding an index on frequently used WHERE conditions."
    
    except Exception as e:
        return f"Could not generate execution plan: {e}"
    
def execute_query(sql_query):
    """Executes a validated and optimized sql query"""
    is_valid, error_msg = validate_sql_query(sql_query)
    if not is_valid:
        print(f"SQL Validation Error: {error_msg}")
        return None
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            fetched_results = result.fetchall()

        index_suggestion = suggest_index(sql_query)

        return {"results": fetched_results, "optimization_tips": index_suggestion}
    except SQLAlchemyError as e:
        print(f"Database Execution Error: {str(e)}")
        return None
    
if __name__ == "__main__":
    user_input = input("Enter your natural language query: ")
    sql_query = generate_sql_query(user_input)

    if sql_query:
        print(f"\nGenerated SQL query:\n{sql_query}")

        execution_results = execute_query(sql_query)
        if execution_results:
            print("\n Query Results:")
            for row in execution_results["results"]:
                print(row)
            print("\nOptimization Tips:", execution_results["optimization_tips"])
        else:
            print("No results found or error executing query")
    else:
        print("Failed to generate a valid sql query.")