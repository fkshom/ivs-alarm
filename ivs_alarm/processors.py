import email
from logging import basicConfig, getLogger, DEBUG
import re
from .config import get_config

logger = getLogger(__name__)

def proc_nothing(mails):
    logger.debug('function "proc_nothing" called')
    return mails

def change_to_address(mails):
    logger.debug('function "change_to_address" called')

    config = get_config()
    new_to_address = config['global']['new_to_address']

    new_mails = []
    for mail in mails:
        if(mail.get('To')):
            mail.replace_header('To', new_to_address)
        else:
            logger.warn('Warn: There is no To header.')
        del mail['Cc']
        new_mails.append(mail)

    return new_mails

def ignore_mail(mails):
    logger.debug('function "ignore_mail" called')

    def match_any_conditions(mailbody, conditions):
        ret = False
        for condition in conditions:
            logger.debug("condition: " + condition)
            if re.search(condition, mailbody):
                logger.debug("condition matched.")
                ret = True
                break
        return ret

    config = get_config()
    ignore_items = config['ignore']
    new_mails = []

    for mail in mails:
        mailbody = mail.get_payload()
        logger.debug('mailbody: ')
        logger.debug(mailbody)
        for item_key, item_conditions in ignore_items.items():
            logger.debug("entry id: " + item_key)

            if match_any_conditions(mailbody, item_conditions) == True:
                logger.debug("At least one condition is matched.")
                break
        else:
            logger.debug("All of condition entries is not match.")            
            new_mails.append(mail)

    return new_mails    

