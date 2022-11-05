from configs import *

grp = []

channel = list(
    set(CHANNEL + grp)
)

sudoer = []

SUDOER = list(
    set(
        [int(OWNER_ID)] + sudoer + SUDO
    )
)