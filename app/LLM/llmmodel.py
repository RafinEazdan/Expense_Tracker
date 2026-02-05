import json
from langchain_community.chat_models import ChatOllama

from routers.reports import get_expenses

expenses = get_expenses()

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


expenses_json = json.dumps(format_reports(expenses), indent=2)


prompt = f"""
    You are a financial assistant

"""