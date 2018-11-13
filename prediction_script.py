"""
Code by Chaitanya Baweja
Created: 8th November
Updated: 12th November
"""
#All Import Libraries
import numpy as np # Handling matrix operations
import matplotlib.pyplot as plt #all plotting functions
import pandas as pd #reading and writing from csv
from sklearn.preprocessing import StandardScaler #for scaling data
from sklearn.neural_network import MLPRegressor #mlp regressor used for prediction
from sklearn.model_selection import train_test_split #splitting data into train and test set

#this dictionary will contain all csv data from excel
csv_data = {}

def accuracy(y, pred_y):
    """
    Function to calculate mean absolute percentage error

    Parameters
    ----------
    y : array_like (list)
        contains ground_truth
    pred_y : array_like (list)
             predictions from model
    Returns
    -------
    a float giving mean absolute percentage error

    Raises
    ------
    ZeroDivisionError
        when y has a zero
    """
    try:
        acc = sum(abs((y-pred_y)/y))/len(y)
        return (acc)*100;
    except ZeroDivisionError:
        print("Rate can't be zero", y)


def load_data(filename):
    """
    Function to load all data from csv in csv_data variable

    Parameters
    ----------
    filename : string, gives the csv filename

    Returns
    -------
    data: pandas dataframe for visualization purposes

    Raises
    ------
    IOError when file cannot be opened
    """

    try:
        data = pd.read_csv(filename)
    except IOError:
        print('Cannot open ', filename)

    #to copy all columns read in data to csv_data dictionary
    for i in list(data):
        csv_data[i] = data[i]

    return data


# we define a global StandardScaler object because we want to use the same scaling
# operation during both training and testing time
scaler = StandardScaler()

def create_training_set(training_variables_type = 4, split_percentage = 0.08):
    """
    Function to split csv data into a training X and Y and test X and Y
    Standardize features by removing the mean and scaling to unit variance

    Parameters
    ----------
    training_variables_type: int, Default 4,
                             if 1 then use training_variables_smallest
                             if 2 then use training_variables_small
                             if 3 then use training_variables_new
                             if 4 then use training_variables_large

    split_percentage: int, Default 0.08,
                      define the test set proportion
                      Example if 0.08, then training set is 92% and test set is 8%
    Returns
    ----------
    X_train: predictor data for training
    y_train: target for training
    X_test: predictor data for testin/g
    y_test: target for testing

    Raises
    ----------
    ValueError if wrong type is given as argument
    """
    global scaler

    #('Lowest Error: (', 'logistic', 'adam', 10, 0.060000000000000005, 6.550900586097088)
    #('Lowest Error: (', 'relu', 'adam', 100, 0.09999999999999999, 6.920795721270003)
    # The best that we have:
    #training_variables_new = 	['decision_gar','buy_age', 'YM', 'male']
    #('Lowest Error: (', 'relu', 'adam', 100, 0.05, 4.549973974801137)
    #('Lowest Error: (', 'relu', 'adam', 100, 0.04, 0.0004, 4.448231151896966)


    # only use phi and decision_gar as features
    training_variables_smallest = ['decision_gar']
    # use the first few features
    training_variables_small = ['dd_freq_m', 'dd_freq_q', 'dd_freq_h', 'phi', 'decision_gar']
    # experimental set of features which work quite well
    training_variables_new = 	['decision_gar','buy_age', 'YM', 'male']
    # found to produce best results even with what feels like quite some noise, additional features thus seem relevant
    training_variables_large = 	['dd_freq_m', 'dd_freq_q', 'dd_freq_h', 'phi', 'decision_gar',
                                'dd_pcode_H', 'dd_pcode_M', 'dd_pcode_L', 'fa', 'buy_age', 'YM', 'male', 'dd_sales_D',
                                'dd_scheme_no', 'yield6', 'yield12', 'yield18', 'yield24', 'yield30', 'yield36', 'yield42',
                                'yield96', 'yield102', 'yield108', 'yield114', 'yield120', 'yield126', 'yield132', 'yield138',
                                'yield144', 'yield150', 'yield156', 'yield162', 'yield168', 'yield174', 'yield180', 'yield186',
                                'yield192', 'yield198', 'yield204', 'yield210', 'yield216', 'yield222', 'yield228', 'yield234',
                                'yield240', 'yield246', 'yield252', 'yield258', 'yield264', 'yield270', 'yield276', 'yield282',
                                'yield288', 'yield294', 'yield300']

    # the training matrix which will have all features column wise, dimensions = (number of records) X (number of features)
    training_X = []
    # the ground truth or target variable containing rates, dimensions = (number of records) X 1
    training_Y = csv_data['rate']
    # assign which features to populate training_X with dependent upon type entered as argumwnt
    try:
        if training_variables_type == 1:
            training_X = csv_data['phi']
            training_variables = training_variables_smallest
        else:
            training_X = csv_data['external']
            if training_variables_type == 2:
                training_variables = training_variables_small
            elif training_variables_type == 3:
                training_variables = training_variables_new
            elif training_variables_type == 4:
                training_variables = training_variables_large
            else:
                raise ValueError('Type can only be between 1 - 4, type specified: ', training_variables_type)
    except ValueError as e:
        print(e.args)

    for i in training_variables:
        training_X = np.column_stack((training_X, csv_data[i]))

    # Standardize features by removing the mean and scaling to unit variance
    # Accuracy improved when this was done.
    scaled_X = scaler.fit_transform(training_X)

    # Split the data into two sets, of 92% training set versus 8% test set,
    # this is done to check the accuracy of the data on unseen data
    # it may make sense to also plot how the operation does on training data to measure training Accuracy
    X_train, X_test, y_train, y_test = train_test_split(scaled_X, training_Y, test_size = split_percentage, random_state = 0)

    return (X_train, X_test, y_train, y_test)

