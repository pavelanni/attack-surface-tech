#!/usr/bin/env python3
import os
import re
import glob

def fix_excessive_backticks(content):
    """Remove backticks from common acronyms and fix broken URLs"""
    
    # Common acronyms that shouldn't have backticks when used as normal words
    common_acronyms = [
        'MIT', 'OS', 'USB', 'CPU', 'GPU', 'RAM', 'ROM', 'SSD', 'HDD',
        'PDF', 'HTML', 'CSS', 'JS', 'XML', 'JSON', 'API', 'SQL', 'DNS',
        'HTTP', 'HTTPS', 'FTP', 'SSH', 'VPN', 'LAN', 'WAN', 'WiFi', 'GPS',
        'SMS', 'MMS', 'URL', 'URI', 'IP', 'TCP', 'UDP', 'SSL', 'TLS',
        'FAQ', 'CEO', 'CTO', 'IT', 'UI', 'UX', 'AI', 'ML', 'AR', 'VR',
        'iOS', 'macOS', 'Windows', 'Linux', 'Android', 'PC', 'Mac',
        'USA', 'UK', 'EU', 'FBI', 'CIA', 'NSA', 'GDPR', 'ISO', 'IEEE',
        'WWW', 'IRC', 'P2P', 'B2B', 'B2C', 'SaaS', 'IaaS', 'PaaS',
        'IDE', 'SDK', 'CLI', 'GUI', 'ASCII', 'UTF', 'RGB', 'CMYK'
    ]
    
    # Remove backticks from common acronyms
    for acronym in common_acronyms:
        # Remove backticks around the acronym when it's used as a normal word
        content = re.sub(rf'`{re.escape(acronym)}`', acronym, content)
    
    # Fix broken URLs - remove backticks from URLs
    # Pattern: `https://...` or `http://...`
    content = re.sub(r'`(https?://[^`\s]+)`', r'\1', content)
    
    # Fix backticks around parts of URLs in markdown links
    # Pattern: [text](`url`) -> [text](url)
    content = re.sub(r'\]\(`([^`]+)`\)', r'](\1)', content)
    
    # Fix backticks in the middle of URLs
    # Pattern: https://example.com/`path` -> https://example.com/path
    content = re.sub(r'(https?://[^\s\]]+)`([^`\s\]]+)`([^\s\]]*)', r'\1\2\3', content)
    
    # Remove backticks from common file extensions when used normally
    file_extensions = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'tar', 'gz']
    for ext in file_extensions:
        content = re.sub(rf'`\.{ext}`', f'.{ext}', content, flags=re.IGNORECASE)
        content = re.sub(rf'`{ext.upper()}`', ext.upper(), content)
    
    return content

def main():
    # Process all chapter files
    chapter_files = glob.glob('/Users/pavel/Projects/attack-surface-tech/mashapedia/content/docs/chapters/*.md')
    
    for filepath in chapter_files:
        print(f"Processing {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_excessive_backticks(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed backticks in {os.path.basename(filepath)}")
        else:
            print(f"  No changes needed in {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()