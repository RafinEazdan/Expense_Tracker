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
async def sql_query_gen(query):
    try:
        prompt = f"""
                You are a data extraction engine.

Your task is to extract values from a natural-language expense description.

Schema
	•	amount: number
	•	category: string
	•	description: string (optional)

Rules
	•	Output ONLY the values in this exact order:
	1.	amount
	2.	category
	3.	description
	•	Separate values using a comma.
	•	Do NOT include field names, keywords, explanations, labels, quotes, or formatting.
	•	If the description is missing, output NULL.
	•	Do NOT add any extra text before or after the values.

User input

{query}

Output format(just give me the values, no extra keywords):
amount, category, description

"""
        response = await model.invoke(prompt)
        print(response)
        # Split safely into at most 3 parts
        # parts = [p.strip() for p in response.split(",", maxsplit=2)]

        # if len(parts) != 3:
        #     raise ValueError("Parsed output is not in expected 3-part format")

        # amount, category, description = parts

        # # If description is missing use None
        # if description.lower() in ("null", ""):
        #     description = None

        return response
    
    except Exception as e:
        print("LLM Failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="LLM failed")