def prediction(X_train, X_test, y_train, y_test):
    """
    Function to fit a model for given

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
    """

    global scaler
    # activation = ['relu']
    # solver = ['adam']
    # alpha=np.arange(0.0001, 0.0011, 0.0001)
    # hidden_size = [10, 30, 50, 70, 100]
    # learning_rate = np.arange(0.01,0.11,0.01)
    # min_activation = ''
    # min_solver = ''
    # min_hidden_size = 0
    # min_learning_rate = 0
    # min_alpha = 0
    # min_error = 100.0
    # total_choices = len(activation)*len(solver)*len(learning_rate)*len(hidden_size)*len(alpha)
    # i = 1
    # for hidden_size_k in hidden_size:
    #     for solver_j in solver:
    #         for activation_i in activation:
    #             for learning_rate_l in learning_rate:
    #                 for alpha_m in alpha:
    #                     nn = MLPRegressor(
    #                     hidden_layer_sizes=hidden_size_k,  activation=activation_i, solver=solver_j,
    #                     learning_rate_init=learning_rate_l, shuffle=True, random_state=0, tol = 0.0001, alpha = alpha_m)
    #
    #
    #                     n = nn.fit(X_train, y_train)
    #                     predicted = nn.predict(X_test)
    #                     #fig, ax = plt.subplots()
    #                     #ax.scatter(y_test, predicted, edgecolors=(0, 0, 0))
    #                     #ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    #                     #ax.set_xlabel('Measured')
    #                     #ax.set_ylabel('Predicted')
    #                     #plt.show()
    #                     acc = accuracy(y_test,predicted)
    #                     if min_error>acc:
    #                         min_error = acc
    #                         min_activation = activation_i
    #                         min_solver = solver_j
    #                         min_hidden_size = hidden_size_k
    #                         min_learning_rate = learning_rate_l
    #                         min_alpha = alpha_m
    #                     i+=1
    #                     print('Prediction Error', i, ' / ', total_choices, ' (',activation_i, solver_j, hidden_size_k, learning_rate_l, alpha_m, acc)
    #                     print('Lowest Error: (',min_activation, min_solver, min_hidden_size, min_learning_rate, min_alpha, min_error)

    min_activation = 'relu'
    min_solver = 'adam'
    min_hidden_size = 70
    min_learning_rate = 0.05
    min_alpha = 0.0008
    nn = MLPRegressor(
    hidden_layer_sizes=min_hidden_size, activation=min_activation, solver=min_solver,
    learning_rate_init=min_learning_rate, shuffle=True, random_state=0, tol = 0.0001, alpha = min_alpha)
    n = nn.fit(X_train, y_train)
    ['dd_freq_m', 'dd_freq_q', 'dd_freq_h', 'phi', 'decision_gar',
                                'dd_pcode_H', 'dd_pcode_M', 'dd_pcode_L', 'fa', 'buy_age', 'YM', 'male', 'dd_sales_D',
                                'dd_scheme_no', 'yield6', 'yield12', 'yield18', 'yield24', 'yield30', 'yield36', 'yield42',
                                'yield96', 'yield102', 'yield108', 'yield114', 'yield120', 'yield126', 'yield132', 'yield138',
                                'yield144', 'yield150', 'yield156', 'yield162', 'yield168', 'yield174', 'yield180', 'yield186',
                                'yield192', 'yield198', 'yield204', 'yield210', 'yield216', 'yield222', 'yield228', 'yield234',
                                'yield240', 'yield246', 'yield252', 'yield258', 'yield264', 'yield270', 'yield276', 'yield282',
                                'yield288', 'yield294', 'yield300']

    external = np.array([0]*9999)
    dd_freq_m = np.array([0]*9999)
    dd_freq_q = np.array([0]*9999)
    dd_freq_h = np.array([0]*9999)
    dd_pcode_H = np.array([0]*9999)
    dd_pcode_M = np.array([1]*9999)
    dd_pcode_L = np.array([0]*9999)
    fa = np.array([0]*9999)
    dd_sales_D = np.array([0]*9999)
    dd_scheme_no = np.array([1]*9999)
    yield6 = np.array([4.66]*9999)
    yield12 = np.array([4.71]*9999)
    yield18 = np.array([4.71]*9999)
    yield24 = np.array([4.71]*9999)
    yield30 = np.array([4.71]*9999)
    yield36 = np.array([4.7]*9999)
    yield42 = np.array([4.69]*9999)
    yield48 = np.array([4.69]*9999)
    yield54 = np.array([4.68]*9999)
    yield60 = np.array([4.67]*9999)
    yield66 = np.array([4.66]*9999)
    yield72 = np.array([4.64]*9999)
    yield78 = np.array([4.63]*9999)
    yield84 = np.array([4.62]*9999)
    yield90 = np.array([4.61]*9999)
    yield96 = np.array([4.6]*9999)
    yield102 = np.array([4.58]*9999)
    yield108 = np.array([4.57]*9999)
    yield114 = np.array([4.56]*9999)
    yield120 = np.array([4.55]*9999)
    yield126 = np.array([4.54]*9999)
    yield132 = np.array([4.53]*9999)
    yield138 = np.array([4.51]*9999)
    yield144 = np.array([4.5]*9999)
    yield150 = np.array([4.49]*9999)
    yield156 = np.array([4.48]*9999)
    yield162 = np.array([4.47]*9999)
    yield168 = np.array([4.46]*9999)
    yield174 = np.array([4.45]*9999)
    yield180 = np.array([4.44]*9999)
    yield186 = np.array([4.42]*9999)
    yield192 = np.array([4.41]*9999)
    yield198 = np.array([4.4]*9999)
    yield204 = np.array([4.38]*9999)
    yield210 = np.array([4.37]*9999)
    yield216 = np.array([4.36]*9999)
    yield222 = np.array([4.34]*9999)
    yield228 = np.array([4.33]*9999)
    yield234 = np.array([4.31]*9999)
    yield240 = np.array([4.3]*9999)
    yield246 = np.array([4.28]*9999)
    yield252 = np.array([4.27]*9999)
    yield258 = np.array([4.25]*9999)
    yield264 = np.array([4.24]*9999)
    yield270 = np.array([4.22]*9999)
    yield276 = np.array([4.21]*9999)
    yield282 = np.array([4.2]*9999)
    yield288 = np.array([4.18]*9999)
    yield294 = np.array([4.17]*9999)
    yield300 = np.array([4.15]*9999)
    phi = np.arange(100,1000000, 100)
    #print phi.shape
    buy_age = np.array([60]*9999)
    YM = np.array([2006.583]*9999)
    male = np.array([1]*9999)
    decision_gar_0 = np.array([0]*9999)
    decision_gar_5 = np.array([5]*9999)
    decision_gar_10 = np.array([10]*9999)
    # ['dd_freq_m', 'dd_freq_q', 'dd_freq_h', 'phi', 'decision_gar',
    #                         'dd_pcode_H', 'dd_pcode_M', 'dd_pcode_L', 'fa', 'buy_age', 'YM', 'male', 'dd_sales_D',
    #                         'dd_scheme_no', 'yield6', 'yield12', 'yield18', 'yield24', 'yield30', 'yield36', 'yield42',
    #                         'yield96', 'yield102', 'yield108', 'yield114', 'yield120', 'yield126', 'yield132', 'yield138',
    #                         'yield144', 'yield150', 'yield156', 'yield162', 'yield168', 'yield174', 'yield180', 'yield186',
    #                         'yield192', 'yield198', 'yield204', 'yield210', 'yield216', 'yield222', 'yield228', 'yield234',
    #                         'yield240', 'yield246', 'yield252', 'yield258', 'yield264', 'yield270', 'yield276', 'yield282',
    #                         'yield288', 'yield294', 'yield300']

    plot_variables_0 = [dd_freq_m, dd_freq_q, dd_freq_h, phi, decision_gar_0,
                        dd_pcode_H, dd_pcode_M, dd_pcode_L, fa, buy_age, YM, male, dd_sales_D,
                        dd_scheme_no, yield6, yield12, yield18, yield24, yield30, yield36, yield42,
                        yield96, yield102, yield108, yield114,  yield120, yield126, yield132, yield138,
                        yield144, yield150, yield156, yield162, yield168, yield174, yield180, yield186,
                        yield192, yield198, yield204, yield210, yield216, yield222, yield228, yield234,
                        yield240, yield246, yield252, yield258, yield264, yield270, yield276, yield282,
                        yield288, yield294, yield300]
    plot_variables_5 = [dd_freq_m, dd_freq_q, dd_freq_h, phi, decision_gar_5,
                        dd_pcode_H, dd_pcode_M, dd_pcode_L, fa, buy_age, YM, male, dd_sales_D,
                        dd_scheme_no, yield6, yield12, yield18, yield24, yield30, yield36, yield42,
                        yield96, yield102, yield108, yield114,  yield120, yield126, yield132, yield138,
                        yield144, yield150, yield156, yield162, yield168, yield174, yield180, yield186,
                        yield192, yield198, yield204, yield210, yield216, yield222, yield228, yield234,
                        yield240, yield246, yield252, yield258, yield264, yield270, yield276, yield282,
                        yield288, yield294, yield300]
    plot_variables_10 = [dd_freq_m, dd_freq_q, dd_freq_h, phi, decision_gar_10,
                        dd_pcode_H, dd_pcode_M, dd_pcode_L, fa, buy_age, YM, male, dd_sales_D,
                        dd_scheme_no, yield6, yield12, yield18, yield24, yield30, yield36, yield42,
                        yield96, yield102, yield108, yield114,  yield120, yield126, yield132, yield138,
                        yield144, yield150, yield156, yield162, yield168, yield174, yield180, yield186,
                        yield192, yield198, yield204, yield210, yield216, yield222, yield228, yield234,
                        yield240, yield246, yield252, yield258, yield264, yield270, yield276, yield282,
                        yield288, yield294, yield300]
    X_plot_0 = external
    X_plot_5 = external
    X_plot_10 = external

    for i in plot_variables_0:
        X_plot_0 = np.column_stack((X_plot_0, i))
    for i in plot_variables_5:
        X_plot_5 = np.column_stack((X_plot_5, i))
    for i in plot_variables_10:
        X_plot_10 = np.column_stack((X_plot_10, i))

    X_plot_0 = scaler.transform(X_plot_0)
    X_plot_5 = scaler.transform(X_plot_5)
    X_plot_10 = scaler.transform(X_plot_10)

    plot_prediction_0 = nn.predict(X_plot_0)
    plot_prediction_5 = nn.predict(X_plot_5)
    plot_prediction_10 = nn.predict(X_plot_10)
    count = 0
    #print plot_prediction_0
    for i in np.arange(len(plot_prediction_0)):
        if (plot_prediction_0[i] < plot_prediction_5[i]) or (plot_prediction_5[i] < plot_prediction_10[i]):
                count+=1

    print("Count: "+str(count)+" out of "+str(len(plot_prediction_0)))

    fig, ax = plt.subplots()
    ax.plot(phi, plot_prediction_0,label = 'decision_0')
    ax.plot(phi, plot_prediction_5,label = 'decision_5')
    ax.plot(phi, plot_prediction_10,label = 'decision_10')
    ax.legend(loc='best')
    #ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel('phi')
    ax.set_ylabel('Predicted')
    plt.show()

    # n = nn.fit(X_train, y_train)
    # predicted = nn.predict(X_test)
    # fig, ax = plt.subplots()
    # ax.scatter(y_test, predicted, edgecolors=(0, 0, 0))
    # ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    # ax.set_xlabel('Measured')
    # ax.set_ylabel('Predicted')
    # plt.show()
    # acc = accuracy(y_test,predicted)




# load_data("data_JMP_impute.csv")
# (X_train, X_test, y_train, y_test) = create_training_set()
# #print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# prediction(X_train, X_test, y_train, y_test)
