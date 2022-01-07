import requests

# -------------------------------------------------------------

google_app_url = "https://script.google.com/macros/s/*************************************/exec"

def sendTable(pd_table,page):
    '''
    Выгрузка в гугл отчет
    
    Параметры:
    table - таблица в формате pandas
    page - страница (par_hist, abs_hist, last_par, last_abs)
    
    '''
    data = {
        "table" : pd_table.to_csv(), 
        "page" : page
    }
    
    res = requests.post(
        google_app_url,
        data = data
    )
    
    return res.content

# -------------------------------------------------------------

def postToChanels(title,message,link):
    data = {
        'regim' : 'post', 
        'title' : title,
        'message' : message, 
        'link' : link
    }

    url = 'https://script.google.com/macros/s/*****************************/exec'
    
    res = requests.post(url=url,data=data)
    return res.content
