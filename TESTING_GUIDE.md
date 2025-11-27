# 🎬 Cinematic Enhancements - Quick Testing Guide

## Before You Start

Make sure you have:

- ✅ Latest code with enhanced prompts
- ✅ Gemini API key configured
- ✅ Manim and dependencies installed
- ✅ FFmpeg in PATH

---

## 🧪 Test Scenarios

### Test 1: Simple Circle (Baseline)

**Prompt:** `"Draw a circle"`

**Expected Cinematic Features:**

- ✅ Gradient background (#0A0A1A to #1A1A3A)
- ✅ 30-40 ambient particles with low opacity
- ✅ Slow camera zoom (scale 0.95 over 3-4 seconds)
- ✅ Circle with GrowFromCenter animation
- ✅ Flash/glow effect after appearance
- ✅ Title text with Write animation
- ✅ rate_func=smooth on all animations
- ✅ Strategic self.wait() pauses
- ✅ Total duration: 8-12 seconds

**How to Test:**

```bash
# Streamlit
streamlit run app.py
# Enter: "Draw a circle"

# Flask
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Draw a circle"}'
```

**Success Criteria:**

- Video has dark gradient background (not black)
- Animation is smooth, not instant
- Camera subtly zooms in
- Circle has glow effect
- Pacing feels professional

---

### Test 2: Math Visualization

**Prompt:** `"Visualize the Pythagorean theorem"`

**Expected Features:**

- ✅ Blue-purple color palette
- ✅ Multiple objects with z-index layering
- ✅ Text appears with Write animation
- ✅ Shapes use GrowFromCenter
- ✅ Waits between each element
- ✅ Professional pacing
- ✅ No LaTeX errors (uses Text class)

**How to Test:**

```bash
# Streamlit only (uses JSON schema)
streamlit run app.py
```

**Success Criteria:**

- All text uses Text class (no MathTex)
- Colors harmonize (blue-purple spectrum)
- Elements appear sequentially with pauses
- Background sets cinematic mood
- No rendering errors

---

### Test 3: Transformation Animation

**Prompt:** `"Show a square transforming into a circle"`

**Expected Features:**

- ✅ Both shapes with cinematic styling
- ✅ Smooth transform with rate_func=smooth
- ✅ Appropriate run_time (>= 1.2 seconds)
- ✅ Pauses before and after transform
- ✅ Potential emphasis flash

**Success Criteria:**

- Transform is smooth, not jarring
- Colors consistent between shapes
- Timing feels natural
- Background enhances focus

---

### Test 4: Complex Educational Content

**Prompt:** `"Explain how binary search works"`

**Expected Features (Streamlit):**

- ✅ JSON includes style block with theme/camera/motion/palette
- ✅ Multiple scenes with consistent styling
- ✅ Code generation respects style configuration
- ✅ Camera movement matches style.camera choice
- ✅ Pacing matches style.motion choice

**Expected Streamlit JSON:**

```json
{
  "title": "Binary Search",
  "style": {
    "theme": "dark-neon",
    "camera": "slow-zoom",
    "motion": "smooth",
    "palette": "blue-purple"
  },
  "scenes": [...]
}
```

**Success Criteria:**

- Phase 1 generates complete style block
- Phase 2 code uses style configuration
- Phase 3 renders without errors
- Final video has consistent aesthetic throughout

---

## 🎨 Testing Different Styles (Streamlit)

### Test with Different Prompts to Trigger Styles

1. **Dark Neon (Default)**

   - Prompt: `"Show a circle"` (will default to dark-neon, slow-zoom, smooth, blue-purple)

2. **Energetic Motion**

   - Prompt: `"Create a fast-paced animation of bouncing balls"`
   - Expected: motion="energetic" in JSON

3. **Calm Mathematical**

   - Prompt: `"Gently explain calculus derivatives"`
   - Expected: motion="calm" in JSON

4. **Professional Corporate**
   - Prompt: `"Present quarterly sales data"`
   - Expected: motion="professional", possibly light-minimal theme

---

## 📊 Quality Checklist

For each test, verify:

### Visual Quality

- [ ] Background is gradient or themed (not plain black/white)
- [ ] Colors harmonize (within same palette family)
- [ ] Particles visible for depth (except light-minimal)
- [ ] No clashing colors

### Animation Quality

- [ ] All animations use rate_func (smooth/ease/rush)
- [ ] run_time >= 1.2 for main animations
- [ ] No instant jumps or .add() for main objects
- [ ] Transforms are smooth

### Pacing Quality

- [ ] self.wait(0.5) at start
- [ ] self.wait(0.2) between objects
- [ ] self.wait(1.0) after transitions
- [ ] self.wait(1.5-2) at end
- [ ] Total duration 8-15 seconds

### Technical Quality

- [ ] No LaTeX errors
- [ ] Class name is GenScene (Flask) or GeneratedScene (Streamlit)
- [ ] No syntax errors
- [ ] Video renders successfully
- [ ] Output file exists and plays

---

## 🐛 Common Issues to Watch For

### Issue 1: Plain Background

**Symptom:** Background is solid black/white
**Cause:** LLM didn't apply background rules
**Fix:** Check system prompt includes background section

### Issue 2: No rate_func

**Symptom:** Animations feel instant/jarring
**Cause:** rate_func not applied
**Fix:** Verify smoothness rules in prompt

### Issue 3: Too Fast

**Symptom:** Video under 5 seconds
**Cause:** Missing waits or low run_time
**Fix:** Check pacing rules enforcement

### Issue 4: No Camera Movement

**Symptom:** Static view throughout
**Cause:** Camera rules not applied
**Fix:** Verify camera movement section in prompt

### Issue 5: Clashing Colors

**Symptom:** Random red, green, blue together
**Cause:** Palette not respected
**Fix:** Check color palette rules in prompt

---

## 📈 Performance Benchmarks

Expected generation times:

| Step                     | Time (Streamlit)  | Time (Flask)      |
| ------------------------ | ----------------- | ----------------- |
| Phase 1: Interpretation  | 2-4 seconds       | N/A               |
| Phase 2: Code Generation | 3-6 seconds       | 4-8 seconds       |
| Phase 3: Rendering       | 8-15 seconds      | 8-15 seconds      |
| **Total**                | **13-25 seconds** | **12-23 seconds** |

Rendering quality settings:

- `-ql` (480p): ~5-8 seconds
- `-qm` (720p): ~8-12 seconds
- `-qh` (1080p): ~15-25 seconds

---

## ✅ Success Indicators

Your enhancements are working if:

1. **Every video has:**

   - Gradient/themed background ✅
   - Smooth animations ✅
   - Strategic pauses ✅
   - Camera movement (unless style=static) ✅
   - Harmonized colors ✅

2. **Error rate decreases:**

   - Before: ~40% failures
   - After: <10% failures

3. **User feedback:**
   - "Wow, this looks professional!"
   - "Better than expected"
   - "Smooth and polished"

---

## 🚀 Next Steps After Testing

If all tests pass:

1. ✅ Enhancements are working correctly
2. Consider adding user-facing style selectors
3. Create animation template library
4. Add more themes/palettes to cinematic_config.py
5. Implement video preview before final render

If tests fail:

1. Check which step is failing (1-6)
2. Review relevant system prompt
3. Verify LLM is respecting instructions
4. Check API response completeness
5. Review error logs for patterns

---

**Happy Testing! 🎬**
