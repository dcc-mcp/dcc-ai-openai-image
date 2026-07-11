from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from typing import Any


SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "webp"}


def output_format(path: str) -> str:
    suffix = Path(path).suffix.lower().lstrip(".")
    if suffix not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {suffix or '<missing>'}")
    return "jpeg" if suffix == "jpg" else suffix


def save_base64_image(encoded: str, output_path: str) -> str:
    target = Path(output_path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(base64.b64decode(encoded, validate=True))
    return str(target)


def descriptor(local_path: str, model: str, prompt: str) -> dict[str, Any]:
    from dcc_mcp_core.asset_import import AssetAttribution, AssetDescriptor, AssetFileVariant

    digest = hashlib.sha256(Path(local_path).read_bytes()).hexdigest()[:20]
    value = AssetDescriptor(
        asset_id=f"openai-image:{digest}",
        variants=[AssetFileVariant(local_path=local_path, format=output_format(local_path), preferred=True)],
        attribution=AssetAttribution(
            source_url="https://developers.openai.com/api/docs/guides/image-generation",
            license_text="Generated with the OpenAI API; usage is subject to the applicable OpenAI terms.",
            attribution_text=f"Generated with {model}.",
        ),
        extra={"model": model, "prompt": prompt},
    )
    value.validate()
    return value.to_dict()

