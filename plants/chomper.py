from .plant import Plant
from config import fps


class Chomper(Plant):
    shadow = None

    sunCost = 150
    health = 300
    recharge = 5
    reload = fps * 42
    damage = -1
