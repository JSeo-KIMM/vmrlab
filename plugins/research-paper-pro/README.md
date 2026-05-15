# Paper Researcher Pro

Academic paper toolkit for robotics and kinematics research.

## Commands

| Command | Description |
|---|---|
| `/research-paper-pro:review <file>` | PhD-level peer review (PDF or Markdown) |
| `/research-paper-pro:convert <file>` | Convert PDF to Obsidian-compatible Markdown |
| `/research-paper-pro:revise <review> <paper>` | Apply tracked revisions based on a review file |
| `/research-paper-pro:paper-draft-pro <draft>` | Polish a casual Korean draft into academic Markdown (optional EN version) |

## Examples

```bash
# Peer review a paper
/research-paper-pro:review ./my_paper.pdf
/research-paper-pro:review ./my_paper.md

# Convert PDF to Markdown
/research-paper-pro:convert ./my_paper.pdf

# Revise a paper based on a review file
/research-paper-pro:revise ./review-detail.md ./my_paper.md

# Polish a Korean draft into an academic-style manuscript
/research-paper-pro:paper-draft-pro ./my_draft.md
```

## Components

- **commands/review.md** — Entry point for peer review
- **commands/convert.md** — Entry point for PDF conversion
- **commands/revise.md** — Entry point for revision based on review
- **commands/paper-draft-pro.md** — Entry point for Korean draft polishing
- **agents/paper-reviewer.md** — Robotics & kinematics PhD reviewer agent
- **agents/paper-converter.md** — PDF-to-Markdown conversion agent
- **agents/paper-reviser.md** — Tracked-changes revision agent
- **agents/paper-drafter.md** — Korean draft polishing agent
- **skills/paper-reviewer-pro/** — Review criteria, checklist, and output format
- **skills/paper-pdf-to-md/** — Conversion rules and Obsidian formatting
- **skills/paper-pdf-to-md/scripts/extract_images.py** — Figure extraction script
- **skills/paper-reviser-pro/** — Tracked-changes revision rules
- **skills/paper-draft-pro/** — Korean draft polishing rules (word count control, [] directive handling, EN translation)

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
