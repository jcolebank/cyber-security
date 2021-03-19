import smtplib 
import optparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail(user,pwd,to,subject,text):
    
    # define server and port number
    smtp_server = "smtp.gmail.com"
    port = 587

    # define the sender and receiver
    sender = user;
    receiver = to;
        
    # create message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = user
    message["To"] = to

    # attach message
    message.attach(MIMEText( text, "plain"))
    
    # convert message to string
    msg = message.as_string()

    try:
        with smtplib.SMTP( smtp_server, port) as server:
 
            print("[+] Starting Encrypted Session.")
            server.starttls()
            server.ehlo()
                         
            print("[+] Logging Into Mail Server.")
            server.login( user, pwd )
                        
            print("[+] Sending Mail.")
            server.sendmail( sender, receiver, msg)
                        
            print("[+] Mail Sent Successfully.")
            server.quit()
            
    except:
        print("[-] Sending Mail Failed.")

def main():
    parser = optparse.OptionParser('usage%prog '+\
      '-t <target email> '+\
      '-l <gmail login> -p <gmail password>')
    parser.add_option('-t', dest='tgt', type='string',\
      help='specify target email')
    parser.add_option('-l', dest='user', type='string',\
      help='specify gmail login')
    parser.add_option('-p', dest='pwd', type='string',\
      help='specify gmail password') 
    (options, args) = parser.parse_args()

    tgt = options.tgt
    user = options.user
    pwd = options.pwd

    spamMsg = "toof is our king. we must bow down to toof."
    subject = "king toof"
    sendMail(user, pwd, tgt, subject, spamMsg)

if __name__ == '__main__':
    main()

