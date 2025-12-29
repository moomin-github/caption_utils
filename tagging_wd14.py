import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from huggingface_hub import hf_hub_download
from onnxruntime import InferenceSession

# ==========================================
# 設定エリア
# ==========================================
IMAGE_DIR = r"D:\StabilityMatrix\Data\Packages\AI-Toolkit\datasets\dataset01" # 画像フォルダ
THRESHOLD = 0.35  # タグを抽出する信頼度（0.3~0.4が一般的）
# ==========================================

def load_model():
    print("Loading WD14 Tagger model...")
    # モデルとタグリストをHugging Faceからダウンロード
    model_path = hf_hub_download(repo_id="SmilingWolf/wd-v1-4-vit-tagger-v2", filename="model.onnx")
    tags_path = hf_hub_download(repo_id="SmilingWolf/wd-v1-4-vit-tagger-v2", filename="selected_tags.csv")
    
    session = InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    tags_df = pd.read_csv(tags_path)
    return session, tags_df

def preprocess_image(image, target_size=448):
    # 画像のリサイズと前処理
    image = image.convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1] # RGB to BGR
    
    # パディングして正方形に
    h, w = image.shape[:2]
    size = max(h, w)
    pad_h = (size - h) // 2
    pad_w = (size - w) // 2
    image = cv2.copyMakeBorder(image, pad_h, size - h - pad_h, pad_w, size - w - pad_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    image = cv2.resize(image, (target_size, target_size), interpolation=cv2.INTER_AREA)
    image = image.astype(np.float32)
    return np.expand_dims(image, axis=0)

def run():
    session, tags_df = load_model()
    
    # タグの分類
    tag_names = tags_df['name'].tolist()
    rating_indices = list(np.where(tags_df['category'] == 9)[0]) # 評価（一般、R18等）
    general_indices = list(np.where(tags_df['category'] == 0)[0]) # 一般的な特徴
    character_indices = list(np.where(tags_df['category'] == 4)[0]) # キャラ名

    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)]

    print(f"Processing {len(image_files)} images...")

    for filename in tqdm(image_files):
        img_path = os.path.join(IMAGE_DIR, filename)
        txt_path = os.path.splitext(img_path)[0] + ".txt"

        try:
            image = Image.open(img_path)
            input_data = preprocess_image(image)
            
            # 推論
            input_name = session.get_inputs()[0].name
            probs = session.run(None, {input_name: input_data})[0][0]

            # 信頼度以上のタグを抽出
            found_tags = []
            for i in general_indices + character_indices:
                if probs[i] > THRESHOLD:
                    name = tag_names[i].replace("_", " ") # アンダーバーをスペースに置換
                    found_tags.append(name)

            # 保存
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(", ".join(found_tags))
                
        except Exception as e:
            print(f"Error {filename}: {e}")

    print("Done! 全てのタグ付けが完了しました。")

if __name__ == "__main__":
    run()