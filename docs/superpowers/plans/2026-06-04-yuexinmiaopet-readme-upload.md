# YueXinMiaoPet README and Upload Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Chinese README for the Codex pet, verify it references existing assets, initialize git, commit every project file, and push to `https://github.com/Tinsiag/YueXinMiaoPet.git`.

**Architecture:** This is a documentation-and-repository setup task. The README is the user-facing entry point; existing GIF assets and generated Codex pet files remain unchanged. Git initialization/upload is performed after README verification so the repository contains a coherent first commit.

**Tech Stack:** Markdown, Git, Bash shell commands, existing Python/Pillow generation script.

---

## File Structure

- Create: `README.md`
  - Chinese project overview, animated previews, install commands, manual install steps, file structure, regeneration and validation notes.
- Existing: `idle.gif`, `running.gif`, `running-left.gif`, `running-right.gif`, `waving.gif`, `jumping.gif`, `waiting.gif`, `failed.gif`, `review.gif`
  - Source GIF files displayed by the README and uploaded unchanged.
- Existing: `build_existing_gif_pet.py`
  - Generation script referenced by the README and uploaded unchanged.
- Existing: `hatch-coding-cat-gif/final/spritesheet.webp`
  - Final Codex pet spritesheet referenced by install instructions and uploaded unchanged.
- Existing: `hatch-coding-cat-gif/final/validation.json`
  - Validation result referenced by the README and uploaded unchanged.
- Existing: `hatch-coding-cat-gif/qa/**`
  - QA previews/reports uploaded unchanged.
- Existing: `docs/superpowers/specs/2026-06-04-yuexinmiaopet-readme-upload-design.md`
  - Approved design spec uploaded with the repository.
- Existing: `docs/superpowers/plans/2026-06-04-yuexinmiaopet-readme-upload.md`
  - This implementation plan uploaded with the repository.

## Task 1: Create README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md**

Create `README.md` with this exact content:

```markdown
# YueXinMiaoPet / Coding Cat GIF

一只为 Codex 准备的动态猫猫终端宠物。这个仓库包含源 GIF、生成脚本、QA 预览文件，以及最终可安装到 Codex 的 `spritesheet.webp`。

## 效果展示

| 状态 | 预览 |
| --- | --- |
| Idle | ![idle](idle.gif) |
| Running | ![running](running.gif) |
| Running Left | ![running-left](running-left.gif) |
| Running Right | ![running-right](running-right.gif) |
| Waving | ![waving](waving.gif) |
| Jumping | ![jumping](jumping.gif) |
| Waiting | ![waiting](waiting.gif) |
| Failed | ![failed](failed.gif) |
| Review | ![review](review.gif) |

## 仓库内容

```text
.
├── idle.gif / running.gif / ...       # 源动画 GIF
├── build_existing_gif_pet.py          # 从源 GIF 生成 Codex 宠物素材的脚本
├── hatch-coding-cat-gif/
│   ├── pet_request.json               # 宠物元信息
│   ├── final/
│   │   ├── spritesheet.webp           # 安装到 Codex 的最终素材
│   │   └── validation.json            # 最终素材校验结果
│   └── qa/                            # QA 预览、动效检查和报告
└── docs/superpowers/                  # 设计与实施记录
```

## 安装到 Codex

Codex 默认使用 `~/.codex` 作为用户数据目录；如果你设置了 `CODEX_HOME`，请把下面命令里的 `~/.codex` 替换成你的 `CODEX_HOME` 路径。

### 快速安装

```bash
git clone https://github.com/Tinsiag/YueXinMiaoPet.git
mkdir -p ~/.codex/pets/coding-cat-gif
cp YueXinMiaoPet/hatch-coding-cat-gif/final/spritesheet.webp ~/.codex/pets/coding-cat-gif/spritesheet.webp
```

### 手动安装

1. 打开仓库页面：`https://github.com/Tinsiag/YueXinMiaoPet`
2. 点击 **Code** → **Download ZIP**，下载并解压。
3. 创建 Codex 宠物目录：

   ```bash
   mkdir -p ~/.codex/pets/coding-cat-gif
   ```

