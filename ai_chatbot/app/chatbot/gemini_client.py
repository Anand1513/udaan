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
            
        # Initialize a simple in-memory cache to save tokens
        self.cache = {}
        self.MAX_CACHE_SIZE = 500

    async def generate_response(self, message: str, history_records=None) -> str:
        """
        Generate a response from Gemini based on the user message and entire conversation history.
        """
        if not self.model:
            return "Error: Gemini model not initialized. Please check your API key in .env file."
            
        # --- CACHING LOGIC: GENERATE UNIQUE KEY ---
        # Create a string representation of the history to ensure context is identical
        history_str = ""
        recent_history = []
        if history_records:
            recent_history = history_records[-10:] if len(history_records) > 10 else history_records
            for r in recent_history:
                history_str += f"{r.role}:{r.content}|"
                
        # Our unique key is the exact message + the exact history context
        cache_key = f"{message.strip().lower()}|{history_str}"
        
        # --- CACHING LOGIC: CHECK CACHE ---
        if cache_key in self.cache:
            print("🟢 CACHE HIT: Returning saved response (0 tokens used)")
            return self.cache[cache_key]
            
        # Convert DB history to Gemini's expected format
        contents = []
        if history_records:
            for record in recent_history:
                # Gemini expects role 'user' or 'model'
                role = "user" if record.role == "user" else "model"
                contents.append({"role": role, "parts": [record.content]})
        else:
            # If no history, just send the current message
            contents.append({"role": "user", "parts": [message]})
            
        try:
            # Send the entire multi-turn conversation context to Gemini
            response = self.model.generate_content(contents)
            response_text = response.text
            
            # --- CACHING LOGIC: SAVE TO CACHE ---
            # Prevent infinite memory growth by removing the oldest item if we hit the limit
            if len(self.cache) >= self.MAX_CACHE_SIZE:
                # In Python 3.7+, dictionaries maintain insertion order
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                
            self.cache[cache_key] = response_text
            
            return response_text
        except Exception as e:
            return f"Error generating response from Gemini: {str(e)}"
