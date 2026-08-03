"""
Genera los dos íconos PNG requeridos por Teams:
  - icon-color.png  → 192x192, violeta sólido
  - icon-outline.png → 32x32, gris sólido

No requiere dependencias externas (solo stdlib de Python).
"""

import struct
import zlib


def make_png(width: int, height: int, r: int, g: int, b: int) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))

    raw = b""
    for _ in range(height):
        raw += b"\x00" + bytes([r, g, b]) * width

    idat = chunk(b"IDAT", zlib.compress(raw, 9))
    iend = chunk(b"IEND", b"")
    return signature + ihdr + idat + iend


if __name__ == "__main__":
    import os

    out_dir = os.path.dirname(os.path.abspath(__file__))

    color_path = os.path.join(out_dir, "icon-color.png")
    with open(color_path, "wb") as f:
        f.write(make_png(192, 192, 124, 58, 237))  # violet-600
    print(f"Creado: {color_path}")

    outline_path = os.path.join(out_dir, "icon-outline.png")
    with open(outline_path, "wb") as f:
        f.write(make_png(32, 32, 124, 58, 237))
    print(f"Creado: {outline_path}")
