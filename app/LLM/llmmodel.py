import json
from langchain_community.chat_models import ChatOllama
from fastapi import HTTPException, status

# expenses = get_expenses()

model = ChatOllama(model="llama3.2:latest")

def format_reports(expenses):
    reports = []
    for e in expenses:
        format = {
        "date": e["date"],
        "amount": float(e["amount"]),
        "category": e["category"],
        "note": e.get("description", "")
        }
        reports.append(format)
    
    return reports


def query_analysis(expenses: dict):
    try:
        expenses_format = format_reports(expenses) 
        expenses_json = json.dumps(format_reports(expenses_format), indent=2)
        prompt =  f"""
    You are a financial assistant. Analyze the expense data and provide clear, 
    concise insights. Focus on patterns, trends, and actionable advice.
    Expense data: {expenses_json}
    """
        response = model.invoke(prompt)

        return response.content
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="LLm Issue")
