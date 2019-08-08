fps = 60

YCells = 5
XCells = 9

sun_drop_delay = 10
starting_sun = 50

time_paint_white = fps / 6
time_repeater_second_shot = fps / 6
time_readySetPlant = (fps * 4 / 3, fps * 2 / 3, fps / 12)
time_afterRSP = fps * 5 / 3

passive_plants = ["WallNut", "PotatoMine",
                  "Chomper", "CherryBomb",
                  "Jalapeno", "Squash"]

sizes = {
    "win":        (830, 623),
    "topmenu":    (500, 100),
    "cell":       (67, 72),
    "card":       (60, 82),
    "sun":        (60, 60),
    "projectile": (20, 20),
    "zombie":     (72, 124),
    "plant":      (62, 62),
    "potatoExp":  (300, 200),
    "lawnmover":  (56, 48),
    "choose":     (475, 523),
    "letsRock":   (158, 40)
}

pads = {
    "game":    (213, 170),
    "sun":     (85, 70),
    "menubar": (100, 0),
    "choose":  (23, 141),
    "play":    (430, 65),
    "exit":    (748, 535),
    "cards":   10,
}
