#!/usr/bin/env python3
"""
Generate Project Kinship thumbnail via OpenAI Images API.

Usage:
    source .venv/bin/activate
    python scripts/generate_thumbnail.py
    python scripts/generate_thumbnail.py --variant short --output assets/thumbnail.png

Requires OPENAI_API_KEY in .env
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

PRIMARY_PROMPT = """Warm cinematic illustration for a tech capstone project thumbnail, 16:9 aspect ratio.
A cozy modern home at golden hour — soft amber window light, dinner table with pasta in the background slightly blurred.
In the foreground, a child (age 10–12, diverse, hopeful expression) holds a phone or tablet showing a gentle glowing orb of warm light shaped like a heart, with subtle friendly AI particle aura in soft pink and sky blue (not robotic, not scary).
Two translucent warm parental presences suggested as soft light silhouettes — one nurturing (motherly warmth, rose gold tones), one supportive (fatherly warmth, calm blue tones) — embracing the scene like digital presence, not replacing real parents.
Small subtle holographic UI elements float delicately: a calendar icon, a dinner plate icon, a shield icon, a home icon — representing AI agents working quietly in the background.
Mood: emotional, trustworthy, human-first AI, family connection, warmth, safety, love.
Style: premium editorial illustration, Pixar-adjacent warmth meets modern tech, soft gradients, no harsh neon, no dystopia, no uncanny faces.
Color palette: warm cream, soft coral, rose gold, gentle sky blue, honey amber.
Leave clear negative space in the upper third for title text overlay.
No logos, no watermarks, no readable text in the image itself.
Highly polished, submission-ready."""

SHORT_PROMPT = """Cinematic warm family illustration, golden hour home interior, child smiling at glowing warm AI presence on phone — soft heart-shaped light, rose gold and sky blue, subtle agent icons (calendar, shield, home) floating gently. Two soft parental light silhouettes suggest Mommy and Daddy digital presence. Emotional, human-first AI, cozy, trustworthy. Upper area empty for text. Editorial illustration style, 16:9, no text, no robots, no dystopia."""

VARIANTS = {
    "primary": PRIMARY_PROMPT,
    "short": SHORT_PROMPT,
}


def generate_image(prompt: str, size: str, output_path: Path, model: str) -> Path:
    try:
        from openai import OpenAI
    except ImportError:
        print("Install openai: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your_"):
        print("Set OPENAI_API_KEY in .env before running.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Model:  {model}")
    print(f"Size:   {size}")
    print(f"Output: {output_path}")
    print("Generating…")

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url
    if not image_url:
        print("No image URL returned.", file=sys.stderr)
        sys.exit(1)

    import urllib.request

    urllib.request.urlretrieve(image_url, output_path)
    print(f"Saved: {output_path}")
    print()
    print("Add title overlay in Canva/Figma:")
    print('  Title:    "Hey Mommy .... Hi Dad"')
    print('  Subtitle: "Multi-Agent AI · Digital Parental Presence"')
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Project Kinship thumbnail")
    parser.add_argument(
        "--variant",
        choices=list(VARIANTS),
        default="primary",
        help="Prompt variant (default: primary)",
    )
    parser.add_argument(
        "--size",
        default="1792x1024",
        choices=["1024x1024", "1792x1024", "1024x1792"],
        help="DALL-E 3 size (1792x1024 ≈ 16:9)",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "assets" / "project_thumbnail.png"),
        help="Output file path",
    )
    parser.add_argument(
        "--model",
        default="dall-e-3",
        help="OpenAI image model",
    )
    args = parser.parse_args()

    prompt = VARIANTS[args.variant]
    generate_image(prompt, args.size, Path(args.output), args.model)


if __name__ == "__main__":
    main()
