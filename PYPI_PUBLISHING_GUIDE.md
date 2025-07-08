# 🚀 PyTAKES PyPI Publishing Guide

## Prerequisites

✅ **Already Completed:**
- Project structure is ready
- `pyproject.toml` is configured
- Apache 2.0 License is in place
- README.md exists
- Source code is in `src/pytakes/`

## Step 1: Create PyPI Account

1. **Create accounts on both:**
   - **TestPyPI (for testing)**: https://test.pypi.org/account/register/
   - **PyPI (production)**: https://pypi.org/account/register/

2. **Enable 2FA** on both accounts (required for publishing)

3. **Create API tokens:**
   - Go to Account Settings → API tokens
   - Create a token for each platform
   - Save these tokens securely!

## Step 2: Configure Authentication

Create a `~/.pypirc` file with your credentials:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

## Step 3: Build the Package

Run these commands in your project directory:

```bash
# Clean any previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m build
```

This creates:
- `dist/pytakes-1.0.0.tar.gz` (source distribution)
- `dist/pytakes-1.0.0-py3-none-any.whl` (wheel distribution)

## Step 4: Test Upload to TestPyPI

```bash
# Upload to TestPyPI first
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m twine upload --repository testpypi dist/*
```

## Step 5: Test Installation from TestPyPI

```bash
# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pytakes
```

## Step 6: Upload to Production PyPI

Once testing is successful:

```bash
# Upload to production PyPI
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m twine upload dist/*
```

## Step 7: Verify Publication

After successful upload:

```bash
# Install from PyPI
pip install pytakes

# Test the installation
python -c "import pytakes; print(pytakes.__version__)"
```

## Step 8: Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `PyTAKES v1.0.0 - Initial Release`
5. Description: Copy from your README or ANNOUNCEMENT.md
6. Attach the built distributions (`dist/` files)

## Security Notes

- **Never commit** your PyPI tokens to git
- **Use API tokens** instead of passwords
- **Enable 2FA** on your PyPI accounts
- **Store tokens securely** (password manager recommended)

## Common Issues & Solutions

### Issue: "Package already exists"
- **Solution**: Increment version number in `pyproject.toml` and rebuild

### Issue: "Authentication failed"
- **Solution**: Check your API token and `~/.pypirc` configuration

### Issue: "Distribution already exists"
- **Solution**: You cannot overwrite existing versions. Increment version.

### Issue: "Invalid classifier"
- **Solution**: Check https://pypi.org/classifiers/ for valid classifiers

## Automated Publishing (Optional)

You can set up GitHub Actions for automatic publishing:

1. Add PyPI tokens to GitHub Secrets
2. Create `.github/workflows/publish.yml`
3. Auto-publish on git tags

## Package Management Commands

```bash
# Check package info
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m twine check dist/*

# Upload with verbose output
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m twine upload --verbose dist/*

# Upload specific file
"/Users/sonishsivarajkumar/Library/Mobile Documents/com~apple~CloudDocs/Personal/code/pytakes/.venv/bin/python" -m twine upload dist/pytakes-1.0.0-py3-none-any.whl
```

## Final Checklist

- [ ] PyPI and TestPyPI accounts created
- [ ] 2FA enabled on both accounts  
- [ ] API tokens created and stored securely
- [ ] `~/.pypirc` configured
- [ ] Package built successfully
- [ ] Tested on TestPyPI
- [ ] Uploaded to production PyPI
- [ ] Installation verified
- [ ] GitHub release created

## Expected Timeline

- **Account setup**: 10-15 minutes
- **Package building**: 2-3 minutes
- **TestPyPI upload**: 2-3 minutes
- **Production upload**: 2-3 minutes
- **Total**: ~20-30 minutes

Once uploaded, your package will be available at: **https://pypi.org/project/pytakes/**

Users can then install it with: `pip install pytakes`
