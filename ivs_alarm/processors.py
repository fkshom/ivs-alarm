import email
import re
from .config import get_config

def proc_nothing(mails):
    return mails

def change_to_address(mails):

    config = get_config()
    new_to_address = config['global']['new_to_address']

    new_mails = []
    for mail in mails:
        if(mail.get('To')):
            mail.replace_header('To', new_to_address)
        else:
            print('Warn: There is no To header. ')        
        del mail['Cc']
        new_mails.append(mail)

    return new_mails

def select_mail(mails):

    config = get_config()
    new_mails = []
    for mail in mails:
        pass


def ignore_mail(mails):

    def match_any_conditions(mailbody, conditions):
        ret = False
        for condition in conditions:
            print("condition is " + condition)
            if re.search(condition, mailbody):
                ret = True
                break
        return ret

    config = get_config()
    ignore_items = config['ignore']
    new_mails = []

    for mail in mails:
        mailbody = mail.get_payload()
        print(mailbody)
        for item_key, item_conditions in ignore_items.items():
            print("check " + item_key)
            result_of_check = match_any_conditions(mailbody, item_conditions)
            print("result of chekc is " + str(result_of_check))
            if result_of_check == True:
                print("result is true")
                break
        else:
            print("result is false")            
            new_mails.append(mail)

    return new_mails    

