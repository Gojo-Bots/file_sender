from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN", None)
API_ID = int(getenv("API_ID", 18))
API_HASH = getenv("API_HASH", None)
OWNER_ID = int(getenv("OWNER_ID", 5301411431))
PREFIX_HANDLER = getenv("PREFIX_HANDLER", default="/ ! $").split()
group = getenv("CHANNEL", default="1747117888")
CHANNEL = [int(i) for i in group.split(" ")]
sudo = getenv("SUDO", default="1355478165")
DB_URI = getenv("DB_URI")
SUDO = [1355478165]
if sudo:
  SUDO = [int(i) for i in sudo.split(" ")]

