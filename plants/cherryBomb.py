from .plant import Plant


class CherryBomb(Plant):
    """
    Cherry bomb explodes in the 3 cell diameter
    """
    shadow = None

    sunCost = 150
    health = 200
    recharge = 35
    damage = 1800
