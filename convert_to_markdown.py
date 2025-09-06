#!/usr/bin/env python3
import re
import os

def convert_asciidoc_to_markdown(content):
    """Convert AsciiDoc content to Markdown format"""
    
    # Convert title (= Title => # Title)
    content = re.sub(r'^= (.+)$', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^== (.+)$', r'## \1', content, flags=re.MULTILINE)
    content = re.sub(r'^=== (.+)$', r'### \1', content, flags=re.MULTILINE)
    
    # Convert definition lists (Term:: Description => **Term**: Description)
    def convert_definition(match):
        term = match.group(1)
        return f'\n### {term}\n'
    
    content = re.sub(r'^([^:]+)::$', convert_definition, content, flags=re.MULTILINE)
    
    # Convert italic _text_ to *text*
    content = re.sub(r'(?<![\\*])_([^_]+)_(?![_*])', r'*\1*', content)
    
    # Convert backticks for inline code
    content = re.sub(r'`([^`]+)`', r'`\1`', content)
    
    # Convert links
    # link:url[text] => [text](url)
    content = re.sub(r'link:([^\[]+)\[([^\]]+)\]', r'[\2](\1)', content)
    
    # Convert quotes
    content = re.sub(r'^\[quote,([^\]]+)\]', r'> *— \1*', content, flags=re.MULTILINE)
    content = re.sub(r'^____$', '', content, flags=re.MULTILINE)
    
    # Remove AsciiDoc specific attributes
    content = re.sub(r'^:.*$', '', content, flags=re.MULTILINE)
    
    # Convert cross-references
    content = re.sub(r'<<([^,>]+),([^>]+)>>', r'[\2](#\1)', content)
    content = re.sub(r'<<([^>]+)>>', r'[See \1](#\1)', content)
    
    # Clean up extra blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content.strip()

def split_chapters(content):
    """Split content into chapters"""
    chapters = {}
    current_chapter = None
    current_content = []
    
    lines = content.split('\n')
    in_intro = True
    intro_content = []
    
    for line in lines:
        if line.startswith('## Chapter '):
            # Save previous chapter
            if current_chapter:
                chapters[current_chapter] = '\n'.join(current_content)
            elif in_intro:
                chapters['introduction'] = '\n'.join(intro_content)
                in_intro = False
            
            # Start new chapter
            match = re.match(r'## Chapter (\d+)', line)
            if match:
                current_chapter = f'chapter{match.group(1)}'
                current_content = [line]
        elif line.startswith('## Epilogue'):
            if current_chapter:
                chapters[current_chapter] = '\n'.join(current_content)
            current_chapter = 'epilogue'
            current_content = [line]
        elif current_chapter:
            current_content.append(line)
        elif in_intro and not line.startswith('# Mashapedia'):
            intro_content.append(line)
    
    # Save last chapter
    if current_chapter:
        chapters[current_chapter] = '\n'.join(current_content)
    
    return chapters

def create_chapter_files(chapters, output_dir):
    """Create individual markdown files for each chapter"""
    
    # Chapter metadata
    chapter_titles = {
        'introduction': 'Introduction',
        'chapter1': 'Chapter 1',
        'chapter2': 'Chapter 2',
        'chapter3': 'Chapter 3',
        'chapter4': 'Chapter 4',
        'chapter5': 'Chapter 5',
        'chapter6': 'Chapter 6',
        'chapter7': 'Chapter 7',
        'chapter8': 'Chapter 8',
        'chapter9': 'Chapter 9',
        'chapter10': 'Chapter 10',
        'chapter11': 'Chapter 11',
        'chapter12': 'Chapter 12',
        'chapter13': 'Chapter 13',
        'chapter14': 'Chapter 14',
        'epilogue': 'Epilogue'
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Create chapters index
    index_content = """---
title: Browse by Chapter
weight: 1
sidebar:
  open: true
---

# Technologies by Chapter

Browse the technologies as they appear in "Attack Surface" chapter by chapter.

{{< cards >}}
"""
    
    weight = 10
    for chapter_key in ['introduction'] + [f'chapter{i}' for i in range(1, 15)] + ['epilogue']:
        if chapter_key in chapters:
            title = chapter_titles.get(chapter_key, chapter_key)
            filename = f'{chapter_key}.md'
            filepath = os.path.join(output_dir, filename)
            
            # Add front matter to chapter content
            chapter_content = f"""---
title: "{title}"
weight: {weight}
---

{chapters[chapter_key]}
"""
            
            with open(filepath, 'w') as f:
                f.write(chapter_content)
            
            # Add to index
            if chapter_key != 'introduction':
                index_content += f'{{{{< card link="/docs/chapters/{chapter_key}" title="{title}" >}}}}\n'
            
            weight += 10
    
    index_content += "{{< /cards >}}"
    
    # Write chapters index
    with open(os.path.join(output_dir, '_index.md'), 'w') as f:
        f.write(index_content)

def create_alphabetical_index(content, output_dir):
    """Create alphabetical index of all terms"""
    
    # Extract all terms
    terms = {}
    term_pattern = r'^### (.+)$'
    
    lines = content.split('\n')
    current_term = None
    current_definition = []
    
    for line in lines:
        match = re.match(term_pattern, line)
        if match:
            # Save previous term
            if current_term:
                terms[current_term] = '\n'.join(current_definition).strip()
            
            # Start new term
            current_term = match.group(1)
            current_definition = []
        elif current_term and line and not line.startswith('#'):
            current_definition.append(line)
    
    # Save last term
    if current_term:
        terms[current_term] = '\n'.join(current_definition).strip()
    
    # Create alphabetical content
    os.makedirs(output_dir, exist_ok=True)
    
    alpha_content = """---
title: Alphabetical Index
weight: 2
---

# Alphabetical Index

All technologies mentioned in "Attack Surface" sorted alphabetically for quick reference.

"""
    
    # Group by first letter
    grouped = {}
    for term in sorted(terms.keys(), key=str.lower):
        first_letter = term[0].upper()
        if first_letter not in grouped:
            grouped[first_letter] = []
        grouped[first_letter].append(term)
    
    # Create content
    for letter in sorted(grouped.keys()):
        alpha_content += f"\n## {letter}\n\n"
        for term in grouped[letter]:
            alpha_content += f"### {term}\n\n{terms[term]}\n\n"
    
    with open(os.path.join(output_dir, '_index.md'), 'w') as f:
        f.write(alpha_content)

def main():
    # Read the main AsciiDoc file
    with open('attack-surface-tech.adoc', 'r') as f:
        content = f.read()
    
    # Convert to Markdown
    markdown_content = convert_asciidoc_to_markdown(content)
    
    # Split into chapters
    chapters = split_chapters(markdown_content)
    
    # Create chapter files
    create_chapter_files(chapters, 'mashapedia/content/docs/chapters')
    
    # Create alphabetical index
    create_alphabetical_index(markdown_content, 'mashapedia/content/alphabetical')
    
    print("Conversion complete!")
    print(f"Created {len(chapters)} chapter files")

if __name__ == '__main__':
    main()