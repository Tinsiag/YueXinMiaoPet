# YueXinMiaoPet README and GitHub Upload Design

Date: 2026-06-04

## Goal

Create a clear Chinese README for the YueXinMiaoPet / Coding Cat GIF Codex pet project, show the pet animation effects, explain how to install the pet into Codex, and upload all current project files to `https://github.com/Tinsiag/YueXinMiaoPet.git`.

## Scope

Include all files currently under `C:\Users\Tinsiag\Desktop\gif` in the GitHub repository, including:

- Source GIF files in the project root.
- `build_existing_gif_pet.py` generation script.
- `hatch-coding-cat-gif/` generated package, QA previews, validation files, and final spritesheet.
- The new `README.md`.
- This design spec.

## README Structure

The README will be written primarily in Chinese and include:

1. Project title and short description.
2. Effect showcase using the existing source GIFs so GitHub renders animated previews.
3. File structure overview.
4. Codex installation instructions with both:
   - Quick install commands using `git clone`, `mkdir`, and `cp`.
   - Manual install steps for users who download the ZIP.
5. Usage/activation note explaining that Codex reads user data from `~/.codex` by default and that `CODEX_HOME` can override it.
6. Regeneration instructions for running `python build_existing_gif_pet.py`.
7. QA/validation summary referencing `hatch-coding-cat-gif/final/validation.json`.

## Installation Design

The README will install the final spritesheet into:

```text
~/.codex/pets/coding-cat-gif/spritesheet.webp
```

The quick install command will clone this GitHub repository, create the target pet directory, and copy `hatch-coding-cat-gif/final/spritesheet.webp` there. Manual installation will describe the same operation step by step.

## Upload Design

Because the current folder is not yet a git repository, implementation will:

1. Initialize git in `C:\Users\Tinsiag\Desktop\gif`.
2. Add remote `origin` pointing to `https://github.com/Tinsiag/YueXinMiaoPet.git`.
3. Stage all project files.
4. Commit with a concise message.
5. Push the branch to GitHub.

Pushing changes affects a remote repository, so it should only be done after the user approves the plan and any required authentication is available.

## Validation

Before claiming completion, implementation should verify:

- `README.md` exists and references existing files.
- Git status is clean after commit/push, or any remaining changes are explained.
- The remote URL is configured correctly.
- Push succeeds, or the user is told what authentication/action is needed.
