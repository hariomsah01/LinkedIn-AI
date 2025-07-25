import os
import cv2
import numpy as np
from rembg import remove
import uuid

def process_image(image_path: str) -> str:
    with open(image_path, "rb") as inp_file:
        input_data = inp_file.read()

    output_data = remove(input_data)
    bg_removed_path = f"{image_path}_nobg.png"
    with open(bg_removed_path, "wb") as out_file:
        out_file.write(output_data)

    result = apply_background(bg_removed_path)

    final_filename = f"{uuid.uuid4().hex}.png"
    output_path = f"app/static/processed/{final_filename}"
    cv2.imwrite(output_path, result)
    os.remove(bg_removed_path)
    return final_filename

def apply_background(fg_path: str) -> np.ndarray:
    fg = cv2.imread(fg_path, cv2.IMREAD_UNCHANGED)
    h, w = fg.shape[:2]
    background = np.full((h, w, 3), (230, 230, 240), dtype=np.uint8)
    if fg.shape[2] == 4:
        alpha = fg[:, :, 3] / 255.0
        for c in range(3):
            background[:, :, c] = (alpha * fg[:, :, c] + (1 - alpha) * background[:, :, c]).astype(np.uint8)
    else:
        background = fg[:, :, :3]
    return background
