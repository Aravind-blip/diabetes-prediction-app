
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
    # Return a fixed list of genders instead of reading from the model
    return JSONResponse(content={"gender": ["Male", "Female"]})


@app.get("/get-smoking")
def getSmokingHistory():
    # Return a fixed list of smoking history categories
    return JSONResponse(
        content={
            "smoking_history": ["never", "former", "current", "ever"]
        }
    )


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
