# 月薪喵

一只为 Codex 准备的动态猫猫终端宠物。这个仓库包含源 GIF、生成脚本、QA 预览文件，以及最终可安装到 Codex 的 `spritesheet.webp` 和 `pet.json`。

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

## 免责声明

本项目为个人学习、技术研究与非商业用途项目，仅用于探索 Codex 动态终端宠物素材的制作、打包与安装流程。

“月薪喵”相关形象、名称、梗图或动画灵感来源于网络流行内容，本项目并非官方项目，也未与相关原作者、权利方或平台存在任何商业合作、授权关系或背书关系。若你不了解“月薪喵”的来源，可自行搜索相关公开资料。

本项目不出售、不收费、不用于商业推广，也不主张对原始角色形象、表情包、GIF 或相关衍生内容拥有版权。仓库中生成的 `spritesheet.webp` 仅作为 Codex 宠物效果预览与个人使用示例。

如果本项目中的任何素材、名称、描述或衍生内容侵犯了你的合法权益，请通过 Issue 或仓库联系方式告知，我会尽快处理，包括但不限于修改说明、替换素材或删除相关内容。

## 仓库内容

```text
.
├── idle.gif / running.gif / ...       # 源动画 GIF
├── build_existing_gif_pet.py          # 从源 GIF 生成 Codex 宠物素材的脚本
├── hatch-coding-cat-gif/
│   ├── pet_request.json               # 宠物元信息
│   ├── final/
│   │   ├── spritesheet.webp           # 安装到 Codex 的最终素材
│   │   ├── pet.json                   # 安装到 Codex 的宠物配置
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
cp YueXinMiaoPet/hatch-coding-cat-gif/final/pet.json ~/.codex/pets/coding-cat-gif/pet.json
```

Windows 上的最终目录示例为 `C:\Users\admin\.codex\pets\coding-cat-gif`，目录内需要同时包含 `spritesheet.webp` 和 `pet.json` 两个文件。

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
   hatch-coding-cat-gif/final/pet.json
   ```

   复制后的路径应为：

   ```text
   ~/.codex/pets/coding-cat-gif/spritesheet.webp
   ~/.codex/pets/coding-cat-gif/pet.json
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
hatch-coding-cat-gif/final/pet.json
```

校验结果见：

```text
hatch-coding-cat-gif/final/validation.json
```

当前校验状态为通过：`ok: true`。
