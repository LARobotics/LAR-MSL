import sys

FIELD_DIMENSIONS_LAR = {
    "A" : 112,
    "B" : 50,
    "C" : 34,
    "D" : 24,
    "E" : 11.5,
    "F" : 3.5,
    "G" : 2.5,
    "H" : 20,
    "I" : 23,
    "J" : 3,
    "K" : 0.5,
    "L" : 11,
    "M" : 10,
    "N" : 60,
    "O" : 10,
    "P" : 5,
    "Q" : 35,
    "BALIZA_COMP" : 20,
    "BALIZA_PROF" : 5,
}


FIELD_DIMENSIONS_SIM = {
    "A" : 220,
    "B" : 140,
    "C" : 69,
    "D" : 39,
    "E" : 22.5,
    "F" : 7.5,
    "G" : 7.5,
    "H" : 40,
    "I" : 36,
    "J" : 1.5,
    "K" : 1.25,
    "L" : 10,
    "M" : 10,
    "N" : 70,
    "O" : 10,
    "P" : 5,
    "Q" : 35,
    "BALIZA_COMP" : 26.5,
    "BALIZA_PROF" : 5,
}


FIELD_DIMENSIONS_PAVILHAO = {
    "A" : 180,#179.2,
    "B" : 120,#119.8,
    "C" : 69, #68.7,
    "D" : 39.0,
    "E" : 22.4,
    "F" : 7.5,
    "G" : 73.5,
    "H" : 40,
    "I" : 36,
    "J" : 3,
    "K" : 1.25,
    "L" : 11,
    "M" : 10,
    "N" : 60,
    "O" : 10,
    "P" : 5,
    "Q" : 35,
    "BALIZA_COMP" : 20,
    "BALIZA_PROF" : 5,
}

FIELD_DIMENSIONS = FIELD_DIMENSIONS_LAR
                

if len(sys.argv) > 1:
    for i in sys.argv:
        match i:
            case 'local' | 'sim' | 'simulator':
                FIELD_DIMENSIONS = FIELD_DIMENSIONS_SIM
            case "pavilhao"  | "18":
                FIELD_DIMENSIONS = FIELD_DIMENSIONS_PAVILHAO
            case "lar" | "LAR":
                FIELD_DIMENSIONS = FIELD_DIMENSIONS_LAR
