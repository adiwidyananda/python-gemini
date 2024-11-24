import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, read
from .database import engine, Base, get_db
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env

# Create tables
Base.metadata.create_all(bind=engine)

# Set up Google API key for Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the FastAPI app
app = FastAPI()

def get_user_info_from_name(name: str):
    """Retrieve user info from the name.

    Args:
        name (str): The name of the user to retrieve.

    Returns:
        dict: A dictionary with user information (name).
    """
    return {"name": name}

@app.post("/chat")
def chat_with_user(text: str, db: Session = Depends(get_db)):
    """Process chat messages and interact with Gemini AI to get user information.

    Args:
        user_query (str): The input message from the user.
        db (Session): The database session for querying user data.

    Returns:
        str: The AI's response to the user.
    """
    # Initialize Gemini AI model with user_info tool
    model = genai.GenerativeModel(model_name='gemini-1.5-flash', tools=[get_user_info_from_name])
    chat = model.start_chat()
    ai_response = chat.send_message(text)

    function_response = ""
    
    # Process the function call in the response from Gemini AI
    for part in ai_response.parts:
        if function_call := part.function_call:
            if function_call.name == "get_user_info_from_name":
                user_name = function_call.args.get('name')
                if user_name:
                    user_info = read.get_user(db, user_name)
                    
                    if user_info:
                        user_info_str = (
                            f"Name: {user_info.name}\n"
                            f"Email: {user_info.email}\n"
                            f"Hobby: {user_info.hobby}\n"
                            f"Job: {user_info.job}\n"
                            f"Age: {user_info.age}"
                        )
                        function_response = f"Here is the user info:\n{user_info_str}\nPlease provide this information to the user."
                    else:
                        return f"Sorry, we couldn't find the user named {user_name}."
    if function_response:

        # Send the user info (or an error message) to the AI for further interaction
        ai_response = chat.send_message(function_response)

        # Extract and return the AI's response
        ai_message = ""
        for part in ai_response.parts:
            if text := part.text:
                ai_message = text

        return ai_message
    else:
        return "Sorry, no valid name provided."