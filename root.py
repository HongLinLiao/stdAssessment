from os import walk
from os.path import join

# XLSX Model
from xlsxHandler import XLSX

from assessment import convertInfo,findPdfLayout, testPdfLayout, getLayoutSetting, attributes, getVariableName

# all file
def root(path, type):

    print("Layout Loading......")

    # get Layout Setting
    layoutSettings = getLayoutSetting()

    print("Layout Loading Complete!")

    if(type==1):
        # ouput excel
        outputFile = XLSX('./output.xlsx')

        sheet =outputFile.getSheetByName(outputFile.workbook.sheetnames[0])

        # file write with append mode
        max_row = outputFile.getSheetMaxRow(sheet) + 1

        # column name
        outputFile.writeDataByLocation(sheet, 'A1', 'Year')
        outputFile.writeDataByLocation(sheet, 'B1', 'Department')
        outputFile.writeDataByLocation(sheet, 'C1', 'Id')
        outputFile.writeDataByLocation(sheet, 'D1', 'School')
        outputFile.writeDataByLocation(sheet, 'E1', 'Name')
        outputFile.writeDataByLocation(sheet, 'F1', 'IsOk')
        outputFile.writeDataByLocation(sheet, 'G1', 'Message')

        cell = [
            'H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ',
            'AR','AS','AT','AU','AV','AW','AX',
            'AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI'
        ]

        for i in range(len(attributes)):
            outputFile.writeDataByLocation(sheet, cell[i]+'1', attributes[i].replace(',',''))

        # pdf count
        pdfCount = 0;
        successCount = 0;

        for root, dirs, files in walk(path):
            for f in files:

                # pdf absolute path
                fullpath = join(root, f)

                # filter not .pdf
                if(fullpath.find('.pdf') != -1):

                    # call parse
                    result = convertInfo(fullpath, layoutSettings)

                    outputFile.writeDataByLocation(sheet, 'A'+str(max_row+pdfCount), result.data.year)
                    outputFile.writeDataByLocation(sheet, 'B'+str(max_row+pdfCount), result.data.department)
                    outputFile.writeDataByLocation(sheet, 'C'+str(max_row+pdfCount), result.data.id)
                    outputFile.writeDataByLocation(sheet, 'D'+str(max_row+pdfCount), result.data.school)
                    outputFile.writeDataByLocation(sheet, 'E'+str(max_row+pdfCount), result.data.name)

                    if(result.isOk == False):
                        outputFile.writeDataByLocation(sheet, 'F'+str(max_row+pdfCount), 'x')
                        outputFile.writeDataByLocation(sheet, 'G'+str(max_row+pdfCount), result.message)
                    else:

                        # score data
                        for i in range(len(attributes)):

                            variableName = getVariableName(attributes[i].split(',')[0], attributes[i].split(',')[1])
                            if(result.data.data != None):
                                score = getattr(result.data.data, variableName)
                                outputFile.writeDataByLocation(sheet, cell[i]+str(max_row+pdfCount), score)
                        
                        successCount = successCount + 1

                    print("%s,%s,%s,%s,%s,%s,%s" % (result.data.year,result.data.department,result.data.id,result.data.school,result.data.name,result.isOk,result.message))

                    pdfCount = pdfCount + 1
                    
        # save file
        outputFile.saveWorkbook()

        print('End!')
        
        print('Success %s pdf.' % (successCount))
        print('Handle %s pdf.' % (pdfCount))
    
    elif(type==2):
        for root, dirs, files in walk(path):
            for f in files:
                # pdf absolute path
                fullpath = join(root, f)

                # filter not .pdf
                if(fullpath.find('.pdf') != -1):
                    findPdfLayout(fullpath)
    
    elif(type==3):
        for root, dirs, files in walk(path):
            for f in files:
                # pdf absolute path
                fullpath = join(root, f)

                # filter not .pdf
                if(fullpath.find('.pdf') != -1):
                    testPdfLayout(fullpath, layoutSettings)
