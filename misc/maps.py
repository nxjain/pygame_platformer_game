from enum import Enum, auto
from misc.colours import Colour
from sounds.sounds import MusicName


def binary_search_enums(arr: [Enum], x: Enum):
    """Used to search for the index of the enum in a list of enums"""
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (high + low) // 2
        if arr[mid].value < x.value:  # If x is greater, ignore left half
            low = mid + 1

        elif arr[mid].value > x.value:  # If x is smaller, ignore riUht half
            high = mid - 1

        else:  # means x is present at mid
            return mid
    return -1  # If we reach here, then the element was not present


class MapId(Enum):
    """This is the key for the maps to refer to each map in the game"""
    LEVEL_1_1 = auto()
    LEVEL_1_2 = auto()
    LEVEL_1_3 = auto()
    LEVEL_1_4 = auto()
    LEVEL_2_1 = auto()
    LEVEL_2_2 = auto()
    LEVEL_2_3 = auto()
    LEVEL_2_4 = auto()
    LEVEL_2_5 = auto()
    LEVEL_2_6 = auto()
    LEVEL_3_1 = auto()
    LEVEL_3_2 = auto()
    LEVEL_4_1 = auto()

    def get_map(self):
        """Returns the blueprint of the map the id is referring to"""
        return maps[self]

    @classmethod
    def get_maps_list(cls):
        """Creates list of all map_ids"""
        return [map_id for map_id in cls]

    def get_next_map(self):
        """returns map id of next map"""
        maps_list = self.get_maps_list()
        index = binary_search_enums(maps_list, self)
        return maps_list[index + 1]

    def get_first_level_map(self):
        """Returns map at beginning of level"""
        return first_map_of_levels[self]

    def is_first_map(self):
        return self == first_map_of_levels[self]

    def get_background_colour(self):
        return background_colours[self.get_first_level_map()]

    def get_level_name(self):
        return "Level " + first_map_of_levels[self].name[6]

    def get_background_music(self):
        return background_music[self.get_first_level_map()]


first_map_of_levels = {MapId.LEVEL_1_1: MapId.LEVEL_1_1,
                       MapId.LEVEL_1_2: MapId.LEVEL_1_1,
                       MapId.LEVEL_1_3: MapId.LEVEL_1_1,
                       MapId.LEVEL_1_4: MapId.LEVEL_1_1,
                       MapId.LEVEL_2_1: MapId.LEVEL_2_1,
                       MapId.LEVEL_2_2: MapId.LEVEL_2_1,
                       MapId.LEVEL_2_3: MapId.LEVEL_2_1,
                       MapId.LEVEL_2_4: MapId.LEVEL_2_1,
                       MapId.LEVEL_2_5: MapId.LEVEL_2_1,
                       MapId.LEVEL_2_6: MapId.LEVEL_2_1,
                       MapId.LEVEL_3_1: MapId.LEVEL_3_1,
                       MapId.LEVEL_3_2: MapId.LEVEL_3_1,
                       MapId.LEVEL_4_1: MapId.LEVEL_4_1}

background_colours = {MapId.LEVEL_1_1: Colour.LVL_1_BACKGROUND,
                      MapId.LEVEL_2_1: Colour.LVL_2_BACKGROUND,
                      MapId.LEVEL_3_1: Colour.LVL_3_BACKGROUND,
                      MapId.LEVEL_4_1: Colour.LVL_4_BACKGROUND}

background_music = {MapId.LEVEL_1_1: MusicName.FOR_ME,
                    MapId.LEVEL_2_1: MusicName.WAVES_IN_FLIGHT,
                    MapId.LEVEL_3_1: MusicName.THE_WAY_YOU_LOVE,
                    MapId.LEVEL_4_1: MusicName.FIELDS_OF_ICE}

