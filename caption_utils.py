import os
import glob

# ==========================================
# 設定エリア
# ==========================================
TARGET_DIR = "path/to/your/dataset"  # .txtファイルがあるフォルダ
TRIGGER_WORD = "style_of_xyz"        # あなたの画風トリガーワード
WORDS_TO_REMOVE = [                  # 削除したいタグ（画風を説明しすぎているもの等）
    "masterpiece", "best quality", "score_9", "score_8_up", "score_7_up",
    "artist name", "sample watermark"
]
# ==========================================

def process_captions():
    files = glob.glob(os.path.join(TARGET_DIR, "*.txt"))
    
    if not files:
        print(f"エラー: {TARGET_DIR} に .txt ファイルが見つかりませんでした。")
        return

    print(f"{len(files)} 件のファイルを処理中...")

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # タグのリスト化（カンマ区切り想定）
        tags = [t.strip() for t in content.split(',') if t.strip()]

        # 1. 特定のワードを削除
        tags = [t for t in tags if t.lower() not in [w.lower() for w in WORDS_TO_REMOVE]]

        # 2. トリガーワードが先頭になければ追加
        if tags and tags[0] != TRIGGER_WORD:
            # 既存のトリガーがあれば削除して先頭へ（重複防止）
            if TRIGGER_WORD in tags:
                tags.remove(TRIGGER_WORD)
            tags.insert(0, TRIGGER_WORD)
        elif not tags:
            tags = [TRIGGER_WORD]

        # 3. 書き戻し
        new_content = ", ".join(tags)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print("処理が完了しました。")

if __name__ == "__main__":
    process_captions()