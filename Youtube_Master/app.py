from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs, BeautifulSoup
import mysql.connector as conn
from mysql.connector import cursor
import os
import requests
from pytube import YouTube
import pymongo
import gridfs
import base64
import urllib
from urllib.request import urlopen as uReq
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from selenium.webdriver.firefox.options import Options
import mysql.connector as conn
from mysql.connector import cursor
from pytube import YouTube
# driver = webdriver.Chrome(ChromeDriverManager().install())
import config
import pandas as pd
from flask import Flask, render_template, request, jsonify, url_for
from flask_cors import CORS, cross_origin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from urllib.parse import urlparse
import config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
ser = Service("chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
# driver = webdriver.Firefox(firefox_options=options)
# from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager # Code 2
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) # Code 3
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import base64
import requests
import logging
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
logging.basicConfig(filename="yt_test.log", level=logging.INFO, format='%(asctime)s %(name)s %(message)s %(levelname)s')
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("google-chrome")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("chromedriver"), options=chrome_options)






commenter_name = []
comments = []
link = []
htmlComment=[]
likes = []
title = []
views = []
yt=[]
ch_for_link=[]
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
options = Options()
client = pymongo.MongoClient("mongodb+srv://Tandon78:Hellodude123@tandon.el8wcqy.mongodb.net/?retryWrites=true&w=majority")
db = client.test
mydb = conn.connect(host="localhost", user="root", password="12345")
cursor = mydb.cursor()







