import os
import requests
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfMerger

# ================= SETTING =================
# 1. ベースとなるURL (数字の部分を {} に置き換えてください)
# 例: .../pages/1/page.svg -> .../pages/{}/page.svg
BASE_URL = ""
# 2. 出力PDFファイル名
output_name = "hoge.pdf"

# 3. ブラウザから取得した Cookie と User-Agent を貼り付けてください
HEADERS = {
    "Cookie": "",
    "User-Agent": ""
}
# ===========================================

def download_and_convert():
    merger = PdfMerger()
    temp_files = [] 
    
    if not os.path.exists("images"):
        os.makedirs("images")

    print("自動ダウンロードを開始します（終了まで自動継続）...")

    page_num = 1 # 1ページ目からスタート
    consecutive_errors = 0 # 安全策（念のため）

    while True:
        url = BASE_URL.format(page_num)
        print(f"確認中: ページ {page_num} ... ", end="")

        try:
            # --- 1. アクセス確認 ---
            response = requests.get(url, headers=HEADERS)
            
            # ステータスコードが200(成功)以外なら終了とみなす
            if response.status_code != 200:
                print(f"-> ページがありません (Status: {response.status_code})。終了処理に入ります。")
                break
            
            print("OK! ダウンロード処理中")

            # --- 2. SVG本体処理 ---
            svg_content = response.text
            page_base_url = url.rsplit('/', 1)[0] 
            
            # --- 3. 画像(JPG等)の自動収集 ---
            linked_images = set(re.findall(r'["\'](images/[^"\']+)["\']', svg_content))
            
            for img_path in linked_images:
                img_url = f"{page_base_url}/{img_path}"
                local_img_path = img_path.replace("/", os.sep)
                os.makedirs(os.path.dirname(local_img_path), exist_ok=True)

                img_res = requests.get(img_url, headers=HEADERS)
                if img_res.status_code == 200:
                    with open(local_img_path, "wb") as f:
                        f.write(img_res.content)

            # --- 4. 変換と保存 ---
            svg_filename = f"temp_page_{page_num}.svg"
            pdf_filename = f"temp_page_{page_num}.pdf"

            with open(svg_filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)

            drawing = svg2rlg(svg_filename)
            renderPDF.drawToFile(drawing, pdf_filename)

            merger.append(pdf_filename)
            
            temp_files.append(svg_filename)
            temp_files.append(pdf_filename)
            
            # 次のページへ
            page_num += 1

        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            # エラーが出てもすぐ止まらず、一応次のページを見てみる（欠番対策）
            consecutive_errors += 1
            if consecutive_errors > 3: # 3回連続エラーなら本当に終了
                print("連続エラーのため停止します。")
                break
            page_num += 1

    # --- 5. 最終保存 ---
    if page_num > 1:
        print(f"PDFを作成しています: {output_name}")
        merger.write(output_name)
        merger.close()

        print("一時ファイルを削除中...")
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)
        print("すべて完了しました！")
    else:
        print("ページを1枚も取得できませんでした。CookieやURLを確認してください。")

if __name__ == "__main__":
    download_and_convert()