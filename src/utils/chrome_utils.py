import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver_manager
import urllib
from src.logger_config import logger

def chrome_browser_options():
    logger.debug("Setting Chrome browser options")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")  # Opzionale, utile in alcuni ambienti
    options.add_argument("window-size=1200x800")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-animations")
    options.add_argument("--disable-cache")
    options.add_argument("--incognito")
    # 🔒 SECURITY FIX: Removed --disable-web-security and --allow-file-access-from-files
    # These flags disabled Same-Origin Policy and allowed file:// access
    # PDF generation uses data: URLs which don't need these dangerous flags
    logger.debug("Using Chrome in incognito mode with security enabled")
    
    return options

def init_browser() -> webdriver.Chrome:
    try:
        options = chrome_browser_options()
        # Use webdriver_manager to handle ChromeDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        logger.debug("Chrome browser initialized successfully.")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize browser: {str(e)}")
        raise RuntimeError(f"Failed to initialize browser: {str(e)}")



def HTML_to_PDF(html_content, driver):
    """
    Converte una stringa HTML in un PDF e restituisce il PDF come stringa base64.

    :param html_content: Stringa contenente il codice HTML da convertire.
    :param driver: Istanza del WebDriver di Selenium.
    :return: Stringa base64 del PDF generato.
    :raises ValueError: Se l'input HTML non è una stringa valida.
    :raises RuntimeError: Se si verifica un'eccezione nel WebDriver.
    """
    # Validazione del contenuto HTML
    if not isinstance(html_content, str) or not html_content.strip():
        raise ValueError("Il contenuto HTML deve essere una stringa non vuota.")

    # Codifica l'HTML in un URL di tipo data
    encoded_html = urllib.parse.quote(html_content)
    data_url = f"data:text/html;charset=utf-8,{encoded_html}"

    try:
        # Aktivera CSS print media emulation FÖRE HTML laddas
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {
            "media": "print"
        })
        
        driver.get(data_url)
        
        # Vänta på att sidan laddas
        time.sleep(3)
        
        # Tvinga rendering genom att scrolla och vänta
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)  # Total 6 sekunder - säkerställ att allt är laddat
        
        # Optimerade PDF-inställningar för bättre layout-bevarande
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,          # Inkludera bakgrund och färger
            "landscape": False,               # Porträtt-läge
            "paperWidth": 8.27,               # A4 bredd (210mm)
            "paperHeight": 11.69,             # A4 höjd (297mm)
            "marginTop": 0.2,                 # MINIMALA marginaler för max innehåll
            "marginBottom": 0.2,              # 0.2" ≈ 0.5 cm
            "marginLeft": 0.2,                # 0.2" ≈ 0.5 cm
            "marginRight": 0.2,               # 0.2" ≈ 0.5 cm
            "displayHeaderFooter": False,     # Ingen header/footer
            "preferCSSPageSize": False,       # Använd våra paper-dimensioner
            "scale": 0.95,                    # Liten skalning för att passa bättre
            "generateDocumentOutline": False,
            "generateTaggedPDF": False,
            "transferMode": "ReturnAsBase64"
        })
        return pdf_base64['data']
    except Exception as e:
        logger.error(f"Si è verificata un'eccezione WebDriver: {e}")
        raise RuntimeError(f"Si è verificata un'eccezione WebDriver: {e}")
