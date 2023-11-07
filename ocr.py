import os
import sys
import pypdfium2 as pdfium

if len(sys.argv)<2 :
    exit(f"Usage: python3 {sys.argv[0]} PDF")

# 打开PDF
print(f"Opening PDF: {sys.argv[1]}")
pdf = pdfium.PdfDocument(sys.argv[1])
pages=len(pdf)

# 加载Paddle OCR
print(f"Loading OCR Engine ...");
from paddleocr import PaddleOCR
from ppocr.utils.logging import get_logger
get_logger().setLevel(40)

ocr = PaddleOCR(
        # use_angle_cls=True,
        # type='structure',
        lang="ch"
)  # need to run only once to download and load model into memory

# 逐页识别
for i in range(pages):
    print(f"\n---- page {i} ----\n")

    img_path = f"./c-{i}.jpg"

    if not os.path.exists(img_path):
        pdf[i].render(scale = 600/72).to_pil().save(img_path)

    result = ocr.ocr(img_path, cls=True)

    for line in result:
        print(line[1][0], flush=True)
