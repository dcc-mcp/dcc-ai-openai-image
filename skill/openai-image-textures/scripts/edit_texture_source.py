from __future__ import annotations

from contextlib import ExitStack
from pathlib import Path
from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _openai_images import descriptor, output_format, save_base64_image


@skill_entry
def main(
    input_path: str,
    prompt: str,
    output_path: str,
    mask_path: str | None = None,
    model: str = "gpt-image-2",
    **_: Any,
) -> dict[str, Any]:
    try:
        from openai import OpenAI  # Lazy import: optional network provider dependency.

        with ExitStack() as stack:
            image = stack.enter_context(Path(input_path).open("rb"))
            kwargs: dict[str, Any] = {
                "model": model,
                "image": image,
                "prompt": prompt,
                "output_format": output_format(output_path),
            }
            if mask_path:
                kwargs["mask"] = stack.enter_context(Path(mask_path).open("rb"))
            response = OpenAI().images.edit(**kwargs)
        path = save_base64_image(response.data[0].b64_json, output_path)
        return skill_success("Texture source edited", file=path, asset_descriptor=descriptor(path, model, prompt))
    except Exception as exc:
        return skill_exception(exc, message="OpenAI texture edit failed")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

