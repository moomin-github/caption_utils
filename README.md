# 画像タグ付け & キャプション処理ツール

これは、LoRA学習用データセット作成のためのユーティリティスクリプト集です。画像の自動タグ付けと、その後のキャプションファイルの整理を効率化します。

## 含まれるスクリプト

1.  **`tagging_wd14.py`**
    WD14 Tagger (v2) を使用して、画像からDanbooruタグを自動的に推論し、同名のテキストファイルとして保存します。
    信頼度（Threshold）によるフィルタリングも行います。

2.  **`caption_utils.py`**
    タグ付けされたテキストファイルに対して、以下の処理を一括で行います。
    *   トリガーワードの先頭への追加
    *   不要なタグ（`masterpiece`など）の削除
    *   重複タグの排除

## 必要要件

以下のPythonライブラリが必要です。

```bash
pip install opencv-python numpy pandas Pillow tqdm huggingface_hub onnxruntime
```
※ GPUを使用して高速化する場合は、`onnxruntime` の代わりに `onnxruntime-gpu` をインストールしてください。

## 使い方

### 1. 自動タグ付け (`tagging_wd14.py`)

1.  スクリプト `tagging_wd14.py` をテキストエディタで開きます。
2.  `設定エリア` の `IMAGE_DIR` を、対象の画像フォルダのパスに変更してください。
    ```python
    IMAGE_DIR = r"C:\Path\To\Your\Images"
    ```
    ※ 必要に応じて `THRESHOLD`（タグ採用のしきい値）も調整可能です（デフォルト 0.35）。
3.  スクリプトを実行します。
    ```bash
    python tagging_wd14.py
    ```

### 2. キャプションの整形 (`caption_utils.py`)

1.  スクリプト `caption_utils.py` をテキストエディタで開きます。
2.  `設定エリア` を変更します。
    ```python
    TARGET_DIR = "C:/Path/To/Your/Dataset"  # .txtファイルがあるフォルダ
    TRIGGER_WORD = "sks girl"               # 学習させたいトリガーワード
    ```
    ※ `WORDS_TO_REMOVE` リストを編集して、削除したいタグを追加・変更することもできます。
3.  スクリプトを実行します。
    ```bash
    python caption_utils.py
    ```

## 注意事項

*   スクリプト内のパスには、Windowsの場合でも `r"..."` を使うか、`/` (スラッシュ) を使用することをお勧めします。
*   `tagging_wd14.py` は初回実行時にモデルファイルをダウンロードするため、時間がかかる場合があります。
