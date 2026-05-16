"""Custom exception classes."""


class DexGAException(Exception):
    """Base exception for DexGA application."""
    pass


class PDFException(DexGAException):
    """Exception related to PDF processing."""
    pass


class LLMException(DexGAException):
    """Exception related to LLM operations."""
    pass


class ValidationException(DexGAException):
    """Exception related to validation."""
    pass


class SessionException(DexGAException):
    """Exception related to session management."""
    pass


class StorageException(DexGAException):
    """Exception related to storage operations."""
    pass


class ConfigException(DexGAException):
    """Exception related to configuration."""
    pass


class TimeoutException(DexGAException):
    """Exception for timeout errors."""
    pass


class ResourceNotFoundError(DexGAException):
    """Exception when resource is not found."""
    pass


class InsufficientResourcesError(DexGAException):
    """Exception when resources are insufficient."""
    pass
