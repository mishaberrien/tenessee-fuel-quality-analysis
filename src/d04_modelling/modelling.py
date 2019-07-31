import pandas as pd
import numpy as np
import sklearn.preprocessing as preprocessing
import statsmodels.api as sm
import sys

from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE, ADASYN


def get_model_pvalue(y_train, X_train):
    logit_model = sm.Logit(y_train, X_train)
    result = logit_model.fit()
    return print('\n PValues for model parameters: \n', result.pvalues)
