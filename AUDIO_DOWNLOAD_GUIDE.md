# Audio Asset Download Guide for Sudoku Flash

This guide provides step-by-step instructions for downloading and installing all audio files needed for Sudoku Flash.

---

## Quick Start

All audio files should be placed in the following directories:
- **Music files**: `assets/music/`
- **Sound effect files**: `assets/sounds/`

The directories have already been created by the game setup.

---

## Required Audio Files

### 1. Background Music

**File**: `background.ogg`
**Location**: `assets/music/background.ogg`

**Download Steps**:
1. Visit: https://opengameart.org/content/puzzle-game-3
2. Click "Download" button
3. Download the file (usually named something like "puzzle-game-3.ogg")
4. Rename to `background.ogg`
5. Place in `assets/music/` directory

**License**: CC0 (Public Domain)
**Author**: Memoraphile

---

### 2. Sound Effects

#### correct.wav
**Location**: `assets/sounds/correct.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/Bertrof/sounds/351566/
2. Click "Download" button (you may need a free Freesound account)
3. Save as `correct.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: Bertrof

---

#### wrong.wav
**Location**: `assets/sounds/wrong.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/Bertrof/sounds/131657/
2. Click "Download" button
3. Save as `wrong.wav`
4. Place in `assets/sounds/` directory

**License**: CC BY 3.0
**Author**: Bertrof
**Attribution**: Required (automatically included in CREDITS.md)

---

#### hint.wav
**Location**: `assets/sounds/hint.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/dland/sounds/320181/
2. Click "Download" button
3. Save as `hint.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: dland

---

#### undo.wav
**Location**: `assets/sounds/undo.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/hotpin7/sounds/843083/
2. Click "Download" button
3. Save as `undo.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: hotpin7

---

#### button.wav
**Location**: `assets/sounds/button.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/Leszek_Szary/sounds/146718/
2. Click "Download" button
3. Save as `button.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: Leszek_Szary

---

#### win.wav
**Location**: `assets/sounds/win.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/plasterbrain/sounds/397355/
2. Click "Download" button
3. Save as `win.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: plasterbrain

---

#### combo.wav
**Location**: `assets/sounds/combo.wav`

**Download Steps**:
1. Visit: https://freesound.org/people/plasterbrain/sounds/397355/
2. Click "Download" button
3. Save as `combo.wav`
4. Place in `assets/sounds/` directory

**License**: CC0 (Public Domain)
**Author**: plasterbrain

---

## Freesound.org Account Setup

Many sound effects require a free Freesound.org account:

1. Go to https://freesound.org
2. Click "Sign Up" in the top right
3. Create a free account (email verification required)
4. Log in to download sounds

**Note**: All downloads are free; no payment required.

---

## File Format Notes

- **Music files**: Should be in OGG format (`.ogg`)
- **Sound effects**: Should be in WAV format (`.wav`)

If downloaded files have different formats:
- You can use free tools like **Audacity** or **FFmpeg** to convert between formats
- Most downloads from these sources will already be in the correct format

---

## Verification Checklist

After downloading all files, verify your directory structure looks like this:

```
assets/
├── music/
│   └── background.ogg
└── sounds/
    ├── button.wav
    ├── combo.wav
    ├── correct.wav
    ├── hint.wav
    ├── undo.wav
    ├── win.wav
    └── wrong.wav
```

**Total Files**: 8 files (1 music + 7 sound effects)

---

## Testing Audio

After downloading all files:

1. Run the game: `python sudoku_flash.py`
2. You should hear background music on the main menu
3. Start a game and test:
   - Click buttons (button sound)
   - Place a correct number (correct sound)
   - Place a wrong number (wrong sound)
   - Use a hint (hint sound)
   - Undo a move (undo sound)
   - Trigger combos by auto-filling cells (combo sound)
   - Complete a puzzle (win sound)

---

## Troubleshooting

### "Sound file not found" warnings

**Problem**: Game shows warnings about missing audio files

**Solution**:
1. Check file names match exactly (case-sensitive)
2. Verify files are in correct directories
3. Ensure file extensions are correct (.wav or .ogg)

### No sound playing

**Problem**: Game runs but no audio plays

**Solution**:
1. Check volume controls in Settings modal
2. Verify "Sound: ON" in settings
3. Check system volume is not muted
4. Ensure pygame mixer initialized (check console for errors)

### Music not looping

**Problem**: Music stops after playing once

**Solution**:
- Background music should loop automatically
- Check `audio_settings.json` for music_volume setting
- If issue persists, verify the OGG file isn't corrupted

### Wrong sound format

**Problem**: Downloaded file won't play

**Solution**:
1. Convert to correct format using Audacity:
   - Open the file in Audacity
   - File > Export > Export as WAV (for sound effects)
   - File > Export > Export as OGG (for music)
2. Save with the correct filename

---

## Alternative Audio Sources

If any of the recommended sounds are unavailable, here are alternative sources:

- **OpenGameArt.org**: https://opengameart.org/
- **Freesound.org**: https://freesound.org/
- **ZapSplat**: https://www.zapsplat.com/ (free with attribution)
- **Incompetech**: https://incompetech.com/ (music, CC BY)

**Remember**: Always check the license and provide attribution where required!

---

## License Compliance

The CREDITS.md file in the project root contains all required attributions for CC BY 3.0 assets. This file is automatically displayed in the game's Credits menu, ensuring proper attribution is always maintained.

**Required Attribution** (already handled in CREDITS.md):
- Bertrof - Error Sound (CC BY 3.0)
- NenadSimic - Button Click (CC BY 3.0)

---

## Need Help?

If you encounter issues:
1. Verify all filenames match exactly (case-sensitive)
2. Check file formats (.wav for SFX, .ogg for music)
3. Ensure files aren't corrupted (try playing in VLC or similar)
4. Check console output for specific error messages

---

**Last Updated**: March 16, 2026
**Author**: Red Donaldson
