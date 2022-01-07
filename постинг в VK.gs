//для получения ключа ссылка
//https://oauth.vk.com/authorize?client_id=6277880&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,photos,offline&response_type=token&v=5.69


function postToVK(title,message,link)
{
  const VK_key = "****************************************************"
  const pageCode = '151828989'
  
  message = title.toString().toUpperCase() + "\n\n" + message
  
  if(link.length > 0)
    message += "\nСсылка " + link
  
  let data = {
    'access_token' : VK_key, 
    "owner_id": '-' + pageCode,
    'from_group' : '1',
    'v' : '5.131',
    'message' : message
  }
  
  let url = 'https://api.vk.com/method/wall.post'
  
  let options = {
    'method': 'post',
    'payload': data
  }
  
  return UrlFetchApp.fetch(url,options).getContentText()
}

function testPostToVK()
{
  res = postToVK("заголовок","текст","http://www.ya.ru")
  Logger.log('------------- VK -----------------')
  Logger.log(res)
  return res
}
