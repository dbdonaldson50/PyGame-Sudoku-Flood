# Quick Test Guide - Enhanced Scoring System

## Testing the Combo System (5 minutes)

### Setup
1. Launch the game: `python3 sudoku_game.py`
2. Select **Easy** mode (9×9 grid - easiest to observe effects)
3. Start a new game

### Test 1: Basic Combo (2 min)
**Goal:** See the combo system in action

1. **Find a strategic cell** - Look for a cell where placing a number will trigger auto-fill
2. **Place the correct digit** (use arrow keys to navigate, type number)
3. **Watch for:**
   - ✨ Green "+5 points" floating up from your cell
   - 💚 Green flash on the cell
   - 🔵 Blue flashes on auto-filled cells
   - 🌟 Gold "+X points" floating from auto-filled cells
   - 📊 Top-right corner shows "1.5x COMBO" or higher
   - 💫 Combo indicator pulses with glow effect

**Expected Score Increase:**
- Without combo: ~10-15 points
- With combo: ~15-25 points (50-100% more!)

### Test 2: Combo Reset (1 min)
**Goal:** See combo reset conditions

1. **Build a combo** (as in Test 1)
2. **Try each reset method:**
   - Place a **wrong digit** → Combo disappears, lose life
   - Use **Hint** (click Hint button) → Combo resets, -10 points
   - Place digit with **no auto-fill** → Combo resets

**Expected Behavior:**
- Combo indicator disappears immediately
- Next auto-fill starts at 1.0x again

### Test 3: Maximum Combo (2 min)
**Goal:** Reach 3.0x multiplier

1. **Find a cell that triggers multiple auto-fills** (usually near the end of game)
2. **Watch the combo build up:**
   - 1st auto-fill: Green (1.0x)
   - 2nd auto-fill: Gold (1.5x)
   - 3rd auto-fill: Orange (2.0x)
   - 4th auto-fill: Red-Orange (2.5x)
   - 5th auto-fill: **Magenta (3.0x MAX!)**

**Expected Visual:**
- Combo indicator shows "3.0x COMBO" in magenta
- Pulsing/glowing effect intensifies
- Point gains are 3x normal

### Test 4: Completion Bonuses (1 min)
**Goal:** Earn bonus points

1. **Complete a row/column/box**
2. **Watch for:**
   - 🎯 Gold "+50" or "+75" floating at top center
   - Bonus added to score immediately
3. **Complete all instances of one number** (e.g., all 9's)
4. **Should see:** Gold "+100" bonus

---

## Visual Effects Checklist

- [ ] **Floating Points:** Text floats upward and fades out
- [ ] **Cell Flash:** Cells briefly light up when filled
- [ ] **Combo Indicator:** Pulses at top-right when active
- [ ] **Color Coding:** Different colors for combo levels
- [ ] **Smooth Animation:** All effects at 60 FPS, no lag

---

## Performance Check

While playing, verify:
- [ ] Game runs smoothly (no stuttering)
- [ ] All animations are fluid
- [ ] No frame drops during combos
- [ ] Multiple effects don't cause slowdown

---

## Configuration Testing (Optional)

Edit `constants.py` to customize:

**Make combos more rewarding:**
```python
COMBO_MULTIPLIERS = [1.0, 2.0, 3.0, 4.0, 5.0]  # Even higher multipliers!
```

**Faster visual feedback:**
```python
FLOATING_TEXT_DURATION = 30  # Faster fade (was 45)
FLASH_DURATION = 15          # Quicker flash (was 20)
```

**Different colors:**
```python
COMBO_COLORS = [
    (0, 255, 0),      # Bright green
    (255, 255, 0),    # Yellow
    (255, 128, 0),    # Orange
    (255, 0, 0),      # Red
    (255, 0, 255)     # Purple
]
```

---

## Troubleshooting

**Q: I don't see combo indicator**
A: You need to trigger auto-fill first. Combo only appears when auto-fill occurs.

**Q: Floating points not showing**
A: They might be too fast. Try increasing `FLOATING_TEXT_DURATION` in constants.py

**Q: Performance issues**
A: Unlikely, but try reducing max combo level or effect duration

**Q: Colors hard to see**
A: Customize `COMBO_COLORS` and `FLASH_COLORS` in constants.py

---

## Quick Score Formula Reference

**Manual Placement:**
- Easy: 5 points
- Medium: 10 points
- Hard: 15 points

**Auto-Fill with Combo:**
- Formula: `(base_points / 2) × combo_multiplier`
- 1.0x: 2.5, 5, or 7.5 points
- 1.5x: 3.75, 7.5, or 11.25 points
- 2.0x: 5, 10, or 15 points
- 2.5x: 6.25, 12.5, or 18.75 points
- 3.0x: 7.5, 15, or 22.5 points

**Bonuses:**
- Row complete: +50
- Column complete: +50
- Box complete: +75
- Number complete (all instances): +100

---

## Success Indicators

You'll know it's working when:
- ✅ Score increases faster with combos
- ✅ Visual effects appear smoothly
- ✅ Combo indicator pulses and changes color
- ✅ Game feels more rewarding and engaging
- ✅ Strategic play is incentivized

**Enjoy the enhanced gameplay! 🎮✨**
