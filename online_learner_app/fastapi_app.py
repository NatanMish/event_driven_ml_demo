from fastapi import FastAPI
from online_learner_app.model_training import main as online_learner_main
import datetime

app = FastAPI()


@app.get("/")
async def root():
    message = online_learner_main()
    return {"message": message, "timestamp": datetime.datetime.now()}
