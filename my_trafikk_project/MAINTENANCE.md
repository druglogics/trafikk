# Template Maintenance Guide

**For:** Template maintainers updating this template when TRAFIKK modules release new versions.

**Time required:** 15-30 minutes per update.

---

## When to Update

- A new module version is released on PyPI or GitHub
- You want to include new features in the template
- A bug fix is important enough to pin the new version

---

## Quick Update Checklist

### Step 1: Test the New Version (10 min)

```bash
# Create a test environment (isolated from current template)
cd /tmp
mkdir trafikk_test
cd trafikk_test

# Copy a recent data sample or use synthetic data
cp -r /path/to/sample_data ./data

# Install the NEW module version (not from requirements.txt)
pip install celios==NEW_VERSION  # or whichever module updated

# Test with one of the template configs
celios config/celios.yaml

# Did it work? Any errors? Any output format changes?
```

**If it fails:** Don't update. File an issue with the module maintainers.

**If it works:** Continue to Step 2.

---

### Step 2: Update requirements.txt (1 min)

```bash
# Update the single line for the module that changed
# FROM:
# siflex==2.0.0

# TO:
# siflex==2.1.0
```

That's it. Just change the version number.

---

### Step 3: Check README for Compatibility Notes

Read through `README.md` and look for:

- Any module-specific instructions
- Config file references
- Expected output paths
- Any examples that might be outdated

**If nothing changed:** Move to Step 4.

**If there are breaking changes** (e.g., new required config field, output folder moved):
- Add a **2-3 line note** to the relevant section in README
- Example:
  ```markdown
  ### Step 6: Siflex — Pathway Analysis & Interactive Visualization
  
  **Note (v2.1.0+):** Siflex now exports pathway data to CSV. Add `"export_format": "csv"` 
  to config/siflex.json to enable this.
  ```

---

### Step 4: Update the Version Line in README (1 min)

At the top of `README.md`, update:

```markdown
> **Last verified:** 2025-05-05 with Celios 1.0.0, Gitsbe 3.2.1, Drexpa 2.1.0, Oris 1.5.2, Synco 1.0.0, Siflex 2.0.0
```

Change only the date and the **one module version** that updated.

---

### Step 5: Commit and Document (5 min)

```bash
# Stage changes
git add requirements.txt README.md

# Commit with clear message
git commit -m "chore: update Siflex to 2.1.0 (adds CSV export feature)"

# Push
git push origin main
```

**Commit message format:**
- `chore: update [Module] to [Version] ([brief description])`
- Examples:
  - `chore: update Oris to 1.6.0 (fixes SLURM timeout bug)`
  - `chore: update Drexpa to 2.2.0 (adds manual drug mappings)`

---

## When There's a Breaking Change

A breaking change = users' old configs will break.

### Example: Oris config format changed

**If you detect this:**

1. **Update requirements.txt** (as always)

2. **Add a clear section to README** before the affected step:

   ```markdown
   ### Step 4: Oris — Synergy Scoring via Signal Propagation
   
   **⚠️ Version 1.6.0+ requires a config change:**
   
   Old config:
   ```toml
   [oris]
   sampling = 50
   ```
   
   New config:
   ```toml
   [oris]
   default_sampling = 50
   media_targets = ["EGFR", "IGF1R"]
   ```
   
   See `config/oris.toml` for a full example.
   ```

3. **Update config/oris.toml** with the new format

4. **Commit:**
   ```bash
   git commit -m "docs: Oris 1.6.0 breaking change - update config format"
   ```

---


## Template Files to Modify

Only these files should ever change:

| File | Why | When |
|------|-----|------|
| `requirements.txt` | Pin new module version | Every update |
| `README.md` | Update version line + add breaking change notes | Every update |
| `config/*.yaml` / `config/*.json` / `config/*.toml` | Only if config format changed | Rarely |

---

## Quick Reference

**Normal update (no breaking changes):**
1. Test new version (works? ✓)
2. Edit `requirements.txt` (change 1 line)
3. Edit `README.md` (update version line only)
4. Commit with clear message

**Breaking change:**
1. Same as above, PLUS
2. Add 2-3 line note to affected README section
3. Update the relevant config file
4. Commit with "docs:" prefix

**Total time: 15-30 min**

---

## Questions?

- New module doesn't work with template? → Check module's changelog or GitHub issues
- Users report issues? → Test with that version, then update if needed
- Unsure if breaking change? → Compare old vs new config examples in module docs

Keep it simple. Update when needed, test first, document changes clearly.
