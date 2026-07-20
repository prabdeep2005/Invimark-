import time
import urllib.request
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent / "models"
CDN = "https://cai-watermark.adobe.net/watermarking/trustmark-models"

FILES = {
    "encoder_Q.onnx": None,
    "decoder_Q.onnx": None,
}


def download_with_progress(url: str, dest: Path) -> None:
    start = time.time()
    last_time = start
    last_bytes = 0

    def hook(block_num: int, block_size: int, total_size: int) -> None:
        nonlocal last_time, last_bytes

        downloaded = block_num * block_size
        now = time.time()

        if now - last_time >= 0.3 or downloaded >= total_size:
            speed = (downloaded - last_bytes) / max(now - last_time, 0.001) / 1e6
            last_time = now
            last_bytes = downloaded

            if total_size > 0:
                percent = min(downloaded / total_size, 1.0)
                bar_len = 40
                filled = int(bar_len * percent)
                bar = "█" * filled + "░" * (bar_len - filled)

                mb_done = downloaded / 1e6
                mb_total = total_size / 1e6

                print(
                    f"\r  [{bar}] {percent * 100:5.1f}%  "
                    f"{mb_done:.1f}/{mb_total:.1f}MB  "
                    f"{speed:.1f}MB/s",
                    end="",
                    flush=True,
                )

    urllib.request.urlretrieve(url, dest, reporthook=hook)

    elapsed = time.time() - start
    avg_speed = dest.stat().st_size / 1e6 / elapsed

    print(
        f"\n  saved: {dest.name} "
        f"({dest.stat().st_size / 1e6:.1f}MB in {elapsed:.1f}s, "
        f"avg {avg_speed:.1f}MB/s)"
    )


def download() -> None:
    MODEL_DIR.mkdir(exist_ok=True)

    for name in FILES:
        dest = MODEL_DIR / name

        if dest.exists() and dest.stat().st_size > 0:
            print(f"  exists: {name}")
            continue

        print(f"  downloading: {name}")

        url = f"{CDN}/{name}"
        download_with_progress(url, dest)


if __name__ == "__main__":
    download()
    print("done")