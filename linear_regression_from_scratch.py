from cmath import nan
from ctypes import sizeof
from random import uniform
from turtle import color, title
from unittest import result
from sklearn import datasets , model_selection, linear_model,metrics
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import time
from itertools import product
import pandas as pd
from statistics import mean


class linear_regression():
    def __init__(self, n_features : int):
        '''
        creates a model with random wight and bias values
        '''
        np.random.seed(10)
        self.weight = np.random.randn(n_features, 1) ## randomly initialise weight
        self.bias = np.random.randn(1) ## randomly initialise bias

    def predict(self,X):
        '''
        Get a prediction from a set of features based on the weights and bias of the model
        '''
        ypred = np.dot(X, self.weight) + self.bias
        return ypred # return prediction

    def score(self,X,y_true,round_to = 4):
        y_pred = self.predict(X)
        # u  = ((y_true - y_pred)** 2).sum()
        # v = ((y_true - y_true.mean()) ** 2).sum()
        # return round((1 - (u/v)),round_to)
        return round(metrics.mean_squared_error(y_true, y_pred),round_to)

    def fit_analytical(self, X_train, y_train):
        '''
        Analytical solution to minimise the mean squared error 
        Not advised for large multi feature datasets as finding inverse of a matrix can be computationally heavy 
        '''
        X_with_bias = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
        optimal_w = np.matmul(
        np.linalg.inv(np.matmul(X_with_bias.T, X_with_bias)),
        np.matmul(X_with_bias.T, y_train),)
        weights = optimal_w[1:]
        bias = optimal_w[0]
        return weights, bias

    def set_params(self, weights, bias):
        '''
        set the parameters manually
        '''
        self.weight = weights
        self.bias = bias

    def get_params(self,deep=False):
        return{'Weight':self.weight,'Bias':self.bias}

    def fit(self,X,y,learningrate = 0.01,iterations = 64, plot = False, batch_size = 32):
        """ Find the multivarite regression model for the data set
        Parameters:
        X: independent variables matrix
        y: dependent variables matrix
        learningrate: factor to reduce change in gradient to avoid deviation, typically between 0 and 1
        iterations: number of times the entire dataset is evaluated
        plot: display inreal time the gradient decent, only works with one parameter.
        batch_size: for mini batch processing to improve efficiency, typically a factor of 32 (32,64,128,256,...)
        Return value: the final weight and bias values
        Credit to https://medium.com/@IwriteDSblog/gradient-descent-for-multivariable-regression-in-python-d430eb5d2cd8 & https://www.geeksforgeeks.org/ml-mini-batch-gradient-descent-with-python/
        """

        def iterate_minibatches(X, y, batchsize, shuffle=True):
            '''
            reduces size of full dataset to batch size
            returns mini_batch containing all of the data broken up into batches
            '''
            assert X.shape[0] == y.shape[0]
            if shuffle:
                indices = np.arange(X.shape[0])
                np.random.seed(2) #set the random seed
                np.random.shuffle(indices)
            for start_idx in range(0, X.shape[0] - batchsize + 1, batchsize): #for every batch in data
                if shuffle:
                    excerpt = indices[start_idx:start_idx + batchsize]
                else:
                    excerpt = slice(start_idx, start_idx + batchsize) #excerpt is the in
                yield X[excerpt], y[excerpt]

        def generateXvector(X):
            """ Taking the original independent variables matrix and add a row of 1 which corresponds to x_0
                Parameters:
                Return value: the matrix that contains all the values in the dataset, not include the outcomes variables. 
            """
            vectorX = np.c_[np.ones((len(X), 1)), X]
            return vectorX

        theta = np.random.randn(len(X[0])+1, 1)
        m = len(X) #length of dataset
        if plot == True: #set up plot
            plt.ion()
            fig, ax = plt.subplots(figsize=(10, 8))
            hypothesis_line, = ax.plot(0, 0,color = 'k')
            training_data = ax.scatter(X,y,color='g', label='mini batch data',zorder=1)
            plt.scatter(X,y,color='r', label='Training Data',zorder=0)
            plt.suptitle("Gradient Decent")
            plt.legend()
        for i in range(iterations):
            for batch in iterate_minibatches(X, y, batch_size):
                X_mini, y_mini = batch
                mini_vectorX = generateXvector(X_mini) #create the parameter vector
                gradients = 2/m * mini_vectorX.T.dot(mini_vectorX.dot(theta) - y_mini) #diferentiate loss with respect to theta(weights)
                theta = theta - learningrate * gradients #move gradients in opposite direction to the increase of loss multiplied be the learning rate factor
                if plot == True:
                    hypothesis_line.set_xdata(X) #update x and y values and draw new line
                    y_pred = X.dot(theta[1:])
                    hypothesis_line.set_ydata(y_pred)
                    training_data.set_offsets(np.c_[X_mini,y_mini])
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    plt.title(f"Itteration {i} of {iterations}")

        y_pred = X.dot(theta[1:]) #calculate predictions
        loss = 1/m *sum((y_pred - y)**2)  #calculate the loss from predictions made
        self.bias = theta[0]
        self.weight = theta[1:]
        return self


    def grid_search_CV(self,X_train,y_train,learningrate_param:list = [0.001],iterations_param:list = [4], batch_size_param:list = [128],num_training_batches:int = 5):
        '''
        X_train: entire inputs training dataset
        y_train: entire outputs training dataset
        learningrate_param:learning rates to be evaluataed
        iterations_param:iterations to be evaluataed
        batch_size_param:batch sizes to be evaluataed
        num_training_batches: number of training batches

        Script breaks up training data into num_training_batches subsets to be cross validated in a grid search
        Returns dataframe of results 
        '''
        def CV_training_batches(X_train,y_train,num_training_batches):
            training_size = X_train.shape[0]//num_training_batches
            X_training_batches = []
            y_training_batches = []
            for start_idx in range(0, X_train.shape[0] - training_size + 1, training_size): #split the training dataset into 5 batches
                excerpt = slice(start_idx, start_idx + training_size)
                X_training_batches.append(X_train[excerpt])
                y_training_batches.append(y_train[excerpt])
            return X_training_batches,y_training_batches

        X_training_batches,y_training_batches = CV_training_batches(X_train,y_train,num_training_batches)
        parameter_combinations = list(product(learningrate_param, iterations_param,batch_size_param)) #create a list of all posible parameter value combinations
        batch_indexs = range(0,num_training_batches)
        parameter_training_scores = []
        parameter_score = []
        for parameter in parameter_combinations: #for each parameter combination
            training_avg_score = []
            for training_batch in batch_indexs:#for each training batch fit the model and get the score of that batch
                lin_reg_model.fit(X_training_batches[training_batch],y_training_batches[training_batch],plot=plot_on,learningrate=parameter[0],iterations=parameter[1],batch_size=parameter[2])
                validation_scores = []
                for i in batch_indexs:
                 if i!=training_batch:
                    validation_scores.append(lin_reg_model.score(X_training_batches[i],y_training_batches[i])) 
                training_avg_score.append(mean(validation_scores))
            parameter_training_scores.append(training_avg_score)
            parameter_score.append(mean(training_avg_score))

        grid_search_results = pd.DataFrame({'Parameters':parameter_combinations,'Training Scores':parameter_training_scores,'Parameter Score':parameter_score})
        return grid_search_results.sort_values(by=['Parameter Score'])

