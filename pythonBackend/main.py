from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import joblib
import pandas as pd
from ses import EmailService
################ AWS SES for email
from pydantic import BaseModel, EmailStr
import boto3
from botocore.exceptions import BotoCoreError, ClientError
# Load trained model and preprocessor at startup
model = tf.keras.models.load_model("saved_model/time_prediction_model.keras")
preprocessor = joblib.load("saved_model/preprocessor_time.pkl")
client_model = tf.keras.models.load_model("saved_model/client_efficiency_model.keras")
client_preprocessor = joblib.load("saved_model/preprocessor_client.pkl")

app = FastAPI(title="Construction Time Prediction API")

# Input schema (based on your CSV features)
class PredictionRequest(BaseModel):
    ActiveEngineHours: float
    IdleTime: float
    FuelUsage_L: float
    LoadUsage: float
    TypeOfProject: str
    Weather_Season: str
    MachineType: str
    SiteDemographic: str
    ContractValue: float
    PromisedTime: float
    ClientEfficiency: float
# For client efficiency
class ClientEfficiencyRequest(BaseModel):
    MachineType: str
    ActiveOperatingHours: float
    IdleTime: float
    FuelConsumption_L: float
    AvgLoad_Tonnes: float
    MaxLoad_Tonnes: float
    AvgEngineRPM: float
    AvgHydraulicPressure_PSI: float
    WeatherConditions: str
    SiteConditions: str
    SupportingStaff: int

@app.post("/predictTime")
def predict(req: PredictionRequest):
    input_dict = {
        "ActiveEngineHours": req.ActiveEngineHours,
        "IdleTime": req.IdleTime,
        "FuelUsage (L)": req.FuelUsage_L,
        "LoadUsage": req.LoadUsage,
        "TypeOfProject": req.TypeOfProject,
        "Weather/Season": req.Weather_Season,
        "MachineType": req.MachineType,
        "SiteDemographic": req.SiteDemographic,
        "ContractValue": req.ContractValue,
        "PromisedTime": req.PromisedTime,
        "ClientEfficiency": req.ClientEfficiency
    }

    input_df = pd.DataFrame([input_dict])

    # 🔑 Apply the same cleaning as training
    input_df.columns = input_df.columns.str.replace(r'[^A-Za-z0-9]+', '_', regex=True).str.lower()

    # Preprocess + predict
    processed_input = preprocessor.transform(input_df)
    prediction = model.predict(processed_input)
    predicted_time = float(prediction.flatten()[0])

    return {"predicted_time_months": round(predicted_time, 2)}
@app.post("/predict_client_efficiency")
def predict_client_efficiency(req: ClientEfficiencyRequest):
    # Convert to DataFrame
    input_df = pd.DataFrame([{
        "MachineType": req.MachineType,
        "ActiveOperatingHours": req.ActiveOperatingHours,
        "IdleTime": req.IdleTime,
        "FuelConsumption(L)": req.FuelConsumption_L,
        "AvgLoad(Tonnes)": req.AvgLoad_Tonnes,
        "MaxLoad(Tonnes)": req.MaxLoad_Tonnes,
        "AvgEngineRPM": req.AvgEngineRPM,
        "AvgHydraulicPressure(PSI)": req.AvgHydraulicPressure_PSI,
        "WeatherConditions": req.WeatherConditions,
        "SiteConditions": req.SiteConditions,
        "SupportingStaff": req.SupportingStaff
    }])

    # Preprocess + predict
    processed_input = client_preprocessor.transform(input_df)
    prediction = client_model.predict(processed_input)
    predicted_efficiency = float(prediction.flatten()[0])

    return {"predicted_client_efficiency": round(predicted_efficiency, 3)}
# Define request model
class EmailRequest(BaseModel):
    to_email: str
    subject: str
    message: str

# Create SES client
# Make sure your AWS credentials are set via env vars, ~/.aws/credentials or IAM role
ses_client = boto3.client("ses", region_name="ap-south-1")  # Change region if needed

@app.post("/send-email")
async def send_email(request: EmailRequest):
    try:
        response = ses_client.send_email(
            Source="your-verified-email@example.com",   # Must be verified in SES
            Destination={"ToAddresses": [request.to_email]},
            Message={
                "Subject": {"Data": request.subject},
                "Body": {
                    "Text": {"Data": request.body}
                }
            }
        )
        return {"message": "Email sent successfully", "message_id": response["MessageId"]}

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ses")
async def send_email(request: EmailRequest):
    print(request)
    try:
        EmailService().send_email(
            to_email=request.to_email,
            subject=request.subject,
            message=request.message
        )
        return {"message": "Mail Sent"}
    except Exception as e:
        return {"error": str(e)}