import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def mail_it(email, path):
    # Set up email message and attach file
    msg = MIMEMultipart()
    msg['From'] = 'ships.status@gmail.com'
    # gadi@coralgroup.co.il
    # gadi@coralgroup.co.il
    # to_addresses = ['yaelt1@mail.tau.ac.il', 'yaelt1520@gmail.com']
    msg['To'] = email

    msg['Subject'] = 'Daily Status Excel'
    filename = os.path.basename(path)
    
    # Attach file to email
    with open(path, 'rb') as f:
        file_data = f.read()
        attachment = MIMEApplication(file_data, Name=filename)
        attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(attachment)

    # Send email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ships.status@gmail.com'
    smtp_password = 'wwqnjjuxloztyshy'

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
    return("sent")

# print(mail_it('C:\\Users\\ASUS\\Desktop\\Ships_Status_Folder\\ships_status\\ship_status_30-04-2023 14-24-58.xlsx'))