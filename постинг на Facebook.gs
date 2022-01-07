function postToFB(subj,text,link) 
{
  let pageCode = '149982995584539'
  let marker = '**************************************************************************************************************'
  
  
  // генерируем все токены и ищем свой
  // https://developers.facebook.com/tools/explorer/2021207188092795?method=GET&path=me%2Faccounts%2F%3Flimit%3D500&version=v3.1
  //
  // отлаживаем новый токен здесь
  // https://developers.facebook.com/tools/debug/accesstoken/?access_token=
  //
  // Срок действия этого нового долгосрочного маркера доступа истечет 4 март 2022 г.:
  
  let data = {
    //'link' : link ,
    'message' : subj + "\n\n" + text,
    'published' : 'true' ,
    'access_token' : marker
  }
  
  if(link !== undefined && link.toString().replace(/[\s\r\n\t ]+/g,"").length > 10)
    data['link'] = link
  
  let options = {
    'method': 'post',
    'payload': data
  };
  
  var url = "https://graph.facebook.com/"+ pageCode + "/feed" ;
  
  UrlFetchApp.fetch(url,options).getContentText()
}

function testFB()
{
  let subj = "тестовый заголовок"
  let text = "тестовый текст"
  let link = 'https://scontent-frx5-1.xx.fbcdn.net/v/t1.0-9/107596675_679433949306105_7701326895959320368_n.jpg'
  
  link = "https://2.bp.blogspot.com/-Y2JAxZsEpiM/Xwnr7dKWNuI/AAAAAAADwtw/KdZofsDhxY8bYEahlq8POx-hhbSfKE4oQCLcBGAsYHQ/s320/%25D0%2592%2B%25D0%25BA%25D0%25B0%25D0%25BA%25D0%25B8%25D1%2585%2B%25D1%2581%25D0%25BE%25D1%2586.%25D1%2581%25D0%25B5%25D1%2582%25D1%258F%25D1%2585%2B%25D0%25BF%25D1%2580%25D0%25B5%25D0%25B4%25D1%2581%25D1%2582%25D0%25B0%25D0%25B2%25D0%25BB%25D0%25B5%25D0%25BD%2B%25D0%25BF%25D1%2580%25D0%25BE%25D0%25B5%25D0%25BA%25D1%2582_.png"
  
  link = "https://youtu.be/nm1c213jwEk"
  
  postToFB(subj,text,link)
}
