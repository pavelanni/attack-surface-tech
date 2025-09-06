# Mashapedia - Hugo Version

This is the Hugo-powered version of the Mashapedia project - a glossary of technologies mentioned in Cory Doctorow's "Attack Surface".

## Features

- **Modern Documentation Site**: Built with Hugo and the Hextra theme
- **Fast Search**: Built-in FlexSearch for quick term lookup
- **Responsive Design**: Works great on desktop and mobile
- **Two Browse Modes**: 
  - Chapter-by-chapter (following the book's structure)
  - Alphabetical index (for quick reference)
- **GitHub Integration**: Easy contributions via pull requests

## Local Development

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.110.0 or later)
- Git

### Running Locally

1. Clone the repository with submodules:
```bash
git clone --recursive https://github.com/pavelanni/attack-surface-tech.git
cd attack-surface-tech/mashapedia
```

2. Start the Hugo development server:
```bash
hugo server --buildDrafts
```

3. Open your browser to http://localhost:1313

### Building for Production

To build the static site:

```bash
hugo --minify
```

The built site will be in the `public/` directory.

## Project Structure

```
mashapedia/
├── content/
│   ├── _index.md           # Homepage
│   ├── docs/
│   │   ├── _index.md       # Documentation landing
│   │   └── chapters/       # Chapter-by-chapter glossary
│   │       ├── introduction.md
│   │       ├── chapter1.md
│   │       └── ...
│   ├── alphabetical/       # Alphabetical index
│   │   └── _index.md
│   └── about/              # About page
│       └── _index.md
├── themes/
│   └── hextra/            # Documentation theme
├── hugo.yaml              # Hugo configuration
└── README.md             # This file
```

## Content Format

The content is written in Markdown with Hugo front matter. Each term follows this format:

```markdown
### Term Name

Definition and explanation of the term.

- [Link to Wikipedia](https://en.wikipedia.org/...)
- [Other reference](https://example.com/...)
```

## Contributing

Contributions are welcome! To add or update terms:

1. Fork the repository
2. Create a feature branch
3. Make your changes to the appropriate Markdown files
4. Test locally with `hugo server`
5. Submit a pull request

## Migration from AsciiDoc

This Hugo version was migrated from the original AsciiDoc format. The conversion script (`convert_to_markdown.py`) in the parent directory handles:

- Converting AsciiDoc syntax to Markdown
- Splitting content into chapters
- Creating the alphabetical index
- Generating Hugo front matter

## Theme

This site uses the [Hextra](https://imfing.github.io/hextra/) theme, which provides:

- Clean, modern documentation design
- Built-in search functionality
- Responsive layout
- Dark mode support
- GitHub integration

## License

This project is licensed under the MIT License - see the LICENSE file in the parent directory for details.

## Acknowledgments

- Cory Doctorow for writing "Attack Surface"
- The Hugo team for the static site generator
- The Hextra theme developers
- All contributors to the glossary