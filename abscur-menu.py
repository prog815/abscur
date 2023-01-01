# %% [code]
def print_menu():
    from IPython.display import Markdown, display

    def print_link(text,link):
        md_code = f"-[{text}]({link})"
        display(Markdown(md_code))

    
    print_link("Источник данных с абсолютными курсами","https://www.kaggle.com/code/eavprog/abscur-data")
    print_link("Последние абсолютные курсы","https://www.kaggle.com/code/eavprog/abscur-posled-kurs")
    print_link("Абсолютные курсы голубых фишек Московской биржи","https://www.kaggle.com/code/eavprog/mmvb-abscur-blue-fishki")