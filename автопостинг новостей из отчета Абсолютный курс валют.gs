function autoPostingAbscurNews() {
  let ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  let page = ss.getSheetByName("Новости")
  
  for(let row= Math.min(page.getLastRow(),100);row>=2;row--)
  {
    let [date,title,text,link] = page.getRange(row, 1, 1, 4).getValues()[0]
    
    if(date.toString().length > 2)
      continue
      
    if(text.length>10 && title.length>10)
    { 
      date = (new Date()).toLocaleDateString()
      page.getRange(row, 1).setValue(date)
      
      let data = {
        'regim' : 'post',
        'title' : title ,
        'message' : text,
        'link' : link
      }
      
      let options = {
        'method': 'post',
        'payload': data
      }
      
      let url = "https://script.google.com/macros/s/**************************************/exec" // ссылка на центральную форму
      
      let res = UrlFetchApp.fetch(url,options).getContentText()
      Logger.log(res)
      
      return
    }
  }
}
