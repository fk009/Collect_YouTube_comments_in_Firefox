"""
複数のURLからコメントを取得するプログラム

setting_folder>youtube_URL.txtに記述したyotubのURLを1行ずつ読み込み、コメントを取得していく

firefoxを使って、GeckoDriverを使って起動する。

"""
import csv
import os
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# FirefoxWebDriverのパスを指定します。
gecko_path = 'F:/geckodriver-v0.34.0-win32/geckodriver.exe'  # ここにダウンロードしたGeckoDriverのパスを指定してください。


import os

# 実行ファイルのディレクトリパスを取得
current_dir = os.path.dirname(__file__)

# 同じ階層の「TEXT_folder」フォルダのパス
csv_file_path = os.path.join(current_dir, "TEXT_folder")

# フォルダが存在しない場合は作成
if not os.path.exists(csv_file_path):
    os.makedirs(csv_file_path)

# YouTubeURLファイルのパス
yotubeURL_file_path = os.path.join(current_dir, "youtube_URL.txt")


# YouTubeの動画URLリスト
youtube_urls = []


# コメントを取得したいyotubeのURLを取得
def read_text_file(URL_path):
    lines = []
    try:
        with open(URL_path, 'r') as file:
            for line in file:
                lines.append(line.strip())  # 改行文字を除去してリストに追加
    except FileNotFoundError:
        print("ファイルが見つかりませんでした。")
    except Exception as e:
        print("エラーが発生しました:", e)
    return lines
youtube_urls = read_text_file(yotubeURL_file_path)

# ブラウザを起動します。
def start_browser():
    options = Options()
    options.page_load_strategy = 'eager'  # ページの読み込み戦略を設定します。
    options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    service = Service(executable_path=gecko_path)
    return webdriver.Firefox(service=service, options=options)

# ランダムにスクロール
def web_scroll_random(browser):

    # 初期のスクロール間隔
    initial_scroll_interval = 0.05
    scroll_amount = 9 # スクロール量の初期値
    total_scroll_pixels = random.randint(120, 180) # スクロールする合計のピクセル数 # スクロール量をランダムに設定（1000～2000）

    # 人がスクロールしたかのような、ゆっくりスクロールする動きを再現
    while scroll_amount < total_scroll_pixels:
        # スクロールを実行し、アニメーション効果を追加
        browser.execute_script(f"window.scrollBy(0, {scroll_amount});")

        # 前回のスクロール間隔を基準にランダム性を加える
        next_scroll_interval = max(0.01, min(initial_scroll_interval + random.uniform(-0.01, 0.01), 0.1))

        # スクロール後の待機時間を追加してアニメーション効果を実感
        scroll_interval = initial_scroll_interval = next_scroll_interval
        time.sleep(scroll_interval)

        # スクロール量を段階的に増加
        scroll_amount += 6  # 適切な値に調整してください

    print(f"{scroll_amount}分スクロールしました")

# コメント取得を試行し、取得したコメントを返す
def get_comments(browser):
    comments = []
    get_total_num = 700 # 取ってくるコメントの数
    attempts = 0 # 新しいコメントの取得ができなかった回数をカウント
    max_attempts = 3  # 最大試行回数を設定します。

    # 求めるコメント数を超えるか、新しいコメントが取得できなくなるまでループ
    while len(comments) < get_total_num and attempts < max_attempts:
        # 画面をスクロール
        web_scroll_random(browser)
        # コメントを取得してリストに追加します。
        comment_elements = browser.find_elements(By.CSS_SELECTOR, '#content-text') # メソッドを使用して、指定されたCSSセレクタに一致するすべての要素を検索
        new_comments = [comment_element.text for comment_element in comment_elements if comment_element.text not in comments] # 取得したコメントに、新しいコメントがあった場合、new_commentsに入れる
        comments.extend(new_comments) # commentsリストの末尾に、new_commentsリストの要素を追加
        # 新しいコメントが取得できない場合、一定時間待ってから再試行します。
        if not new_comments: # リストが空かチェック
            attempts += 1
            print("新しいコメントが見つかりませんでした。再試行します...")
            time.sleep(5)
        else:
            attempts = 0  # 新しいコメントが取得できた場合は試行回数をリセットします。
    return comments

# 取得したコメントをcsvとして出力
def write_comments_to_csv(movie_name, comments):
    """
    取得したコメントをcsvとして出力
    (動画の名前, 取得したコメントリスト)
    """
    csv_file_path_movie = csv_file_path + "\\" + movie_name + ".csv"

    # CSVファイルにコメントを書き込む
    with open(csv_file_path_movie, "w", newline="", encoding="utf-8") as csvfile:
        # CSVライターを作成し、ヘッダーを書き込む
        writer = csv.writer(csvfile)
        writer.writerow(["i", "comment"])

        # コメントをCSVファイルに書き込む
        for i, comment in enumerate(comments, start=1):
            writer.writerow([i, comment])

    print("CSVファイルにコメントが書き込まれました:", csv_file_path_movie)

# ファイル登録できない記号を半角空白に変換する処理
def replace_invalid_characters(variable):
    # 空白と「#」以外の記号を検索する正規表現パターン
    pattern = re.compile(r'[^\w\s#]')  # \w は英数字、\s は空白、# は「#」を表す

    # 正規表現パターンに一致する部分を半角空白に置換する
    replaced_variable = re.sub(pattern, ' ', variable)
    
    return replaced_variable



# 各動画のコメントを取得します。
for youtube_url in youtube_urls:
    print(f"Scraping comments for: {youtube_url}")
    browser = start_browser()
    # YouTubeの動画ページにアクセスします。
    browser.get(youtube_url)
    time.sleep(4)  # ページの読み込みを待ちます。

    # 画面をスクロール
    web_scroll_random(browser)

    # コメントを取得します。
    comments = get_comments(browser)

    # 取得したコメントを出力します。
    for i, comment in enumerate(comments, start=1):
        print(f"Comment {i}: {comment}")

    # タイトル要素を取得
    titles = browser.find_elements(By.CSS_SELECTOR, "#title h1 yt-formatted-string")

    # タイトルに特殊記号があれば、それを削除する
    titles_ok = replace_invalid_characters(titles[0].text)

    # 取得したコメントをCSVとして出力
    write_comments_to_csv(titles_ok, comments)

    # ブラウザを終了します。
    browser.quit()
    print("\n\n")
