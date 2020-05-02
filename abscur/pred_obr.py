import numpy as np

def exp_sglaj(X,alpha=0.9):
    """ 
        Вычисляет экспоненциальное сглаживание от ряда
        X - ряд данных
        alpha - коэффициент сглаживания
    """
    res = np.array(X)
    for i in range(1,len(X)):
        res[i] = alpha*res[i] + (1-alpha)*res[i-1]
    return res
