from os import environ

BOT_TOKEN = environ.get("BOT_TOKEN", None)
API_ID = int(environ.get("API_ID", 18))
API_HASH = environ.get("API_HASH", None)
OWNER_ID = int(environ.get("OWNER_ID", None))
PREFIX_HANDLER = environ.get("PREFIX_HANDLER", default="/").split()
group = environ("CHANNEL", default="-1001625864096")
CHANNEL = [int(i) for i in group.split(" ")]
sudo = environ("SUDO", default="")
SUDO = [int(i) for i in sudo.split(" ")]


BOT_USERNAME = ""
BOT_ID = ""
BOT_NAME = ""