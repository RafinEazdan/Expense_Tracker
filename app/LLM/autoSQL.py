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
                You are a strict data extraction engine.

You MUST follow the rules exactly.

TASK:
Extract values from the user input.

SCHEMA:
amount (number)
category (string)
description (string)

DESCRIPTION RULE (IMPORTANT):
- If the user does NOT explicitly mention a description,
  you MUST generate a short, reasonable description
  based on the category and context.
- The description must be 2–5 words.
- Do NOT invent unnecessary details.

OUTPUT RULES (CRITICAL):
- Output EXACTLY one single line
- Output ONLY raw values
- Order must be: amount, category, description
- Separate values using commas
- NO explanations
- NO labels
- NO quotes
- NO newlines
- NO extra spaces

USER INPUT:
{query}

VALID OUTPUT EXAMPLES:
56,food,meal expense
120,transport,uber ride
30,coffee,morning coffee

NOW OUTPUT:

"""
        response_all = model.invoke(prompt)
        response = response_all.content
        print(response)
        # Split safely into at most 3 parts
        parts = [p.strip() for p in response.split(",")]

        amount, category, description = parts
        # print(f"Amount is: {amount}, Category:{category}, Desc: {description}")
        return amount, category, description
    
    except Exception as e:
        print("LLM Failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="LLM failed")