4. 将下面文件复制过去：

   ```text
   hatch-coding-cat-gif/final/spritesheet.webp
   ```

   复制后的路径应为：

   ```text
   ~/.codex/pets/coding-cat-gif/spritesheet.webp
   ```

5. 重新打开 Codex，选择或启用 `coding-cat-gif` 宠物。

## 重新生成素材

如果你修改了源 GIF，可以重新运行生成脚本：

```bash
python build_existing_gif_pet.py
```

脚本会重新生成 `hatch-coding-cat-gif/final/spritesheet.webp`，并更新 QA/校验文件。

## 校验信息

当前最终素材位于：

```text
hatch-coding-cat-gif/final/spritesheet.webp
```

校验结果见：

```text
hatch-coding-cat-gif/final/validation.json
```

当前校验状态为通过：`ok: true`。
```

- [ ] **Step 2: Verify README references existing files**

Run:

```bash
test -f README.md && test -f idle.gif && test -f running.gif && test -f running-left.gif && test -f running-right.gif && test -f waving.gif && test -f jumping.gif && test -f waiting.gif && test -f failed.gif && test -f review.gif && test -f hatch-coding-cat-gif/final/spritesheet.webp && test -f hatch-coding-cat-gif/final/validation.json
```

Expected: command exits with status 0 and no output.

## Task 2: Initialize Git Repository

**Files:**
- Modify/create: `.git/` internal git metadata

- [ ] **Step 1: Initialize git if needed**

Run:

```bash
git status --short || git init
```

Expected:
- If the directory is already a git repository, `git status --short` prints status.
- If not, `git init` initializes a repository.

- [ ] **Step 2: Configure remote origin**

Run:

```bash
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin https://github.com/Tinsiag/YueXinMiaoPet.git
else
  git remote add origin https://github.com/Tinsiag/YueXinMiaoPet.git
fi
git remote -v
```

Expected: output contains both fetch and push URLs for `https://github.com/Tinsiag/YueXinMiaoPet.git`.

- [ ] **Step 3: Set default branch name**

Run:

```bash
git branch -M main
```

Expected: command exits with status 0 and no output.

## Task 3: Commit All Files

**Files:**
- Stage/commit: all files in `C:\Users\Tinsiag\Desktop\gif`

- [ ] **Step 1: Review working tree before staging**

Run:

```bash
git status --short
```

Expected: output lists untracked project files including `README.md`, GIF files, `build_existing_gif_pet.py`, `hatch-coding-cat-gif/`, and `docs/`.

- [ ] **Step 2: Stage all project files**

Run:

```bash
git add README.md idle.gif running.gif running-left.gif running-right.gif waving.gif jumping.gif waiting.gif failed.gif review.gif build_existing_gif_pet.py hatch-coding-cat-gif docs
```

Expected: command exits with status 0 and no output.

- [ ] **Step 3: Verify staged files**

Run:

```bash
git status --short
```

Expected: listed files are staged with `A` status.

- [ ] **Step 4: Commit staged files**

Run:

```bash
git commit -m "$(cat <<'EOF'
Add Coding Cat GIF Codex pet

Add the generated Codex pet assets, source GIFs, README installation instructions, and design/implementation notes for YueXinMiaoPet.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds and prints a new commit hash.

## Task 4: Push to GitHub

**Files:**
- Remote repository: `https://github.com/Tinsiag/YueXinMiaoPet.git`

- [ ] **Step 1: Push main branch**

Run:

```bash
git push -u origin main
```

Expected: push succeeds. If GitHub authentication is required, git prompts or fails with an authentication message; the user should authenticate and rerun the command.

- [ ] **Step 2: Verify clean status**

Run:

```bash
git status --short
git remote -v
```

Expected:
- `git status --short` prints no file changes.
- `git remote -v` shows `origin` pointing to `https://github.com/Tinsiag/YueXinMiaoPet.git`.

## Self-Review

- Spec coverage: README creation, effect showcase, Codex quick/manual installation, all-file upload, git initialization, commit, push, and validation are covered.
- Placeholder scan: no TBD/TODO/fill-in-later placeholders are present.
- Type/command consistency: file paths and remote URL match the approved spec.
