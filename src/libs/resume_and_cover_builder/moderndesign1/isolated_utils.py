"""
Modern Design 1 - Helt isolerade utilities
INGA global_config beroenden
"""

import time
import base64
from typing import Any, Dict, List
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessage
from loguru import logger

class IsolatedLoggerChatModel:
    """
    Isolerad ChatModel för Modern Design 1
    INGEN global_config - bara ren AI-funktionalitet
    """
    
    def __init__(self, chat_model: ChatOpenAI):
        self.llm = chat_model
        self.max_retries = 15
        self.retry_delay = 10
        
    def __call__(self, messages: Any) -> str:
        """
        Anropar AI-modellen med retry-logik
        INGEN loggning till fil - bara console logging
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"🤖 Modern Design 1: AI-anrop (försök {attempt + 1}/{self.max_retries})")
                
                if isinstance(messages, str):
                    response = self.llm.invoke([{"role": "user", "content": messages}])
                else:
                    response = self.llm.invoke(messages)
                
                if isinstance(response, AIMessage):
                    result = response.content
                else:
                    result = str(response)
                
                logger.info(f"✅ Modern Design 1: AI-svar mottaget ({len(result)} tecken)")
                return result
                
            except Exception as e:
                logger.warning(f"⚠️ Modern Design 1: AI-anrop misslyckades (försök {attempt + 1}): {e}")
                
                if attempt < self.max_retries - 1:
                    logger.info(f"🔄 Modern Design 1: Väntar {self.retry_delay}s innan nästa försök...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Modern Design 1: Alla AI-försök misslyckades efter {self.max_retries} försök")
                    raise
        
        raise Exception("Modern Design 1: AI-anrop misslyckades efter alla försök")
    
    def invoke(self, messages: Any) -> str:
        """
        Invoke metod för kompatibilitet med AI-generator
        """
        return self.__call__(messages)

def create_isolated_llm(api_key: str) -> IsolatedLoggerChatModel:
    """
    Skapar en isolerad LLM för Modern Design 1
    
    Args:
        api_key: OpenAI API-nyckel
        
    Returns:
        IsolatedLoggerChatModel: Isolerad AI-modell
    """
    chat_model = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=api_key,
        temperature=0.4,
        timeout=60
    )
    
    return IsolatedLoggerChatModel(chat_model)

def image_to_base64(image_path: str) -> str:
    """
    Isolerad image_to_base64 för Modern Design 1
    INGEN global_config beroende
    
    Args:
        image_path (str): Path to the image file

    Returns:
        str: Base64 encoded string of the image

    Raises:
        FileNotFoundError: If the image file doesn't exist
        Exception: If there's an error reading the file
    """
    try:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_string = base64.b64encode(image_data).decode('utf-8')
            logger.debug(f"Modern Design 1: Successfully converted image {image_path} to base64")
            return base64_string
    except FileNotFoundError as e:
        logger.error(f"Modern Design 1: Error converting image to base64: {e}")
        raise
    except Exception as e:
        logger.error(f"Modern Design 1: Unexpected error converting image to base64: {e}")
        raise
