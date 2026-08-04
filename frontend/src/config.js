// Config file to define API URL dynamically depending on local development or production.
export const API_BASE_URL = 
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : 'https://employee-attrition-prediction-4-1xie.onrender.com';
