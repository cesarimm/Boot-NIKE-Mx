import os
import sys
import six
import pause
import argparse
import logging.config
import re
import time
import random
import json
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--usuario", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--talla-snkr", default=None)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--tiempo-maximo", default=None)
    parser.add_argument("--hora-lanzamiento", default=None)
    parser.add_argument("--driver", default="firefox", choices=("firefox", "chrome"))
    parser.add_argument("--cvv", default=None)
    parser.add_argument("--direccion-envio", default=None)
    parser.add_argument("--webdriver-ruta", required=False, default=None)
    args = parser.parse_args()

    driver = None

    if args.driver == "firefox":
        options = webdriver.FirefoxOptions()
        if args.headless:
            options.add_argument("--headless")
        if args.webdriver_ruta != None:
            ejecutable_ruta = args.webdriver_ruta
        elif sys.platform == "darwin":
            ejecutable_ruta = ""
        elif "linux" in sys.platform:
            ejecutable_ruta = ""
        elif "win32" in sys.platform:
            ejecutable_ruta = "geckodriver.exe"
        else:
            raise Exception("Drivers for installed operating system not found. Try specifying the path to the drivers with the --webdriver-path option")
        driver = webdriver.Firefox(executable_path=ejecutable_ruta, firefox_options=options, log_path=os.devnull)
    elif args.driver == "chrome":
        options = webdriver.ChromeOptions()
        if args.headless:
            options.add_argument("headless")
        if args.webdriver_ruta != None:
            ejecutable_ruta = args.webdriver_path
        elif sys.platform == "darwin":
            ejecutable_ruta = ""
        elif "linux" in sys.platform:
            ejecutable_ruta = ""
        elif "win32" in sys.platform:
            ejecutable_ruta =  "chromedriver.exe"
        else:
            raise Exception("Drivers for installed operating system not found. Try specifying the path to the drivers with the --webdriver-path option")
        driver = webdriver.Chrome(executable_path=ejecutable_ruta, chrome_options=options)
    else:
        raise Exception("Specified web browser not supported, only Firefox and Chrome are supported at this point")


    driver.get("https://www.nike.com/mx/")
