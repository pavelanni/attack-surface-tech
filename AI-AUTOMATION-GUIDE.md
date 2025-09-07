---
title: "AI automation guide for future companion sites"
weight: 999
---

# Using AI to create book companion sites

This document outlines how to use LLMs to create similar technology glossary sites for future books, based on the Mashapedia model.

## Overview

Creating a companion site like Mashapedia can be partially automated using modern LLMs. This approach can reduce initial work by 70-80%, allowing you to focus on quality control and adding unique insights.

## Prerequisites

- The full text of the book (with proper permissions)
- This Mashapedia site as a template/example
- Access to a capable LLM (Claude, GPT-4, etc. with ~100k+ token context)

## Process

### Step 1: Prepare your materials

1. Export several sample chapters from Mashapedia as examples
2. Have the new book's text ready in digital format
3. Prepare the Hugo site structure from this project

### Step 2: Create the extraction prompt

Use a prompt like this:

```
Here's a glossary site I created for Cory Doctorow's "Attack Surface":
[Include 2-3 sample chapters from Mashapedia showing the format]

Please analyze this new book [paste full text] and create a similar glossary:
1. Identify all technologies, tools, hacking concepts, and technical references
2. Group them by chapter
3. For each term, provide:
   - A brief explanation (2-3 sentences)
   - Why it's relevant to the story
   - Links to Wikipedia or official documentation
4. Format as Markdown using the same structure as the examples
```

### Step 3: What the AI can automate

- **Initial identification** of technical terms and concepts
- **Drafting basic definitions** with appropriate context
- **Suggesting relevant links** to Wikipedia and documentation
- **Organizing by chapter** maintaining narrative flow
- **Creating Markdown structure** ready for Hugo

### Step 4: Human review and enhancement

You'll still need to:

1. **Verify accuracy** of technical definitions
2. **Add personal insights** and commentary
3. **Check links** are current and relevant
4. **Add context** about why terms matter to the story
5. **Ensure consistency** in tone and style
6. **Fill gaps** the AI might have missed

### Step 5: Technical implementation

1. Use the same Hugo + Hextra structure from this project
2. Copy the `/mashapedia/` directory as your starting point
3. Replace content in `/content/docs/chapters/`
4. Update site metadata in `hugo.yaml`
5. Generate new social media images with DALL-E
6. Deploy to Cloudflare Pages

## Example workflow

```bash
# 1. Clone this project structure
cp -r mashapedia/ new-book-companion/

# 2. Clear old content
rm new-book-companion/content/docs/chapters/*.md

# 3. Generate new content with AI
# [Use the LLM to process the book]

# 4. Add generated markdown files
# 5. Review and edit
# 6. Deploy
```

## Tips for better results

- **Provide clear examples** - The more sample content you show, the better the output
- **Process in chunks** - Consider processing 3-4 chapters at a time for better accuracy
- **Iterate on definitions** - Ask the AI to expand on interesting technologies
- **Cross-reference** - Have the AI identify connections between technologies across chapters

## Time and effort estimation

- **Traditional manual approach**: 40-60 hours
- **AI-assisted approach**: 10-15 hours
  - AI processing: 1-2 hours
  - Review and editing: 6-8 hours  
  - Site setup and deployment: 2-3 hours
  - Polish and personal touches: 2-3 hours

## Ethical considerations

- Always ensure you have rights to process the book text
- Credit the original author appropriately
- Add value through your curation and insights
- Consider reaching out to the author - they might appreciate the companion resource!

## Future improvements

As LLMs improve, consider:
- Automated link validation
- Cross-referencing between terms
- Generating comprehension questions
- Creating visual diagrams of technology relationships
- Building interactive timelines of technology mentions

---

*This guide was created based on the experience of building Mashapedia for "Attack Surface" and represents best practices as of 2024.*