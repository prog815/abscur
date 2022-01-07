// полуавтоматический
// отправляем письмо в "задавальник"
// далее руками на телефоне

function postToWhatsApp(title,message,link)
{
  if(link.length > 0)
    message += "\nСсылка " + link
  GmailApp.sendEmail("eavprog+**********@rmilk.com", "Новость abscur для публикации в Whatsap https://chat.whatsapp.com/KrNJXAKizPxDlDSjYfdpQs ^today !1" , title + "\n\n" + message)
}

function testPostToWhatsApp()
{
  postToWhatsApp("заголовок","текст","http://www.ya.ru")
}
