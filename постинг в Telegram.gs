function postToTelegram(title,message,link)
{
  const BOT_TOKEN = '********************************'
  const chanel = "@AbsCur"
  
  message = title.toString().toUpperCase() + "\n\n" + message
  
  if(link.length > 0)
    message += "\n\nСсылка " + link
    
  let data = {
    'chat_id': chanel,
    'text' : message
  }
  
  let url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage'
  
  let options = {
    'method': 'post',
    'payload': data
  }
  
  return UrlFetchApp.fetch(url,options).getContentText()
}

function testPostToTelegram()
{
  res = postToTelegram("заголовок","текст","http://www.ya.ru")
  Logger.log('------------- Telegram -----------------')
  Logger.log(res)
  return res
}
