from xlwt import Workbook

def write_data_noSpeed(subject_num, scoreNoSpeed, levelNoSpeed, enjoyNoSpeed):

    book = Workbook()
    sheetName = 'subject_%d_raw_data.xls'%subject_num
    sheet1 = book.add_sheet(sheetName)

    def setDataLabels():
        sheet1.write(0, 0, "overallSkill")
        sheet1.write(0, 1, "scoreNoSpeed")
        sheet1.write(0, 2, "levelNoSpeed")
        sheet1.write(0, 3, "enjoyNoSpeed")

    def setData(scoreNoSpeed, levelNoSpeed, enjoyNoSpeed):
        sheet1.write(1, 1, scoreNoSpeed)
        sheet1.write(1, 2, levelNoSpeed)
        sheet1.write(1, 3, enjoyNoSpeed)
    
    setDataLabels()
    setData(scoreNoSpeed, levelNoSpeed, enjoyNoSpeed) 
    book.save(sheetName)

