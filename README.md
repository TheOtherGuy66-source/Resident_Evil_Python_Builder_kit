## To Build

1. You need Python installed.
2. You need to create a folder for RE1, RE2, and RE3.

### Game Versions/ Folder names.

- **RE1** = BIOHAZARD Mediakite
- **RE2** = Biohazard-2-apan-source-next
- **RE3** = Bio Hazard 3 (SOURCENEXT)

### RE1 Modes

RE1 has NVIDIA and AMD modes.

### Mod Names for the Zips

- **RE1**:
  - `Biohazard_mod.zip`
  - `dgVoodoo_AMD_fix.zip`
- **RE2**:
  - `Bio2_mod.zip`
- **RE3**:
  - `Bio3_mod.zip`

### Build Instructions

To build, you need the Team X mods, then overwrite those with the Seamless HD mods. Next, get the Classic Rebirth DLL, update the EXE pack, and include it in the mod zip for each version of the game.

### AMD Fix for RE1

For the AMD fix on RE1, you'll need to find:

- `D3DImm.dll`
- `dgVoodoo.conf`
- `re_ddraw.dll`

These must be the Japanese version of Biohazard for Classic Rebirth to work.

### Additional Notes

The mod linker drive links aren't working anymore. I haven't reuploaded them due to issues with the people in charge of these projects, but you could easily fork it yourself and create the linkage for it.

It's pretty much extremely easy. You have your game folder and then your mod zip. The game folder must be on your desktop, and the zips can be on your desktop or downloads folder. The script can detect if you're syncing to OneDrive. It will see the folder and zip for auto-detection and then do all of the stuff for you.

Once you have built the mod zip, it will be really helpful for those that have trouble with technical stuff like this.
