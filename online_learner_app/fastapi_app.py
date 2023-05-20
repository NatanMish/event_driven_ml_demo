from fastapi import FastAPI
from online_learner_app.model_training import main as online_learner_main
import datetime
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class Batch(BaseModel):
    messages: Optional[List[str]] = None

@app.post("/batch/")
async def root(batch: Batch):
    message = online_learner_main(batch.messages)
    return {"message": message, "timestamp": datetime.datetime.now()}
