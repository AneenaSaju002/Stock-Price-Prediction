# Meta Stock Price Prediction (GRU-LSTM Model)

This project predicts Meta Platforms Inc.'s (META/FB) future stock prices (both opening and closing values) using a hybrid deep learning model combining GRU and LSTM neural networks. It helps traders, investors, and financial analysts forecast stock trends for better decision-making.  

Key Functionalities  
1. Dual-Price Prediction  
   - Forecasts next-day opening & closing prices based on historical data.  
2. Deep Learning Architecture  
   - Uses GRU (Gated Recurrent Unit) + LSTM (Long Short-Term Memory) layers to capture time-series patterns.  
   - Prevents overfitting with Dropout layers and optimizes training with Adam.  
3. Data Processing
   - Normalizes stock prices (0-1 scale) for better model performance.  
   - Splits data into 80% training & 20% testing sets.  
4. Performance Evaluation 
   - Measures accuracy using R² score (coefficient of determination).  
   - Generates visual comparisons (Matplotlib plots) of predicted vs actual prices.  

Real-World Applications  
- Algorithmic Trading: Automate buy/sell decisions based on predictions.  
- Financial Dashboards: Integrate with tools like Streamlit for real-time insights.    
Tech Stack : Python,Keras/TensorFlow,Pandas,Matplotlib,scikit-learn
