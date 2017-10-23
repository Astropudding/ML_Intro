from sklearn.model_selection import KFold
import numpy as np

def stack_pred(estimator, X, y, Xt, k=3, method='predict'):

    X = np.array(X)
    y = np.array(y)

    sX = np.zeros(X.shape[0])
    sXt = []

    kf = KFold(n_splits = k, shuffle = True, random_state = 2)
    for result in kf.split(X):
        model = estimator.fit(X[result[0]], y[result[0]])
        sX[result[1]] = model.predict(X[result[1]])
        sXt.append(model.predict(Xt))

    sXt = sum(sXt)/len(sXt)

    return sX, sXt
