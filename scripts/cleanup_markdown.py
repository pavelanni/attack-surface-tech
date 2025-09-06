#!/usr/bin/env python3
import re
import os
import glob

def fix_wikipedia_urls(text):
    """Fix Wikipedia URLs - replace asterisks with underscores"""
    # Fix patterns like https://en.wikipedia.org/wiki/Something*with*asterisks
    text = re.sub(
        r'(https://en\.wikipedia\.org/wiki/[^\s\)]+)',
        lambda m: m.group(1).replace('*', '_'),
        text
    )
    # Also fix the display text in markdown links
    text = re.sub(
        r'\[([^\]]*\*[^\]]*)\]\((https://en\.wikipedia\.org[^\)]+)\)',
        lambda m: f'[{m.group(1).replace("*", "_")}]({m.group(2).replace("*", "_")})',
        text
    )
    return text

def fix_all_urls(text):
    """Fix underscores appearing as asterisks in all URLs"""
    # Fix URLs in plain format
    text = re.sub(
        r'(https?://[^\s\)]+\*[^\s\)]*)',
        lambda m: m.group(1).replace('*', '_'),
        text
    )
    return text

def standardize_learn_more(text):
    """Standardize all 'More:' sections to 'Learn more:'"""
    text = re.sub(r'^More:\s*$', '**Learn more:**', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*Learn more:\*\*\s*$', '\n**Learn more:**', text, flags=re.MULTILINE)
    return text

def add_code_formatting(text):
    """Add backticks for technical terms and abbreviations"""
    # Common technical abbreviations
    tech_terms = [
        'FIFO', 'LIFO', 'GIGO', 'MIT', 'SSH', 'USB', 'HTTPS', 'SSL', 'TLS',
        'IP', 'TCP', 'UDP', 'DNS', 'VPN', 'API', 'CPU', 'GPU', 'RAM', 'ROM',
        'BIOS', 'OS', 'VM', 'GUI', 'CLI', 'IDE', 'SDK', 'APK', 'iOS', 'GPS',
        'NFC', 'RFID', 'IMSI', 'PGP', 'RSA', 'AES', 'SHA', 'MD5', 'XML', 'JSON',
        'HTML', 'CSS', 'JS', 'SQL', 'PHP', 'URL', 'URI', 'HTTP', 'FTP', 'SMTP',
        'POP3', 'IMAP', 'LDAP', 'DHCP', 'NAT', 'LAN', 'WAN', 'MAC', 'WLAN',
        'ISP', 'CDN', 'DDoS', 'IDS', 'IPS', 'SIEM', 'SOC', 'OSINT', 'CTF',
        'APT', 'IOC', 'TTP', 'MITRE', 'CVE', 'CVSS', 'OWASP', 'XSS', 'CSRF',
        'SQLi', 'RCE', 'LFI', 'RFI', 'XXE', 'SSRF', 'IDOR', 'JWT', 'OAuth',
        'SAML', 'MFA', '2FA', 'OTP', 'PIN', 'KMS', 'HSM', 'TPM', 'PKI', 'CA',
        'CRL', 'OCSP', 'CSR', 'SSL/TLS', 'VoIP', 'PBX', 'SIP', 'RTP', 'PSTN',
        'GSM', 'CDMA', 'LTE', '5G', 'IoT', 'MQTT', 'CoAP', 'LoRa', 'BLE',
        'USLON', 'GULAG', 'COINTELPRO', 'FBI', 'NSA', 'CIA', 'EFF', 'MIT',
        'CALEA', 'IED', 'RPG', 'MRE', 'FOB', 'PX', 'USG', 'MRAP', 'EXIF',
        'SIM', 'OMFG', 'ZOMFG', 'WAP', 'ARGs', 'UUCP', 'IRS', 'SUP',
        'PDF', 'EPUB', 'MOBI', 'DVD'
    ]
    
    # Add backticks to standalone tech terms (word boundaries)
    for term in tech_terms:
        # Skip if already in backticks
        text = re.sub(
            rf'(?<!`)\b({term})\b(?!`)',
            r'`\1`',
            text
        )
    
    # Format domain names and email-like patterns
    text = re.sub(r'(\s)([a-zA-Z0-9]+\.(onion|com|org|net|io|gov|edu))(\s|[,\.]|$)', r'\1`\2`\4', text)
    
    # Format commands (common patterns)
    commands = ['git', 'ssh', 'npm', 'pip', 'docker', 'kubectl', 'curl', 'wget', 'grep', 'sed', 'awk']
    for cmd in commands:
        text = re.sub(rf'(\s)({cmd})(\s)', r'\1`\2`\3', text)
    
    return text

def fix_quote_blocks(text):
    """Fix quote formatting and code blocks"""
    # Fix the Blinkenlights German text - find and format as code block
    blinkenlights_pattern = r'(ACHTUNG!.*?BLINKENLICHTEN\.)'
    text = re.sub(
        blinkenlights_pattern,
        lambda m: '```\n' + m.group(1) + '\n```',
        text,
        flags=re.DOTALL
    )
    
    # Fix author quotes to use proper blockquote
    text = re.sub(
        r'^> \*\*— ([^*]+)\*\*\s*\n>(.+)$',
        r'> \2\n>\n> — *\1*',
        text,
        flags=re.MULTILINE
    )
    
    # Clean up standalone quote attributions
    text = re.sub(
        r'^> \*\*— ([^*]+)\*\*\s*$',
        r'',
        text,
        flags=re.MULTILINE
    )
    
    return text

def remove_cross_references(text):
    """Remove AsciiDoc cross-reference artifacts"""
    # Remove [[chapter-X]] patterns
    text = re.sub(r'\[\[chapter-\d+\]\]', '', text)
    text = re.sub(r'\[\[epilogue\]\]', '', text)
    text = re.sub(r'\[\[.+?\]\]', '', text)
    
    # Remove "See technologies from" lines
    text = re.sub(r'^See technologies from .+$', '', text, flags=re.MULTILINE)
    
    # Clean up resulting empty lines
    text = re.sub(r'\n\n\n+', '\n\n', text)
    
    return text

def add_visual_separation(text):
    """Add horizontal rules between terms for better separation"""
    # Don't add separator after main headings or before subheadings
    lines = text.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        result.append(line)
        
        # Check if this is a term heading (### **Something**)
        if line.startswith('### **') and i < len(lines) - 1:
            # Look ahead to find where this term's content ends
            # (next term or section starts)
            j = i + 1
            while j < len(lines):
                if lines[j].startswith('###') or lines[j].startswith('##') or lines[j].startswith('#'):
                    # Found next heading, add separator before it
                    # But only if there's actual content
                    if j > i + 2:  # Has content
                        result.insert(len(result) - 1, '\n---\n')
                    break
                j += 1
    
    return '\n'.join(result)

def fix_formatting_issues(text):
    """Fix various formatting issues"""
    # Fix "### **" appearing on separate lines
    text = re.sub(r'^### \*\*\s*\n(.+)\*\*', r'### **\1**', text, flags=re.MULTILINE)
    
    # Fix orphaned asterisks
    text = re.sub(r'^([A-Z][^*\n]+)\*\*\s*$', r'### **\1**', text, flags=re.MULTILINE)
    
    # Fix backticks in contractions
    text = text.replace("`'", "'")
    text = text.replace("'`", "'")
    
    # Ensure proper spacing around headings
    text = re.sub(r'(\n###[^\n]+\n)([^\n])', r'\1\n\2', text)
    
    # Remove trailing whitespace
    text = re.sub(r' +$', '', text, flags=re.MULTILINE)
    
    # Fix multiple blank lines
    text = re.sub(r'\n\n\n+', '\n\n', text)
    
    return text

def process_file(filepath):
    """Process a single markdown file"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all fixes in order
    content = fix_wikipedia_urls(content)
    content = fix_all_urls(content)
    content = standardize_learn_more(content)
    content = add_code_formatting(content)
    content = fix_quote_blocks(content)
    content = remove_cross_references(content)
    content = fix_formatting_issues(content)
    
    # Add visual separation last to avoid interfering with other fixes
    if 'alphabetical' in filepath or 'chapter' in filepath:
        content = add_visual_separation(content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Fixed URLs, formatting, and styling")

def main():
    """Process all markdown files in the Hugo content directory"""
    content_dir = 'mashapedia/content'
    
    # Find all markdown files
    md_files = glob.glob(f'{content_dir}/**/*.md', recursive=True)
    
    print(f"Found {len(md_files)} markdown files to process\n")
    
    for filepath in md_files:
        # Skip index files that don't contain term definitions
        if '_index.md' in filepath and 'chapters' not in filepath and 'alphabetical' not in filepath:
            print(f"Skipping {filepath} (index file)")
            continue
        
        process_file(filepath)
    
    print("\n✅ Cleanup complete!")
    print("\nFixed:")
    print("  • Wikipedia and other URLs (replaced * with _)")
    print("  • Standardized 'Learn more:' sections")
    print("  • Added code formatting for technical terms")
    print("  • Fixed quote and code blocks")
    print("  • Removed cross-reference artifacts")
    print("  • Added visual separation between terms")
    print("  • Fixed various formatting issues")

if __name__ == '__main__':
    main()