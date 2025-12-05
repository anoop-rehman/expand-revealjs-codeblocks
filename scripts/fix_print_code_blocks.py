#!/usr/bin/env python3
"""
Fix print CSS for Quarto reveal.js slides to ensure scrollable code snippets
are fully visible when printing (Ctrl+P).

This script adds CSS rules to the @media print section to:
- Remove overflow restrictions on code blocks
- Ensure all code content is visible when printing
- Prevent code blocks from being cut off
"""

import re
import os
from pathlib import Path


def fix_print_css(html_content):
    """
    Add CSS rules to fix code block printing issues.
    
    Args:
        html_content: The HTML content as a string
        
    Returns:
        Modified HTML content with print CSS fixes
    """
    # CSS rules to add for print media
    print_css_fixes = """    div.sourceCode { overflow: visible !important; max-height: none !important; }
    pre.sourceCode { overflow: visible !important; max-height: none !important; }
    pre > code.sourceCode { overflow: visible !important; max-height: none !important; }
    code.sourceCode { overflow: visible !important; max-height: none !important; }
"""
    
    # Check if fixes are already present
    if 'div.sourceCode { overflow: visible !important' in html_content:
        return html_content  # Already fixed
    
    # Find @media print block by locating the opening brace and finding its matching closing brace
    media_print_start = html_content.find('@media print {')
    if media_print_start == -1:
        # No @media print block found, add one before </style>
        style_close_pos = html_content.find('  </style>')
        if style_close_pos != -1:
            media_print_block = f'    @media print {{\n{print_css_fixes}    }}\n'
            return html_content[:style_close_pos] + media_print_block + html_content[style_close_pos:]
        return html_content
    
    # Find the matching closing brace for @media print
    # Start after the opening brace
    brace_count = 0
    pos = media_print_start + len('@media print {')
    start_pos = pos
    
    while pos < len(html_content):
        if html_content[pos] == '{':
            brace_count += 1
        elif html_content[pos] == '}':
            if brace_count == 0:
                # Found the matching closing brace
                # Insert CSS fixes before this closing brace
                before_brace = html_content[:pos]
                after_brace = html_content[pos:]
                return before_brace + print_css_fixes + '    ' + after_brace
            brace_count -= 1
        pos += 1
    
    # If we couldn't find the closing brace, return original
    return html_content


def process_html_file(file_path):
    """
    Process a single HTML file to fix print CSS.
    
    Args:
        file_path: Path to the HTML file
    """
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has the fix
        if 'div.sourceCode { overflow: visible !important' in content:
            print(f"  ✓ Already fixed: {file_path.name}")
            return False
        
        # Apply the fix
        modified_content = fix_print_css(content)
        
        if modified_content != content:
            # Backup original file
            backup_path = file_path.with_suffix('.htm.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  → Backup created: {backup_path.name}")
            
            # Write modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"  ✓ Fixed: {file_path.name}")
            return True
        else:
            print(f"  ⚠ No changes made: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function to process all HTML files in the inputs directory."""
    # Get the project root (parent of scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    inputs_dir = project_root / 'inputs'
    
    if not inputs_dir.exists():
        print(f"Error: Inputs directory not found: {inputs_dir}")
        return
    
    # Find all HTML files
    html_files = list(inputs_dir.glob('*.htm')) + list(inputs_dir.glob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {inputs_dir}")
        return
    
    print(f"Found {len(html_files)} HTML file(s) to process\n")
    
    fixed_count = 0
    for html_file in html_files:
        if process_html_file(html_file):
            fixed_count += 1
        print()
    
    print(f"Summary: {fixed_count} file(s) fixed, {len(html_files) - fixed_count} file(s) unchanged")


if __name__ == '__main__':
    main()

