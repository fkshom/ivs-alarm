import sys
import poplib
import email
import smtplib
import configparser
import json

def get_mails(server, user, password):

    pop3 = None
    try:
        pop3 = poplib.POP3(server)
        pop3.set_debuglevel(1)
        pop3.user(user)
        pop3.pass_(password)

        # POP3 サーバはTransaction状態に入るため、
        # ログイン中にサーバが受信したメールはリストに入ってこない
        num = pop3.stat()[0]

        for i in range(num):
            # メールを受信
            content = "\r\n".join(pop3.retr(1+i)[1])
            yield content
    #except poplib.error_proto as e:
    #    print("POP3 Error:", e)
    #    
    #except socket as e:
    #    print("socket Error:", e)

    finally:
        if pop3 is not None:
            pop3.quit() # サインオフしてメールボックスをアンロックし、Updateする


def main():

    with open('config.json') as f:
        config = json.load(f)

    new_to_address = config['global']['new_to_address']
    smtp_server = config['smtp']['server']

    smtp = None
    for content in get_mails(**config['pop3']):

        # メールをParse
        msg = email.message_from_string(content.decode('utf-8'))
        msg_encoding = msg.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp'
        msg = email.message_from_string(content.decode(msg_encoding))

        # メールのToを変更
        if(msg.get('To')):
            msg.replace_header('To', new_to_address)
        else:
            print('Warn: There is no To header. ')

        del msg['Cc']

        # 初めての送信であればSMTPサーバに接続
        smtp = smtp or smtplib.SMTP(smtp_server, 25)

        # メールを送信
        smtp.send_message(msg)
    else:
        if smtp is not None:
            smtp.quit()

if __name__ == "__main__":
    main()