
import os, json, numpy as np, httpx
from request_context import current_request_var

def execute():
    request = current_request_var.get()
    # get all the headers and return as a json
    return request.headers