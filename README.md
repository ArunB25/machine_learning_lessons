# machine_learning_lessons
**Tasks undertaken to learn about machine learning**

## Linear Regression
### **house_price_predictions.py**
1. Load in the California house pricing data and unpack the features and labels
2. Import a linear regression model from sklearn
3. Fit the model
4. use test values of house features and predict it's price
5. Compute the score of the model on the training data
6. Compute the score of the model on the training data

---

### **best_dataset.py**
1. Find 3 sklearn regression datasets
2. Write a loop which fits a linear regression model for each dataset and saves its score
3. Take a quick look at what the score actually represents

The make_regression always achieves a perfect score of 1 as its a curated data set made for linear regression, The California house data set achieves a score of 0.606 and the diabetes dataset with 0.518 showing that this linear regression model would make better prdictions on the california housing data set than it would with the diabetes one.

---

### **best_model.py**
1. Train at least 3 different sklearn regression models on a dataset
2. Repeat the experiment for at least 3 different regression datasets
3. For each data set record 
    1. The score
    2. Time taken to fit
    3. Time taken to predict on the whole training set
    4. The size of the model occupied in memory (look up how to do that)

This script compares a several individual features from the califronia housing dataset with 3 different regression models. For each feature a subplot is created with 3 plots one for each regression model, displaying plots of the training data with the models hypothesis and the predictions of the test data with the real values. The models score, time taken to fit and predict as well as the models size is also shown in the titles of each subplot. This script shows the performance of the 3 selected models for each feature, it also shows what features are more suitable to predict house prices.

---

### **linear_regression_from_scratch.py**
This script is a culminataion of many tasks to learn about linear regression by creating it from scratch, and optimising the model with various techniques

Basic outline of construction of the script
1. Load in the California dataset for testing and debugging
2. Create a class called LinearRegression
3. Randomly initialise two attributes for the weight and bias
4. Create a .predict method which takes in some data and returns a linear prediction
5. Create a .fit_analytical method which computes the analytical solution
6. Create a .fit method which uses gradient descent to optimise the model
7. Compare created model to SKlearns linear regression model

### **Topics carried out to learn about and improve the model**
#### **Gradient Decent**  
Break down of the algorithm
1. Make predictions Ypred = WX + b
2. Evaluate Loss L = 1/m[ (Ypred - Y)^2 ]
3. Differentiate loss with respect to parameters, to find vector of maximum increase in loss

Derivation to of loss with respect to weights
    
    L = 1/m[ (Ypred - Y)^2 ]  Loss calculation
    L = 1/m[ (WX + b - Y)^2 ]
    L = 1/m[ (WX + b - Y)(WX + b - Y) ]
    L = 1/m[ (WX)^2 +WXb - WXY + WXb + b^2 - Yb - WXY - Yb + Y^2 ]
    L = 1/m[ (WX)^2 +2WXb - 2WXY + b^2 - 2Yb + Y^2 ]
    dL/dW = 1/m[ 2W(X^2) + 2Xb - 2XY ]
    dL/dW = 1/m[ 2X(WX + b - y) ]
    dL/dW = 1/m[ 2X(Ypred - y) ]

4. Update parameters in opposite diection to increase in loss and multiply by learning rate to avoid divergence 

    W = W - dl/dw*(learning rate)

5. Repeat for n itterations

#### **Mini batching**
It can be very time consuming performing gradient decent calculations for the entire training data set every itteration. Mini batching invloves splitting the training data (full batch) up into smaller equally sized subsets (mini batches) which will be evalued over each epoch (on pass of entire training data). This process ensures that there will be enough memory free for the calculations if there is a very large training set.

#### **Hyper parameter optimisation**
To find the optimal hyperparameters cross validation was use with a grid search. So that the model doesnt over fit, cross validation was used, this is when the training data is split up into training data and valdiation data which is used to attain the score of the test. In this case, the training data was split into 5 even subsets, then each one is used to train the data and the other 4 is used to validate it and get a score. This is repeated for all 5 subsets with each one having a turn to train the model whilst the others validate the results. This process is repeated in the grid seach which tests every possible combination of a list of pramaters to assertain the optima hyperparameters for the dataset.

#### **Bias and Variance**

Bias is when the average of the difference between the predicted parameters and true parameters of the training set. This represents how well the model is trained on the training set and could indicate if the capacity of the model could be increased.

Variance is when you expect the predicted best parameters to be different from their average value. This represents how the model may vary with different datasets to see if the model is overfitting.

https://www.youtube.com/watch?v=EuBBz3bI-aA


---
### **Regularization-Experiments.py**

Regularizing a polynomial model's capacity

1. create a (20 by 1) matrix of random x values between 0 and 1
    these will be our design matrix (20 examples, 1 feature)
2. defing some function which takes in those single feature examples and returns a new design matrix with an extra column representing the x-squared values
3. generalise this function to be able to return you features which are powers of x up to some number
4. define a function which computes a label such as y = 2 + x + 0.2*x^2 + 0.1*x^2
5. visualise this on a X-Y graph and play around with the coefficients until you get a function that is not too boring (linear)
6. split the data into train and val
7. fit a model to these labels, firstly just passing your model the original features (x^1)
8. visualise the predictions against the label
9. you should see that the model is underfit
10. now train a series of models on design matrix that contain sequentially increasing powers of x
11. include powers of x way above those which your labels are based on
e.g. go up to features where x^12 is included
12. the models trained on these should overfit the data (easy to do if you make the train set small)
13. grid search over the capacity hyperparam (which power of x is included) to evaluate each model on the train and val set
14. dicsuss: what were the results?"