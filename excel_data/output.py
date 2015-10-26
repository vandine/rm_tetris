from xlwt import Workbook
# create workbook in separate module, feed that workbook to this function!!!!!
def write_data_noSpeed(BOOK, SHEET, SHEETNAME, PRACTICE, subject_num, scoreNoSpeed, levelNoSpeed, enjoyNoSpeed, timeNoSpeed):

    row = PRACTICE-2

    def setData(scoreNoSpeed, levelNoSpeed, enjoyNoSpeed, timeNoSpeed):
        SHEET.write(row, 0, row)
        SHEET.write(row, 2, scoreNoSpeed)
        SHEET.write(row, 3, levelNoSpeed)
        SHEET.write(row, 4, enjoyNoSpeed)
        SHEET.write(row, 5, timeNoSpeed)
    
    setData(scoreNoSpeed, levelNoSpeed, enjoyNoSpeed, timeNoSpeed) 
    BOOK.save(SHEETNAME)

