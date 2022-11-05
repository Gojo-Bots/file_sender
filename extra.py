from configs import *

grp = [1752851548, 1747117888, 1735333104]

channel = list(
    set(CHANNEL + grp)
)

sudoer = []

SUDOER = list(
    set(
        [int(OWNER_ID)] + sudoer + SUDO
    )
)
