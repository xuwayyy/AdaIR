import os
import shutil
from PIL import Image

# 数据集根目录
root = r"D:\Reproduce\AdaIR\data\All-In-One-Remote\UCMerced"

# 超分倍率
factor = 4

for split in ["train", "test"]:
    split_dir = os.path.join(root, split)

    # 输出目录
    hr_dir = os.path.join(split_dir, "HR")
    lr_dir = os.path.join(split_dir, "LR_Bicubic", f"x{factor}")

    os.makedirs(hr_dir, exist_ok=True)
    os.makedirs(lr_dir, exist_ok=True)

    # 遍历 train/test 下的 tif 图片
    for filename in os.listdir(split_dir):
        file_path = os.path.join(split_dir, filename)

        # 只处理 tif/tiff 文件
        if not os.path.isfile(file_path):
            continue

        if not filename.lower().endswith((".tif", ".tiff")):
            continue

        # =========================
        # 1. HR：复制原图
        # =========================
        hr_path = os.path.join(hr_dir, filename)
        shutil.copy2(file_path, hr_path)

        # =========================
        # 2. LR：Bicubic 下采样 x4
        # =========================
        with Image.open(file_path) as img:

            # 如果是多页 TIFF，只处理第一页
            img = img.copy()

            width, height = img.size

            new_width = width // factor
            new_height = height // factor

            lr_img = img.resize(
                (new_width, new_height),
                Image.Resampling.BICUBIC
            )

            # 文件名添加 x4
            name, ext = os.path.splitext(filename)
            lr_filename = f"{name}x{factor}{ext}"

            lr_path = os.path.join(lr_dir, lr_filename)

            # 保存为 TIFF
            lr_img.save(lr_path)

        print(f"[{split}] {filename} -> {lr_filename}")

print("\n处理完成！")