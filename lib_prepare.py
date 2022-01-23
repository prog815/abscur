# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def windowTransformWithAllDays(inp_df,window):
    '''
    Оконное преобразование 
    
    Дополнительно в процессе оконного преобразования переходит к полному числу календарных дней.
    Пустоты заполняется NaN.
    Затем стандартное оконное преобразование.
    Затем возврат к рабочим дням поданым на входе.
    
    Параметры:
    inp_df - DataFrame подлежащий оконному преобразованию
    window - размер окна преобразования
    
    Возращает:
    DataFrame с числом столбцов большем в число раз равному размеру окна
    '''
    inp = inp_df.values
    ind = inp_df.index.values

    ext_ind = pd.to_datetime(pd.date_range(ind[0],ind[-1])).values
    df = pd.DataFrame(index=ext_ind,columns=inp_df.columns)
    df.loc[ind,:] = inp

    res_df = pd.DataFrame(index=ext_ind)
    columns = []
    for w in range(window):
        res_df = pd.concat([res_df,df.shift(w)],axis=1)
        columns += [str(col) + '_' + str(w) for col in df.columns]
    res_df.columns = columns
    return res_df.loc[ind,:]

# windowTransformWithAllDays(d_data,2)



class PrepData:
    X = None # массив входов уже в окне трехмерный (id,window,feature_inp)
    Y = None # массив выходов для соответствующего входа двумерная (id,feature_out)
    
    window = None
    train_len = None
    val_len = None
    test_part = None
    
    all_len = None
    learn_len = None
    test_len = None
    
    def __init__(self,X,Y,window,train_len,val_len,test_part=0.3,**others):
        """создание класса источника данных для модели прогнозирования"""
        
        assert window > 1
        assert train_len > 10
        assert val_len > 1
        assert X.shape[0] == Y.shape[0]
        
        # выход сразу сдвигаем назад (для прогноза)
        self.Y = pd.DataFrame(Y,copy=True).shift(-1).values
        
        # вход гусеницей раскладываем по окну
        self.X = np.ones((X.shape[0],window,X.shape[1]))
        d = pd.DataFrame(X,copy=True)
        for n in range(window):
            self.X[:,n,:] = d.shift(n).values
        
        self.test_part, self.window, self.train_len, self.val_len  = test_part,window,train_len,val_len
        
        self.all_len = X.shape[0]
        self.test_len = int(self.all_len * test_part)
        self.learn_len = self.all_len - self.test_len - 1 # на одну (последнюю после теста calc-строку) меньше
        
        assert self.train_len + self.window + self.val_len < self.learn_len
    
    def get_rand_learn_vib(self):
        """извлечение случайной выборки для обучения модели"""
        top = self.learn_len - self.val_len
        bot = self.window + self.train_len
        rnd = np.random.randint(bot,top)
        
        X_train = self.X[rnd-self.train_len:rnd,...]
        Y_train = self.Y[rnd-self.train_len:rnd,...]
        
        X_val = self.X[rnd:rnd+self.val_len,...]
        Y_val = self.Y[rnd:rnd+self.val_len,...]
        
        return X_train, Y_train, X_val, Y_val
    
    def get_last_learn_vib(self):
        """последняя выборка для генерации прогноза на завтра"""
        X_train = self.X[-self.train_len-1:-1,...]
        Y_train = self.Y[-self.train_len-1:-1,...]
        
        X_calc = self.X[-1,...].reshape(1,self.window,-1)
        
        return X_train, Y_train, X_calc
    
    def progon(self):
        """Генератор для прогона модели по всей выборке"""
        for n in range(0,self.all_len-1-self.val_len,self.val_len):
            X_train = None
            Y_train = None
            
            if n > self.train_len + self.window:
                X_train = self.X[n-self.train_len:n,...]
                Y_train = self.Y[n-self.train_len:n,...] 
            
            X_val = self.X[n:n+self.val_len,...]
            Y_val = self.Y[n:n+self.val_len,...]
            
            yield X_train, Y_train, X_val, Y_val

# data = PrepData(
#     X = dClose.values,
#     Y = dClose.values,
#     window = 5,
#     train_len = 500,
#     val_len = 10,
#     test_part = 0.25
# )

