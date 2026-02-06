import json
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from fastapi import HTTPException, status

load_dotenv()

model = ChatOllama(model=os.getenv("LLM_MODEL"))

def format_reports(expenses):
    reports = []
    for e in expenses:
        format = {
        "date": str(e["created_at"]),
        "amount": float(e["amount"]),
        "category": e["category"],
        "note": e.get("description", "")
        }
        reports.append(format)
    
    return reports


async def query_analysis(expenses: dict):
    try:
        expenses_format = format_reports(expenses) 
        expenses_json = json.dumps(expenses_format, indent=2)
        prompt =  f"""
You are a creative financial story writer and analyser.
You tell a very short story based on the expenses done by the user. The story will reflect the analysis of their expenditure.
- write maximum 3-4 short sentences
- add light jokes and humor
- make it funny
- dont hurt the user feelings (like not calling them fat, lazy etc)
- the story can be fantasy mixed with real life touch.
- dont show the stats directly, you can show but not like a list
- do not ask any follow up question ever
- try add timeline like months
Expense data:
{expenses_json}
    """
        response = model.invoke(prompt)

        return response.content
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="LLm Issue")
