# Coverage Roadmap: From 75% to 80%

**Current Status:** 75% overall coverage  
**Target:** 80% overall coverage  
**Gap:** 5% additional coverage needed

## Current Coverage Breakdown

| File | Current Coverage | Target | Gap |
|------|------------------|--------|-----|
| **src/constants.py** | 100% | 80% | ✅ Exceeded |
| **src/game_logic.py** | 95% | 80% | ✅ Exceeded |
| **src/sudoku_game.py** | ~65% | 80% | ❌ -15% |
| **src/ui_renderer.py** | ~35% | 60% | ❌ -25% |

## What's Needed to Reach 80%

### Priority 1: src/sudoku_game.py (65% → 80%)

**Gap Analysis:**
The main game class has good coverage of core functionality but lacks tests for:

1. **UI Interaction Methods** (15-20 tests needed):
   - `handle_click()` - Mouse click handling for different UI elements
   - `handle_key()` - Keyboard event routing
   - `move_selection()` - Arrow key navigation edge cases
   - Button click handling in different game states

2. **Animation State Management** (8-10 tests needed):
   - `update_animation()` - Animation frame progression
   - `start_animation()` - Animation initialization with various inputs
   - Animation cleanup and edge cases
   - Concurrent animation scenarios

3. **Scoring System Edge Cases** (10-12 tests needed):
   - `reset_combo()` - Combo reset scenarios
   - `check_completion_bonuses()` - Row/column/box/number completion
   - Points overflow scenarios
   - Score calculation with max combo multiplier
   - Negative score scenarios

4. **Visual Effects Management** (8-10 tests needed):
   - `add_floating_point()` - Floating point text creation
   - `add_cell_flash()` - Cell flash effect creation
   - Effect cleanup and expiration
   - Maximum concurrent effects

**Estimated Tests Required:** 40-50 additional tests

**Implementation Strategy:**
```python
# Example test structure needed:

class TestUIInteraction:
    def test_handle_click_on_cell(self):
        """Test clicking on different cells"""
        
    def test_handle_click_on_button(self):
        """Test clicking on UI buttons"""
        
    def test_handle_key_arrow_navigation(self):
        """Test arrow key navigation"""
        
    def test_handle_key_digit_input(self):
        """Test digit input in different states"""

class TestAnimationSystem:
    def test_animation_progression(self):
        """Test animation frame updates"""
        
    def test_animation_completion(self):
        """Test animation ending"""
        
    def test_multiple_animations(self):
        """Test overlapping animations"""

class TestScoringAdvanced:
    def test_completion_bonuses_all_types(self):
        """Test row/col/box/number bonuses"""
        
    def test_score_with_max_combo(self):
        """Test scoring at 3.0x multiplier"""
        
    def test_combo_reset_scenarios(self):
        """Test all combo reset conditions"""

class TestVisualEffects:
    def test_floating_points_creation(self):
        """Test adding floating point effects"""
        
    def test_cell_flash_effects(self):
        """Test cell flash creation and cleanup"""
        
    def test_effect_expiration(self):
        """Test automatic effect removal"""
```

### Priority 2: src/ui_renderer.py (35% → 50-60%)

**Gap Analysis:**
UI rendering is challenging to test due to Pygame dependencies, but we can test:

1. **Testable Pure Logic** (10-15 tests needed):
   - Color calculation functions
   - Position calculation functions
   - Text formatting functions
   - Layout calculations

2. **Mock-based Rendering Tests** (15-20 tests needed):
   - Drawing function call sequences
   - Parameter validation
   - Conditional rendering logic
   - Error handling in render functions

**Limitation:** Full UI testing requires complex Pygame mocking. Targeting 50-60% is realistic without browser-style integration tests.

**Estimated Tests Required:** 25-35 additional tests

**Implementation Strategy:**
```python
# Example test structure:

class TestRenderingLogic:
    def test_combo_color_selection(self):
        """Test color selection based on combo level"""
        
    def test_button_position_calculation(self):
        """Test button positioning logic"""
        
    def test_text_truncation(self):
        """Test long text handling"""

class TestRenderingWithMocks:
    def test_draw_board_calls(self, mock_pygame):
        """Test draw_board makes correct Pygame calls"""
        
    def test_draw_floating_points(self, mock_pygame):
        """Test floating point rendering"""
        
    def test_hover_effect_rendering(self, mock_pygame):
        """Test hover state changes rendering"""
```

