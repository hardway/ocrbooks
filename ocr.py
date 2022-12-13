import os
import sys

if len(sys.argv)<2 :
    exit(f"Usage: python3 {sys.argv[0]} PDF")

pdf=sys.argv[1]

pages=os.popen(f"exiftool \"{pdf}\" | grep 'Page Count' | cut -f 2 -d:").read()
pages=int(pages);

from paddleocr import PaddleOCR
from ppocr.utils.logging import get_logger
get_logger().setLevel(40)

ocr = PaddleOCR(
        # use_angle_cls=True,
        # type='structure',
        lang="ch"
)  # need to run only once to download and load model into memory

for i in range(pages):
    print(f"\n---- page {i} ----\n")

    img_path = f"./c-{i}.jpg"

    if not os.path.exists(img_path):
        os.system(f"convert -density 300 {pdf}[{i}] {img_path}")

    result = ocr.ocr(img_path, cls=True)

    for line in result:
        print(line[1][0], flush=True)
