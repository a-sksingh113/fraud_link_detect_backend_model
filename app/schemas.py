from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

class URLPredictionResponse(BaseModel):
    prediction: int  
