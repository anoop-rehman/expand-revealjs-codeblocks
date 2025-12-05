# ECE444 Lecture Slides - Print Fix

This repository contains scripts to fix printing issues with Quarto reveal.js slide decks.

## Problem

When printing Quarto reveal.js slides (Ctrl+P or Cmd+P), scrollable code snippets are cut off at the bottom. The code blocks have `overflow: auto` for screen viewing, but this causes content to be hidden when printing.

## Solution

The `fix_print_code_blocks.py` script automatically adds CSS rules to the `@media print` section of HTML files to ensure all code content is visible when printing.

**Important:** The script keeps all files in `inputs/` untouched. It copies HTML files and their associated `_files` folders to the `outputs/` directory, then applies the fixes to the copied files.

## Usage

### Fix all HTML files

```bash
python3 scripts/fix_print_code_blocks.py
```

The script will:
- Find all `.htm` and `.html` files in the `inputs/` directory
- Copy HTML files to the `outputs/` directory
- Copy associated `_files` folders (containing CSS, JS, and other assets) to `outputs/`
- Add print CSS fixes to ensure code blocks are fully visible
- Keep all original files in `inputs/` untouched

### What gets fixed

The script adds the following CSS rules to the `@media print` block:

```css
div.sourceCode { overflow: visible !important; max-height: none !important; }
pre.sourceCode { overflow: visible !important; max-height: none !important; }
pre > code.sourceCode { overflow: visible !important; max-height: none !important; }
code.sourceCode { overflow: visible !important; max-height: none !important; }
```

These rules ensure that:
- Code blocks don't have overflow restrictions when printing
- Maximum height limits are removed
- All code content is visible in the printed output

## Project Structure

```
lectures/
├── inputs/              # Source HTML files (Quarto reveal.js slides)
│   ├── lecture-*.htm    # Lecture slide files
│   └── lecture-*_files/ # Associated assets (CSS, JS, etc.)
├── outputs/             # Output directory (fixed HTML files and _files folders)
├── scripts/             # Utility scripts
│   └── fix_print_code_blocks.py
└── README.md           # This file
```

## Notes

- **Input files are never modified** - all changes are made to copies in `outputs/`
- The script copies both HTML files and their associated `_files` folders to maintain styling
- The script is idempotent - running it multiple times is safe
- Files that have already been fixed will still be copied to outputs
- The script preserves all existing CSS rules and only adds the print fixes
- Use the files in `outputs/` for printing - they have the fixes applied

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

