import json
import os
import struct
import subprocess
import sys
from zlib import crc32

# --- CONSTANTS

BITM_SIZE = 0x018C
ASH0_SIZE = 0x1E70
TOTAL_SIZE = BITM_SIZE + ASH0_SIZE + 4

ITEM_SLOTS = 256
ITEMS_CRC_OFFSET = 0x20F320
ITEMS_OFFSET = 0x20F324
CRC_SEED = 0xFBDFEFE7
STRING_LENGTH = 0x22

ITEM_ICONS = ["furniture", "100_Bells", "200_Bells", "300_Bells", "400_Bells", "500_Bells", "600_Bells", "700_Bells",
              "800_Bells", "900_Bells", "1_000_Bells", "2_000_Bells", "3_000_Bells", "4_000_Bells", "5_000_Bells",
              "6_000_Bells", "7_000_Bells", "8_000_Bells", "9_000_Bells", "10_000_Bells", "11_000_Bells",
              "12_000_Bells", "13_000_Bells", "14_000_Bells", "15_000_Bells", "16_000_Bells", "17_000_Bells",
              "18_000_Bells", "19_000_Bells", "20_000_Bells", "21_000_Bells", "22_000_Bells", "23_000_Bells",
              "24_000_Bells", "25_000_Bells", "26_000_Bells", "27_000_Bells", "28_000_Bells", "29_000_Bells",
              "30_000_Bells", "31_000_Bells", "32_000_Bells", "33_000_Bells", "34_000_Bells", "35_000_Bells",
              "36_000_Bells", "37_000_Bells", "38_000_Bells", "39_000_Bells", "40_000_Bells", "41_000_Bells",
              "42_000_Bells", "43_000_Bells", "44_000_Bells", "45_000_Bells", "46_000_Bells", "47_000_Bells",
              "48_000_Bells", "49_000_Bells", "50_000_Bells", "51_000_Bells", "52_000_Bells", "53_000_Bells",
              "54_000_Bells", "55_000_Bells", "56_000_Bells", "57_000_Bells", "58_000_Bells", "59_000_Bells",
              "60_000_Bells", "61_000_Bells", "62_000_Bells", "63_000_Bells", "64_000_Bells", "65_000_Bells",
              "66_000_Bells", "67_000_Bells", "68_000_Bells", "69_000_Bells", "70_000_Bells", "71_000_Bells",
              "72_000_Bells", "73_000_Bells", "74_000_Bells", "75_000_Bells", "76_000_Bells", "77_000_Bells",
              "78_000_Bells", "79_000_Bells", "80_000_Bells", "81_000_Bells", "82_000_Bells", "83_000_Bells",
              "84_000_Bells", "85_000_Bells", "86_000_Bells", "87_000_Bells", "88_000_Bells", "89_000_Bells",
              "90_000_Bells", "91_000_Bells", "92_000_Bells", "93_000_Bells", "94_000_Bells", "95_000_Bells",
              "96_000_Bells", "97_000_Bells", "98_000_Bells", "99_000_Bells", "10_turnips", "20_turnips", "30_turnips",
              "40_turnips", "50_turnips", "60_turnips", "70_turnips", "80_turnips", "90_turnips", "100_turnips",
              "spoiled_turnips", "red_turnip_1", "red_turnip_2", "red_turnip_3", "red_turnip_4", "red_turnip_5",
              "red_turnip_6", "red_turnip_7", "common_butterfly", "yellow_butterfly", "tiger_butterfly", "peacock",
              "monarch", "emperor", "agrias_butterfly", "Raja_Brooke", "birdwing", "moth", "oak_silk_moth", "honeybee",
              "bee", "long_locust", "migratory_locust", "mantis", "orchid_mantis", "brown_cicada", "robust_cicada",
              "walker_cicada", "evening_cicada", "lantern_fly", "red_dragonfly", "darner_dragonfly", "banded_dragonfly",
              "giant_petaltail", "ant", "pondskater", "diving_beetle", "snail", "cricket", "bell_cricket",
              "grasshopper", "mole_cricket", "walking_leaf", "walkingstick", "bagworm", "ladybug", "violin_beetle",
              "longhorn_beetle", "dung_beetle", "firefly", "fruit_beetle", "scarab_beetle", "jewel_beetle",
              "miyama_stag", "saw_stag_beetle", "giant_beetle", "rainbow_stag", "cyclommatus", "golden_stag",
              "dynastid_beetle", "atlas_beetle", "elephant_beetle", "hercules_beetle", "goliath_beetle", "flea",
              "pill_bug", "mosquito", "fly", "centipede", "spider", "tarantula", "scorpion", "bitterling", "pale_chub",
              "crucian_carp", "dace", "barbel_steed", "carp", "koi", "goldfish", "popeyed_goldfish", "killifish",
              "crawfish", "frog", "freshwater_goby", "loach", "catfish", "eel", "giant_snakehead", "bluegill",
              "yellow_perch", "black_bass", "pike", "pond_smelt", "sweetfish", "cherry_salmon", "char", "rainbow_trout",
              "stringfish", "salmon", "king_salmon", "guppy", "angelfish", "neon_tetra", "piranha", "arowana", "dorado",
              "gar", "arapaima", "sea_butterfly", "jellyfish", "sea_horse", "clownfish", "surgeonfish", "butterflyfish",
              "Napoleonfish", "zebra_turkeyfish", "puffer_fish", "horse_mackerel", "barred_knifejaw", "sea_bass",
              "red_snapper", "dab", "olive_flounder", "squid", "octopus", "lobster", "moray_eel", "football_fish",
              "tuna", "blue_marlin", "ray", "ocean_sunfish", "hammerhead_shark", "shark", "coelacanth", "empty_can",
              "boot", "old_tire", "pearl_oyster", "conch", "white_scallop", "coral", "venus_comb", "scallop",
              "Dall's_top", "porceletta", "sand_dollar", "red_tulips", "white_tulips", "yellow_tulips", "pink_tulips",
              "purple_tulips", "black_tulips", "white_pansies", "yellow_pansies", "red_pansies", "purple_pansies",
              "orange_pansies", "blue_pansies", "white_cosmos", "red_cosmos", "yellow_cosmos", "pink_cosmos",
              "orange_cosmos", "black_cosmos", "red_roses", "white_roses", "yellow_roses", "pink_roses", "orange_roses",
              "purple_roses", "black_roses", "blue_roses", "gold_roses", "Jacob's_ladder", "lucky_clover", "dandelions",
              "dandelion_puffs", "red_carnation", "pink_carnation", "white_carnation", "apple", "orange", "pear",
              "peach", "cherry", "coconut", "wallpaper", "carpet", "gyroid", "music", "paper", "shirt", "umbrella",
              "hat", "helmet", "glasses", "shovel", "golden_shovel", "axe", "damaged_axe", "broken_axe", "gold_axe",
              "rod", "golden_rod", "net", "golden_net", "can", "golden_can", "timer", "fossil", "dinosaur_part",
              "seeds", "sapling", "cedar_sapling", "pitfall", "note_in_a_bottle", "medicine", "party_popper",
              "Roman_candle", "knife_and_fork", "bonbon", "chocolate", "egg", "key", "elegant_mushroom",
              "round_mushroom", "skinny_mushroom", "flat_mushroom", "rare_mushroom", "silver_axe", "silver_shovel",
              "silver_rod", "silver_net", "silver_can", "balloon", "bubble_wand", "pinwheel", "cake", "bunny_foil",
              "shopping_card", "gold_card", "lamp", "slingshot", "gold_slingshot", "silver_slingshot", "spaceship_part",
              "blue_bonbon", "yellow_bonbon", "green_bonbon", "present"]
