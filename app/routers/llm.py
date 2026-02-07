from fastapi import APIRouter, status, HTTPException, Depends
from psycopg import Connection

from app.database import get_db
from app.oauth import get_current_user

from app.LLM.storyLLM import query_analysis
from app.LLM.autoSQL import sql_query_gen

from app.schemas import ExpenseResponse, ExpenseReport

router = APIRouter(
    tags=["AI Model Requests"]
)

@router.get("/llm/analysis/story",status_code=status.HTTP_200_OK)
async def analysis(db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # print(f"Current user = {current_user["id"]}")
    try:
        with db.cursor() as cursor:
            cursor.execute('''SELECT * from expenses where owner_id = %s;''', (current_user["id"],))
            expenses = cursor.fetchall()
            # print(expenses) # Query is successful

        try:
            lm_reponse = await query_analysis(expenses)

            return lm_reponse
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="LLM Could not be called")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts Not Found!")
    


@router.post("/llm/sql-gen",status_code=status.HTTP_200_OK, response_model=ExpenseResponse)
async def sql_gen(query:str ,db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        owner_id = current_user["id"]
        lm_reponse = await sql_query_gen(query, owner_id)
        with db.cursor() as cursor:
            cursor.execute('''SELECT * from expenses where owner_id = %s;''', (current_user["id"],))
            expenses = cursor.fetchall()
            # print(expenses) # Query is successful

        try:

            return lm_reponse
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="LLM Could not be called")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts Not Found!")
