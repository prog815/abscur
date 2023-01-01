# %% [code]
def print_menu():
    from IPython.display import Markdown, display
    
    text = """# Оглавление проекта \"Абсолютный валютный курс\" 
- [Источник данных с абсолютными курсами](https://www.kaggle.com/code/eavprog/abscur-data) 
- [Последние абсолютные курсы](https://www.kaggle.com/code/eavprog/abscur-posled-kurs)
- [Абсолютные курсы голубых фишек Московской биржи](https://www.kaggle.com/code/eavprog/mmvb-abscur-blue-fishki)"""
    
    display(Markdown(text))
    
    
  