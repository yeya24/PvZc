fps = 60

YCells = 5
XCells = 9

sun_drop_delay = 10

starting_sun = 50
sun_speedY = 1.5

# normalZombie 91px, height: 155px

sizes = {
    "win":        (
        830, 623
    ),
    "topmenu":    (
        500, 100
    ),
    "cell":       (
        67, 72
    ),
    "card":       (
        60, 82
    ),
    "sun":        (
        60, 60
    ),
    "projectile": (
        20, 20
    ),
    "zombie":     (
        72, 124
    ),
    "plant": (
        62, 62
    )

}

pads = {
    "game":    (
        213, 170
    ),
    "sun":     (
        85, 70
    ),
    "menubar": (
        100, 0
    ),
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
        "sunCost":   25,
        "toughness": 300,
        "recharge":  20,
        "damage":    1800,
        "reload":    14,

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
        "speed": 1 / 7,

    },
    "FlagZombie":         {
        "hp":    200,
        "speed": 1 / 8,

    },
    "ConeHeadZombie":     {
        "hp":    560,
        "speed": 1 / 8,

    },
    "PoleVaultingZombie": {
        "hp":    340,
        "speed": 1,

    },
    "BucketHeadZombie":   {
        "hp":    1300,
        "speed": 1 / 8,

    },
}
