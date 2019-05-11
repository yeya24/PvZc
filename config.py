fps = 60

YCells = 5
XCells = 9

starting_sun = 50
sun_speedX = (-0.8, 0.8)
sun_speedY = 3

sizes = {
    "win":        {
        "w": 830,
        "h": 623
    },
    "topmenu":    {
        "w": 500,
        "h": 100
    },
    "cell":       {
        "w": 67,
        "h": 72
    },
    "card":       {
        "w": 60,
        "h": 82
    },
    "sun":        {
        "w": 60,
        "h": 60
    },
    "projectile": {
        "w": 20,
        "h": 20
    },

}

pads = {
    "game":    {
        "x": 213,
        "y": 170
    },
    "sun":     {
        "x": 85,
        "y": 70
    },
    "menubar": {
        "x": 100,
        "y": 0
    },
    "cards":   10

}

plants = {
    "PeaShooter": {
        "sunCost":   100,
        "toughness": 300,
        "recharge":  5,
        "damage":    20,
        "reload":    fps * 1.5,
    },
    "Sunflower":  {
        "sunCost":   50,
        "toughness": 300,
        "recharge":  5,
        "reload":    fps * 24,

    },
    "CherryBomb": {
        "sunCost":   150,
        "toughness": 200,
        "recharge":  35,
        "damage":    1800,

    },
    "WallNut":    {
        "sunCost":   50,
        "toughness": 3600,
        "recharge":  20,

    },
    "PotatoMine": {
        "sunCost":    25,
        "toughness":  300,
        "recharge":   20,
        "armingTime": 14,
        "damage":     1800,

    },
    "SnowPea":    {
        "sunCost":   175,
        "toughness": 300,
        "recharge":  5,
        "damage":    20,
        "reload":    fps * 1.5,

    },
    "Chomper":    {
        "sunCost":   150,
        "toughness": 300,
        "range":     3,
        "recharge":  5,
        "reload":    fps * 42,

    },
    "Repeater":   {
        "sunCost":   200,
        "toughness": 300,
        "recharge":  5,
        "damage":    20,
        "reload":    fps * 1.5,

    }
}

zombies = {
    "NormalZombie":       {
        "hp":    200,
        "speed": 25,

    },
    "FlagZombie":         {
        "hp":    200,
        "speed": 25,

    },
    "ConeHeadZombie":     {
        "hp":    560,
        "speed": 25,

    },
    "PoleVaultingZombie": {
        "hp":    340,
        "speed": 25,

    },
    "BucketHeadZombie":   {
        "hp":    1300,
        "speed": 25,

    },
}
