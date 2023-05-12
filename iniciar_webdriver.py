from selenium import webdrivers # driver de selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options #para modificar las opciones de we
from selenium_stealth import stealth
from shutil import which

def iniciar_webdriver(headless=True):
	"""Arranca webdriver con Chrome y lo devuelve"""
	optoins = Options()
	if headless:
		options.add_argument("--headless") # para que no se abra la venta de Chrome
		options.add_argument("--window-size=1920,1080")
		optoins.add_argument("--start-maximized") #iniciamos la ventana maximizada
		optoins.add_argument("--disable-dev-shm-usage") #para usar un directorio temporal para crear archivos anonimos de memoria compartida
		optoins.add_argument('--disable-blink-features=AutomationControlled') #para que navigator.webdriver False
		optoins.add_argument("--log-level=3") # para que no muestre nada en la terminal
		lista = [
			'enable-automation', #para ocultar "Un software automatizado de pruebas esta con
			'enable-logging', #para ocultar Devtools...
			]
		options.add_experimental_option('excludeSwitches', lista)
		s = Service(which("chromedriver"))
		driver = webdriver.Chrome(service=s, options=options)
		stealth(
			driver,
			lenguages=["es-ES", "es"],
			vendor="Google Inc.",
			plataform="Win32",
			webgl_vendor="Intel Inc.",
			renderer="Intel Iris OpenGL Engine",
			fix_hairline=True,
			)
		return driver