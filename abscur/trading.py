import numpy as np

# ----------------------------------------------------------------------

def sim_full_order(ohlc_df,tp=0.01,sl=0.005,dist=5):
    """
    Прогон полного ордера

    Открытие ордеров должно происходить в точке Open тика
    
    Закрытие должно происходить по достижению TakeProfit 
    (с прибылью) или StopLoss (с убытком)
    
    Параметры:
    ohlc_df - Pandas DataFrame со столбцами Open, High и Low
    tp - уровень прибыли в долях от 1-цы
    sl - уровень убытков в долях от 1-цы
    dist - максимальное кол-во тиков жизни ордера до убыточного закрытия

    Возвращает легкую копию ohlc_df с дополнительными столбцами:
    'buy_set','sell_set' - ряды ордеров на покупку и продажу. Каждый ряд содержит: 
        1 - ордер открытый в этот тик прибыльный
        0 - ордер в этот тик был убыточным
    'buy_res','sell_res' - ряды с результатами изменений отработки ордеров на покупку и продажу
    'all_res' - ряд с результатами относительных изменений одновременной отработки 
    """
    res = ohlc_df.copy(deep=False)
    
    buy_set,sell_set = get_order_set(res,tp,sl,dist)
    
    res['buy_set'] = buy_set
    res['sell_set'] = sell_set
    
    buy_res = order_res_to_profit(buy_set,tp,sl)
    sell_res = order_res_to_profit(sell_set,tp,sl)
    
    res['buy_res'] = buy_res
    res['sell_res'] = sell_res
    
    all_res = buy_res + sell_res
    
    res['all_res'] = all_res
    
    return res

# ----------------------------------------------------------------------

def get_order_set(ohlc_df,tp=0.01,sl=0.005,dist=5):
    """
    Функция считает ряды срабатывания ордеров на buy и на sell
    
    Открытие ордеров должно происходить в точке Open тика
    
    Закрытие должно происходить по достижению TakeProfit 
    (с прибылью) или StopLoss (с убытком)
    
    Параметры:
    ohlc_df - Pandas DataFrame со столбцами Open, High и Low
    tp - уровень прибыли в долях от 1-цы
    sl - уровень убытков в долях от 1-цы
    dist - максимальное кол-во тиков жизни ордера до убыточного закрытия

    Возвращает:
    (set_buy,set_sell) ряды ордеров на покупку и продажу
    
    каждый ряд содержит: 
    1 - ордер открытый в этот тик прибыльный
    0 - ордер в этот тик был убыточным
    """
    
    all_len = ohlc_df.Open.shape[0]
    
    set_buy = np.zeros((all_len))
    set_sell = np.zeros((all_len))

    for i in range(all_len-1):
        _open = ohlc_df.Open[i]
        
        # для ордера на покупку - buy
        _tp = _open*(1+tp)
        _sl = _open*(1-sl)
        for k in range(dist):
            if i+k >= all_len:
                break
            if ohlc_df.Low[i+k] <= _sl:
                break # достигли стопа
            if ohlc_df.High[i+k] >= _tp:
                set_buy[i] = 1
                break # достигли профита

        # для ордера на продажу - sell
        _tp = _open*(1-tp)
        _sl = _open*(1+sl)
        for k in range(dist):
            if i+k >= all_len:
                break
            if ohlc_df.High[i+k] >= _sl:
                break # достигли стопа
            if ohlc_df.Low[i+k] <= _tp:
                set_sell[i] = 1
                break # достигли профита

    return set_buy,set_sell

# ----------------------------------------------------------------------

def order_res_to_profit(order_res,tp=0.01,sl=0.005):
    """
    функция получения финансового результата от отработки ордеров

    Параметры: 
    order_res - ряд результатов отработки ордера (0-неудачно, 1-удачно)
    tp - уровень TakeProfit (доля от единицы)
    sl - уровень StopLoss (доля от единицы)

    Результат:
    res - ряд результатов (относительных изменений) для каждого тика
    """
    res = np.zeros_like(order_res)
    res[order_res==1] = + tp
    res[order_res==0] = - sl
    return res
