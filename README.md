# YouTube Comment Scraper

YouTubeの複数の動画から自動的にコメントを収集し、CSVファイルに保存するPythonスクリプトです。

## 概要

![pinterest_profile_image](https://github.com/fk009/Collect_YouTube_comments_in_Firefox/raw/main/images/ss_img_1.png)


このプログラムは、指定されたYouTube動画のURLリストからコメントを自動取得し、動画ごとに整理されたCSVファイルとして出力します。SeleniumとFirefoxブラウザを使用して、人間らしいスクロール動作を模擬しながらコメントを収集します。

## 主な機能

- 複数のYouTube動画URLからの一括コメント取得
- 動画タイトル名でのCSVファイル自動生成
- 人間らしいランダムスクロール機能
- ファイル名に使用できない特殊文字の自動変換
- 各動画最大700件のコメント取得（設定可能）

## 必要な環境

### システム要件
- Python 3.6以上
- Mozilla Firefox ブラウザ
- Windows OS（パス設定がWindows向け）

### 必要なPythonライブラリ
```bash
pip install selenium
```

### 追加ソフトウェア
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases)をダウンロードし、適切な場所に配置

## セットアップ

1. **GeckoDriverの設定**
   - GeckoDriverをダウンロードし、任意のフォルダに展開
   - スクリプト内の`gecko_path`変数を実際のパスに変更
   ```python
   gecko_path = 'F:/geckodriver-v0.34.0-win32/geckodriver.exe'
   ```

2. **Firefoxの設定**
   - Firefoxがデフォルトの場所にインストールされていない場合、`binary_location`を調整
   ```python
   options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
   ```

3. **フォルダ構成**
   ```
   プロジェクトフォルダ/
   ├── youtube_comment_scraper.py
   ├── youtube_URL.txt
   └── TEXT_folder/（自動生成される）
   ```

## 使用方法

1. **URLリストの準備**
   - プロジェクトフォルダに`youtube_URL.txt`ファイルを作成
   - 取得したいYouTube動画のURLを1行ずつ記述
   ```
   https://www.youtube.com/watch?v=VIDEO_ID_1
   https://www.youtube.com/watch?v=VIDEO_ID_2
   https://www.youtube.com/watch?v=VIDEO_ID_3
   ```

2. **スクリプトの実行**
   ```bash
   python youtube_comment_scraper.py
   ```

3. **結果の確認**
   - `TEXT_folder`フォルダ内に動画タイトル名のCSVファイルが生成されます
   - 各CSVファイルには番号とコメント内容が保存されます

## 出力ファイル形式

生成されるCSVファイルの構造：
| i | comment |
|---|---------|
| 1 | 最初のコメント |
| 2 | 二番目のコメント |
| ... | ... |

## 設定のカスタマイズ

### コメント取得数の変更
```python
get_total_num = 700  # この値を変更してコメント取得数を調整
```

### スクロール設定の調整
```python
total_scroll_pixels = random.randint(120, 180)  # スクロール範囲の調整
scroll_amount = 9  # スクロール量の初期値
```

### 再試行回数の設定
```python
max_attempts = 3  # コメント取得の最大試行回数
```

## 注意事項

- **利用規約の遵守**: YouTubeの利用規約に従って使用してください
- **レート制限**: 大量のリクエストを避け、適切な間隔を置いて実行してください
- **ブラウザ操作**: スクリプト実行中はFirefoxブラウザが自動で操作されます
- **ネットワーク**: 安定したインターネット接続が必要です

## トラブルシューティング

### よくある問題と解決方法

1. **GeckoDriverが見つからない**
   - パスが正しいか確認
   - GeckoDriverの実行権限を確認

2. **Firefoxが起動しない**
   - Firefoxのインストール場所を確認
   - `binary_location`の設定を確認

3. **コメントが取得できない**
   - YouTube動画がコメント無効になっていないか確認
   - ネットワーク接続を確認

4. **CSVファイルが生成されない**
   - `TEXT_folder`の書き込み権限を確認
   - 動画タイトルに特殊文字が含まれていないか確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 免責事項

このツールは教育目的で作成されました。使用に際してはYouTubeの利用規約を遵守し、適切な使用を心がけてください。作者は本ツールの使用によって生じる如何なる問題についても責任を負いません。
