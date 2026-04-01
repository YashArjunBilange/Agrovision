# Agrovision Render Deployment TODO

## Previous Steps (Done):
- [x] Procfile created
- [x] runtime.txt / .python-version updated
- [x] requirements.txt fixed for CPU torch + loose versions

## Current Fix (Python 3.10.11):
- [ ] Update .python-version to 3.10.11 (user-tested, full wheels on Render)
- [ ] Pin streamlit==1.29.0 (exact match)

## Deploy:
- Push changes, manual deploy on Render.

**Notes:** 3.10.11 resolves Streamlit wheel issues; torch CPU works.
