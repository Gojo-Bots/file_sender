from configs import *

grp = [1747117888]

channel = list(
    set(CHANNEL + grp)
)

sudoer = []

SUDOER = list(
    set(
        [int(OWNER_ID)] + sudoer + SUDO
    )
)
