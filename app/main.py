# app/main.py
from fastapi import FastAPI, HTTPException
import boto3
import json
import logging
from datetime import datetime

from pydantic import BaseModel

app = FastAPI()
s3 = boto3.client('s3')
bedrock = boto3.client('bedrock-runtime')

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(request: PredictRequest):
    try:
        response = bedrock.invoke_model(
            modelId="meta.llama3-1-8b-instruct-v1:0",
            body=json.dumps({
                "prompt": request.text,
                "max_gen_len": 256,
                "temperature": 0.7
            })
        )
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": request.text,
            "response": response['body'].read().decode()
        }
        
        try:
            s3.put_object(
                Bucket="ml-api-logs-dev",
                Key=f"logs/{datetime.now().strftime('%Y-%m-%d')}/request.json",
                Body=json.dumps(log_entry)
            )
        except Exception as e:
            logging.error(f"S3 error: {str(e)}")
        
        return {"prediction": response}
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))