class Youtube:

    app = Flask(__name__)

    @app.route('/',methods=['GET'])  # route to display the home page
    @cross_origin()
    def homePage():
        logging.info("Welcome to Youtube Scrapping")
        return render_template("index.html")





    @app.route('/details',methods=['POST','GET']) # route to show the review comments in a web UI
    @cross_origin()
    def index():
        if request.method == 'POST':
            all_videos = []
            img = []
            image_content = []
            channelName=[]
            ch_for_link=[]

            url = request.form['content']
            reviews=[]


            # using driver for the url

            driver.get(url)
            driver.maximize_window()

            time.sleep(5)


            last_height = 200
            start_height = 0
            while last_height < 5000:
                driver.execute_script("window.scrollTo(" + str(start_height) + ", " + str(last_height) + ");")
                start_height = last_height
                last_height = last_height + 700
                time.sleep(2)

                # Making page static
            try:
                bs = BeautifulSoup(driver.page_source, 'html.parser')
                bigbox = bs.select("#meta #video-title-link")
            except Exception as e:
                logging.exception(e)


            try:
                bs = BeautifulSoup(driver.page_source, 'html.parser')
                img = bs.select("#contents #content #dismissible #thumbnail .style-scope img")
            except Exception as e:
                logging.exception(e)

            try:
                imga=[]
                for i in range(0, 50):
                    all_videos.append(bigbox[i]['href'])

                    imga.append(img[i]['src'])
                    image_content.append(requests.get(imga[i]).content)
            except Exception as e:
                logging.exception(e)

            # Channel Name

            try:
                channel = bs.select_one("#container #text-container #text")
                channelName = channel.text
                ch_for_link.append((channel.text).replace(" ", ""))
            except Exception as e:
                logging.exception(e)

            # Getting half link of all the channels

            try:
                Video_No = 1
                for i in range(0, 50):
                    link.append("www.youtube.com" + all_videos[i])
            except Exception as e:
                logging.exception(e)

            try:
                bs = BeautifulSoup(driver.page_source, 'html.parser')
                title=bs.select("#details #meta .style-scope #video-title")
            except Exception as e:
                logging.exception(e)

            try:
                for i in range(0,50):
                    all_vids_new = all_videos[i].replace("/watch?v=", "")
                    dict={"S.No":i+1,"Title":title[i].text,"Thumbnail": imga[i],"Link":all_vids_new}
                    reviews.append(dict)
            except Exception as e:
                logging.exception(e)

            return render_template('results.html', reviews=reviews)



    @app.route("/details/<lnk>")  # route to show the review comments in a web UI
    def moreinfo(lnk):
        commentsNew = []
        details=[]
        linkk=lnk

        driver.get("https://www.youtube.com/watch?v="+linkk)
        last_height = 100
        start_height = 0
        time.sleep(10)
        try:
            bs = BeautifulSoup(driver.page_source, 'html.parser')
            likes.append(bs.select_one("#segmented-like-button div span"))
            title.append(bs.select_one("#title h1 yt-formatted-string"))
            views.append(bs.select_one("#info-container #info .bold"))
            Youtuber_name=bs.select_one("#container #text-container yt-formatted-string a")
            Y_Name=Youtuber_name.text

        except Exception as e:
            logging.exception(e)

        mongoThumbnail = bs.select_one(".ytp-ad-preview-image")
        mongoThumbnailF = mongoThumbnail.contents[0]['src']
        base64image = base64.b64encode(requests.get(mongoThumbnailF).content)

        while last_height < 10000:
            driver.execute_script("window.scrollTo(" + str(start_height) + ", " + str(last_height) + ");")
            start_height = last_height
            last_height = last_height + 500
            time.sleep(2)

        try:
            bs = BeautifulSoup(driver.page_source, 'html.parser')
            name = bs.select("#contents #author-text span")
            bs = BeautifulSoup(driver.page_source, 'html.parser')
            comment = bs.select("#content #content-text")
        except Exception as e:
            logging.exception(e)


        # print(comment)
        # coll = db1[channelName + "'s video no. " + str(i)]
        MongoComments=[]
        try:
            for j in range(0, len(name)):
                cn = (str(name[j].text).replace("  ", ""))
                cn = (cn).replace("\n", "")
                c = (str(comment[j].text))
                commentsNew.append({"Name": cn,
                             "Comment": c})
                print(commentsNew)
        except Exception as e:
            logging.exception(e)

        try:
            detail = {"Title":title[0].text,"Views":views[0].text,"Likes":likes[0].text,"Comments": commentsNew}
            details.append(detail)
        except Exception as e:
            logging.exception(e)



        # SQL Connection

        # print(comments)

        s1 = "create table IF NOT EXISTS YTProject.YouTubeDetails(Youtuber_name varchar(50), Video_Title varchar(200),likes varchar(20), Views varchar(30), Comments text(150000))"
        s2 = "insert into YTProject.YouTubeDetails values(%s,%s,%s,%s,%s)"
        try:
            data = (Y_Name,title[0].text,likes[0].text,views[0].text, str(commentsNew))
        except Exception as e:
            logging.exception(e)


        try:
            cursor.execute(s1)
            cursor.execute(s2, data)
            mydb.commit()
        except Exception as e:
            logging.exception(e)




        # MongoDB Connection



        # i = 1
        # c = ch_for_link[0]

        try:
            db1 = client['YTProj']
            coll = db1[title[0].text ]
            dataMongo=[{"Thumbnail":base64image,"Comments":str(commentsNew)}]
            coll.insert_many(dataMongo)
        except Exception as e:
            logging.exception(e)


        return render_template('more1.html', htmlComment=details)
        # return lnk



    @app.route("/download/<int:Downlink>")  # route to show the review comments in a web UI
    def download(Downlink):

        yt = YouTube(link[Downlink-1])
        ys = yt.streams.get_by_resolution('360p')
        # Starting download
        logging.info("Downloading...")
        ys.download("./videos", str(Downlink) + ".mp4")
        logging.info("Downloaded😊😊")
        folder = '1nElCMe8B7caNjitJC-jQbb8Wnv7PHNRS'
        Downloadlink = []
        # Upload files
        directory = "./videos/"+ str(Downlink) + ".mp4"

        # filename = os.path.join(directory, f)

        title=str(Downlink)+".mp4"
        gfile = drive.CreateFile({'parents': [{'id': folder}], 'title': title})
        gfile.SetContentFile(directory)
        gfile.Upload()
        logging.info("Uploaded")
        # SET PERMISSION
        permission = gfile.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})

        # SHARABLE LINK
        Downloadlink.append(gfile['alternateLink'])
        logging.info("link shared")
        return render_template('download.html', Dlink=str(Downloadlink[0]))



        # return str(Downloadlink)












    if __name__ == "__main__":
        # app.run(host='127.0.0.1', port=8002, debug=True)
        # app.run(host="0.0.0.0",debug=True,port=os.environ['PORT'])
        app.run()





