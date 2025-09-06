#!/usr/bin/env python3
import re
import glob

def remove_duplicate_title(filepath):
    """Remove duplicate h2 title that matches frontmatter title"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter title
    frontmatter_match = re.match(r'^---\ntitle: "(.+)"\nweight: \d+\n---\n', content)
    if not frontmatter_match:
        print(f"  ⚠️  Could not parse frontmatter in {filepath}")
        return False
    
    title = frontmatter_match.group(1)
    
    # Remove the duplicate h2 title if it exists
    # Pattern to match: ## Chapter X or ## Introduction or ## Epilogue
    # followed by optional blank lines and a separator
    patterns_to_remove = [
        rf'\n## {re.escape(title)}\n+',  # Exact match with title
        r'\n## Chapter \d+\n+',           # Any chapter number
        r'\n## Introduction\n+',          # Introduction
        r'\n## Epilogue\n+',              # Epilogue
    ]
    
    original_content = content
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '\n', content)
    
    # Also clean up if there's a separator right after frontmatter
    content = re.sub(r'(---\n)\n+---\n', r'\1', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all chapter files"""
    
    # Find all chapter markdown files
    chapter_files = glob.glob('mashapedia/content/docs/chapters/*.md')
    
    # Exclude the index file
    chapter_files = [f for f in chapter_files if not f.endswith('_index.md')]
    
    print(f"Found {len(chapter_files)} chapter files to process\n")
    
    updated_count = 0
    for filepath in sorted(chapter_files):
        filename = filepath.split('/')[-1]
        print(f"Processing {filename}...")
        if remove_duplicate_title(filepath):
            print(f"  ✓ Removed duplicate title")
            updated_count += 1
        else:
            print(f"  - No duplicate title found")
    
    print(f"\n✅ Complete! Updated {updated_count} files")

if __name__ == '__main__':
    main()