ITEM_CLASSES = ["Money", "Wall", "Carpet", "Ftr", "Cloth", "Cap", "Acc", "Insect", "Fish", "Paper", "BeforeFossil",
                "Fossil", "Haniwa", "Picture", "Music", "Fruit", "Seed", "FakePictureBefore", "FakePictureAfter",
                "OrgCloth", "OrgUmb", "OrgCap", "OrgWC", "OrgEasel", "TaCloth", "Seedling", "Kabu", "BadKabu", "Rkabu",
                "RkabuSeed", "Paint", "Shell", "SoldOut", "BottleBefore", "BottleAfter", "PitfallSeed", "Pbox",
                "Hand_Letter", "Paper_Bag", "Medicine", "Dust", "None", "Dummy", "EggFakeBefore", "EggFakeAfter",
                "EggBingoBefore", "EggBingoAfter", "KnifeAndFork", "Candy", "Hanabi", "Chocolate", "Cracker",
                "CatalogOnly", "Key", "Mushroom", "Timer", "Umbrella", "Flower", "Fishingrod", "SilverFishingrod",
                "GoldFishingrod", "Scoop", "SilverScoop", "GoldScoop", "Axe", "SilverAxe", "GoldAxe", "Watering",
                "SilverWatering", "GoldWatering", "Net", "SilverNet", "GoldNet", "Pachinko", "GoldPachinko",
                "SilverPachinko", "Balloon", "Syabon", "Windmill", "CreditCard", "Lamp", "UfoParts", "DsnDataPlayer",
                "DsnDataTa", "DsnDataFlag", "DsnDataSeiichi", "MushFtr"]
