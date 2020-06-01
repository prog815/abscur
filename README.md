# abscur
Библиотека python для доступа к данным проекта "Абсолютный курс"

# Установка
```
! pip install git+https://github.com/prog815/abscur

import abscur
```

# Состав

## Методы

get_abs_curses() - Возвращает абсолютные курсы в виде объекта Pandas.DataFrame 

get_pairs_curses() - Возвращает курсы валютных пар в виде объекта Pandas.DataFrame

## Классы

PairAbsConverter - Класс преобразования между парными курсами и абсолютными

## Модуль pred_obr - Предобработка

pred_obr.exp_sglaj() - экспоненциальное сглаживание


## Модуль trading - Трейдинг

trading.get_order_set() - Функция считает ряды срабатывания ордеров на buy и на sell

trading.order_res_to_profit() - Функция получения финансового результата от отработки ордеров

trading.sim_full_order() - Прогон полного ордера

## Модуль optim - Оптимизация

optim.GenomOptim() - Класс генетической оптимизации

## Модуль alpari - Обработка данных тикеров Альпари

alpari.get_page_links() - Функция извлечения ссылок из веб страницы

alpari.get_topics() - Функция для получения списка разделов

alpari.get_topic_instuments() - Функция получения списка инструментов отдельного раздела

alpari.get_instruments_years() - список годов внутри инструмента

alpari.get_zip_list() - Список файлов архивов внутри года

alpari.get_zip() - Загружает один месяц по имени архива сгруппированный по минутам

alpari.get_cot_hist() - История котировок
