---
name: typst-documents
description: Use Typst to author, refactor, and compile source-first PDF documents such as resumes, cover letters, technical guides, systems-engineering templates, reports, checklists, and review packets. Prefer this over word-processor workflows when the document should be reproducible, reviewable, template-driven, or compiled in CI.
---

# Typst Documents

Use this skill when the job is to create, revise, template, or compile a Typst document.

This skill generalizes private working patterns from source-first document repos without carrying over private names, companies, roles, contacts, stories, or other personal content. Keep the reusable structure; replace all domain content with the user's current, explicit inputs.

Start here:

- `typst compile input.typ output.pdf`
- `typst watch input.typ output.pdf`
- `typst --version`
- `just build` when the repo already has a `justfile` build contract

Prefer checked-in `.typ` source as the canonical artifact. Treat generated PDFs as outputs unless the repo explicitly tracks them for review or distribution.

## When to Use

Use this skill for:

- resumes, cover letters, job packets, one-pagers, or portfolio PDFs
- engineering documents such as design reviews, trade studies, requirements traceability matrices, FMEAs, ICDs, test plans, and specifications
- technical guides, interview prep packets, runbooks, cheat sheets, and workshop handouts
- converting an ad hoc Markdown or prose draft into a styled, repeatable PDF
- creating a reusable Typst template with small `#let` helpers instead of copy-pasted formatting
- adding build/watch/clean recipes around Typst compilation

Do not use this skill when:

- the target output is primarily a web page, slide deck, spreadsheet, or plain Markdown note
- the user needs pixel-perfect brand work better handled in a design tool
- the document contains private source material that has not been explicitly authorized for reuse in the current output
- a short prose answer is enough and no durable source artifact is needed

## Privacy and Source Discipline

When learning from an existing private document repo:

1. Inspect structure, commands, conventions, reusable macros, and build shape.
2. Do **not** copy personal names, email addresses, phone numbers, addresses, company contacts, role-specific details, interview notes, job descriptions, private metrics, anecdotes, or unpublished strategy notes into a shared skill or public repo.
3. Replace concrete private examples with neutral placeholders such as `Candidate Name`, `Company`, `Role`, `Project`, `Requirement`, or `Decision`.
4. Keep any examples short enough to teach syntax, not enough to reveal source content.
5. Before committing, search the diff for private strings from the source repo.

A good generalized skill says “use a source-first `.typ` file, reusable `#let` helpers, checked-in build recipes, and compile verification.” It does not say whose resume, which company, which interview, or which private content inspired the pattern.

## Core Typst Document Pattern

Use this baseline shape unless the repo already has a stronger local template:

```typst
#set document(title: "Document Title", author: "Author")
#set page(margin: (x: 0.7in, y: 0.55in))
#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, leading: 0.55em)
#set list(spacing: 0.35em)

#show link: it => underline(text(fill: rgb("#0366d6"), it))
#show heading.where(level: 2): it => {
  v(0.6em)
  text(weight: "bold", tracking: 0.08em, upper(it.body))
  line(length: 100%, stroke: 0.5pt)
  v(0.25em)
}

#let section_card(title, body) = block[
  *#title*
  #body
]

= Document Title

== Section

- Keep content specific, factual, and reviewable.
- Move repeated formatting into helpers instead of copying layout blocks.
```

Working rules:

- Put document metadata, page geometry, text settings, paragraph/list spacing, link styling, and heading styling at the top.
- Prefer semantic helpers such as `#let role(...)`, `#let finding(...)`, `#let requirement(...)`, `#let decision(...)`, or `#let contact_block(...)` over manual repeated formatting.
- Keep helper names domain-neutral unless the repo's domain vocabulary is already stable.
- Use real Typst primitives first; add packages only when they remove substantial noise.
- For dense engineering tables, `@preview/tablex` can be useful, but verify package availability with a compile.
- Use one source file per final PDF unless there is a clear shared template module.
- Keep Markdown-like headings and bullets where possible so diffs stay readable.
- Avoid binary-only edits. If a PDF changes, there should be a corresponding `.typ` source change or documented rebuild reason.

## Document Families

### Resumes and Cover Letters

For career documents:

- Keep the master source of truth separate from tailored outputs.
- Copy layout rules from a known-good template, not from memory.
- Use stable filename conventions that encode candidate, organization, and role without spaces when the repo already has one.
- Keep contact/header blocks consistent across variants.
- Compile every tailored document after edits.
- Never invent metrics, dates, employers, titles, credentials, or contact details.

### Engineering Templates

For systems-engineering documents:

- Model repeated records as helpers: findings, requirements, risks, actions, interfaces, verification events, or trade options.
- Use stable IDs where review will reference rows later, e.g. `REQ-001`, `IF-001`, `RISK-001`, or `FIND-001`.
- Separate content from status metadata when practical: requirement text, owner, verification method, status, and rationale should be distinct fields.
- Make tables readable in PDF **and** reviewable in source; if a table becomes too wide, use landscape pages, smaller text in the table block, or split the table.
- Add a revision/history section for documents that will be reviewed repeatedly.

### Guides, Cheat Sheets, and Packets

For long-form guides:

- Define a compact page/header style once.
- Use consistent callouts for warnings, examples, decisions, and next actions.
- Add a table of contents only when it materially improves navigation.
- Break very long documents into clear sections with predictable heading levels.
- Compile early; layout problems get harder to debug after the document is full.

## Build Workflow

Prefer the repo's existing task runner if present:

```sh
just build
just watch
just clean
```

If no task runner exists, use direct Typst commands:

```sh
typst compile docs/report.typ docs/report.pdf
typst watch docs/report.typ docs/report.pdf
```

For multiple PDFs, add a deterministic build recipe instead of relying on ad hoc shell history:

```make
build:
    typst compile docs/report.typ docs/report.pdf
    typst compile docs/checklist.typ docs/checklist.pdf

watch:
    typst watch docs/report.typ docs/report.pdf

clean:
    rm -f docs/*.pdf
```

Keep the recipe simple. Do not add a custom generator until repeated source patterns prove that helpers or templates are insufficient.

## Validation

Before finalizing Typst work:

1. Run `typst --version` if the environment is unknown.
2. Run the narrow compile command or the repo's `just build`.
3. If compile fails, fix the first Typst diagnostic before making broad layout changes.
4. Inspect the changed source diff for accidental private content, stale placeholders, and broken links.
5. When a PDF is produced for review, verify that the PDF path exists and mention the compile command used.

Useful checks:

```sh
typst compile input.typ output.pdf
git diff -- '*.typ' ':(exclude)*.pdf'
git diff --check
```

## Output Contract

When completing a Typst document task, report:

- source file(s) changed or created
- generated PDF path(s), if any
- exact compile/build command run
- any remaining placeholders or user-supplied facts still needed
- whether generated PDFs were committed or left as local artifacts, following repo convention

## Common Pitfalls

- Copying private examples into a portable skill or public template.
- Editing only the PDF instead of the `.typ` source.
- Forgetting to compile after a small style change.
- Overusing packages for layout that Typst primitives can express clearly.
- Making tables visually dense but impossible to review in source.
- Letting resume variants drift in header/contact/link style.
- Hard-coding repo-specific names in reusable helpers.
- Treating generated PDFs as canonical when the source should drive review.
