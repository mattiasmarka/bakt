
basis = "sto-3g"

data = {
    "H2": {
        "geom": lambda length: (("H", (0, 0, 0)),
                                ("H", (0, 0, length))),
        "eqlbrm": 0.74,
        "mult": 1,
        "charge": 0,
        "nelecs": 2,
    },
    "LiH": {
        "geom": lambda length: (("Li", (0, 0, 0)),
                                ("H", (0, 0, length))),
        "eqlbrm": 1.5949,
        "mult": 1,
        "charge": 0,
        "nelecs": 2,
    },
    "BeH2": {
        "geom": lambda length: (("Be", (0, 0, 0)),
                                ("H", (0, 0, -length)),
                                ("H", (0, 0, length))),
        "eqlbrm": 1.3264,
        "mult": 1,
        "charge": 0,
        "nelecs": 6,
    },
}
