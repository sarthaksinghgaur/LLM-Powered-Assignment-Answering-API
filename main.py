from fastapi import FastAPI, Query, Request, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse
import uvicorn
from request_context import current_request_var

from request_parser import extract_info
from models import SimilarityRequest

import os, datetime

from GA_registry import GARegistry

app = FastAPI()
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def set_request_global(request: Request, call_next):
    token = current_request_var.set(request)  # Store request in context
    response = await call_next(request)
    current_request_var.reset(token)  # Reset after request is done
    return response

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello V 1.10 , FastAPI! at " + str(datetime.datetime.now())}

@app.post("/api")
async def process_request(
        question: str = Form(...),
        file: Optional[UploadFile] = File(None)
    ):
    try:
        #data = question
        #print(data)
        use_case = extract_info(question)
        if use_case:
            if file is None:
                result =  GARegistry[use_case["GA_No"]](question, use_case["parameters"])
            else:
                file_bytes = await file.read()
                use_case["parameters"]["content_type"] = file.content_type
                use_case["parameters"]["file_extention"] = file.filename.split(".")[-1]
                use_case["parameters"]["_file_"] = file
                result = GARegistry[use_case["GA_No"]](question, use_case["parameters"], file_bytes)
                #return result
            
            return {
                    "answer": result
                } 
        
        return {"error": "No use case found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/parse")
async def process_request(
        question: str = Form(...),
        file: Optional[UploadFile] = File(None)
    ):
    try:
        return extract_info(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/wikiheaders")
async def get_wiki_headers(country: str):
    from GA4 import Q43
    return Q43.get_country_outline(country)

@app.post("/similarity")
async def get_similarity(smilar_request: SimilarityRequest):
    from GA3 import Q37
    return Q37.get_similarity(smilar_request.docs, smilar_request.query)

@app.get("/execute")
def execute(q: str = Query(..., description="Query to match a function")):
    from GA3 import Q38
    result = Q38.parse_llm_task(q)
    #print(result)
    return result

@app.get("/fastapi/api")
def get_students(class_: list[str] = Query(default=None, alias="class")):
    from GA2 import Q29
    return Q29.get_students(class_)

@app.get('/headers')
def get_headers():
    return {"headers": dict(current_request_var.get().headers)}

# Serve the favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)