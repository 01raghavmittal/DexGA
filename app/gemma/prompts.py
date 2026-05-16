"""Prompt templates and builders for Gemma LLM."""

from typing import Dict, Optional, List
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PromptTemplates:
    """Predefined prompt templates."""
    
    # Information extraction prompt
    EXTRACT_INFO = """
    You are a document analysis assistant. Extract key information from the provided document.
    
    Document:
    {document}
    
    Query: {query}
    
    Please provide:
    1. The extracted information
    2. The page number where this information was found
    3. A confidence score (0-100)
    
    Format your response as JSON with keys: "information", "page", "confidence"
    """
    
    # Chat with document prompt
    CHAT_WITH_DOCUMENT = """
    You are a helpful assistant analyzing a document. Answer questions based on the document content.
    
    Document:
    {document}
    
    Previous conversation:
    {context}
    
    User question: {query}
    
    Please provide a concise answer and mention the relevant page number if applicable.
    """
    
    # Summarization prompt
    SUMMARIZE = """
    Please summarize the following document in {max_sentences} sentences:
    
    {document}
    """
    
    # Entity extraction prompt
    EXTRACT_ENTITIES = """
    Extract all named entities (people, organizations, locations, dates, etc.) from the following document:
    
    {document}
    
    Format as JSON with entity type as key and list of entities as value.
    """
    
    # Question answering prompt
    ANSWER_QUESTION = """
    Based on the following document, answer this question: {query}
    
    Document:
    {document}
    
    Provide a clear, concise answer with relevant page references.
    """
    
    # Comparison prompt
    COMPARE_DOCUMENTS = """
    Compare the following two documents:
    
    Document 1:
    {doc1}
    
    Document 2:
    {doc2}
    
    Focus: {focus}
    
    Provide a detailed comparison.
    """


class PromptBuilder:
    """Builds dynamic prompts."""
    
    @staticmethod
    def build_extraction_prompt(
        document: str,
        query: str,
        template: Optional[str] = None
    ) -> str:
        """
        Build information extraction prompt.
        
        Args:
            document: Document text
            query: Extraction query
            template: Optional custom template
            
        Returns:
            Formatted prompt
        """
        template = template or PromptTemplates.EXTRACT_INFO
        prompt = template.format(document=document, query=query)
        logger.debug("Extraction prompt built")
        return prompt
    
    @staticmethod
    def build_chat_prompt(
        document: str,
        query: str,
        context: str = "",
        template: Optional[str] = None
    ) -> str:
        """
        Build chat prompt.
        
        Args:
            document: Document text
            query: User query
            context: Previous conversation context
            template: Optional custom template
            
        Returns:
            Formatted prompt
        """
        template = template or PromptTemplates.CHAT_WITH_DOCUMENT
        prompt = template.format(document=document, query=query, context=context)
        logger.debug("Chat prompt built")
        return prompt
    
    @staticmethod
    def build_summarization_prompt(
        document: str,
        max_sentences: int = 5,
        template: Optional[str] = None
    ) -> str:
        """
        Build summarization prompt.
        
        Args:
            document: Document text
            max_sentences: Maximum sentences in summary
            template: Optional custom template
            
        Returns:
            Formatted prompt
        """
        template = template or PromptTemplates.SUMMARIZE
        prompt = template.format(document=document, max_sentences=max_sentences)
        logger.debug("Summarization prompt built")
        return prompt
    
    @staticmethod
    def build_entity_extraction_prompt(
        document: str,
        template: Optional[str] = None
    ) -> str:
        """
        Build entity extraction prompt.
        
        Args:
            document: Document text
            template: Optional custom template
            
        Returns:
            Formatted prompt
        """
        template = template or PromptTemplates.EXTRACT_ENTITIES
        prompt = template.format(document=document)
        logger.debug("Entity extraction prompt built")
        return prompt
    
    @staticmethod
    def build_qa_prompt(
        document: str,
        query: str,
        template: Optional[str] = None
    ) -> str:
        """
        Build Q&A prompt.
        
        Args:
            document: Document text
            query: Question
            template: Optional custom template
            
        Returns:
            Formatted prompt
        """
        template = template or PromptTemplates.ANSWER_QUESTION
        prompt = template.format(document=document, query=query)
        logger.debug("Q&A prompt built")
        return prompt
    
    @staticmethod
    def build_custom_prompt(template: str, **kwargs) -> str:
        """
        Build custom prompt with keyword arguments.
        
        Args:
            template: Prompt template
            **kwargs: Template variables
            
        Returns:
            Formatted prompt
        """
        try:
            prompt = template.format(**kwargs)
            logger.debug("Custom prompt built")
            return prompt
        except KeyError as e:
            logger.error(f"Missing template variable: {str(e)}")
            raise ValueError(f"Missing template variable: {str(e)}")
    
    @staticmethod
    def add_context_to_prompt(base_prompt: str, context: str) -> str:
        """
        Add context to prompt.
        
        Args:
            base_prompt: Base prompt
            context: Additional context
            
        Returns:
            Prompt with added context
        """
        return f"{context}\n\n{base_prompt}"
    
    @staticmethod
    def add_instructions_to_prompt(base_prompt: str, instructions: str) -> str:
        """
        Add instructions to prompt.
        
        Args:
            base_prompt: Base prompt
            instructions: Special instructions
            
        Returns:
            Prompt with instructions
        """
        return f"{base_prompt}\n\nSpecial Instructions:\n{instructions}"
