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
