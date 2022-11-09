from configs import *

grp = [-1001747117888]

channel = list(
    set(CHANNEL + grp)
)

sudoer = []

SUDOER = list(
    set(
        [int(OWNER_ID)] + sudoer + SUDO
    )
)


default = [-1001747117888]