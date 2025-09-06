#!/usr/bin/env python3
import re
import glob

def fix_malformed_headings(filepath):
    """Fix incomplete or malformed headings in markdown files"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove incomplete headings like "### **" with nothing after
    content = re.sub(r'^### \*\*\s*$', '', content, flags=re.MULTILINE)
    
    # Remove standalone "###" with nothing after
    content = re.sub(r'^###\s*$', '', content, flags=re.MULTILINE)
    
    # Remove incomplete headings at end of file
    content = re.sub(r'\n### \*\*\s*\Z', '', content)
    
    # Clean up multiple consecutive separators
    content = re.sub(r'(\n---\n)\n+---\n', r'\1', content)
    
    # Clean up trailing separators at end of file
    content = re.sub(r'\n---\n*\Z', '\n', content)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all chapter and alphabetical files"""
    
    # Find all markdown files in chapters and alphabetical
    files = glob.glob('mashapedia/content/docs/chapters/*.md')
    files.extend(glob.glob('mashapedia/content/alphabetical/*.md'))
    
    print(f"Found {len(files)} files to check\n")
    
    fixed_count = 0
    for filepath in sorted(files):
        filename = filepath.split('/')[-1]
        print(f"Checking {filename}...")
        if fix_malformed_headings(filepath):
            print(f"  ✓ Fixed malformed headings")
            fixed_count += 1
        else:
            print(f"  - No issues found")
    
    print(f"\n✅ Complete! Fixed {fixed_count} files")

if __name__ == '__main__':
    main()