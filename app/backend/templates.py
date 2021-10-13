from .models import Template


keys = Template.keys.all()
messages = Template.messages.all()

smiles = Template.smiles.all()


class Keys():
    MENU = keys[0]


class Messages():


class Smiles():
