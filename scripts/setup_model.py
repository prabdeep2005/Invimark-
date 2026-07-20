import hashlib
from pdb import _Mode
import urllib.request
from pathlib import Path

MODEL_DIR = Path("__file__").parent.parent / "models"
CDN = "https://cai-watermark.adobe.net/watermarking/trustmark-models"

FILES = {
    "encoder_Q.onxx": None,
    "decoder_Q.onnx": None,
}

def download():
    _MODEL_DIR.mkdir(exist_ok=True)
    for name in FILES:
        dest = MODEL_DIR / name
        if dest.exist() and dest.stat().st_size > 0:
            print(f"exists:{name}")
            continue
        url = f"{CDN}/{name}"
        print(f"downloading:{name}")
        urllib.request.urlretrieve(url, dest)
        print(f"  saved: {dest} ({dest.stat().st_size/ 1e6:.1f})MB")
if__name__ == "__main__":
    download()
    print("done")