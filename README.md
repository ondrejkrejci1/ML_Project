# **AI Decathlon Predictor**

This project is an advanced web application based on machine learning that predicts the total score in a decathlon based on selected events.

## **What is the project about?**

The application addresses a real-world problem faced by athletes and coaches—how specific performances affect the overall result. Unlike standard calculators that use static tables, this system employs a Gradient Boosting Regressor trained on historical data from thousands of decathlons.

### **Key Features:**

* **Dynamic Discipline Selection:** The user can select 3 to 5 disciplines on which to base the prediction.  
* **Ensemble Learning:** The system does not use a single model but averages the results of 10 independently trained models for maximum stability and error elimination.  
* **Intelligent Caching:** Trained models are serialized to disk. When the same combination of disciplines is selected again, the model loads instantly without the need for retraining.

### **Data Collecting & Preparation**
The training data for this project was gathered using a custom-built Python web scraper. The data was extracted directly from decathlon2000.com, a comprehensive portal dedicated to recording, displaying, and informing about the world of decathlon.

Once the raw data was collected, it underwent a rigorous cleaning and transformation process to ensure the highest possible accuracy and reliability of the machine learning model. First, all records containing incomplete data or 'DNF' (Did Not Finish) flags were completely removed from the dataset. Following this, a strict outlier filter was applied to prevent the model from learning from impossible anomalies or typographical errors in the source data. Specifically, any record containing a performance better than the all-time decathlon world best for that specific event was discarded.

## **Installation and Setup**

### 1\. **Prerequisites**

Make sure you have Python 3.9 or newer installed.

### **2\. Installing libraries**

In the project’s root directory, open a terminal and install the necessary dependencies:  

`pip install pandas scikit-learn streamlit joblib numpy`

### **3\. Data Preparation**

Make sure you have a file named `data_complete.csv` in the `data/` folder. You can edit the file paths and the list of disciplines in config.json.

### 

### **4\. Launching the app**

You run the app using the Streamlit framework in the console:

`streamlit run app.py`

## **Structure of project**

ML\_Project/  
├── data/  
├── saved\_models/  
├── src/  
│   ├── data\_loader.py  
│   ├── ml\_engine.py  
│   └── view.py  
├── config.json  
└── app.py



