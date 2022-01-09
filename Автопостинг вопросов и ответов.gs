function postOneQuestToChanels() 
{
  let ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  let page = ss.getSheetByName("Вопросы и ответы")
  
  let vls = page.getRange(2, 1, page.getLastRow()-1, 3).getValues().filter(function (elem){
    return elem[0].toString().length > 0 && elem[1].toString().length > 0 && elem[2].toString().length > 0
  })
  
  let [qst,ans,link] = vls[Math.floor(Math.random()*vls.length)]
  
  let data = {
    'regim' : 'post',
    'title' : qst ,
    'message' : ans,
    'link' : link
  }
  
  let options = {
    'method': 'post',
    'payload': data
  }
  
  let url = "https://script.google.com/macros/s/******************************/exec" // ссылка на центральную форму
  
  let res = UrlFetchApp.fetch(url,options).getContentText()
  Logger.log(res)
  
  return
}
