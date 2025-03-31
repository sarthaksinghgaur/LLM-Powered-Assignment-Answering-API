
from contextvars import ContextVar
from fastapi import Request

# Create a context variable for storing the request
current_request_var: ContextVar[Request] = ContextVar("current_request")