from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import os
import uuid
from pathlib import Path
from typing import Any
import urllib.request


SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "webp"}
API_BASE = "https://api.openai.com/v1"


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


def _headers(content_type: str) -> dict[str, str]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return {"Authorization": f"Bearer {key}", "Content-Type": content_type}


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(API_BASE + path, data=body, headers=_headers("application/json"), method="POST")
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def post_multipart(path: str, fields: dict[str, str], files: dict[str, str]) -> dict[str, Any]:
    boundary = f"dccmcp-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks += [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
        ]
    for name, file_path in files.items():
        source = Path(file_path).expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        mime = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
        chunks += [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{source.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode(),
            source.read_bytes(),
            b"\r\n",
        ]
    chunks.append(f"--{boundary}--\r\n".encode())
    content_type = f"multipart/form-data; boundary={boundary}"
    request = urllib.request.Request(API_BASE + path, data=b"".join(chunks), headers=_headers(content_type), method="POST")
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


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
