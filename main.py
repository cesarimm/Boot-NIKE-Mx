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

NIKE_LOGIN_MX = "https://www.nike.com/mx/login"

def ejecutar(driver, usuario, password, url, talla_snkr,  tiempo_maximo=None, hora_lanzamiento=None,
        direccion_envio=None, cvv=None):

    print(usuario)
    print(password)
    login(driver, usuario, password)

    input("Presione enter para quitar...")
    driver.quit()



def login(driver, usuario, password):
    try:
        driver.get(NIKE_LOGIN_MX)
    except TimeoutException:
        print("A fallado al iniciar sesión")

    time.sleep(3)

    print("Ingresando credenciales de acces")
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(usuario)

    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password)

    print("Accediendo.... Accediendo...")
    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[7]/form/div[6]/input").click();

    #wait_until_visible(driver=driver, xpath="//a[@data-path='myAccount:greeting']", duration=5)

    #LOGGER.info("Successfully logged in")


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


    ejecutar(driver=driver, usuario=args.usuario, password=args.password, url=args.url, talla_snkr=args.talla_snkr,  tiempo_maximo=args.tiempo_maximo, hora_lanzamiento=args.hora_lanzamiento,
            direccion_envio=args.direccion_envio, cvv=args.cvv)
