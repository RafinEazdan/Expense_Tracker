from fastapi import APIRouter, status, HTTPException, Depends
from psycopg import Connection

from app.database import get_db
from app.oauth import get_current_user

from app.LLM.llmmodel import query_analysis

router = APIRouter(
    tags=["AI Model Requests"]
)

@router.get("/llm/analysis",status_code=status.HTTP_200_OK)
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