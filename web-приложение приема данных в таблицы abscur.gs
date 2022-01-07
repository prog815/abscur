function doGet(e) {
  regim = e.parameter.regim
  if(regim == "update_report")
  {
    date = e.parameter.date
    ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
//    SpreadsheetApp.enableBigQueryExecution()
    ss.refreshAllDataSources()
    ss.rename("отчет по абсолютным курсам на " + date)
    return HtmlService.createHtmlOutput("отчет обновлен");
  }
  else
    return HtmlService.createHtmlOutput("не поддерживается");
}


function update_rep()
{
  SpreadsheetApp.enableBigQueryExecution()
  ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  ss.refreshAllDataSources()
//    ss.rename("отчет по абсолютным курсам на " + date)
}


// ---------------------------------------------------------------------------------------

function doPost(e) {
//  var params = JSON.stringify(e)
  csv = e.parameter.table
  page = e.parameter.page
  
  ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  
  if(page == "par_hist")
    s = ss.getSheetByName("История парных курсов")
  else if(page == "abs_hist")
    s = ss.getSheetByName("История абсолютных курсов")
  else if(page == "last_par")
    s = ss.getSheetByName("Последние парные курсы")
  else if(page == "last_abs")
    s = ss.getSheetByName("Последние абсолютные курсы")
  else
    return HtmlService.createHtmlOutput("не нормальный режим");
  
  res = Utilities.parseCsv(csv)
  for(let r=1;r<res.length;r++)
    for(let c=1;c<res[r].length;c++)
      res[r][c] = res[r][c].toString().replace('.',',')
  
  s.clear()
  s.getRange(1, 1, res.length, res[0].length).setValues(res)
  
  return HtmlService.createHtmlOutput("загрузили");
}

// ---------------------------------------------------------------------------------------


function obrTable()
{
  ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  s = ss.getSheetByName("abscur")
  csv = s.getRange(1,1).getValue()
  
  res = Utilities.parseCsv(csv)
  
  s.getRange(2, 1, res.length, res[0].length).setValues(res) 
  
  return
}

// ---------------------------------------------------------------------------------------

function myFunction() {
  
  ss = SpreadsheetApp.openById("1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U")
  
  
  s = ss.getSheetByName("Лист1")
  s.getRange(4, 3).setValue(Math.floor(Math.random()*1000))
  
  ss.refreshAllDataSources()
  
  
}
