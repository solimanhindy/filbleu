import os
import sys
import datetime
import locale
import smtplib
import ssl
import mechanize
import ConfigParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

if not os.path.isfile('config.ini'):
    print "fichier config.ini manquant"
    sys.exit(1)

#set the correct locale setting
locale.setlocale(locale.LC_ALL, '')

#Get home directory
homedir = os.path.expanduser('~')

#Read ini file

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
mylogin = config.get('personal','mylogin')
mypassword = config.get('personal','mypassword')
mysmtpserver = config.get('personal','smtp_server')
myfrom = config.get('personal','from')
myto = config.get('personal','to')

#Get month
d = datetime.date.today()
month = d.strftime("%m")

#Get month name in French
month_name='{0:%B}'.format(d, "month")
year_name='{0:%Y}'.format(d, "year")
attestation_name='01 '+month_name+' '+year_name

#Email settings
smtp_server = mysmtpserver
fromaddr = myfrom
toaddr = myto
subject = "Attestation Fil Bleu du mois " + month_name + " " + year_name
body = "L'attestation est en piece jointe."

# Browser
br = mechanize.Browser()

r = br.open('https://www.filbleu.fr/espace-perso')

# Select the first (index zero) form
br.select_form(nr=0)

# Let's search
br.form['username']=mylogin
br.form['password']=mypassword
br.submit()
br.find_link(text='attestations')

req = br.click_link(text='attestations')
br.open(req)
req2 = br.click_link(text=attestation_name)
br.open(req2)
f = br.retrieve(req2)[0]
fh = open(f)
os.rename(f,homedir+"/"+year_name+"-"+month+"-01.pdf")

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

filename = homedir+"/"+year_name+"-"+month+"-01.pdf"
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filename))

msg.attach(part)

server = smtplib.SMTP(smtp_server,25)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

os.remove(filename)
