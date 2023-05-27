from fastapi import FastAPI
from online_learner_app.model_training import main as online_learner_main
import datetime
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class DataPoints(BaseModel):
    messages: Optional[List[str]] = None


@app.post("/data_points/")
async def root(data_points: DataPoints):
    message = online_learner_main(data_points.messages)
    return {"message": message, "timestamp": datetime.datetime.now()}
