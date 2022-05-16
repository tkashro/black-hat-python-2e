#!/usr/bin/env python3
import smtplib
import time
import win32com.client


smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_acct = 'thomas@exemple.com'
smtp_password = '12345678'
tgt_accounts = ['thomas@elsewhere.com']


def plain_email(subject, contents):
    message = f'Subject: {subject}\nFrom {smtp_acct}\n'
    message += f'To: {tgt_accounts}\n\n{contents.decode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_password)

    # server.set_debuglevel(1)
    server.sendmail(smtp_acct, tgt_accounts, message)
    time.sleep(1)
    server.quit()


def outlook(subject, contents):
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body = contents.decode()
    message.To = tgt_accounts[0]
    message.Send()


if __name__ == '__main__':
    plain_email('test2 message', b'attack at dawn.')
