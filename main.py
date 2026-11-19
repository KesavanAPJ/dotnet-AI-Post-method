import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

load_dotenv()
app = FastAPI()  # keep your existing one, don't create a second

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # reuse yours if already there


# 1. What the "parcel" coming IN looks like
class PromptRequest(BaseModel):
    prompt: str


# 2. What the "parcel" going OUT looks like
class PromptResponse(BaseModel):
    answer: str


# 3. The POST endpoint
@app.post("/generate", response_model=PromptResponse)
def generate(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        result = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=request.prompt
        )
        return PromptResponse(answer=result.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))