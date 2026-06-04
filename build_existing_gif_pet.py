#!/usr/bin/env python3
"""Build a Codex pet from the existing state GIFs in this folder."""

from __future__ import annotations

import json
import math
from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_WIDTH = 192
CELL_HEIGHT = 208
PET_ID = "coding-cat-gif"
DISPLAY_NAME = "Coding Cat GIF"
DESCRIPTION = "A larger smooth coding cat pet assembled from the existing GIF animations."
TARGET_WIDTH = 178
TARGET_HEIGHT = 188
MAX_UPSCALE = 1.50

STATE_SPECS = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
]


def color_distance(left: tuple[int, int, int], right: tuple[int, int, int]) -> float:
    return math.sqrt(sum((left[index] - right[index]) ** 2 for index in range(3)))


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    data = bytearray(rgba.tobytes())
    for index in range(0, len(data), 4):
        if data[index + 3] == 0:
            data[index] = 0
            data[index + 1] = 0
            data[index + 2] = 0
    return Image.frombytes("RGBA", rgba.size, bytes(data))


def load_gif(path: Path) -> tuple[list[Image.Image], list[int]]:
    with Image.open(path) as opened:
        frames: list[Image.Image] = []
        durations: list[int] = []
        for index in range(getattr(opened, "n_frames", 1)):
            opened.seek(index)
            frames.append(opened.convert("RGBA").copy())
            durations.append(int(opened.info.get("duration", 40) or 40))
    return frames, durations


def dominant_border_color(frames: list[Image.Image]) -> tuple[int, int, int]:
    samples: Counter[tuple[int, int, int]] = Counter()
    for frame in frames[: min(len(frames), 10)]:
        rgba = frame.convert("RGBA")
        width, height = rgba.size
        pixels = rgba.load()
        for x in range(width):
            for y in (0, height - 1):
                red, green, blue, alpha = pixels[x, y]
                if alpha:
                    samples[(red, green, blue)] += 1
        for y in range(height):
            for x in (0, width - 1):
                red, green, blue, alpha = pixels[x, y]
                if alpha:
                    samples[(red, green, blue)] += 1
    return samples.most_common(1)[0][0]


def opaque_background_candidate(frames: list[Image.Image]) -> bool:
    for frame in frames:
        alpha = frame.getchannel("A")
        if sum(alpha.histogram()[1:]) != frame.width * frame.height:
            return False
    return True


def seed_points(width: int, height: int, include_bottom: bool) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for x in range(width):
        points.append((x, 0))
        if include_bottom:
            points.append((x, height - 1))
    for y in range(height):
        points.append((0, y))
        points.append((width - 1, y))
    return points


def remove_connected_background(
    image: Image.Image,
    background: tuple[int, int, int],
    *,
    include_bottom: bool,
    threshold: float = 18.0,
) -> tuple[Image.Image, int]:
    """Remove only background-colored pixels connected to trusted image borders."""

    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        red, green, blue, alpha = pixels[x, y]
        return alpha > 0 and color_distance((red, green, blue), background) <= threshold

    for x, y in seed_points(width, height, include_bottom):
        index = y * width + x
        if not visited[index] and is_background(x, y):
            visited[index] = 1
            queue.append((x, y))

    removed = 0
    while queue:
        x, y = queue.popleft()
        red, green, blue, _alpha = pixels[x, y]
        pixels[x, y] = (0, 0, 0, 0)
        removed += 1
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            index = ny * width + nx
            if visited[index] or not is_background(nx, ny):
                continue
            visited[index] = 1
            queue.append((nx, ny))

    return clear_transparent_rgb(rgba), removed


def sample_indices(durations: list[int], count: int) -> list[int]:
    total = sum(max(1, duration) for duration in durations)
    starts: list[int] = []
    elapsed = 0
    for duration in durations:
        starts.append(elapsed)
        elapsed += max(1, duration)

    indices: list[int] = []
    for slot in range(count):
        target = slot * total / count
        index = max(0, min(len(starts) - 1, len(starts) - 1))
        for candidate, start in enumerate(starts):
            end = starts[candidate + 1] if candidate + 1 < len(starts) else total
            if start <= target < end:
                index = candidate
                break
        indices.append(index)
    return indices


