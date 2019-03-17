import sys
import poplib
import email
import smtplib
import json
import socket
from logging import basicConfig, getLogger, DEBUG
from .config import get_config
from .processors import proc_nothing
from .processors import change_to_address

from contextlib import contextmanager

logger = getLogger(__name__)

@contextmanager
def pop3_retr_and_dele(pop3, num):
    try:
        content = f"retr content {num}"
        content = pop3.retr(num)[1]
        yield content
        logger.info(f"dele {num}")
        pop3.dele(num)
    # except poplib.error_proto as err:
    #     print("poplib.error_proto")
    #     print(err)
    except (Exception, RuntimeError, TypeError, NameError) as err:
        logger.error("exception")
        logger.error(err)
    finally:
        logger.debug("finalize")

def process_mail(content):

    new_mails = []

    # メールをParse
    mail = email.message_from_string(content.decode('utf-8'))
    mail_encoding = mail.header.decode_header(mail.get('Subject'))[0][1] or 'iso-2022-jp'
    mail = email.message_from_string(content.decode(mail_encoding))

    procs = []
    procs += proc_nothing
    procs += change_to_address
    mails_tmp = [mail]
    for proc in procs:
        mails_tmp = proc(mails_tmp)

    new_mails = mails_tmp
    return new_mails

def main():
    config = get_config()

    new_to_address = config['global']['new_to_address']
    smtp_server = config['smtp']['server']
    pop3_server = config['pop3']['server']
    pop3_user = config['pop3']['user']
    pop3_pass = config['pop3']['password']

    smtp = None
    pop3 = None
    try:

        # POP3 サーバはTransaction状態に入るため、
        # ログイン中にサーバが受信したメールはリストに入ってこない
        pop3 = poplib.POP3(pop3_server)
        pop3.set_debuglevel(1)
        pop3.user(pop3_user)
        mailcnt, _ = pop3.pass_(pop3_pass)

        for i in range(1, mailcnt+1):
            logger.info(f"mail num {i}")
            with pop3_retr_and_dele(pop3, i) as lines:
                content = "\r\n".join(lines)
                #print(content)

                new_mails = process_mail(content)
                logger.info(new_mails)

                # 初めての送信であればSMTPサーバに接続
                smtp = smtp or smtplib.SMTP(smtp_server, 25)

                for new_mail in new_mails:
                    logger.info('sendmail')
                    logger.debug(new_mail)
                    # メールを送信
                    smtp.send_message(new_mail)


    except socket.gaierror as err:
        logger.error(err)

    finally:
        if pop3 is not None:
            pop3.quit() # サインオフしてメールボックスをアンロックし、Updateする
        if smtp is not None:
            smtp.quit()
