function doPost(e) {
  // regim = {'post'} - режим постинга
  // title - заголовок сообщения
  // message - текстовое сообщение (для твиттера будет урезаться)
  // link - ссылка в конце сообщения (лучше ее делать короткой)
  
  regim = e.parameter.regim
  if(regim == "post")
  {
    title = e.parameter.title
    message = e.parameter.message
    link = e.parameter.link
    
    postToBlogger(title,message,link)
    
    Utilities.sleep(1*1000)
    postToWhatsApp(title,message,link)
    
    Utilities.sleep(1*1000)
    postToViber(title,message,link)
    
    Utilities.sleep(1*1000)
    postToFB(title,message,link)
    
    postToVK(title,message,link)
    
    postToTelegram(title,message,link)
    
    return HtmlService.createHtmlOutput("OK");
  }
  else
    return HtmlService.createHtmlOutput("не поддерживается");
}
