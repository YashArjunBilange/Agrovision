# Agrovision Render FINAL FIX

**Issue:** --index-url overrode PyPI (no streamlit in torch CPU index).

**Fix:** --extra-index-url for torch CPU + default PyPI for streamlit/etc.

requirements.txt:
```
--extra-index-url https://download.pytorch.org/whl/cpu
torch
torchvision
streamlit==1.38.0
Pillow
ultralytics
opencv-python-headless
```
(1.38.0 latest stable 3.10 compat; unpinned others).

.python-version: 3.10.11

Push & deploy—build succeeds!
