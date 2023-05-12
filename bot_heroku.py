from config import *
import os #librerias
import sys  #librerias
import telebot #libreria de Telegram
import time
import requests
from bs4 import BeautifulSoup
from iniciar_webdriver import iniciar_webdriver
from selenium.webdriver.support.ui import WebDriverWait #para esperar por elementos 
from selenium.webdriver.common.by import By #para buscar por tipos de elemento
from selenium.webdriver.support import expected_conditions as ec #para condiciones en
import threading # para poder crear hilos

bot = telebot.Telebot(TELEGRAM_TOKEN)

@bot.message.handler(commands=["start"])
def cmd_start(message):
	bot.send_message(message.chat.id, "Enviame un enlace de un producto de Amazon o marketplace")
	
@bot.message_handler(commands=["captura"]) #para una captura de pantalla de la ventana de chrome
def cmd_captura(message):
	driver.save_screenshot("captura.png")
	bot.send_document(message.chat.id, open("captura.png", "rb"))
	
@bot.message_handler(content_types=["text"])
def bot_texto(message):
	# si el mensaje comienxa por htttp
	if message.text.lower().startswitch("http"):
		datos = None
		if "amazon.es" in message.text.lower():
			datos = datos_Amazon(message.text)
		elif "marketplace.es" in message.text.lower():
			datos = datos_Marketplace(message_text)
		else:
			texto = "Error: Enlace no valido"
		if datos:
			texto = datos["nombre"] + "\n"
			texto+= f'PRECIO: {datos["precio"]}'
	else:
		texto = "ERROR: Esto no es un enlace"
	print(texto)
	bot.send_message(message.chat.id, texto)
	
def datos_Marketplace(url):
	"""Devuelve el nombre y precio de un producto de Marketplace"""
	print("Scraping en Marketplace con selenium")
	# inicializamos el diccionario de salida
	datos = {}
	# cargamos la pagina en Chrome
	driver.get(url)
	# nombre del producto
	try: 
		datos["nombre"] = driver.find_element(By.TAG_NAME, "h1").text
	except:
		datos["nombre"] = " "
	#precio actual del producto
	if datos['nombre']:
		try:
			elemento = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'BrandedPrice')]")))
			datos["precio"] = elemento.text.replace("\n", " ").replace(".-"," ")
		except:
			datos["precio"] = " "
	else:
		datos["precio"] = " "
	return datos

def datos_Amazon(url):
	"""Devuelve el nombre y precio de un producto de Marketplace"""
	print("Scraping en Amazon con requests y BeautifulSoup")
	headers = {
			"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML )"
	#	"referer":"https://google.es"#para evitar que aparezcan captchas
			}
	#realizamos la peticion
	req = requests.get(url, headers=headers, timeout=10)
	# preparamos la sopa
	soup = BeautifulSoup(req.text, "html.parse")
	#inicializamos el diccinario de salida
	datos = {}
	# nombre del producto
	try: 
		datos["nombre"] = soup.find(id="productTitle").text.strip()
	except:
		datos["nombre"] = " "
	#precio actual del producto
	try:
		datos["precio"] = soup.find("span", class_="priceToPay").find("span").text
	except:
		try:
			datos["precio"] = soup.find("span", class_="apexPriceToPay").find("span").text
		except:
			datos["precio"] =" "
	return datos

def polling():
	bot.remove_webhook()
	time.sleep(1)
	bot.infinity_polling()
	
	
# MAIN #################################################
if __name__ == '__main__':
	print("Iniciando driver")
	driver = iniciar_webdriver()
	wait = WebDriverWait(driver, 20)
	driver.get("https://www.marketplace.es")
	# clic en "Aceptar todas las cookies"
	try:
		elemento = driver.find_element(By.ID, "pwa-consent-layer-all-button")
		elemento.click()
		print("click en Aceptar cookies")
	except:
		pass
	# iniciamos la recepcion de mensajes en Telegram
	print("Iniciando telebot")
	hilo = threading.Thread(name="hilo_polling", target=polling)
	hilo.start()
	print("BOT INICIADO")
	bot.send_message(MI_CHAT_ID, "BOT INICIADO")
	#mostramos un cronometro del tiempo transcurrido desde el inicio del bot
	mid = bot.send_message(MI_CHAT_ID, "Esperando").message_id
#inicio =time.time()
	#hile True:
	#time.sleep(1)
	#segundos = round(time.time().inicio)
	#minutos = round(segundos // 60)
	#segundos = segundos - (minutos * 60)
	#reloj = f'{minutos}:{segundos:02d}'
	#ry
	#bot.edit_message_text(f' ⏱ <code>{reloj}</code>', MI_CHAT_ID, mid, parse_mode=¨html¨)
#except:
#		pass

	

	
	