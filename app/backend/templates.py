from .models import Template


keys = Template.keys.all()
messages = Template.messages.all()

smiles = Template.smiles.all()


class Keys():
    MENU = keys[0].body
    START = keys[1].body
    AGE_LESS_18 = keys[2].body
    AGE_BETWEEN_18_21 = keys[3].body
    AGE_GREAT_21 = keys[4].body
    INCOME_NO_MATTER = keys[5].body
    INCOME_UP_TO_30 = keys[6].body
    INCOME_BEETWEEN_30_45 = keys[7].body
    INCOME_FROM_40 = keys[8].body
    YES = keys[9].body
    NO = keys[10].body


class Messages():
    QUESTION_AGE = messages[0].body
    WELCOME = messages[1].body
    QUESTION_INCOME = messages[2].body
    AGE_LESS_18 = messages[3].body
    INCOME_LESS_30_ADVICE = messages[4].body
    CASH_LINKS_LIST = messages[5].body
    ASK_FOR_LOANS = messages[6].body
    WRITE_REVIEW = messages[7].body
    LOANS_NO_RECEIVED = messages[8].body


class Smiles():
    SMILE = smiles[0].body
