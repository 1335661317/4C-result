"""
2016 年参加 CCCC 所做的榜单爬取工具
"""
import urllib
import requests
from bs4 import BeautifulSoup
import re

def getAuthenticityToken():
    indexPage = "https://www.patest.cn/users/sign_in"
    indexContent = urllib.request.urlopen(indexPage).read()
    bsObj = BeautifulSoup(indexContent,"html.parser")
    authenElement = bsObj.find(attrs={"name": "authenticity_token"})
    authenticity_token = authenElement['value']
    #print(indexContent)

    print ("Authenticity Token is " + authenticity_token)
    return authenticity_token

def genPostInfo(username, password, authenticity_token):
    data = {
        'authenticity_token': authenticity_token,
        'user[handle]': username,
        'user[password]': password,
        'user[remember_me]': '0',
    }
    return data

contestID = input('Please enter the ID of contest(Get it form ranklist Url): ')
loginName = input("Enter the user name: ")
loginPass = input("Enter the password: ")

print("Starting pull the page content...")
authenticityToken = getAuthenticityToken()
request = requests.session()
request.post("https://www.patest.cn/users/sign_in", genPostInfo(loginName, loginPass, authenticityToken))

rankPageUrl = 'https://www.patest.cn/contests/' + contestID + '/ranklist'

response = request.get(rankPageUrl)

print("Get rank list page...OK")

#print response.text

rankSoup = BeautifulSoup(response.text,"html.parser").find(id="ranklist")

outputFilter = input("Please enter the filter: ")

outputFileName = input("Please enter the output file name(*.html): ")

ytuList = rankSoup.find_all(text=re.compile("[0-9a-zA-Z_]*" + outputFilter + "[0-9a-zA-Z_]*"))

outputFile = open(outputFileName, 'w')

headd = request.get('http://3.ytujk1532.applinzi.com/cccc.php')
#outputFile.write("<table border='1px'>")
#outputFile.write(str(rankSoup.find("thead")))

outputFile.write(str(headd.text))
outputFile.write("<tbody>")
for eachRecord in ytuList:
    outputFile.write(str(eachRecord.parent.parent))

outputFile.write("</tbody></table>")
print ("All process has been done. Please check result in " + outputFileName)
