# ⚙️ Smart Rental Tracking System – Backend Services

> Powering the **Caterpillar Digital Hackathon-winning solution** with scalable APIs, predictive ML models, and AWS integrations.
> This backend orchestrates the core functionality behind the **Smart Rental Tracking System**, enabling dealers to manage fleets, track operators, and forecast demand with real-time intelligence.

---

## 📌 Overview

The backend is the **engine** of the Smart Rental Tracking System, providing:

* Robust **Express.js REST APIs** for dealer dashboards, operators, and inventory management.
* A dedicated **Python ML FastAPI service** for demand forecasting, rental return prediction, and efficiency scoring.
* **AWS-integrated services** for notifications and secure resource management.
* Database and IoT integrations to ensure high availability, scalability, and traceability.

This repo complements the [Frontend WebApp (Next.js)](https://github.com/Krishnanshu-Khanna/EquiTrack-CAT-Hackathon-WebPage-Nextjs) and serves as the central point for backend logic.

---

## 🛠️ Tech Stack

### Node.js Backend (Root Folder)

* [Express.js](https://expressjs.com/) – REST API framework
* [MongoDB](https://www.mongodb.com/) – Dealer, operators, and fleet data
* [AWS SES](https://aws.amazon.com/ses/) – Dealer email notifications
* [Boto3](https://boto3.amazonaws.com/) / [Botocore](https://botocore.amazonaws.com/) – AWS integration
* [JWT](https://jwt.io/) – Secure authentication

### Python ML Backend (`./pythonBackend`)

* [FastAPI](https://fastapi.tiangolo.com/) – High-performance API service
* [TensorFlow](https://www.tensorflow.org/) – Deep Neural Networks for rental return prediction
* [Scikit-learn](https://scikit-learn.org/) – Predictive analytics and preprocessing
* [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) – Time-series and tabular data handling
* [Uvicorn](https://www.uvicorn.org/) – ASGI server for FastAPI

---

## 🚀 Key Backend Features

* 📊 **Dealer API Services** – CRUD operations for dealers, operators, and inventory.
* 🛰️ **GPS & IoT Integration** – Secure zone validation and RFID-based theft detection.
* 🔮 **Rental Return Predictor** – TensorFlow DNN predicting return timelines.
* 🤖 **LLM-Based Demand Forecasting** – Natural language-enhanced prediction service.
* ⚡ **Efficiency Scoring Engine** – Operator and client efficiency metrics from daily logs.
* 📧 **AWS SES Email Alerts** – Real-time dealer notifications.

---


## ⚡ Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/Krishnanshu-Khanna/EquiTrack-CAT-Hackathon-Backend-Node.git
cd EquiTrack-CAT-Hackathon-Backend-Node
```

### 2. Start Express.js Server

```bash
npm install
npm run start
```

This launches the dealer-facing backend APIs.

### 3. Start ML FastAPI Server

```bash
cd pythonBackend
pip install -r requirements.txt
uvicorn main:app --reload
```

This launches the ML prediction service.

---

## 📸 Backend Screenshots

1. 🛰️ **GPS & IoT Safe Zone Validation**
![WhatsApp Image 2025-09-24 at 20 24 44_77040b87](https://github.com/user-attachments/assets/e0061c68-9aaf-42a9-a321-22468c58ac56)

2. 🔮 **ML-Based Rental Forecasting Logs**
![WhatsApp Image 2025-09-24 at 20 24 44_202273b5](https://github.com/user-attachments/assets/7153699b-a7f4-402e-ade7-9aa3518da768)

3. 📊 **API Response Samples (Postman Collection)**
   Stock prediction 
<img width="1513" height="713" alt="image" src="https://github.com/user-attachments/assets/9f7ed835-fcd3-4d2e-baf6-99032b4193e1" />
Client efficiency 
<img width="1512" height="718" alt="image" src="https://github.com/user-attachments/assets/bd5ec032-ea06-45b6-bad3-0c6d806647a3" />


---

## 🙌 Acknowledgements

* Developed during the **Caterpillar Digital Hackathon** 🏆
* Backend built to scale with **ML, IoT, and AWS-first principles**
* Thanks to the hackathon mentors, judges, and team contributors.

---

## Contributors

<a href="https://github.com/Krishnanshu-Khanna/EquiTrack-CAT-Hackathon-Backend-Node/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Krishnanshu-Khanna/EquiTrack-CAT-Hackathon-Backend-Node" />
</a>
