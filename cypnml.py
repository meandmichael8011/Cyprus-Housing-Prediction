
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
st.title('''Cyprus Housing''')
st.subheader("Get a prediction for your house price")
st.image('cypr.png')
st.subheader("")
button1 = st.checkbox('Load up the data and train the model (it can take up to 5 minutes, please be patient')
if st.session_state.get('button') != True:
    st.session_state['button'] = button1
if st.session_state['button'] == True:
    @st.cache_data
    def dataframe_creation(linker):
      link = linker
      br = requests.get(link)
      page = br.content
      soup = bs(page, 'html.parser')
      #PRICES
      advert = soup.find_all("div", attrs={"class": "advert__content-header"})
      price_list = [] ##################FINAL COLUMN
      import re

      html_code = str(advert)
      matches = re.findall(r'<b>(€)</b>(.*?)</span>', html_code)

      for match in matches:
          euro = match[0]
          number = match[1]
          number = number.split(" ")[0]
          number22 = number.replace(".", "")
          price_list.append(number22)
      #SQUARE METERS
      #advert__content-feature
      meters = soup.find_all("div", attrs={"class": "advert js-item-listing"})
      newiter = str(meters)
      again = newiter.split("mask")
      newmeterlist = []
      meter_list = [] ###### FINAL COLUMN
      for snip in again:
        meterage = re.findall(r'\d+\s*m²', snip)
        if meterage != None:
          newmeterlist.append(meterage)
        else:
          newmeterlist.append(str("0"))
      newmeterliste = newmeterlist[:-1]
      for x in newmeterliste:
        ui = str(x)
        oii = ui[2:-5]
        try:
          meter_list.append(int(oii))
        except ValueError as e:
          meter_list.append(int(0))
      # CITY LOCATION
      city = soup.find_all("div", attrs={"class": "advert__content-place"})
      city2 = str(city)
      city3 = re.findall(r'>(.*?)</div>', city2)
      city_list = [] #### THIS DATA
      for z in city3:
        koks = z.split(",")[0]
        city_list.append(koks)
      #CONDO TYPE
      condo = soup.find_all("div", attrs={"class": "advert__content-features"})
      oi = str(condo)
      full = re.findall(r'743\.png\)"></div><div>(.*?)</div>', oi)
      room_list = []  ##################FINAL COLUMN
      for y in full:
        if y == "Studio":
          room_list.append(0)
        else:
          room_list.append(y)
      #LINK
      linksearcher = soup.find_all("a", attrs={"class": "mask"})
      linksss = str(linksearcher)
      lsearcher = re.findall(r'href="/adv/[^"]+"></a>', linksss)
      linklister = []
      for xy in lsearcher:
          fullstr = "https://www.bazaraki.com" + xy[6:-6]
          linklister.append(fullstr)

      dataframe = pd.DataFrame({
          "Prices": price_list,
          "Square Meters": meter_list,
          "Room Number": room_list,
          "City": city_list,
          "Link": linklister
      })
      return dataframe

    # MAXIMUM NUMBER OF PAGES

    site1 = requests.get("https://www.bazaraki.com/real-estate-to-rent/apartments-flats/")
    site1c = site1.content
    findlim = bs(site1c, 'html.parser')
    lastpage = findlim.find_all("ul", attrs={"class": "number-list"})
    lastpage2 = str(lastpage)
    lastpage3 = re.findall(r'>(.*?)</a>', lastpage2)
    intl = []
    for x in lastpage3:
      intl.append(int(x))
    limi = max(intl)
    def createList(r1, r2):
        return list(range(r1, r2+1))
    r1, r2 = 1, limi
    limlist = createList(r1, r2)

    dfr = pd.DataFrame({
          "Prices": [],
          "Square Meters": [],
          "Room Number": [],
          "City": [],
          "Link": []
      })
    for x in limlist:
      link = 'https://www.bazaraki.com/real-estate-to-rent/apartments-flats/?page=' + str(x)
      oi = dataframe_creation(link)
      dfr = pd.concat([dfr, oi])
      dfr = dfr.reset_index(drop=True)

    frame = dfr

    finale1 = frame
    finale1['Prices'] = finale1['Prices'].astype(int)
    fix1 = []
    for xz in finale1['Room Number']:
        if xz == "6 and more":
            xz = int(6)
            fix1.append(xz)
        else:
            fix1.append(int(xz))
    finale1['Room Number'] = fix1

    class DomCy:
        def __init__(self, domlink):
            self.domlink = domlink
            path = "C:/Program Files/Google/chromedriver-win64/chromedriver.exe"
            service = Service(path)
            driver = webdriver.Chrome(service=service)
            driver.get(self.domlink)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/button[2]'))).click()
            num = 21
            x = 1
            while x == 1:
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="element-list"]/div/div/div[' + str(num) + ']/div'))).click()
                    num += 22
                except TimeoutException:
                    break
            bspage = driver.page_source
            soup = bs(bspage, 'html.parser')
            gens1 = soup.find_all("div", attrs={"class": "search-item js-filter-search"})
            gens2 = str(gens1).split("search-item js-filter-search")
            self.gensf = gens2[1:]
            self.souper = soup

        def prices(self):
            prclist = []
            for c in self.gensf:
                pattern4 = re.findall(r'<span>(.*?)</span>', c)
                if str(pattern4) == '[]':
                    prclist.append(0)
                else:
                    pe1 = str(pattern4)
                    pe2 = int(pe1[7:-2].replace(" ", ""))
                    prclist.append(pe2)
            return prclist

        def sqmeters(self):
            sqmlist = []
            for z in self.gensf:
                pattern3 = re.findall(r'area: (.*?)<sup>2</sup>', z)
                try:
                    elem1 = str(pattern3)
                    elem2 = int(elem1[2:-4])
                    sqmlist.append(elem2)
                except ValueError:
                    sqmlist.append(0)
            return sqmlist

        def bedrooms(self):
            bedlist = []
            for y in self.gensf:
                pattern2 = re.findall(r'Bedrooms:(.*?);', y)
                try:
                    bedlist.append(int(pattern2[0]))
                except IndexError:
                    bedlist.append(0)
            return bedlist

        def cities(self):
            citlist = []
            for x in self.gensf:
                pattern1 = re.findall(r'<b>(.*?)</b>', x)
                if pattern1 != None:
                    citlist.append(pattern1[0])
                else:
                    citlist.append(0)
            return citlist

        def flatlinks(self):
            finalfindlink = []
            findlinks = self.souper.find_all("div", attrs={"class": "swiper-slide swiper-slide-active"})
            pattern5 = re.findall(r'<a href=(.*?) rel="nofollow">', str(findlinks))
            for lou in pattern5:
                full = 'https://dom.com.cy' + lou[1:-1]
                finalfindlink.append(full)
            return finalfindlink

    @st.cache_data
    def getDomCy(insert):
        oir = DomCy(insert)
        dfr32 = pd.DataFrame({
            "Prices": oir.prices(),
            "Square Meters": oir.sqmeters(),
            "Room Number": oir.bedrooms(),
            "City": oir.cities(),
            "Link": oir.flatlinks()})
        fullframe = dfr32
        fik2 = pd.concat([finale1, fullframe], axis=0)
        return fik2

    finale2 = getDomCy('https://dom.com.cy/en/catalog/rent/type-apartment/')


    @st.cache_data
    def homecyinfo(linking):
        link = linking
        br = requests.get(link)
        page = br.content
        soup = bs(page, 'html.parser')
        ####PRICE
        homeprices = []
        money80 = soup.find_all("div", attrs={"class": "price"})
        for den in money80:
            gp = re.findall(r'class="price">(.*?)<', str(den))
            try:
                uaua = str(gp)[3:-2].replace(",", "")
                homeprices.append(int(uaua))
            except ValueError:
                homeprices.append(int(0))
        ####SQUARE METERS
        homemeters = []
        sqm80 = soup.find_all("ul", attrs={"class": "specs"})
        for el in sqm80:
            ui = str(el)[:-13] + "|"
            sqmatcher = re.findall(r'<li>(.*?)\|', ui)
            sq2 = str(sqmatcher)[-6:-2]
            sq3 = re.findall(r'\d+', sq2)
            homemeters.append(int(sq3[0]))
        ####ROOM NUMBER
        homeroomnums = []
        ROOM80 = soup.find_all("ul", attrs={"class": "specs"})
        for e in ROOM80:
            roomatcher = re.findall(r'<li>(.*?)be', str(e))
            try:
                homeroomnums.append(int(str(roomatcher)[2:-2]))
            except ValueError:
                homeroomnums.append(0)
        ####CITY
        city80 = soup.find_all("div", attrs={"class": "location"})
        homecities = []
        for sh in city80:
            ore = str(sh)
            homecities.append(ore)
        normcit = []
        for qr in homecities:
            hmmatcher = re.findall(r'\t(.*?)\t', qr)
            normcit.append(hmmatcher[6])
        ####LINK
        homelinklist = []
        link80 = soup.find_all("a", attrs={"class": "whole"})
        itemlink = re.findall(r'<a aria-label(.*?)</a>', str(link80))
        for fs in itemlink:
            gq = fs.split("href=")
            homelinklist.append("https://home.cy/" + (gq[1])[2:-2])

        dataframe80 = pd.DataFrame({
            "Prices": homeprices,
            "Square Meters": homemeters,
            "Room Number": homeroomnums,
            "City": normcit,
            "Link": homelinklist})

        return dataframe80


    #### NUMBER OF PAGES
    linklimhome = "https://home.cy/real-estate-to-rent?p=1"
    brhome = requests.get(linklimhome)
    pagehome = brhome.content
    souphome = bs(pagehome, 'html.parser')
    homelimit11 = []
    pagenum = souphome.find_all("div", attrs={"class": "paging"})
    limiting1 = re.findall(r'"next">(.*?)</a>', str(pagenum))
    for xq in limiting1:
        try:
            homelimit11.append(int(xq))
        except ValueError:
            pass
    que = max(homelimit11)

    def createlisthome(r3, r4):
        return list(range(r3, r4 + 1))

    r3, r4 = 1, que
    finalhomelim = createlisthome(r3, r4)  ################# ITERATE OVER THIS
    homecydfr = pd.DataFrame({
        "Prices": [],
        "Square Meters": [],
        "Room Number": [],
        "City": [],
        "Link": []})
    for ot in finalhomelim:
        link = 'https://home.cy/real-estate-to-rent?p=' + str(ot)
        qrg = homecyinfo(link)
        homecydfr = pd.concat([homecydfr, qrg])
        homecydfr = homecydfr.reset_index(drop=True)

    homecydfr['Square Meters'] = homecydfr['Square Meters'].astype(int)
    homecydfr['Room Number'] = homecydfr['Room Number'].astype(int)
    homecydfr['Prices'] = homecydfr['Prices'].astype(int)

    finale3 = pd.concat([finale2, homecydfr], axis=0)
    finale4 = finale3.reset_index(drop=True)
    finale4


    dumcit = pd.get_dummies(finale4['City'], dtype=int)
    finale5 = finale4.drop("City", axis=1)
    finale6 = pd.concat([finale5, dumcit], axis=1)

    train = finale6.iloc[:6000]
    test = finale6.iloc[6000:]
    X_train = train[['Square Meters', 'Room Number', 'Famagusta', 'Larnaca',
                     'Limassol', 'Nicosia', 'Paphos']]
    y_train = train['Prices']
    X_test = test[['Square Meters', 'Room Number', 'Famagusta', 'Larnaca',
                   'Limassol', 'Nicosia', 'Paphos']]
    y_test = test['Prices']
    from sklearn.ensemble import GradientBoostingRegressor
    import numpy as np
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.01, max_depth=60)
    model.fit(X_train, y_train)
    done = "x"
try:
    if done == "x":
        citier = [0, 0, 0, 0, 0]
        with st.form("my_form"):
            st.write("Price Predictor")
            squ = st.slider("How many square meters do you expect?", min_value=10, max_value=500, step=1)
            rms = st.slider("How many rooms do you expect?", min_value=0, max_value=5, step=1)
            cityy = st.radio("What city do you expect?", ['Famagusta', 'Larnaca', 'Limassol', 'Nicosia', 'Paphos'])
            submitted = st.form_submit_button("Submit")
            if submitted:
                if cityy == "Famagusta":
                    citier[0] = 1
                if cityy == "Larnaca":
                    citier[1] = 1
                if cityy == "Limassol":
                    citier[2] = 1
                if cityy == "Nicosia":
                    citier[3] = 1
                if cityy == "Paphos":
                    citier[4] = 1
                predi = model.predict([[int(squ), int(rms), citier[0], citier[1], citier[2], citier[3], citier[4]]])
                st.write(predi)
except NameError as e:
    pass


















