# Protocol Reference

## Project overview package

Use first for repository or folder analysis.

- Include the root path.
- Include a controlled-depth tree.
- Include file counts by suffix.
- Include key files and short summaries.
- Include read errors when they occur.

## File summary package

Use when the model needs detail before exact content.

- Include the full file path.
- Include type, size, line count, and encoding.
- Include a short preview.
- Include structure lines such as imports, functions, or headings.

## File page package

Use when the model asks for exact content.

- Include `FILE`.
- Include `PAGE`.
- Include `LINES`.
- Include `CHARS`.
- Include `TRUNCATED`.
- Wrap body text in `CONTENT-BEGIN` and `CONTENT-END`.

## Extracted text package

Use for PDF and Word files.

- Include source path and source type.
- Include success or failure.
- Include extracted text when available.
- Include a reason when extraction fails.
- State that the original binary was not sent.
