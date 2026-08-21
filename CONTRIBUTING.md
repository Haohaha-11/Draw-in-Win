# Contributing

Thank you for improving Draw-in-Win. The repository is most useful when every visualization is easy to discover, visually inspect, and reproduce.

## Before opening a pull request

1. Put new work in the closest existing collection or explain why a new collection is needed.
2. Use repository-relative paths based on `pathlib.Path(__file__)`; never commit a user profile or drive-specific absolute path.
3. Keep sample data small, documented, and suitable for redistribution.
4. Export at least one 300-DPI PNG preview. Prefer SVG for editable artwork and add PDF when it supports a publication workflow.
5. Do not commit proprietary fonts, credentials, virtual environments, model caches, or editor metadata.
6. Run `python tools/check_repository.py` and execute the affected visualization in a clean environment.

## Style guidance

- Give axes explicit labels and include units where applicable.
- Use color palettes that remain legible when printed and, where practical, for viewers with color-vision deficiencies.
- Keep text readable at the final publication size.
- Seed random generators when randomness is only used to construct an example.
- Avoid calling `plt.show()` before `savefig`, because some backends clear or block the figure.
- Prefer functions and a guarded `if __name__ == "__main__":` entry point for new scripts.

## Data and provenance

Document where data comes from, what each column means, and whether it is observed, simulated, or transformed. Never submit private, licensed, or personally identifying data without explicit redistribution rights.

## Pull request description

Include:

- the chart family and intended use;
- the script and data paths;
- a representative preview;
- commands used for validation;
- known limitations or external data requirements.
