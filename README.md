# ECE444 Lecture Slides - Print Fix

This repository contains scripts to fix printing issues with Quarto reveal.js slide decks.

## Problem

When printing Quarto reveal.js slides (Ctrl+P or Cmd+P), scrollable code snippets are cut off at the bottom. The code blocks have `overflow: auto` for screen viewing, but this causes content to be hidden when printing.

## Solution

The `fix_print_code_blocks.py` script automatically adds CSS rules to the `@media print` section of HTML files to ensure all code content is visible when printing.

## Usage

### Fix all HTML files in inputs folder

```bash
python3 scripts/fix_print_code_blocks.py
```

The script will:
- Find all `.htm` and `.html` files in the `inputs/` directory
- Create backup files (`.bak`) before making changes
- Add print CSS fixes to ensure code blocks are fully visible
- Skip files that have already been fixed

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
├── outputs/             # Output directory
├── scripts/             # Utility scripts
│   └── fix_print_code_blocks.py
└── README.md           # This file
```

## Notes

- Backup files (`.bak`) are created automatically before modifications
- The script is idempotent - running it multiple times is safe
- Files that have already been fixed will be skipped
- The script preserves all existing CSS rules and only adds the print fixes

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

