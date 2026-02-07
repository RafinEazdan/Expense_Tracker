import json
import os
from urllib import response
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from fastapi import HTTPException, status

from app.schemas import ExpenseReport

load_dotenv()
model = ChatOllama(model=os.getenv("LLM_MODEL"))

expense_report = ExpenseReport.model_json_schema()
# expense_response = ExpenseResponse.model_json_schema()
table_name = "expenses"
# print(f"Expense Report: {expense_report} \n Expense Response: {expense_response}")
def sql_query_gen(query):
    try:
        prompt = f"""
                You are a database engineer.

Your task is to convert a natural-language instruction into a valid SQL INSERT statement.

Context:
- Target table name: {table_name}
- Table schema :{expense_report}


Rules:
- Generate ONLY a single SQL INSERT statement.
- Use ONLY the fields defined in the schema.
- Do NOT add explanations, comments, or extra text.
- Do NOT assume fields that are not provided.
- If a field is optional and missing, omit it from the INSERT.
- Values must be correctly typed and SQL-safe.

User input (natural language):
"{query}"

Output:
A valid SQL INSERT statement for the given table.

"""

        reponse = model.invoke(prompt)

        return response
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="LLM failed")



