from xlwt import Workbook

def write_survey_ans(BOOK, SHEET, SHEETNAME, survey_ans, PRACTICE):
    col = PRACTICE+6

    for i in xrange(1, 17):
        SHEET.write(i, col, survey_ans[i-1])

    BOOK.save(SHEETNAME)
    
    

