# VIVA Preparation Guide 🎓

Here are beginner-friendly answers to help you prepare for a Data Science / Machine Learning project VIVA or interview!

### 1. What is regression?
Regression is a type of Machine Learning where the goal is to predict a **continuous number** (like price, temperature, or salary). This is different from Classification, which predicts a category (like "Spam" or "Not Spam").

### 2. Why is this a regression problem?
We are predicting the **Car Selling Price**. Because price is a continuous number (e.g., $15,000 or $15,001.50) and not a fixed category, this is fundamentally a regression problem.

### 3. What is Linear Regression?
Linear Regression is one of the simplest algorithms. It tries to draw a straight "line of best fit" through the data points so that the distance between the line and the actual data points is as small as possible. 

### 4. What is Random Forest?
A Random Forest is an "ensemble" algorithm. Instead of building one decision tree, it builds many (a forest of) decision trees. Each tree looks at a random subset of data and makes a price prediction. The final prediction is just the average of what all the individual trees predicted. It is very powerful and highly resistant to overfitting!

### 5. What is overfitting?
Overfitting happens when a model essentially "memorizes" the training data but fails to understand the actual underlying patterns. Because it memorized the training data, it performs incredibly well during training but does a terrible job when predicting on new, unseen test data.

### 6. What is train-test split?
Train-test split is how we evaluate our model. We hide a portion of our data (e.g., 20%) from the model and use the remaining 80% to "teach" (train) it. Once it's trained, we test it on that hidden 20% to see how it performs in the real world. 

### 7. What is MAE?
**Mean Absolute Error (MAE)** tells us, on average, how far off our predictions are. If the MAE is 3.5, it means our predicted car prices are, on average, off by $3,500 from the actual price. Lower is better.

### 8. What is RMSE?
**Root Mean Squared Error (RMSE)** is similar to MAE, but it squares the errors before averaging them. This heavily penalizes the model for making huge mistakes. If the model makes one massive prediction error, the RMSE will shoot up. Lower is better.

### 9. What is R²?
**R-Squared (R²)** tells us the "goodness of fit." It represents the percentage of the car price that can be explained by our inputs (like Engine Size, MPG, etc.). An R² of 0.86 means our model explains 86% of the factors that affect the car's price! Closer to 1.0 is better.

### 10. Why can't we use only R²?
R² tells us how well the model "fits" the data, but it doesn't give us the error in actual dollars. A model might have a high R², but the MAE could still reveal that the predictions are off by thousands of dollars. We need MAE/RMSE to understand the real-world financial error.

### 11. What is data leakage?
Data leakage happens when you accidentally give the model access to information during training that it wouldn't have in the real world. In our project, if we kept `Min.Price` and `Max.Price` in the dataset, the model would cheat by using them to guess the exact `Price`.

### 12. Why do we encode categorical variables?
Machine learning math requires numbers. Algorithms cannot multiply or add words like "Sporty" or "Compact." We use techniques like One-Hot Encoding to convert these text categories into binary columns (1s and 0s) so the math works.

### 13. Why do we save the preprocessing pipeline?
During training, we calculated the 'median' for missing values and the 'mean/scale' for StandardScaler. When a new user inputs their car details in the frontend, we must use those *exact same mathematical rules* to prepare their input. By saving the pipeline, we guarantee consistency and prevent errors.

### 14. Why use FastAPI?
FastAPI is a modern, ultra-fast Python framework for building web APIs. It is highly favored in Data Science because it naturally supports asynchronous code, handles data validation automatically via Pydantic, and creates self-documenting APIs out of the box.

### 15. How does React communicate with FastAPI?
React uses a browser feature called `fetch` (or Axios) to send an HTTP request to FastAPI over a network port (e.g., `localhost:8000`). It sends the car details inside a JSON packet. FastAPI reads the JSON, processes it, and sends a JSON response back to React.

### 16. How does the final prediction happen?
1. The user types car details into the React frontend and clicks predict.
2. React sends this data as JSON to the FastAPI backend.
3. FastAPI loads our saved `best_model.pkl`.
4. The pipeline inside the model cleans the data and converts the text into numbers.
5. The Random Forest algorithm uses its mathematical trees to calculate a price.
6. FastAPI wraps this price in JSON and sends it back.
7. React displays the final estimated dollar amount on the screen!
