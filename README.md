# Mashapedia: Technologies of _Attack Surface_ by Cory Doctorow

A comprehensive glossary of technologies mentioned in Cory Doctorow's book _Attack Surface_, built with Hugo and organized for easy reference.

## About this project

I have read this book recently (of course, after reading the previous two, _Little Brother_ and _Homeland_)
and noticed that I am not very familiar with some technologies mentioned in the book.
So I googled and learned about them and decided to collect the links and short descriptions here in this repo.

The project has been migrated from AsciiDoc to a Hugo static site for better navigation and organization.

## Structure

- **`mashapedia/`** - Hugo static site with the glossary
- **`asciidoc-legacy/`** - Original AsciiDoc source files
- **`scripts/`** - Python conversion and maintenance scripts

## Development

To run the development server:

```bash
cd mashapedia
hugo server --buildDrafts --port 1313
```

To build the site:

```bash
cd mashapedia
hugo
```

## Contributing

Feel free to fork and edit/expand this document and then open a PR. I appreciate all feedback and help.

## Links

- [Live site](https://pavelanni.github.io/attack-surface-tech/) (if deployed)
- [Cory Doctorow's page](https://craphound.com/)
- [Attack Surface page](https://craphound.com/category/attacksurface/)
- [Little Brother and Homeland](https://craphound.com/category/littlebrother/)