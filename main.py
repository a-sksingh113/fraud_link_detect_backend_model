from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import URLRequest, URLPredictionResponse
from app.predict import predict_from_url

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
   allow_origin_regex=".*", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Links Spam Classifier API is running."}

@app.post("/predict4", response_model=URLPredictionResponse)
async def predict_url(request: URLRequest):
    prediction = predict_from_url(request.url)
    return URLPredictionResponse(prediction=prediction)
