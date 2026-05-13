import os
import google.generativeai as genai
from typing import List, Dict, Optional

class GeminiChatbot:
    """Handles communication with the Google Gemini API."""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY environment variable not set.")
        else:
            genai.configure(api_key=api_key)
            
        from app.chatbot.udaan_context import UDAAN_SYSTEM_PROMPT
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=UDAAN_SYSTEM_PROMPT
            )
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            self.model = None

    async def generate_response(self, message: str, history_records=None) -> str:
        """
        Generate a response from Gemini based on the user message and entire conversation history.
        """
        if not self.model:
            return "Error: Gemini model not initialized. Please check your API key in .env file."
            
        # Convert DB history to Gemini's expected format
        contents = []
        if history_records:
            for record in history_records:
                # Gemini expects role 'user' or 'model'
                role = "user" if record.role == "user" else "model"
                contents.append({"role": role, "parts": [record.content]})
        else:
            # If no history, just send the current message
            contents.append({"role": "user", "parts": [message]})
            
        try:
            # Send the entire multi-turn conversation context to Gemini
            response = self.model.generate_content(contents)
            return response.text
        except Exception as e:
            return f"Error generating response from Gemini: {str(e)}"
