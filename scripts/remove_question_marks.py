#!/usr/bin/env python3
import os
import re
import glob

def remove_question_marks(content):
    """Remove problematic encoding characters that display as question marks"""
    
    # Remove various problematic Unicode characters that might show as ?
    # Common replacements for encoding issues
    replacements = [
        ('\ufffd', ''),  # Unicode replacement character
        ('����', ''),    # Multiple replacement characters
        ('���', ''),     # Triple replacement characters
        ('��', ''),      # Double replacement characters  
        ('\u00bf', ''),  # Inverted question mark that might be misencoded
    ]
    
    # Apply all replacements
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Remove any remaining isolated question marks at the end of files
    # but be careful not to remove legitimate question marks in content
    content = re.sub(r'\s*\?\?\?\?+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\?\?\?\?+\s*$', '', content)
    
    return content

def main():
    # Process all chapter files
    chapter_files = glob.glob('/Users/pavel/Projects/attack-surface-tech/mashapedia/content/docs/chapters/*.md')
    
    for filepath in chapter_files:
        print(f"Processing {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = remove_question_marks(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Removed question mark characters from {os.path.basename(filepath)}")
        else:
            print(f"  No question mark characters found in {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()