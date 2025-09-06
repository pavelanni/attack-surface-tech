#!/usr/bin/env python3
import os
import re
import glob

def remove_asciidoc_artifacts(content):
    """Remove remaining AsciiDoc syntax artifacts"""
    
    # Remove AsciiDoc line continuation markers (+ on their own line)
    content = re.sub(r'^[[:space:]]*\+[[:space:]]*$', '', content, flags=re.MULTILINE)
    
    # Remove AsciiDoc code block delimiters (---- on their own line)
    content = re.sub(r'^-{4,}$', '', content, flags=re.MULTILINE)
    
    # Remove AsciiDoc section delimiters (==== on their own line)
    content = re.sub(r'^={4,}$', '', content, flags=re.MULTILINE)
    
    # Remove other common AsciiDoc artifacts
    # Remove empty attribute lists like [source,bash] that might be leftover
    content = re.sub(r'^\[source[^\]]*\]$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\[listing\]$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\[quote[^\]]*\]$', '', content, flags=re.MULTILINE)
    
    # Clean up multiple consecutive empty lines (leave max 2)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

def main():
    # Process all chapter files
    chapter_files = glob.glob('/Users/pavel/Projects/attack-surface-tech/mashapedia/content/docs/chapters/*.md')
    
    for filepath in chapter_files:
        print(f"Processing {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = remove_asciidoc_artifacts(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Removed AsciiDoc artifacts from {os.path.basename(filepath)}")
        else:
            print(f"  No AsciiDoc artifacts found in {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()