if __name__ == "__main__":
    plot_on = False #display live plot of gradient decent and results of the 2 models 
    X, y = datasets.fetch_california_housing(return_X_y=True)
    X = X[:,0:1] ##reduce parameters to 1
    y = y.reshape((-1, 1)) #convert to column vector
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3)

    

    lin_reg_model = linear_regression(X.shape[1])

    learningrate_param = [0.01,0.001,0.0001,0.00001,0.000001] #define the parameters and values to optimise for
    iterations_param = [2,4,8,16,32,64,128,256]
    batch_size_param = [32,64,128,256,512,1024]
    grid_search_results = lin_reg_model.grid_search_CV(X_train,y_train,learningrate_param,iterations_param,batch_size_param)
    print(grid_search_results.head())

    optimum_parameters = grid_search_results['Parameters'].iloc[0]

    start_time = time.time()
    lin_reg_model.fit(X_train,y_train,plot=plot_on,learningrate=optimum_parameters[0],iterations=optimum_parameters[1],batch_size=optimum_parameters[2])
    time_to_fit = round(time.time() - start_time, 3)
    scratch_mse = round(metrics.mean_squared_error(y_test, lin_reg_model.predict(X_test)),5)
    print(f"Scratch MSE:{scratch_mse} | Time to fit {time_to_fit}s | Scratch models coefs:{lin_reg_model.weight} | Intercept:{lin_reg_model.bias}")
   
    plot_on = True
    if plot_on:
        plt.figure
        plt.subplot(2, 1, 1)
        plt.scatter(X_train,y_train ,color='g', label='Training Data',zorder=0)
        plt.plot(X_train, lin_reg_model.predict(X_train),color='b',label='Hypothesis',zorder=1)
        plt.scatter(X_test, lin_reg_model.predict(X_test),color='r',label='Predicted Test Data',zorder=2)
        plt.scatter(X_test, y_test,color='k',label='Real Test Data', marker="2",zorder=3)
        plt.ylabel('House Value')
        plt.legend()
        plt.title(f'Made from scratch Linear Regression - MSE {scratch_mse} | Time to fit {time_to_fit}s')

    start_time = time.time()
    sklearn_model = linear_model.LinearRegression().fit(X_train, y_train) #create instance of the linear regression model
    time_to_fit = round(time.time() - start_time, 3)
    sklearn_mse = round(metrics.mean_squared_error(y_test, sklearn_model.predict(X_test)),5)
    print(f"Sklearn MSE:{sklearn_mse} | Time to fit {time_to_fit}s |SKlearn coefs:{sklearn_model.coef_} | Intercept:{sklearn_model.intercept_}")
    if plot_on:
        plt.subplot(2, 1, 2)
        plt.scatter(X_train,y_train ,color='g', label='Training Data',zorder=0)
        plt.plot(X_train, sklearn_model.predict(X_train),color='b',label='Hypothesis',zorder=1)
        plt.scatter(X_test, sklearn_model.predict(X_test),color='r',label='Predicted Test Data',zorder=2)
        plt.scatter(X_test, y_test,color='k',label='Real Test Data', marker="2",zorder=3)
        plt.ylabel('House Value')
        plt.legend()
        plt.title(f'SKlearn Linear Regression - MSE {sklearn_mse} | Time to fit {time_to_fit}s')
        plt.show()