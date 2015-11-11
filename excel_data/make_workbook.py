from xlwt import Workbook

def make_workbook(subject_num, version):
    book = Workbook()
    sheetName = 'subject_%d_raw_data.xls' %(subject_num)
    main_sheet = book.add_sheet(sheetName)

    main_sheet.write(0, 0, "trial")
    main_sheet.write(0, 1, "overallSkill")
    main_sheet.write(0, 2, "score")
    main_sheet.write(0, 3, "level")
    main_sheet.write(0, 4, "enjoyment")
    main_sheet.write(0, 5, "time")
    main_sheet.write(0, 7, "trial 1")
    main_sheet.write(0, 8, "trial 2")
    main_sheet.write(0, 9, "trial 3")
    main_sheet.write(0, 10,"trial 4")
    main_sheet.write(0, 11,"trial 5")
    main_sheet.write(0, 14, "version")
    main_sheet.write(1, 14, version)

    return(book, main_sheet, sheetName)
