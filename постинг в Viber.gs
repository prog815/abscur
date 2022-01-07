// полуавтоматический постинг
// отправляет письмо в "задавальник"
// далее руками на телефоне

function postToViber(title,message,link)
{
  if(link.length > 0)
    message += "\nСсылка " + link
  GmailApp.sendEmail("eavprog+************@rmilk.com", "Новость abscur для публикации в Viber https://invite.viber.com/?g2=AQB63y7Cm%2BNJK0tNZW%2F9kI00M6Wr8HuZ7XeamzN4jZCve8Aq9%2FiD3DY56Eqcf7dc ^today !1" , title + "\n\n" + message)
}

function testPostToViber()
{
  postToViber("заголовок","текст","http://www.ya.ru")
}
