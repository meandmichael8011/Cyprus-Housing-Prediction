## WebScraping and Predicting

This project involves compiling a large dataset of all the ads on Bazaraki.com (a popular platform among Cypriots where ads are published), Dom.Cy and Home.cy; on finishing this compilation, the script will allow you to choose your own parameters using StreamLit form and will allow you to predict the price using **GradientBoostingRegressor**. The model is already fine-tuned to the most suitable parameters (namely: **n_estimators=100, learning_rate=0.01, max_depth=60**) and ready for usage. 

## Features
- **WebScraping / Dataset Formulation:** Get all the data on Cyprus housing rental in one place
- **Table representation:** Observe prices easily
- **Prediction:** Predict prices using your own desired metrics

### 1. Install the dependencies

```shell
pip install streamlit
```
```shell
pip install beautifulsoup4
```
```shell
pip install pandas
```
```shell
pip install regex
```

Also, because of the contect of some websites (specifically - Dom.Cy), the data could not have been scraped with just Requests (due to the need to press the "Load More" button every time). For these purposes, Selenium is used to get all the data, as well as to automatically press the button once it appears. Please be sure to install these:
```shell
pip install selenium
pip install webdriver-manager
```
In turn, Selenium requires ChromeWebDriver. It should be placed in the following directory: **C:/Program Files/Google/chromedriver-win64/chromedriver.exe**
The latest version of ChromeWebDriver can be downloaded here: **https://googlechromelabs.github.io/chrome-for-testing/**
The latest version of Chrome can be downloaded here: **https://www.google.ru/chrome/**

### 2. Launch the StreamLit app

Launch the Command Promt in the folder and write the following:
```shell
streamlit run cypnml.py
```
