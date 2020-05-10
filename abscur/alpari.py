main_url = 'http://ticks.alpari.org/'

temp_dir = None

# -------------------------------------------

def get_page_links(url):
    """
    Функция извлечения ссылок из веб страницы

    Параметры:
    url - адрес страницы

    Возвращает список ссылок
    """
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    page = urlopen(url)
    soup = BeautifulSoup(page,features="lxml")
    return [link.get('href') for link in soup.find_all('a')]

# -------------------------------------------

def get_topics():
    """
    Функция для получения списка топиков. 
    
    Возвращает список.

    Примеры:
    print(get_topics())

    """
    links = get_page_links(main_url)
    topics_list = list(filter(lambda s:s != '',map(lambda s:s.replace('..','').replace('/',''),links)))
    return topics_list

# -------------------------------------------

def get_topic_instuments(topic):
    """
    Функция получения списка инструментов отдельного раздела

    Параметры:
    topic - имя раздела

    Возвращает список инструментов

    Примеры:
    get_topic_instuments('nano')
    
    """
    links = get_page_links(main_url + topic)
    istruments_list = list(filter(lambda s:s != '',map(lambda s:s.replace('..','').replace('/',''),links)))
    return istruments_list

# -------------------------------------------

def get_instruments_years(topic,instrument):
    """
    список годов внутри инструмента

    Параметры:
    topic - раздел
    instrument - инстумент

    Возвращает список

    Примеры:
    get_instruments_years('nano','AUDCAD')

    """
    links = get_page_links(main_url + topic + '/' + instrument)
    years_list = list(filter(lambda s:s != '',map(lambda s:s.replace('..','').replace('/',''),links)))
    return years_list

# -------------------------------------------

def get_zip_list(topic,instrument,year):
    """
    Список файлов архивов внутри года

    Параметры:
    topic - раздел
    instrument - инстумент
    year - год

    Возвращает список

    Примеры:
    get_zip_list('nano','AUDCAD','2020')

    """
    links = get_page_links(main_url + topic + '/' + instrument + '/' + year)
    zip_list = list(filter(lambda s: '.zip' in s,map(lambda s:s.replace('/',''),links)))
    return zip_list

# -------------------------------------------

def get_zip(topic,instrument,year,zip_name):
    """
    Загружает один месяц по имени архива сгруппированный по минутам.
    Для исключения повторной загрузки по сети кеширует в темпе.

    Параметры:
    topic - раздел
    instrument - инстумент
    year - год
    zip_name - имя файла архива

    Возвращает таблицу Pandas.DataFrame

    Примеры:
    get_zip('nano','AUDCAD','2020','202003_nano_AUDCAD.zip')

    """
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen
    import datetime
    import tempfile
    import pandas as pd
    import os.path

    global temp_dir
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()

    temp_file_path = temp_dir + '/' + zip_name + '.csv'

    if os.path.exists(temp_file_path):
        return pd.read_csv(temp_file_path,index_col='DateTime',parse_dates=True)

    resp = urlopen(f'http://ticks.alpari.org/{topic}/{instrument}/{year}/{zip_name}')
    zipfile = ZipFile(BytesIO(resp.read()))
    res = pd.DataFrame()
    for fname in zipfile.namelist():
        df = pd.read_csv(zipfile.open(fname),sep='\t',parse_dates=True)
        # print(fname)
        if df.shape[0] > 0:
            df['Rate'] = (df.RateBid + df.RateAsk)/2
            df['DateTime'] = pd.to_datetime(df.RateDateTime).apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,dt.minute))
            df = df[['DateTime','Rate']]
            df = df.groupby(['DateTime']).agg(['first','max','min','last'])
            df.columns = ['open','high','low','close']
            res = res.append(df)
    res.to_csv(temp_file_path)
    print(zip_name,'загружен из сети')
    return res

# -------------------------------------------

def get_cot_hist(topic:str,instruments,diap:str,tick:str='1d'):
    """
    История котировок

    Параметры:
    topic - раздел (строка)
    instruments - инструменты (строка или список)
    diap - диапазон загружаемой истории (строка: 1m, 2m, 3m, 6m, 1y, 2y, 3y, 4y, 5y)
    tick - глубина группировки (строка: 1, 5, 15, 30, 1h, 3h, 6h, 12h, 1d)

    Возвращает Pandas.DataFrame 

    Пример:
    get_cot_hist('nano',['EURUSD','AUDCAD', 'AUDCHF'],'2m','15')

    """
    import pandas as pd
    import datetime

    diaps = {'1m':1,
             '2m':2,
             '3m':3,
             '6m':6,
             '1y':12,
             '2y':24,
             '3y':36,
             '4y':48,
             '5y':60}
    assert diap in diaps.keys(), "Неверное значение для <diap>"
    start_mon = diaps[diap]*31*24*60*60
    start_mon = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()-start_mon)
    start_mon = str(start_mon.year*100+start_mon.month)

    ticks = {'1':1, 
            '5':5,
            '15':15,
            '30':30,
            '1h':60,
            '3h':3*60,
            '6h':6*60,
            '12h':12*60,
            '1d':24*60}
    assert tick in ticks.keys(), "Неверное значение для <tick>"
    dt = ticks[tick]
    
    def get_one_instr(instr:str):
        res = pd.DataFrame()
        years = get_instruments_years(topic,instr)
        for year in filter(lambda y: y >= start_mon[:4],years):
            for zip_name in filter(lambda fn: fn>= start_mon, get_zip_list(topic,instr,year)):
                df = get_zip(topic,instr,year,zip_name)
                if df.shape[0] <= 0:
                    continue
                df = df.groupby(lambda d:datetime.datetime.fromtimestamp(d.timestamp()//(dt*60)*(dt*60))) \
                        .agg({'open':'first','high':'max','low':'min','close':'last'})
                res = res.append(df)
        return res
    
    if type(instruments) == str:
        return get_one_instr(instruments)
    
    res = pd.DataFrame()
    for instr in instruments:
        df = get_one_instr(instr)
        df.columns = pd.MultiIndex.from_arrays([[instr]*4,df.columns])
        res = pd.concat([res,df],axis=1)
    return res
