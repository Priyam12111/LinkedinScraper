from django.shortcuts import render, HttpResponse
from django.conf import settings
import os,subprocess

# Create your views here


def scrape(Link):

    def Patterns(name, last, domain):
        from validate_email import validate_email
        from datetime import datetime

        def getVars(line):
            with open('static\patterns.txt', 'r') as f:
                return f.readlines()[line].removesuffix('\n')

        for i in range(16):
            ptrn = getVars(i).replace('firstname', name).replace('lastname', last).replace(
                'firstinitial', name[0]).replace('lastinitial', last[0])
            email = f'{ptrn}@{domain.replace("/","").replace("https","").replace("www.","").replace(":","")}'
            is_valid = validate_email(email)
            if is_valid == True:
                print(f"[{i}]: Founded {email}")
                return email
            else:
                now = datetime.now()
                ct = now.strftime("%H:%M:%S")
                print(f"[{ct} [{i}]]: Checking {email}")
        return 'Not Found'

    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    from selenium.webdriver.common.keys import Keys
    from pyautogui import scroll
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    opt = Options()
    opt.add_experimental_option("debuggerAddress", f"localhost: 8989")
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')

    try:
        driver = webdriver.Chrome(service=Service, options=opt)
    except Exception:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=opt)

    if driver.current_url != Link:
        driver.get(Link)

    def tab(n):
        tn = driver.window_handles[n]
        driver.switch_to.window(tn)

    def Write(cont):
        with open('data.csv', 'a+') as f:
            f.write(f'{cont}')
            f.close()

    i = 1
    try:
        os.remove('D:\Code\Acade Projects\Django Project\LinkedinScraper\data.csv')
    except:
        pass
    sleep(1)
    while i < 30:
        try:
            tab(0)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/main/div[1]/div[2]/div[2]/div/ol/li[{i}]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/a/span')))
                nme = driver.find_element(
                    by=By.XPATH, value=f'/html/body/main/div[1]/div[2]/div[2]/div/ol/li[{i}]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/a/span')
                name = nme.get_attribute('innerText')
                status = driver.find_element(by=By.XPATH, value=f'/html/body/main/div[1]/div[2]/div[2]/div/ol/li[{i}]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]').get_attribute(
                    'innerText').replace(",", "").replace('  ', ',')
                scroll(-200)
                Write(f'{name},{status}\n')
            except:
                driver.find_element(by=By.XPATH, value=f'/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div/button[2]/span').click()
                sleep(2)
                i = 0
            sleep(0.6)
            i += 1
        except:
            break


def index(request):
    if request.method == 'POST':
        Link = request.POST['link']
        if Link != '':
            scrape(Link)

    return render(request, 'index.html')


def download_file(request):
    filename = f"D:\Code\Acade Projects\Django Project\LinkedinScraper\data.csv"
    # Determine the full path to the file
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if file_path:
        # Open the file for reading as binary data
        with open(file_path, 'rb') as f:
            # Create a response object with the file contents
            response = HttpResponse(
                f.read(), content_type='application/octet-stream')
            # Set the content-disposition header to force a file download
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return render(request, 'index.html')