## Recommended Approach

### Phase 1: Quick Wins (Get to 78%)
**Time: 2-3 hours**

Focus on sudoku_game.py easy additions:
1. Add 15-20 tests for scoring edge cases
2. Add 10-12 tests for basic UI interaction
3. Add 8-10 tests for animation state

Expected coverage gain: +3%

### Phase 2: Deep Testing (Reach 80%)
**Time: 3-4 hours**

1. Complete sudoku_game.py coverage:
   - All UI interaction methods
   - All animation scenarios
   - All scoring combinations
   - All visual effect scenarios

2. Add selective ui_renderer.py tests:
   - Pure logic functions
   - Simple mock-based tests

Expected coverage gain: +2%

### Phase 3: Polish (Exceed 80%)
**Time: 2-3 hours**

1. Add property-based tests for game_logic.py
2. Add integration-style tests
3. Add performance regression tests
4. Document all edge cases

Expected coverage gain: +2-3%

## Tools and Techniques

### 1. Identify Uncovered Lines
```bash
# Run with missing lines report
pytest --cov=src --cov-report=term-missing

# Generate HTML report for detailed view
pytest --cov=src --cov-report=html
open tests/TestResults/htmlcov/index.html
```

### 2. Mock Pygame Components
```python
from unittest.mock import Mock, patch, MagicMock

@pytest.fixture
def mock_pygame(monkeypatch):
    """Mock Pygame for UI testing"""
    mock_surface = Mock()
    mock_font = Mock()
    # ... setup mocks
    return mock_surface, mock_font
```

### 3. Use Parametrize for Multiple Scenarios
```python
@pytest.mark.parametrize("combo_count,expected_multiplier", [
    (0, 1.0),
    (1, 1.5),
    (2, 2.0),
    (3, 2.5),
    (4, 3.0),
    (5, 3.0),  # Max
])
def test_combo_multiplier(combo_count, expected_multiplier):
    """Test combo multiplier at different levels"""
    # ...
```

## Challenges and Constraints

### Technical Challenges:
1. **Pygame Dependency**: UI rendering requires extensive mocking
2. **State Complexity**: Game has many interacting state variables
3. **Visual Effects**: Animations are time-based and hard to test
4. **User Interaction**: Click/key events require event simulation

### Trade-offs:
- **80% coverage is achievable** but requires significant test infrastructure
- **85%+ coverage would require**: Integration tests, visual regression tests, or headless Pygame
- **Diminishing returns**: Last 5% takes 50% more effort than first 75%

## Success Criteria

To reach and maintain 80% coverage:

✅ **Coverage Metrics:**
- Overall: ≥ 80%
- constants.py: ≥ 95% (already achieved)
- game_logic.py: ≥ 90% (already achieved)
- sudoku_game.py: ≥ 80%
- ui_renderer.py: ≥ 50%

✅ **Test Quality:**
- All critical paths covered
- Edge cases tested
- Negative scenarios included
- Fast execution (< 30 seconds for full suite)

✅ **Maintainability:**
- Clear test names
- Good documentation
- Minimal mocking complexity
- Easy to run and debug

## Next Steps

1. **Review current coverage report**:
   ```bash
   pytest --cov=src --cov-report=html
   open tests/TestResults/htmlcov/index.html
   ```

2. **Prioritize uncovered lines**: Focus on critical business logic first

3. **Add tests incrementally**: Commit after each test class addition

4. **Monitor progress**: Run coverage after each session

5. **Document assumptions**: Note any intentionally untested code

## Estimated Timeline

- **Quick wins (78%)**: 2-3 hours
- **Reach 80%**: Additional 3-4 hours
- **Polish (82%+)**: Additional 2-3 hours

**Total effort: 7-10 hours** of focused test development

---

**Note**: The 75% → 80% journey requires primarily testing sudoku_game.py's UI interaction and animation systems. These are well-defined areas that can be systematically covered with mock-based testing.
