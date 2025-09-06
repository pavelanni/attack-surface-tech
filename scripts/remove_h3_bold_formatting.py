#!/usr/bin/env python3
import os
import re
import glob

def remove_h3_bold_formatting(content):
    """Remove ** bold formatting from h3 headings"""
    
    # Pattern to match ### **text** and replace with ### text
    # This handles various cases:
    # ### **Term**
    # ### **Term with spaces**
    # ### **`Term with backticks`**
    pattern = r'^### \*\*(.*?)\*\*$'
    
    def replace_heading(match):
        heading_text = match.group(1)
        return f'### {heading_text}'
    
    content = re.sub(pattern, replace_heading, content, flags=re.MULTILINE)
    
    return content

def main():
    # Process all chapter files
    chapter_files = glob.glob('/Users/pavel/Projects/attack-surface-tech/mashapedia/content/docs/chapters/*.md')
    
    for filepath in chapter_files:
        print(f"Processing {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = remove_h3_bold_formatting(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Removed bold formatting from h3 headings in {os.path.basename(filepath)}")
        else:
            print(f"  No h3 bold formatting found in {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()