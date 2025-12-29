# Caption Utils & Auto Tagger

画像生成AIの学習データセット作成を支援するユーティリティスクリプト集です。
画像の自動タグ付けと、キャプションファイルの加工（トリガーワードの追加、不要なタグの削除）を行います。

## 機能

1.  **`tagging_wd14.py`**: WD14 Tagger モデルを使用して、指定したフォルダ内の画像に自動でタグ付けを行い、同名の `.txt` ファイルを生成します。
2.  **`caption_utils.py`**: 生成されたキャプションファイル (`.txt`) を一括処理します。
    *   特定のタグ（クオリティタグなど）の削除
    *   トリガーワードの先頭への追加

## 環境構築

### 必要条件

*   Python 3.10 以上 (推奨)
*   CUDA対応GPU (推奨。`onnxruntime-gpu` を使用するため)

### インストール手順

1.  リポジトリをクローンまたはダウンロードします。
2.  PowerShellなどでフォルダを開き、以下のコマンドを実行して仮想環境を作成し、依存ライブラリをインストールします。

```powershell
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 依存ライブラリのインストール
pip install -r requirements.txt
```

## 使い方

スクリプトを使用する前に、各ファイルの「設定エリア」を編集して、対象フォルダやパラメータを指定してください。

### 1. タグ付け (`tagging_wd14.py`)

画像フォルダ内の画像（.jpg, .png, .webpなど）に対してタグ付けを行います。

1.  `tagging_wd14.py` をテキストエディタで開きます。
2.  以下の設定項目を変更します。
    ```python
    IMAGE_DIR = r"D:\path\to\images"  # 画像があるフォルダのパス
    THRESHOLD = 0.35                  # タグ採用の閾値 (0.35前後が推奨)
    ```
3.  実行します。
    ```powershell
    python tagging_wd14.py
    ```
4.  画像と同じフォルダに `.txt` ファイルが生成されます。

### 2. キャプションの加工 (`caption_utils.py`)

タグ付けされた `.txt` ファイルを整理します。

1.  `caption_utils.py` をテキストエディタで開きます。
2.  以下の設定項目を変更します。
    ```python
    TARGET_DIR = "path/to/dataset"       # .txtファイルがあるフォルダ
    TRIGGER_WORD = "my_lora_trigger"     # 追加したいトリガーワード
    WORDS_TO_REMOVE = [ ... ]            # 削除したいタグのリスト
    ```
3.  実行します。
    ```powershell
    python caption_utils.py
    ```
4.  対象フォルダ内のすべての `.txt` ファイルが更新されます。
