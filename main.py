from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# यहाँ अपनी असली Gemini API की डालें (AIzaSy... वाली)
genai.configure(api_key="AIzaSyAs64E5iQQLDCAO0wtGJ0IgXkzlvYmJ1Rg")

# यहाँ pro की जगह flash कर दिया है
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    user_message: str
    dob: Optional[dict] = None

@app.post("/chat")
async def ai_astrologer_chat(request: ChatRequest):
    try:
        system_prompt = "तुम एक विश्व-स्तरीय ज्योतिषी हो। तुम्हें वैदिक ज्योतिष, केपी, नाड़ी, लो शु ग्रिड, और हस्तरेखा का गहन ज्ञान है। यूज़र के सवाल का सटीक जवाब दो।"
        
        response = model.generate_content(system_prompt + "\nयूज़र का सवाल: " + request.user_message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"तकनीकी समस्या: {str(e)}"}