def data_to_window(data,window):
    wData = np.ones((data.shape[0],window,data.shape[1]))
    d = pd.DataFrame(data)
    for n in range(window):
        wData[:,n,:] = d.shift(n).values
    return wData

# print('test - data_to_window')
# data = np.random.rand(10,2)
# res = data_to_window(data,3)
# res.shape

def date_to_input(dateIndex):
    days = dateIndex.day.values
    weekdays = dateIndex.weekday.values
    months = dateIndex.month.values
    x2sc = lambda x,per: np.transpose([np.sin(x/per*2*np.pi),np.cos(x/per*2*np.pi)])
    inputData = np.hstack([x2sc(days,31),x2sc(weekdays,7),x2sc(months,12)])
    return inputData

# print('test - date_to_input')
# date_to_input(pd.date_range('2021-09-14',periods=5))

def split_learn_calc(*inps,gorizont=1):
    res = []
    
    for inp in inps:
        inp1 = inp.copy()
        inp1[gorizont:,...] = inp1[:-gorizont,...]
        inp1[0,...] = np.nan
        res.append(inp1)
        
    for inp in inps:
        res.append(np.array([inp[-1,...]]))
        
    return res

# print('test - split_learn_calc')
# split_learn_calc(np.random.rand(10,2),np.random.rand(10,1)+10)

def chistim_pustoty(*inps):
    
    index = []
    for inp in inps:
        axis = tuple(range(1,len(inp.shape)))
        index.append(np.all(~np.isnan(inp),axis=axis))
    index = np.all(np.array(index),axis=0)
    return tuple([inp[index,...] for inp in inps])

# print('test - chistim_pustoty')
# data1 = np.random.rand(10,3,2)
# data1[6,0,1] = np.nan
# data2 = np.random.rand(10,1)
# data2[1,0] = np.nan
# data3 = pd.date_range('2021-09-14',periods=10)
# [v.shape for v in chistim_pustoty(data1,data2,data2,data3.values[:,np.newaxis])]

def learn_val_random_vib(*inps,learnVibLen,valVibLen):
    startLearn = np.random.randint(inps[0].shape[0] - learnVibLen - valVibLen)
    startVal = startLearn + learnVibLen
    
    res = []
    
    for inp in inps:
        res.append(inp[startLearn:(startLearn+learnVibLen),...])
        res.append(inp[startVal:(startVal+valVibLen),...])
    
    return tuple(res)


def df_cols_to_num(df,*col_names):
    """ преобразование строки в число
    """
    for fld in col_names:
        try:
            df[fld] = pd.to_numeric(df[fld].str.replace(',','.'),errors='coerce')
        except:
            pass
    return

def df_cols_to_date(df,*col_names):
    """ преобразование строки в дату
    """
    for fld in col_names:
        try:
            df[fld] = pd.to_datetime(df[fld],errors='coerce')
        except:
            pass
    return

def df_cols_as_object(df,*col_names):
    """ пеервод в категориальный вид
    """
    for fld in col_names:
        try:
            df[fld] = df[fld].astype('object')
        except:
            pass
    return


def df_col_report(df):
    """Отчет по столбцам
    """
    resRep = []
    for colName in df.columns:
        col = df[colName]
        resRep.append([colName,col.dtype,len(col.unique()),col.unique()[:8]])
    return pd.DataFrame(resRep,columns=['Поле','тип','число уникальных','пример'])

def df_hist_report(df):
    import matplotlib.pyplot as plt
    k = 1
    names = []
    clmns = 3
    rows = int(1+len(df.columns)/clmns)
    plt.figure(figsize=(22,5*rows))
    for colName in df.columns:
        col = df[colName]
        vls = col.unique()
        x = [str(v) for v in col.value_counts().index]
        h = list(col.value_counts().values)

        if len(x) > 1:
            plt.subplot(rows,clmns,k)
            k += 1
            if len(x) > 3:
                names.append(colName)

            if col.dtype.name == 'object':
                col.value_counts()[:15].plot.barh()
                # plt.xticks(rotation=30)

            else:

                pd.to_numeric(col,errors='coerce').hist(bins=min(100,len(x)))
            plt.title(f'<{colName}> - uniq: {len(vls)}')
    plt.tight_layout()
    plt.show()
    return
