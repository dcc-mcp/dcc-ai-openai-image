import base64
import importlib.util
from pathlib import Path


MODULE = Path(__file__).parents[1] / "skill/openai-image-textures/scripts/_openai_images.py"
SPEC = importlib.util.spec_from_file_location("_openai_images", MODULE)
images = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(images)


def test_save_and_format(tmp_path):
    target = tmp_path / "texture.png"
    assert images.output_format(str(target)) == "png"
    assert Path(images.save_base64_image(base64.b64encode(b"image").decode(), str(target))).read_bytes() == b"image"


def test_rejects_unknown_format():
    try:
        images.output_format("texture.tga")
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("unknown formats must fail")
