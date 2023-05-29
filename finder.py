import zipfile
from numpy.lib.shape_base import column_stack
import requests
import progressManager as pm
import xmltodict
import json
import pandas as pd
import xml.etree.ElementTree as elemTree
from urllib.request import urlopen
from zipfile import ZipFile, is_zipfile
from io import BytesIO
from bs4 import BeautifulSoup


#standard dictionary
#[haveCB, numOfSEQ, arrayOfSEQ, arrayOfSb_bgn_dt, arrayOfSb_end_dt]

getStock = 'https://opendart.fss.or.kr/api/950130.xml'

getReport = 'https://opendart.fss.or.kr/api/list.xml'
#reportUrl = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo='
reportUrl = 'https://opendart.fss.or.kr/api/document.xml'
getAllStockCodes = 'https://opendart.fss.or.kr/api/corpCode.xml'

bgn_de = '20180117'
end_de = '20210801'


def testFunction(key):
    resp = urlopen("http://openapi.foodsafetykorea.go.kr/api/"+'9617043b65de4e64911b'+"/C005/xml/1/5")
    #if rceptNo[i].get_text() == "20210217900277":
    #    continue
    #try:
    #    with ZipFile(BytesIO(resp.read())) as zf:
    #        file_list = zf.namelist()
    #        while len(file_list) > 0:
    #            file_name = file_list.pop()
    #            CBreport = zf.open(file_name).read().decode('euc-kr')
    #            #print(BeautifulSoup(zf.open(file_name).read().decode('euc-kr'),'html.parser'))
    #            break
    #        print(BeautifulSoup(CBreport,"html.parser"))
    #except Exception:
    #    pass
    soup = BeautifulSoup(resp, "xml")

    print(soup)


def pilgrim(key):
    resp = urlopen(getAllStockCodes + "?crtfc_key=" + key)
    with ZipFile(BytesIO(resp.read())) as zf:
        file_list = zf.namelist()
        while len(file_list) > 0:
            file_name = file_list.pop()
            corpCode = zf.open(file_name).read().decode()
            break

    tree = elemTree.fromstring(corpCode)
    stockLists = tree.findall('list')
    corpName = [x.findtext("corp_name") for x in stockLists]
    stockCode = [x.findtext("stock_code") for x in stockLists]
    #print(corpName)
    #print(stockCode)

    stockDict = {}
    df = pd.DataFrame(columns=['stockName','stockCode','haveCB'])

    for i in range(0,len(corpName)):
        stockDict[corpName[i]]=stockCode[i]
    bigCount = 0
    count = 0
    columnCount = 0
    for stock in list(stockDict.keys()):
        if len(stockDict[stock]) == 6:
            dict = searchStock(stockDict[stock], key)
            ##print(dict)
            if dict["haveCB"] :
                df.loc[count] = {'stockName' : stock, 'stockCode' : stockDict[stock]}
                for i in range(0,dict["numOfSEQ"]):
                    if dict["numOfSEQ"] > columnCount:
                        df["회차"+str(columnCount)] = ""
                        df["전환청구시작일"+str(columnCount)] = ""
                        df["전환청구종료일"+str(columnCount)] = ""
                        df["전환가액"+str(columnCount)] = ""
                        columnCount+=1
                    df.loc[[count],["회차"+str(i)]] = [dict["listOfSEQ"][i]]
                    df.loc[[count],["전환청구시작일"+str(i)]] = [dict["listOfSb_bgn_dt"][i]]
                    df.loc[[count],["전환청구종료일"+str(i)]] = [dict["listOfSb_end_dt"][i]]
                    df.loc[[count],["전환가액"+str(i)]] = [dict["listOfExe_prc"][i]]
                count+=1
        bigCount+=1
        
            #if count == 10:
            #    break
        
        pm.progress.setProgressGage((bigCount/len(stockDict)*100))

        if count>200 :
            pm.progress.setProgressGage(100)
            print(df)
            break
        #print(bigCount/len(corpName)*100)
    df.to_excel('stockCodes.xlsx',index=False)
    #soup = BeautifulSoup(corpCode, 'xml')
    #lists = soup.find_all('list')
    #result = [x for x in lists if len(x.find('stock_code').get_text())==6]
    #data = []
    #for x in result:
    #    data.append(xmltodict.parse(str(x))['list'])
    #json.dumps(data)
    #for i in range(0,(len(data))):
    #    print(data[i])
    print("Function Pilgrim Finished")
    

def searchStock(stockCode, key):
    response = requests.get(getReport+"?crtfc_key="+key+"&corp_code="+stockCode+"&bgn_de="+bgn_de+"&end_de="+end_de+"&last_reprt_at=N&pblntf_ty=B&page_count=20")
    soup = BeautifulSoup(response.text,'lxml')
    if "전환사채권발행결정" in soup.text:
        dict = {'haveCB' : True, 'numOfSEQ' : 0}
        
        listOfSEQ = []
        listOfSb_bgn_dt = []
        listOfSb_end_dt = []
        listOfExe_prc = []
        reportNm = soup.select("report_nm")
        rceptNo = soup.select("rcept_no")
        for i in range(0, len(reportNm)):
            if "전환사채권발행결정" in reportNm[i].get_text():    
                resp = urlopen(reportUrl+"?crtfc_key="+key+"&rcept_no="+rceptNo[i].get_text())
                #if rceptNo[i].get_text() == "20180525000319":
                #    continue
                ##print("현재 공시 번호 : " + rceptNo[i].get_text())
                try:
                    with ZipFile(BytesIO(resp.read())) as zf:
                        file_list = zf.namelist()
                        while len(file_list) > 0:
                            file_name = file_list.pop()
                            CBreport = zf.open(file_name).read().decode('euc-kr')
                            break
                    soup = BeautifulSoup(CBreport,"html.parser")
                except Exception:
                    continue
    
                
            #print(soup)
                sb_bgn_dt = soup.select("[aunit='SB_BGN_DT']")
                sb_end_dt = soup.select("[aunit='SB_END_DT']") 
                seq_no = soup.select("[acode='SEQ_NO']")
                exe_prc = soup.select("[acode='EXE_PRC']")

               
                ##print("사채전환시작일 : " + sb_bgn_dt[0].get_text())
                ##print("사채전환만기일 : " + sb_end_dt[0].get_text())
                ##print("회차 : " + seq_no[0].get_text())
                ##if len(rceptNo)-1!=i:
                ##    print("다음 공시 번호 : " + rceptNo[i+1].get_text())
                flag = True
                for i in listOfSEQ:
                    ##print(str(i) + " and " + seq_no[0].get_text() +" are same?")
                    if str(i) == str(seq_no[0].get_text()):
                        ##print("yes")
                        flag = False
                    ##else:
                        ##print("no")
                if flag:
                    dict["numOfSEQ"] += 1
                    listOfSEQ.append(str(seq_no[0].get_text()))
                    listOfSb_bgn_dt.append(sb_bgn_dt[0].get_text())
                    listOfSb_end_dt.append(sb_end_dt[0].get_text())
                    listOfExe_prc.append(exe_prc[0].get_text())
            dict["listOfSEQ"] = listOfSEQ
            dict["listOfSb_bgn_dt"] = listOfSb_bgn_dt
            dict["listOfSb_end_dt"] = listOfSb_end_dt
            dict["listOfExe_prc"] = listOfExe_prc
        return dict
    else:
        dict = {'haveCB' : False}
        return dict

def test():
    print(searchStock("031860", "4ee05faa25d33dd19a2ad57abb8af4c713045991"))

#test()
#testFunction("4ee05faa25d33dd19a2ad57abb8af4c713045991")