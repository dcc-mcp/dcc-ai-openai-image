from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _openai_images import descriptor, output_format, save_base64_image


@skill_entry
def main(
    prompt: str,
    output_path: str,
    model: str = "gpt-image-2",
    size: str = "1024x1024",
    quality: str = "medium",
    **_: Any,
) -> dict[str, Any]:
    try:
        from openai import OpenAI  # Lazy import: optional network provider dependency.

        response = OpenAI().images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            output_format=output_format(output_path),
        )
        path = save_base64_image(response.data[0].b64_json, output_path)
        return skill_success("Texture source generated", file=path, asset_descriptor=descriptor(path, model, prompt))
    except Exception as exc:
        return skill_exception(exc, message="OpenAI texture generation failed")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

