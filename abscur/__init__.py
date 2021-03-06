from . import pred_obr
from . import trading
from . import optim
from . import alpari

# -----------------------------------------------------------------------

def get_abs_curses():
    """
    Возвращает абсолютные курсы в виде объекта Pandas.DataFrame
    Сами курсы расположены по ссылке https://docs.google.com/spreadsheets/d/1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE/edit#gid=1476745765
    """
    url = "https://docs.google.com/spreadsheets/d/1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE/export?format=csv&id=1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE&gid=1476745765"
    import pandas as pd
    data = pd.read_csv(url,decimal=',',parse_dates=[0],index_col=0,dayfirst=True)
    data.index.name = 'Date'
    return data

# -----------------------------------------------------------------------

def get_pairs_curses():
    """
    Возвращает курсы валютных пар в виде объекта Pandas.DataFrame
    Сами курсы расположены по ссылке https://docs.google.com/spreadsheets/d/1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE/edit#gid=1416147692
    """
    url = "https://docs.google.com/spreadsheets/d/1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE/export?format=csv&id=1lKtuxBLBBWX9_7_JA3M4jJ3U0nGQcla3HHyG_m7SMdE&gid=1416147692"
    import pandas as pd
    data = pd.read_csv(url,decimal=',',parse_dates=[0],index_col=0,dayfirst=True)
    data.index.name = 'Date'
    return data

# -----------------------------------------------------------------------

class PairAbsConverter:
    """
    Класс преобразования между парными курсами и абсолютными

    Свойства: 
    Pairs - список валютных пар
    Abs - список валют
    PA - матрица перехода от пар к абсолютам
    AP - матрица перехода от абсолютов к парам

    Методы:
    __init__ - конструктор
    pairs2abs - преобразование от парных курсов к абсолютным
    abs2pairs - преобразование от абсолютных курсов к парным

    """
    Pairs = None
    Abs = None
    PA = None
    AP = None
    
    def __init__(self,pars:list):
        """
        Инициализация класса преобразований между парными и абсолютными курсами

        Аргументы:
        pairs - список валютных пар

        """
        import numpy as np

        self.Pairs = pars
        
        self.Abs = []
        add2abs = lambda a: self.Abs.append(a) if a not in self.Abs else None
        for pair in self.Pairs:
            abs1,abs2 = pair[:3],pair[3:]
            add2abs(abs1)
            add2abs(abs2)

        self.AP = np.zeros((len(self.Abs),len(self.Pairs)))
        for j in range(self.AP.shape[1]):
            abs1,abs2 = self.Pairs[j][:3],self.Pairs[j][3:]
            self.AP[self.Abs.index(abs1),j] = 1     # числитель
            self.AP[self.Abs.index(abs2),j] = -1    # знаменатель

        self.PA = np.linalg.pinv(self.AP)   #  как псевдообратную

    def pairs2abs(self,P):
        """
        Преобразование из парных курсов в абсолютные

        Параметры:
        P - матрица парных курсов (столбцы - валютные пары)

        Возвращает матрицу абсолютных курсов (по столбцам валюты)
        """
        import numpy as np
        
        return np.exp(
            np.matmul(
                np.log(P),
                self.PA
            )
        )

    def abs2pairs(self,A):
        """
        Преобразование от абсолютных курсов к парным

        Параметры:
        P - матрица абсолютных курсов (столбцы - валюты)

        Возвращает матрицу парных курсов (по столбцам валютные пары)
        """
        import numpy as np
        
        return np.exp(
            np.matmul(
                np.log(A),
                self.AP
            )
        )
