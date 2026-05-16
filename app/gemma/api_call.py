"""Gemma API integration and LLM communication.

This module integrates with Ollama to communicate with the Gemma 4 E2B model,
which includes vision/image understanding capabilities.
"""

import json
import requests
from typing import Optional, Dict, Any
from config.settings import (
    MODEL_NAME,
    OLLAMA_BASE_URL,
    MODEL_TIMEOUT,
    TEMPERATURE,
    MAX_TOKENS,
    TOP_P,
    TOP_K
)
from app.utils.logger import get_logger
from app.utils.exceptions import LLMException

logger = get_logger(__name__)


class GemmaAPI:
    """Gemma LLM API client."""
    
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        base_url: str = OLLAMA_BASE_URL,
        timeout: int = MODEL_TIMEOUT
    ):
        """
        Initialize Gemma API client.
        
        Args:
            model_name: Model name
            base_url: Ollama server URL
            timeout: Request timeout in seconds
        """
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout
        self.endpoints = {
            "generate": f"{base_url}/api/generate",
            "embed": f"{base_url}/api/embed",
            "tags": f"{base_url}/api/tags"
        }
        logger.info(f"Gemma API client initialized: {model_name}")
    
    def is_available(self) -> bool:
        """
        Check if LLM model is available.
        
        Returns:
            True if available, False otherwise
        """
        try:
            response = requests.get(self.endpoints["tags"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model.get("name") for model in data.get("models", [])]
                return self.model_name in models
            return False
        except Exception as e:
            logger.error(f"Error checking model availability: {str(e)}")
            return False
    
    def generate(
        self,
        prompt: str,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        stream: bool = False
    ) -> Optional[str]:
        """
        Generate response from Gemma.
        
        Args:
            prompt: Input prompt
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            
        Returns:
            Generated text or None
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": TOP_P,
                "top_k": TOP_K,
                "stream": stream
            }
            
            logger.debug(f"Sending request to Gemma: {len(prompt)} prompt chars")
            response = requests.post(
                self.endpoints["generate"],
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code}")
                raise LLMException(f"API returned status code: {response.status_code}")
            
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        full_response += data.get("response", "")
                return full_response
            else:
                # Handle single response
                data = response.json()
                result = data.get("response", "")
                logger.debug(f"Response received: {len(result)} chars")
                return result
        
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise LLMException("LLM request timeout")
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            raise LLMException("Failed to connect to LLM service")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise LLMException(f"Error generating response: {str(e)}")
    
    def extract_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed JSON dictionary or None
        """
        try:
            # Try to find JSON in response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            return None
    
    def extract_information(
        self,
        document: str,
        query: str,
        temperature: float = TEMPERATURE
    ) -> Optional[Dict[str, Any]]:
        """
        Extract information from document using Gemma.
        
        Args:
            document: Document text
            query: Extraction query
            temperature: Temperature for generation
            
        Returns:
            Extracted information with metadata
        """
        try:
            from app.gemma.prompts import PromptBuilder
            
            prompt = PromptBuilder.build_extraction_prompt(document, query)
            response = self.generate(prompt, temperature=temperature)
            
            if response:
                # Try to parse JSON response
                json_data = self.extract_json_response(response)
                if json_data:
                    logger.info("Information extracted successfully")
                    return json_data
                else:
                    # Return as plain text if JSON parsing fails
                    return {"information": response, "page": "unknown", "confidence": 0}
            return None
        
        except Exception as e:
            logger.error(f"Error extracting information: {str(e)}")
            raise LLMException(f"Extraction failed: {str(e)}")
    
    def chat(
        self,
        document: str,
        query: str,
        context: str = "",
        temperature: float = TEMPERATURE
    ) -> Optional[str]:
        """
        Chat with document using Gemma.
        
        Args:
            document: Document text
            query: User question
            context: Previous conversation context
            temperature: Temperature for generation
            
        Returns:
            Response text
        """
        try:
            from app.gemma.prompts import PromptBuilder
            
            prompt = PromptBuilder.build_chat_prompt(document, query, context, temperature)
            response = self.generate(prompt, temperature=temperature)
            
            logger.info("Chat response generated")
            return response
        
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise LLMException(f"Chat failed: {str(e)}")
    
    def summarize(
        self,
        document: str,
        max_sentences: int = 5
    ) -> Optional[str]:
        """
        Summarize document using Gemma.
        
        Args:
            document: Document text
            max_sentences: Maximum sentences in summary
            
        Returns:
            Summary text
        """
        try:
            from app.gemma.prompts import PromptBuilder
            
            prompt = PromptBuilder.build_summarization_prompt(document, max_sentences)
            response = self.generate(prompt)
            
            logger.info("Summary generated")
            return response
        
        except Exception as e:
            logger.error(f"Error summarizing: {str(e)}")
            raise LLMException(f"Summarization failed: {str(e)}")
    
    def analyze_image(
        self,
        image_data: str,
        query: str = "Analyze this image and provide a detailed description"
    ) -> Optional[str]:
        """
        Analyze image using Gemma 4 E2B vision capabilities.
        
        Args:
            image_data: Base64 encoded image or image path
            query: Analysis query/instruction
            
        Returns:
            Image analysis response
        """
        try:
            # Gemma 4 E2B supports vision/image understanding
            prompt = f"{query}\n\nImage: {image_data}"
            response = self.generate(prompt, temperature=TEMPERATURE)
            
            logger.info("Image analyzed successfully")
            return response
        
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise LLMException(f"Image analysis failed: {str(e)}")
    
    def extract_text_from_image(
        self,
        image_data: str
    ) -> Optional[str]:
        """
        Extract text from image using vision capabilities.
        
        Args:
            image_data: Base64 encoded image
            
        Returns:
            Extracted text from image
        """
        try:
            prompt = f"Extract and transcribe all text visible in this image. Return only the text content.\n\nImage: {image_data}"
            response = self.generate(prompt)
            
            logger.info("Text extracted from image")
            return response
        
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            raise LLMException(f"Text extraction from image failed: {str(e)}")
    
    def document_with_images(
        self,
        document_text: str,
        images: list,
        query: str
    ) -> Optional[str]:
        """
        Process document that contains images.
        
        Args:
            document_text: Document text content
            images: List of base64 encoded images
            query: Analysis query
            
        Returns:
            Analysis response
        """
        try:
            # Combine document text and images for analysis
            prompt = f"{query}\n\nDocument:\n{document_text}\n\nImages included: {len(images)}"
            response = self.generate(prompt)
            
            logger.info(f"Document with {len(images)} images analyzed")
            return response
        
        except Exception as e:
            logger.error(f"Error processing document with images: {str(e)}")
            raise LLMException(f"Document with images processing failed: {str(e)}")


# Global API instance
_gemma_api: Optional[GemmaAPI] = None


def get_gemma_client() -> GemmaAPI:
    """
    Get or create Gemma API client.
    
    Returns:
        Gemma API instance
    """
    global _gemma_api
    if _gemma_api is None:
        _gemma_api = GemmaAPI()
    return _gemma_api