def union_bbox(frames: list[Image.Image]) -> tuple[int, int, int, int]:
    boxes = [frame.getbbox() for frame in frames]
    boxes = [box for box in boxes if box is not None]
    if not boxes:
        return (0, 0, 1, 1)
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def normalize_row_frames(frames: list[Image.Image]) -> tuple[list[Image.Image], dict[str, object]]:
    crop_box = union_bbox(frames)
    crop_width = max(1, crop_box[2] - crop_box[0])
    crop_height = max(1, crop_box[3] - crop_box[1])
    scale = min(TARGET_WIDTH / crop_width, TARGET_HEIGHT / crop_height, MAX_UPSCALE)
    out_width = max(1, round(crop_width * scale))
    out_height = max(1, round(crop_height * scale))

    outputs: list[Image.Image] = []
    for frame in frames:
        cropped = frame.crop(crop_box)
        resized = cropped.resize((out_width, out_height), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
        left = (CELL_WIDTH - out_width) // 2
        top = (CELL_HEIGHT - out_height) // 2
        cell.alpha_composite(clear_transparent_rgb(resized), (left, top))
        outputs.append(clear_transparent_rgb(cell))

    return outputs, {
        "crop_box": list(crop_box),
        "scale": scale,
        "output_viewport": [out_width, out_height],
    }


def checker(size: tuple[int, int], square: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (250, 250, 250, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if ((x // square) + (y // square)) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill=(225, 225, 225, 255))
    return image


def composite_thumbnail(frame: Image.Image, size: tuple[int, int]) -> Image.Image:
    bg = checker(size)
    sprite = frame.copy()
    bbox = sprite.getbbox()
    if bbox:
        sprite = sprite.crop(bbox)
        sprite.thumbnail((size[0] - 12, size[1] - 12), Image.Resampling.LANCZOS)
        bg.alpha_composite(sprite, ((size[0] - sprite.width) // 2, (size[1] - sprite.height) // 2))
    return bg


def make_cutout_check(
    output: Path,
    records: list[dict[str, object]],
    originals: dict[str, list[Image.Image]],
    processed: dict[str, list[Image.Image]],
) -> None:
    check_records = [record for record in records if record.get("background_removed")]
    check_states = [record["state"] for record in check_records]
    if not check_states:
        return

    thumb_w, thumb_h = 150, 150
    columns = 4
    row_h = 24 + thumb_h * 2
    sheet = Image.new("RGB", (columns * thumb_w, len(check_states) * row_h), "#ffffff")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, record in enumerate(check_records):
        state = str(record["state"])
        source_frames = originals[state]
        final_frames = processed[state]
        samples = list(record.get("sampled_indices", []))
        if len(samples) < columns:
            samples = sample_indices([40] * len(source_frames), columns)
        for col, index in enumerate(samples[:columns]):
            x = col * thumb_w
            y = row * row_h
            draw.text((x + 4, y + 4), f"{state} #{index}", fill="#111111", font=font)
            before = composite_thumbnail(source_frames[index], (thumb_w, thumb_h)).convert("RGB")
            after = composite_thumbnail(final_frames[col], (thumb_w, thumb_h)).convert("RGB")
            sheet.paste(before, (x, y + 24))
            sheet.paste(after, (x, y + 24 + thumb_h))
            draw.rectangle((x, y + 24, x + thumb_w - 1, y + 24 + thumb_h - 1), outline="#999999")
            draw.rectangle(
                (x, y + 24 + thumb_h, x + thumb_w - 1, y + 24 + thumb_h * 2 - 1),
                outline="#18a058",
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def make_motion_filmstrip(frames_root: Path, output: Path) -> None:
    thumb_w, thumb_h = 120, 130
    label_h = 22
    sheet = Image.new(
        "RGB",
        (8 * thumb_w, len(STATE_SPECS) * (thumb_h + label_h)),
        "#f8f8f8",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, (state, count) in enumerate(STATE_SPECS):
        y = row * (thumb_h + label_h)
        draw.rectangle((0, y, 8 * thumb_w, y + label_h - 1), fill="#111111")
        draw.text((6, y + 5), f"{state} ({count})", fill="#ffffff", font=font)
        for col in range(8):
            x = col * thumb_w
            bg = checker((thumb_w, thumb_h))
            if col < count:
                with Image.open(frames_root / state / f"{col:02d}.png") as opened:
                    frame = opened.convert("RGBA")
                preview = frame.copy()
                preview.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
                bg.alpha_composite(preview, ((thumb_w - preview.width) // 2, (thumb_h - preview.height) // 2))
            sheet.paste(bg.convert("RGB"), (x, y + label_h))
            draw.rectangle((x, y + label_h, x + thumb_w - 1, y + label_h + thumb_h - 1), outline="#d0d0d0")
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def main() -> None:
    root = Path(__file__).resolve().parent
    run_dir = root / "hatch-coding-cat-gif"
    frames_root = run_dir / "frames"
    qa_dir = run_dir / "qa"
    frames_root.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    manifest_rows: list[dict[str, object]] = []
    originals_by_state: dict[str, list[Image.Image]] = {}
    final_by_state: dict[str, list[Image.Image]] = {}

    for state, expected_count in STATE_SPECS:
        source_path = root / f"{state}.gif"
        if not source_path.is_file():
            raise SystemExit(f"missing source GIF: {source_path}")

        raw_frames, durations = load_gif(source_path)
        originals_by_state[state] = [frame.copy() for frame in raw_frames]
        background_removed = False
        removed_counts: list[int] = []
        background_color: tuple[int, int, int] | None = None

        if opaque_background_candidate(raw_frames):
            background_color = dominant_border_color(raw_frames)
            include_bottom = state != "waving"
            processed_frames = []
            for frame in raw_frames:
                processed, removed = remove_connected_background(
                    frame,
                    background_color,
                    include_bottom=include_bottom,
                )
                processed_frames.append(processed)
                removed_counts.append(removed)
            raw_frames = processed_frames
            background_removed = True
        else:
            raw_frames = [clear_transparent_rgb(frame) for frame in raw_frames]

        indices = sample_indices(durations, expected_count)
        sampled = [raw_frames[index] for index in indices]
        normalized, row_info = normalize_row_frames(sampled)
        final_by_state[state] = normalized

        state_dir = frames_root / state
        state_dir.mkdir(parents=True, exist_ok=True)
        for old in state_dir.glob("*.png"):
            old.unlink()
        outputs = []
        for index, frame in enumerate(normalized):
            out = state_dir / f"{index:02d}.png"
            frame.save(out)
            outputs.append(str(out))

        record = {
            "state": state,
            "source": str(source_path),
            "source_frames": len(raw_frames),
            "sampled_indices": indices,
            "expected_frames": expected_count,
            "source_durations_ms": sorted(set(durations)),
            "background_removed": background_removed,
            "background_color": list(background_color) if background_color else None,
            "removed_background_pixels_minmax": [min(removed_counts), max(removed_counts)] if removed_counts else None,
            **row_info,
        }
        records.append(record)
        manifest_rows.append({"state": state, "frames": outputs, "source_gif": str(source_path)})

    pet_request = {
        "pet_id": PET_ID,
        "display_name": DISPLAY_NAME,
        "description": DESCRIPTION,
        "source": "existing state GIFs",
        "cell": {"width": CELL_WIDTH, "height": CELL_HEIGHT},
        "chroma_key": {"hex": "#00FF00", "rgb": [0, 255, 0]},
        "notes": [
            "Opaque white-background GIFs were cut out with border-connected background removal only.",
            "Per-state frames were sampled by GIF timing and scaled to be a little larger inside each 192x208 cell.",
        ],
    }
    (run_dir / "pet_request.json").write_text(json.dumps(pet_request, indent=2) + "\n", encoding="utf-8")
    (frames_root / "frames-manifest.json").write_text(
        json.dumps(
            {
                "ok": True,
                "source": "existing GIF timing samples",
                "chroma_key": {"hex": "#00FF00", "rgb": [0, 255, 0], "threshold": 0},
                "rows": manifest_rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (qa_dir / "existing-gif-build-summary.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    make_cutout_check(qa_dir / "cutout-check.png", records, originals_by_state, final_by_state)
    make_motion_filmstrip(frames_root, qa_dir / "motion-filmstrip.png")
    print(json.dumps({"ok": True, "run_dir": str(run_dir), "frames_root": str(frames_root)}, indent=2))


if __name__ == "__main__":
    main()
