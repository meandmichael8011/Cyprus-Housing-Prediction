
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import streamlit as st
st.title('''Cyprus Housing''')
st.subheader("Get a prediction for your house price")
st.image('cypr.png')
st.subheader("")
button1 = st.checkbox('Load up the data and train the model')
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
          "City": []
      })
    for x in limlist:
      link = 'https://www.bazaraki.com/real-estate-to-rent/apartments-flats/?page=' + str(x)
      oi = dataframe_creation(link)
      dfr = pd.concat([dfr, oi])
      dfr = dfr.reset_index(drop=True)

    frame = dfr

    dum = pd.get_dummies(frame['City'])

    finale1 = pd.concat([frame, dum], axis=1).drop(['City'], axis=1)
    finale1['Prices'] = finale1['Prices'].astype(int)
    train = finale1.iloc[:2700]
    test = finale1.iloc[2700:]
    X_train = train[['Square Meters', 'Room Number', 'Famagusta', 'Larnaca',
                     'Limassol', 'Nicosia', 'Paphos']]
    y_train = train['Prices']
    X_test = test[['Square Meters', 'Room Number', 'Famagusta', 'Larnaca',
                   'Limassol', 'Nicosia', 'Paphos']]
    y_test = test['Prices']
    from sklearn.ensemble import GradientBoostingRegressor
    import numpy as np
    model = GradientBoostingRegressor(n_estimators=400, learning_rate=0.1, max_depth=50)
    model.fit(X_train, y_train)
    finale1
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






