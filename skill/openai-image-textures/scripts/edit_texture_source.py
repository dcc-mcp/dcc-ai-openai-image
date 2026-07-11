from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _openai_images import descriptor, output_format, post_multipart, save_base64_image


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
        files = {"image[]": input_path}
        if mask_path:
            files["mask"] = mask_path
        response = post_multipart("/images/edits", {
            "model": model,
            "prompt": prompt,
            "output_format": output_format(output_path),
        }, files)
        path = save_base64_image(response["data"][0]["b64_json"], output_path)
        return skill_success("Texture source edited", file=path, asset_descriptor=descriptor(path, model, prompt))
    except Exception as exc:
        return skill_exception(exc, message="OpenAI texture edit failed")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