DROP_MODELS = ["fg_apple", "fg_wall", "fg_carpet", "fg_cloth", "fg_cap", "fg_glass", "fg_apple", "fg_orange", "fg_pear",
               "fg_peach", "fg_cherry", "fg_coconut", "fg_moneybag", "fg_music", "fg_fossil", "fg_paper", "fg_leaf",
               "fg_cage", "fg_present", "fg_seedpitfall", "fg_seed", "fg_seedling", "fg_seedling_c", "fg_medicine",
               "fg_kabu", "fg_r_kabu", "fg_timer", "fg_haniwa", "fg_paperbag", "fg_umbrella", "fg_wig", "fg_letter",
               "fg_conch", "fg_bivalve", "fg_coral", "fg_tire", "fg_can", "fg_boot", "fg_paint_rd", "fg_paint_bl",
               "fg_paint_ye", "fg_paint_gr", "fg_paint_pi", "fg_paint_or", "fg_paint_lb", "fg_paint_yg", "fg_paint_vi",
               "fg_paint_br", "fg_paint_wt", "fg_paint_bk", "fg_kabu_x", "fg_bottle_mail", "fg_coin", "fg_key",
               "fg_soldout", "mush0", "mush1", "mush2", "mush3", "mush4", "fg_cake", "fg_chocolate", "fg_candy",
               "fg_egg", "fg_bone", "fg_card", "fg_gd_card", "fg_grace_soldout", "fg_lamp", "fg_ufo_parts", "fg_axe",
               "fg_S_axe", "fg_G_axe", "fg_jyoro", "fg_S_jyoro", "fg_G_jyoro", "fg_net", "fg_S_net", "fg_G_net",
               "fg_pole", "fg_S_pole", "fg_G_pole", "fg_scoop", "fg_S_scoop", "fg_G_scoop", "fg_sling", "fg_S_sling",
               "fg_G_sling", "fg_easter_ticket", "fg_present_gr"]


# --- DATA HELPERS

def get_int8(data, off: int) -> int:
    return data[off]


def get_uint8(data, off: int) -> int:
    return data[off] & 0xFF


def get_int16(data, off: int) -> int:
    return struct.unpack_from(">h", data, off)[0]


