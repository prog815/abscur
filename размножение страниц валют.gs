ss_id = "1CrNvvV-p6XG7lSJXftPKk_aY4nuH4WK25rPxaNKrM3U"

// размножение страниц валют
function curListMult() {
  ss = SpreadsheetApp.openById(ss_id)
  curList = ss.getSheetByName("Расшифровка валют").getRange("B2:B46").getValues()
  for(let n=0;n<curList.length;n++)
  {
    cur = curList[n][0]
    if(cur != "AUD")
    {
      new_ss = ss.getSheetByName("AUD").copyTo(ss)
      new_ss.setName(cur)
      new_ss.getRange("C1").setValue(cur)
      
      var charts = new_ss.getCharts();
      var chart = charts[charts.length - 1];
      new_ss.removeChart(chart);
      
      chart = new_ss.newChart()
      .setChartType(Charts.ChartType.TIMELINE)
      .addRange(new_ss.getRange('\'История абсолютных курсов\'!A1:A1308'))
      .addRange(new_ss.getRange('\'История абсолютных курсов\'!' + new_ss.getRange(1, 2+n, 1308, 1).getA1Notation()))
      .setMergeStrategy(Charts.ChartMergeStrategy.MERGE_COLUMNS)
      .setTransposeRowsAndColumns(false)
      .setNumHeaders(-1)
      .setHiddenDimensionStrategy(Charts.ChartHiddenDimensionStrategy.IGNORE_BOTH)
      .setOption('useFirstColumnAsDomain', true)
      .setOption('domainAxis.direction', 1)
      .setOption('dateFormat', 'dd.MM.yyyy')
      .setOption('series.0.labelInLegend', 'AUD')
      .setPosition(3, 1, 29, 9)
      .build();
      new_ss.insertChart(chart);
      
      Logger.log(cur)
//      return
    }
  }
  
  return
}
