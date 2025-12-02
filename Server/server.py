
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import util
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    util.load_artifacts()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-gender")
def getGender():
    return JSONResponse(content={"gender": util.get_gender()})


@app.get("/get-smoking")
def getSmokingHistory():
    return JSONResponse(content={"smoking_history": util.get_smoking_history()})


@app.post("/get-prediction")
def getPrediction(payload: dict = Body(...)):
    prediction = util.get_Prediction(
        payload["age"],
        payload["hypertension"],
        payload["heart_disease"],
        payload["bmi"],
        payload["HbA1c_level"],
        payload["blood_glucose_level"],
        payload["gender"],
        payload["smoking_history"]
    )

    return JSONResponse(content={"Prediction": int(prediction)})
