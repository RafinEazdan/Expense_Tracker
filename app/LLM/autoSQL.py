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

You are NOT an assistant.
You are NOT allowed to explain anything.
You are NOT allowed to show reasoning.

Your ONLY job is to output extracted values.

TASK:
Extract values from the user input.

SCHEMA:
amount (number)
category (string)
description (string)

CATEGORY RULE (CRITICAL):
- If the expense matches one of the predefined categories, you MUST use it.
- If none match, generate a short suitable category (1–3 words, Title Case).

PREDEFINED CATEGORIES:
Food & Dining
Transportation
Shopping
Entertainment
Bills & Utilities
Healthcare
Travel
Education
Personal Care

DESCRIPTION RULE:
- If the user does not explicitly give a description,
  generate a short reasonable description (2–5 words).
- No assumptions, no stories.

OUTPUT RULES (ABSOLUTE):
- Output ONLY the final values
- Output EXACTLY ONE LINE
- Format: amount,category,description
- NO explanations
- NO reasoning
- NO bullet points
- NO labels
- NO prefixes
- NO suffixes
- NO quotes
- NO markdown
- NO newlines
- NO extra spaces
- If ANY rule is violated, the output is INVALID

USER INPUT:
{query}

FINAL OUTPUT (VALUES ONLY):
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



