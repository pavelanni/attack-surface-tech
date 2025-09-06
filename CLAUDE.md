# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This is a documentation project that creates a "Mashapedia" - a glossary of technologies mentioned in Cory Doctorow's book "Attack Surface". The project is written in AsciiDoc format and generates HTML documentation.

## Key files

- `attack-surface-tech.adoc` - Main glossary file with technology terms organized chapter-by-chapter
- `mashapedia-alphabetical.adoc` - Alphabetically sorted version of the glossary
- `index.adoc` - Entry point page with introduction and links to both versions
- `chapter*.adoc` - Individual chapter files with glossary terms
- `sort_glossary.py` - Python script to sort glossary terms alphabetically

## Development commands

### Sort glossary alphabetically

```bash
python3 sort_glossary.py > mashapedia-alphabetical.adoc
```

### Generate HTML from AsciiDoc

To generate HTML files from AsciiDoc sources, you need to have asciidoctor installed:

```bash
# Install asciidoctor (if not installed)
gem install asciidoctor

# Generate HTML
asciidoctor attack-surface-tech.adoc
asciidoctor mashapedia-alphabetical.adoc
asciidoctor index.adoc
```

## Project structure

The repository contains:
- AsciiDoc source files documenting technology terms from the book
- Pre-generated HTML files for viewing the documentation
- Custom CSS stylesheets in `stylesheets/` directory
- Python utility script for sorting the glossary

## Glossary format

Each glossary entry follows the AsciiDoc definition list format:

```asciidoc
Term Name::
Description of the term with explanations and links.
* Link 1
* Link 2
```

Terms are organized by chapter in the main file and alphabetically in the sorted version.