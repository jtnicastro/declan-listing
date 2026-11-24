"""Swap an edited photo set into Alana's page.

Usage: python3 tools/swap_in_edited.py <dir-with-edited> <n1> <n2> ...
Each edited file must be named declan-NN.jpg (NN = 01..14). The current
photos/full/declan-NN.jpg moves to photos/orig/ (and its thumb to
photos/thumb-orig/), the edited file becomes photos/full/declan-NN.jpg, and
HAS_EDIT is switched on for those photos in index.html.
"""
import sys, os, re, shutil
from PIL import Image

src, nums = sys.argv[1], [int(n) for n in sys.argv[2:]]
os.makedirs("photos/orig", exist_ok=True)
os.makedirs("photos/thumb-orig", exist_ok=True)
for n in nums:
    name = f"declan-{n:02d}.jpg"
    if not os.path.exists(f"photos/orig/{name}"):
        shutil.move(f"photos/full/{name}", f"photos/orig/{name}")
        shutil.move(f"photos/thumb/{name}", f"photos/thumb-orig/{name}")
    im = Image.open(os.path.join(src, name)).convert("RGB")
    im.save(f"photos/full/{name}", quality=92)
    t = im.copy(); t.thumbnail((640, 640), Image.LANCZOS); t.save(f"photos/thumb/{name}", quality=88)
    if n == 1:
        b = im.copy(); b.thumbnail((1600, 1600), Image.LANCZOS); b.save("photos/banner.jpg", quality=85)

html = open("index.html").read()
flags = ",".join("true" if (k + 1) in nums else "false" for k in range(15))
html = re.sub(r"const HAS_EDIT=[^;]*;", f"const HAS_EDIT=[{flags}];", html, count=1)
open("index.html", "w").write(html)
print("swapped", nums)
