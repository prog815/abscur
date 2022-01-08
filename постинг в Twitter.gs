function postToTwitter(title,message,link)
{
//  link = linkUkor(link)
//  link = 'http://www.abscur.ru'
  message = title + "\n" + message
  if( message.length + link.length > 270 )
    message = message.substring(0,270-link.length) + "..."
  GmailApp.sendEmail("eavprog+*******@rmilk.com", "Новость abscur для публикации в Twitter https://twitter.com/abscurs ^today !1" , message + "\n" + link)
}

function testPostToTwitter()
{
  postToTwitter("Абсолютные курсы на 2022-01-07","AUD 13.5114(-0.71%), CAD 14.8185(0.34%), HKD 2.4182(0.03%), JPY 0.1628(0.33%), SEK 2.0633(-0.26%), USD 18.8663(0.12%), CHF 20.4714(-0.33%), EUR 21.3026(-0.06%), CNY 2.9573(-0.26%), CZK 0.8721(0.19%), GBP 25.5276(-0.06%), ILS 6.0597(-0.4%), NOK 2.1226(-0.32%), NZD 12.7151(-0.68%), RUB 0.247(0.5%), SGD 13.8596(-0.14%), ZAR 1.2016(1.07%), AED 5.1377(0.12%), ARS 0.1828(-0.01%), BRL 3.3201(0.53%), CLP 0.0225(0.23%), COP 0.0047(0.03%), DKK 2.8647(-0.01%), EGP 1.2027(0.13%), HUF 0.0592(0.55%), IDR 0.0013(0.39%), INR 0.2535(0.14%), ISK 0.1459(0.26%), KRW 0.0156(-0.42%), KWD 62.4361(0.09%), KZT 0.0436(0.15%), MXN 0.9206(0.47%), MYR 4.4802(-0.33%), PEN 4.7582(-0.03%), PHP 0.3658(-1.2%), PKR 0.1068(-0.05%), PLN 4.6808(0.36%), QAR 5.1831(0.12%), RON 4.3163(0.05%), SAR 5.0312(0.17%), THB 0.5623(-0.79%), TRY 1.3689(-0.56%), TWD 0.6831(0.04%), UAH 0.6928(0.05%), VND 0.0008(0.17%)","https://docs.google.com/spreadsheets/d/1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
}
