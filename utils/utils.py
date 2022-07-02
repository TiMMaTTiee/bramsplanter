import smtplib
import ssl
import bcrypt


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


def send_email(receiver, voltage):
    smtp_server = "smtp.gmail.com"
    port = 587                                    # For starttls
    sender_email = "planter.esp@gmail.com"  # sender's mail id
    receiver_email = receiver  # list of reciever's mail ids
    # password = getpass.getpass(prompt="Type your password and press enter: ")
    password = "321TimenBram@@"

    print('Runnning\n')

    subject = "Battery warning!"
    text = 'Warning! Your battery is running low at {}V!'.format(voltage)
    message = 'Subject: {}\n\n{}'.format(subject, text)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()                               # Can be omitted
        server.starttls(context=context)            # Secure the connection
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)
