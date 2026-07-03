"""
이미지를 rows x cols 격자로 분할하는 스크립트

사용법:
    python split_image.py sheet.png --rows 4 --cols 4
    python split_image.py sheet.png --rows 3 --cols 5 --outdir out --prefix hs
    # 결과: hs0.png, hs1.png, hs2.png, ... (왼쪽→오른쪽, 위→아래 순)
"""

import argparse
from pathlib import Path

from PIL import Image


def split_image(image_path: str, rows: int, cols: int, outdir: str = "output", prefix: str = "tile") -> list[Path]:
    img = Image.open(image_path)
    out_dir = Path(outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 나눗셈이 딱 떨어지지 않아도 자투리 픽셀이 버려지지 않도록
    # 각 셀의 경계를 미리 계산해둔다.
    x_bounds = [round(img.width * c / cols) for c in range(cols + 1)]
    y_bounds = [round(img.height * r / rows) for r in range(rows + 1)]

    saved_paths = []
    for y in range(rows):
        for x in range(cols):
            box = (x_bounds[x], y_bounds[y], x_bounds[x + 1], y_bounds[y + 1])
            crop = img.crop(box)
            index = y * cols + x
            save_path = out_dir / f"{prefix}{index}.png"
            crop.save(save_path)
            saved_paths.append(save_path)

    return saved_paths


def main():
    parser = argparse.ArgumentParser(description="이미지를 격자 형태로 분할합니다.")
    parser.add_argument("image", help="분할할 이미지 파일 경로")
    parser.add_argument("--rows", type=int, required=True, help="세로 분할 개수")
    parser.add_argument("--cols", type=int, required=True, help="가로 분할 개수")
    parser.add_argument("--outdir", default="output", help="결과 저장 폴더 (기본: output)")
    parser.add_argument("--prefix", default="tile", help="저장 파일명 접두사 (기본: tile)")
    args = parser.parse_args()

    paths = split_image(args.image, args.rows, args.cols, args.outdir, args.prefix)
    print(f"{len(paths)}개 조각을 '{args.outdir}' 폴더에 저장했습니다.")


if __name__ == "__main__":
    main()