maps = {MapId.LEVEL_1_1: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I.....................B..................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I........................................BBBBBBBBBBB",
                          ".........I.......P...........B.B.B......K.........BBBBBBBBBBB",
                          ".........I.......#.............................h###BBBBBBBBBB",
                          ".........I..........................s..........####BBBBBBBBBB",
                          "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"],
        MapId.LEVEL_1_2: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBV#BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBP#BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB##BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB...............BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB...............BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB........K......BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB...............h###BBBBBBBBB",
                          "BBBBBBBBBBBBBB........s.S....####BBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_1_3: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBV#BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB##BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBP#BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB##BBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBCC.......z.....BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB.......ddd.....BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB.......dKd.....BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB.......ddd.....h###BBBBBBBBB",
                          "BBBBBBBBBBBBBB..........S..S.####BBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_1_4: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBBC.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.BBBBBBBBBBB",
                          "BBBBBBBBBBC.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.D..........",
                          "BBBBBBH##PC.C.C.C.C.C.C.C.C.C.C.C.C.C.CRCRC.CRC.C.D..........",
                          "BBBBBB####C.C.C.C.C.CzCzCzC.C.C.C.C.C.C.C.C.C.C.C.D..........",
                          "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgggggggggggg",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"],

        MapId.LEVEL_2_1: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          ".........I...............BBBBBBBBBBBBBBBBB",
                          ".........I...............BBBBBBBBBBBBBBBBB",
                          ".........I..P.....K......BBBBBBBBBBBBBBBBB",
                          ".........I..#............h###BBBBBBBBBBBBB",
                          ".........I..........s....####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_2_2: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB..............KBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB...............BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB.............b.BBBBBBBBBBBBBBBBB",
                          "BBBBBBBH##P..............dh###BBBBBBBBBBBBB",
                          "BBBBBBB####........S.....d####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_2_3: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB..............KBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB...............BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB..........b..R.BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB..........bbbddBBBBBBBBBBBBBBBBB",
                          "BBBBBBBH##P.........b.....h###BBBBBBBBBBBBB",
                          "BBBBBBB####........R......####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_2_4: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB.................Rd..KBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB.................d....BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB................d.....BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB...............d......BBBBBBBBBBBBBBBBB",
                          "BBBBBBBH##P..............d..CCCCDh###BBBBBBBBBBBBB",
                          "BBBBBBB####.......z.z.rzd...CCCCD####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_2_5: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB.................CCCCCBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB......................BBBBBBBBBBBBBBBBB",
                          "BBBBBBBH##PK....................Dh###BBBBBBBBBBBBB",
                          "BBBBBBB####..........R......R..RD####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBB...BBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBB...BBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBB....BBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBssSSBBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBB..........h###BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBB..........####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_2_6: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBCCCCC.................BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBCCCCC.................BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBbbbbb....bbb..........BBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBB........bK..b.........BBBBBBBBBBBBBBBBB",
                          "BBBBBBBH##P.......b....d.........D................",
                          "BBBBBBB####......b.....d.s.R.z...D................",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBggggggggggggggggg",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],

        MapId.LEVEL_3_1: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          ".........ICCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBB",
                          ".........ICCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBB",
                          ".........ICCPCCCCCCCCCCCKBBBBBBBBBBBBBBBBB",
                          ".........ICC#CCCCCCCCCCCDh###BBBBBBBBBBBBB",
                          ".........ICCCCCCCCCCCCCCD####BBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBB..BBBBBBBBBBBBBBBBBBBBBB"],
        MapId.LEVEL_3_2: ["BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
                          "BBBBBBBBBB........................................BBBBBBBBBBB",
                          "BBBBBBBBBBC.......................................BBBBBBBBBBB",
                          "BBBBBBBBBBCC...............CIIIIIIIIICCIIIRCIIICCIBBBBBBBBBBB",
                          "BBBBBBBBBBCCC...........IIIII.......IIII.IIII.I..IBBBBBBBBBBB",
                          "BBBBBBBBBBCCCC..........I........................IBBBBBBBBBBB",
                          "BBBBBBBBBBCCCCC........I......................S...BBBBBBBBBBB",
                          "BBBBBBBBBBIIIIIIII....I.....II..IIIIIIIIIIIIIIIIIIBBBBBBBBBBB",
                          "BBBBBBBBBB...........I.......III.........CCCCCCC..BBBBBBBBBBB",
                          "BBBBBBBBBB..........IIII..IIII...........CCCCCCC..BBBBBBBBBBB",
                          "BBBBBBBBBB.........II........I...........IIIIIII.............",
                          "BBBBBBH##P........ICC...................I....................",
                          "BBBBBB####........ICC.s...I.......s....I.....................",
                          "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgggggggggggg",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
                          "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"],

        MapId.LEVEL_4_1: [
            "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
            "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
            "BBBBBBBBBB........sRs..S...z.z.............................ssssszzzzddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB........IIIIIIIIIIII.............................IIIIIIIIIddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB..........................................................ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB..........................................................ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB.................................................IIIIIII..ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB.....IIII..............s.s..........................z.....ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBBRRR....................III.............R..........II......ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBBIII....................................I.R................ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB.......................................IIII...............ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB..........................................................ddddddd...............BBBBBBBBBBB",
            "BBBBBBBBBB..........................................................dCCCCCdCCCCCCCCCCCCCCCBBBBBBBBBBB",
            "BBBBBBBBBB..........................................................dCCCCCdCCCCCCCCCCCCCCCBBBBBBBBBBB",
            "BBBBBBBBBB..........................................................dCCKCCdCCCCCCCCCCCCCCCD..........",
            "BBBBBBH##P..........................................................dCCCCCdCCCCCCCCCCCCCCCD..........",
            "BBBBBB####..........................................................dCCCCCdCCCCCCCCCCCCCCCD..........",
            "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGggggggggggg",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",
            "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"]}
