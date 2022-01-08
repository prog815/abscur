function linkUkor(link)
{
  let url = "https://clck.ru/--?url=" + link
  return UrlFetchApp.fetch(url).getContentText()
}

function testUkor()
{
  let res = linkUkor("http://www.yandex.ru")
  return res
}
