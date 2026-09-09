# requirements: fastapi, uvicorn, pyswisseph, google-generativeai
from fastapi import FastAPI
import swisseph as swe
import google.generativeai as genai

app = FastAPI()

# अपनी फ्री Gemini API की सेट करें
genai.configure(api_key="AQ.Ab8RN6Jb9WYigpVxIenzcDc5IAsjVAIoIEZo_1P1ARXzgBszmQ")
model = genai.GenerativeModel('gemini-1.5-pro')

def get_planetary_positions(year, month, day, hour, lat, lon):
    swe.set_ephe_path('/usr/share/ephe') # Ephemeris फाइल्स का पाथ
    julian_day = swe.julday(year, month, day, hour)
    
    # सूर्य और चंद्रमा की पोजीशन का एक उदाहरण
    sun_pos = swe.calc_ut(julian_day, swe.SUN)[0]
    moon_pos = swe.calc_ut(julian_day, swe.MOON)[0]
    
    return f"सूर्य की डिग्री: {sun_pos[0]:.2f}, चंद्रमा की डिग्री: {moon_pos[0]:.2f}"

@app.post("/chat")
async def ai_astrologer_chat(user_message: str, dob: dict):
    # 1. एस्ट्रोलॉजी डेटा कैलकुलेट करें
    astro_data = get_planetary_positions(dob['year'], dob['month'], dob['day'], dob['hour'], dob['lat'], dob['lon'])
    
    # 2. AI को डीप नॉलेज के साथ इंस्ट्रक्शन दें (System Prompt)
    system_prompt = f"""
    तुम एक विश्व-स्तरीय ज्योतिषी हो। तुम्हें वैदिक ज्योतिष, केपी, नाड़ी, लो शु ग्रिड, और हस्तरेखा (Palmistry) का गहन ज्ञान है।
    यूज़र का ग्रहीय डेटा: {astro_data}
    यूज़र के सवाल का जवाब इस डेटा और अपने डीप नॉलेज को मिलाकर दो।
    """
    
    # 3. AI से जवाब जनरेट करें
    response = model.generate_content(system_prompt + "\nयूज़र का सवाल: " + user_message)
    return {"reply": response.text}

# रन करने के लिए: uvicorn main:app --reload
