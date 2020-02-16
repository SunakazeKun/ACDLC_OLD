
# ACDLC: Animal Crossing City Folk DLC tool
![Ingame screenshot](screenshots/scr0.png)
**ACDLC** allows the creation, insertion and management of DLC items in *Animal Crossing City Folk* (also known as *Let's Go to the City* in PAL regions). To use this tool, you simply need to extract the game's savedata file *rvforest.dat*. As ACDLC uses Python scripts you need to have Python 3 installed on your computer system.

# Features
The primary purpose of this tool is to create custom DLC items that can be added in *City Folk*. These items, often referred to as Hacked Downloadable Content (HDLC), were significantly prominent among early online players. Still, there was no proper guide explaining how to create new items and the possibilities were limited. Using this tool, however, we can finally create and set-up our own items and insert them into the game.
Of course, the tool can be used to insert official DLC into the game as well, most of which is not obtainable since the shutdown of Nintendo's online services for the DS and Wii systems. Even [unreleased DLC items](https://www.youtube.com/watch?v=ZCOThZxtvRs) can be added!

# Usage
***Make sure to always create backups of your savedata!!***

This is a command line tool but it is very simple to use, we promise! Again, you need the game's savedata file.
First of all, we need to open the Command Prompt and navigate to the ACDLC folder. The easiest way is to hold Shift, right click in the folder and select *Open Command Prompt here*. Then you are ready to go!
After inserting any DLC item, use [ACToolkit](https://actoolkit.com/) to add the item to your inventory.

## Insert all official DLC
```
python acdlc.py -ia save_file l_official_dlc.json
Example: python acdlc.py -ia D:/saves/rvforest.dat l_official_dlc.json
```
Most people are interested in importing all DLC into the game. If that's the case, use this command. Obviously, *save_file* should be replaced with the path to the savedata file. The *-ia* command is explained in more detail below.

## List items
```
python acdlc.py -l save_file
Example: python acdlc.py -l D:/saves/rvforest.dat
```
This lists what item each DLC slot contains. It is helpful to track any free or occupied slots.

## Create item
```
python acdlc.py -c folder_name item_name
Example: python acdlc.py -c dlc red_Pikmin
```
Creates the binary data for a DLC item. The example will create the item located at *src/dlc/red_Pikmin.** The *bin* file will be saved into the *final* directory.

## Insert item
```
python acdlc.py -i save_file item_name slot use_precreated
Example: python acdlc.py -i D:/saves/rvforest.dat red_Pikmin 48 y
```
Adds a single item at the specified slot into your savefile. To retrieve the slot ID of a specific item, you may want to use the *-l* command first. The item binaries are found inside the *final* folder. However, if you replace *use_precreated* with "*y*", the item is loaded from *final_original* instead.

## Remove item
```
python acdlc.py -r save_file slot
Example: python acdlc.py -r D:/saves/rvforest.dat 127
```
Clears the specified slot in your savedata.

## Insert all items
```
python acdlc.py -ia save_file json_file
Example: python acdlc.py -ia D:/saves/rvforest.dat l_official_dlc.json
```
Inserts all DLC items specified in the JSON-file. The format for these lists is kept simple and is pretty self-explanatory. Here's an example.
```
[
    {
        "Item": "sporty_wall",
        "Slot": 0,
        "UsePrecreated": true
    },
    {
        "Item": "golden_wallpaper",
        "Slot": 2,
        "UsePrecreated": true
    },
    {
        "Item": "creepy_wallpaper",
        "Slot": 3,
        "UsePrecreated": true
    }
]
```

## Remove all items
```
python acdlc.py -ra save_file
Example: python acdlc.py -ra D:/saves/rvforest.dat
```
Removes every DLC item and clears all slots in your savedata.

# Credits
Huge thanks to *Larsenv* for figuring out the checksum seed! The ASH compressor was created by *conanac*.
