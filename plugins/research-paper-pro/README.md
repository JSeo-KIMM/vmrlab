# Paper Researcher Pro

Academic paper toolkit for robotics and kinematics research.

## Commands

| Command | Description |
|---|---|
| `/research-paper-pro:review <file>` | PhD-level peer review (PDF or Markdown) |
| `/research-paper-pro:convert <file>` | Convert PDF to Obsidian-compatible Markdown |

## Examples

```bash
# Peer review a paper
/research-paper-pro:review ./my_paper.pdf
/research-paper-pro:review ./my_paper.md

# Convert PDF to Markdown
/research-paper-pro:convert ./my_paper.pdf
```

## Components

- **commands/review.md** — Entry point for peer review
- **commands/convert.md** — Entry point for PDF conversion
- **agents/paper-reviewer.md** — Robotics & kinematics PhD reviewer agent
- **agents/paper-converter.md** — PDF-to-Markdown conversion agent
- **skills/paper-reviewer-pro/** — Review criteria, checklist, and output format
- **skills/paper-pdf-to-md/** — Conversion rules and Obsidian formatting
- **skills/paper-pdf-to-md/scripts/extract_images.py** — Figure extraction script

## Requirements

```bash
pip install pymupdf
```

## Installation

```bash
# Test without installing
claude --plugin-dir ./research-paper-pro

# Install for current user (all projects)
claude plugin install ./research-paper-pro --scope user

# Install for current project only
claude plugin install ./research-paper-pro --scope project
```
