function postToBlogger(title,message,link)
{
  if(link.length > 0)
    message += "\nСсылка " + link
  GmailApp.sendEmail("eav-prog1.********@blogger.com", title, message)
}

function testPostToBlogger()
{
  postToBlogger("заголовок","текст","http://www.ya.ru")
}