def get_uint16(data, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def get_int32(data, off: int) -> int:
    return struct.unpack_from(">i", data, off)[0]


def get_uint32(data, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]


def get_bytes(data, off: int, len: int) -> bytearray:
    return bytearray(data[off:off + len])


def put_int8(data, off: int, val: int):
    data[off] = val


def put_uint8(data, off: int, val: int):
    data[off] = val & 0xFF


def put_int16(data, off: int, val: int):
    struct.pack_into(">h", data, off, val)


def put_uint16(data, off: int, val: int):
    struct.pack_into(">H", data, off, val)


def put_int32(data, off: int, val: int):
    struct.pack_into(">i", data, off, val)


def put_uint32(data, off: int, val: int):
    struct.pack_into(">I", data, off, val)


def put_bytes(data, off: int, val):
    for i in range(len(val)):
        data[off + i] = val[i]


def get_item_name(data, off: int) -> str:
    return get_bytes(data, off, STRING_LENGTH).decode("utf_16_be").strip('\0')


def put_item_name(data, off: int, name: str):
    for i in range(STRING_LENGTH):
        data[off + i] = 0

    rawstr = (name + '\0').encode('utf-16be')
    rawlen = len(rawstr)

    if rawlen > STRING_LENGTH:
        rawlen = STRING_LENGTH - 2

    for i in range(rawlen):
        data[off + i] = rawstr[i]


# --- ITEM CREATION, etc.


class BITM:
    def __init__(self):
        self.price = 0
        self.itemID = 0
        self.inventoryIcon = ITEM_ICONS[0]
        self.unkC = 0
        self.unkE = 0
        self.unk10 = 0x1701
        self.jpName = ""
        self.enName = ""
        self.spName = ""
        self.frName = ""
        self.enNameEur = ""
        self.geName = ""
        self.itName = ""
        self.spNameEur = ""
        self.frNameEur = ""
        self.krName = ""
        self.className = ITEM_CLASSES[3]
        self.unk167 = 0
        self.dropModel = DROP_MODELS[0]
        self.unk169 = bytearray(35)

    @staticmethod
    def load(file: str):
        raw = open(file, 'rb').read()

        if raw[:4].decode("ascii") != "BITM":
            return None

        item = BITM()
        item.price = get_int32(raw, 0x004)
        item.itemID = get_uint16(raw, 0x008)
        item.inventoryIcon = ITEM_ICONS[get_uint16(raw, 0x00A)]
        item.unkC = get_int16(raw, 0x00C)
        item.unkE = get_int16(raw, 0x00E)
        item.unk10 = get_int16(raw, 0x010)
        item.jpName = get_item_name(raw, 0x012)
        item.enName = get_item_name(raw, 0x034)
        item.spName = get_item_name(raw, 0x056)
        item.frName = get_item_name(raw, 0x078)
        item.enNameEur = get_item_name(raw, 0x09A)
        item.geName = get_item_name(raw, 0x0BC)
        item.itName = get_item_name(raw, 0x0DE)
        item.spNameEur = get_item_name(raw, 0x100)
        item.frNameEur = get_item_name(raw, 0x122)
        item.krName = get_item_name(raw, 0x144)
        item.className = ITEM_CLASSES[get_uint8(raw, 0x166)]
        item.unk167 = get_uint8(raw, 0x167)
        item.dropModel = DROP_MODELS[get_uint8(raw, 0x168)]
        item.unk169 = get_bytes(raw, 0x169, 0x23)

        return item

    def store(self) -> bytearray:
        raw = bytearray(BITM_SIZE)

        put_bytes(raw, 0x000, "BITM".encode('ascii'))
        put_int32(raw, 0x004, self.price)
        put_uint16(raw, 0x008, self.itemID)
        put_uint16(raw, 0x00A, ITEM_ICONS.index(self.inventoryIcon))
        put_int16(raw, 0x00C, self.unkC)
        put_int16(raw, 0x00E, self.unkE)
        put_int16(raw, 0x010, self.unk10)
        put_item_name(raw, 0x012, self.jpName)
        put_item_name(raw, 0x034, self.enName)
        put_item_name(raw, 0x056, self.spName)
        put_item_name(raw, 0x078, self.frName)
        put_item_name(raw, 0x09A, self.enNameEur)
        put_item_name(raw, 0x0BC, self.geName)
        put_item_name(raw, 0x0DE, self.itName)
        put_item_name(raw, 0x100, self.spNameEur)
        put_item_name(raw, 0x122, self.frNameEur)
        put_item_name(raw, 0x144, self.krName)
        put_uint8(raw, 0x166, ITEM_CLASSES.index(self.className))
        put_uint8(raw, 0x167, self.unk167)
        put_uint8(raw, 0x168, DROP_MODELS.index(self.dropModel))
        put_bytes(raw, 0x169, self.unk169)

        return raw

    def save(self, file: str):
        with open(file, 'wb') as f:
            f.write(self.store())
            f.flush()

    @staticmethod
    def load_json(jsonfile: str):
        item = BITM()
        data = json.load(open(jsonfile, encoding="utf-8"))
        names = data["Names"]

        item.itemID = data["ItemID"]
        item.className = data["ClassName"]
        item.inventoryIcon = data["InventoryIcon"]
        item.dropModel = data["DropModel"]
        item.price = data["Price"]
        item.unkC = data["UnkC"]
        item.unkE = data["UnkE"]
#        item.unk10 = data["Unk10"]
        item.jpName = names["JpJapanese"]
        item.enName = names["UsEnglish"]
        item.spName = names["UsSpanish"]
        item.frName = names["UsFrench"]
        item.enNameEur = names["EuEnglish"]
        item.spNameEur = names["EuSpanish"]
        item.frNameEur = names["EuFrench"]
        item.geName = names["EuGerman"]
        item.itName = names["EuItalian"]
        item.krName = names["KrKorean"]
        item.unk167 = data["Unk167"]

        for i in range(35):
            item.unk169[i] = data["Unk169"][i]

        return item

    def store_json(self) -> dict:
        dump = {}
        names = {}

        names["JpJapanese"] = self.jpName
        names["UsEnglish"] = self.enName
        names["UsSpanish"] = self.spName
        names["UsFrench"] = self.frName
        names["EuEnglish"] = self.enNameEur
        names["EuSpanish"] = self.spNameEur
        names["EuFrench"] = self.frNameEur
        names["EuGerman"] = self.geName
        names["EuItalian"] = self.itName
        names["KrKorean"] = self.krName

        dump["Names"] = names
        dump["ItemID"] = self.itemID
        dump["ClassName"] = self.className
        dump["InventoryIcon"] = self.inventoryIcon
        dump["DropModel"] = self.dropModel
        dump["Price"] = self.price
        dump["UnkC"] = self.unkC
        dump["UnkE"] = self.unkE
#        dump["Unk10"] = self.unk10
        dump["Unk167"] = self.unk167
        dump["Unk169"] = list(self.unk169)

        return dump

    def save_json(self, jsonfile: str):
        with open(jsonfile, 'w', encoding='utf8') as f:
            json.dump(self.store_json(), f, ensure_ascii=False, indent=4)


def create_item(srcdir: str, item: str):
    jsonpath = "src/{0}/{1}.json".format(srcdir, item)
    brespath = "src/{0}/{1}.brres".format(srcdir, item)
    ash0path = "src/{0}/{1}.brres.ash".format(srcdir, item)
    binpath = "build/{0}.bin".format(item)

    if not os.path.isfile(jsonpath):
        raise Exception("Error: Can't find JSON file")

    if not os.path.isfile(brespath):
        raise Exception("Error: Can't find BRRES file")

    bitmdata = BITM.load_json(jsonpath)

    if bitmdata.itemID >= 4096:
        raise Exception("Error: Item ID should not be greater than 4095")

    subprocess.call(["ashenc.exe", brespath])
    ash0data = open(ash0path, "rb").read()
    os.remove(ash0path)

    if len(ash0data) > ASH0_SIZE:
        raise Exception("Compressed BRRES data is too large. Couldn't create item.")

    outdata = bitmdata.store() + ash0data + bytearray(ASH0_SIZE - len(ash0data))
    outdata += struct.pack(">I", crc32(outdata, CRC_SEED))

    with open(binpath, 'wb') as f:
        f.write(outdata)
        f.flush()

    print("Successfully created item.")


# --- SAVE DATA MANAGING


def _load_save(savefile: str) -> bytearray:
    return bytearray(open(savefile, "rb").read())


def _store_save(savefile: str, savedata: bytearray):
    checksum = crc32(savedata[ITEMS_OFFSET:ITEMS_OFFSET + ITEM_SLOTS * TOTAL_SIZE], CRC_SEED)
    put_uint32(savedata, ITEMS_CRC_OFFSET, checksum)

    with open(savefile, 'wb') as f:
        f.write(savedata)
        f.flush()


def list_items(savefile: str):
    savedata = _load_save(savefile)

    for i in range(ITEM_SLOTS):
        offset = ITEMS_OFFSET + i * TOTAL_SIZE

        if savedata[offset:offset + 0x4].decode("ascii") == "BITM":
            print("{0}: {1} ({2})".format(i, get_item_name(savedata, offset + 0x34), get_uint16(savedata, offset + 0x8)))
        else:
            print("{0}: (empty)".format(i))


def _insert_item(savedata: bytearray, itemname: str, slot: int, original=False):
    item = open(("build/original/{0}.bin" if original else "build/{0}.bin").format(itemname), 'rb').read()

    if len(item) != TOTAL_SIZE:
        print("Item binary size is not 8KB.")

    if slot < ITEM_SLOTS:
        put_bytes(savedata, ITEMS_OFFSET + slot * TOTAL_SIZE, item)


def insert_item(savefile: str, item: str, slot: int, original=False):
    savedata = _load_save(savefile)
    _insert_item(savedata, item, slot, original)
    _store_save(savefile, savedata)

    print("Successfully inserted item.")


def insert_all_items(savefile: str, jsonfile: str):
    savedata = _load_save(savefile)
    jsondata = json.load(open(jsonfile, encoding="utf-8"))

    if len(jsondata) == 0:
        raise Exception("Found no items to insert.")

    for info in jsondata:
        _insert_item(savedata, info["Item"], info["Slot"], info["UsePrecreated"])

    _store_save(savefile, savedata)

    print("Successfully inserted all items.")


def remove_item(savefile: str, slot: int):
    savedata = _load_save(savefile)
    if slot < ITEM_SLOTS:
        for i in range(TOTAL_SIZE):
            savedata[ITEMS_OFFSET + slot * TOTAL_SIZE + i] = 0
    _store_save(savefile, savedata)

    print("Successfully removed item.")


def remove_all_items(savefile: str):
    savedata = _load_save(savefile)

    for i in range(ITEM_SLOTS * TOTAL_SIZE):
        savedata[ITEMS_OFFSET + i] = 0

    _store_save(savefile, savedata)

    print("Successfully removed all items.")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        operation = sys.argv[1]

        if operation == "-h":
            print("-- ACDLC.py COMMANDS --")
            print("-h   Help         : -h")
            print("-c   Create item  : -c folder_name item_name")
            print("-l   List items   : -l save_file")
            print("-i   Insert item  : -i save_file item_name slot use_precreated")
#            print("-e   Extract item : -e save_file slot")
            print("-r   Remove item  : -r save_file slot")
            print("-ia  Insert all   : -ia save_file json_file")
#            print("-ea  Extract all  : -ea save_file")
            print("-ra  Remove all   : -ra save_file")
        elif operation == "-c":
            create_item(sys.argv[2], sys.argv[3])
        elif operation == "-l":
            list_items(sys.argv[2])
        elif operation == "-i":
            insert_item(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] == 'y')
        elif operation == "-e":
            pass
        elif operation == "-r":
            remove_item(sys.argv[2], int(sys.argv[3]))
        elif operation == "-ia":
            insert_all_items(sys.argv[2], sys.argv[3])
        elif operation == "-ea":
            pass
        elif operation == "-ra":
            remove_all_items(sys.argv[2])
