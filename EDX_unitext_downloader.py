import os
import requests
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfMerger

# ================= SETTING =================
# 1. ベースとなるURL (数字の部分を {} に置き換えてください)
# 例: .../pages/1/page.svg -> .../pages/{}/page.svg
BASE_URL = "https://app.d-text-service.jp/file/99200/book/data/OEBPS/pages/{}/page.svg"
# 2. 出力PDFファイル名
output_name = "CA_Sec2_Text.pdf"

# 3. ブラウザから取得した Cookie と User-Agent を貼り付けてください
HEADERS = {
    "Cookie": "ApplicationGatewayAffinityCORS=b35b56c2684328fd4a813b6fbf0101ac; ApplicationGatewayAffinity=b35b56c2684328fd4a813b6fbf0101ac; token=nxBaAfKWma3cglvMrsk9jLN8Yy-QNIhwyBJLQ5U9CWMyw8zX8IJOaBu1EgWZg8P8LZC2bBAN5wQlWG9Mrvo8779EIgz1t1vn4m7c9nnlO4RNeGj8On86knBrE5sH7QXlEzSfpfCc7AlLmx4; refresh-token=lX_i38j8Ny_PGZocODNCyRUcyzdWT9-7VekJvm_BM-EzwzaMr6X6tn5qECY4uZarz1bKz0jtj5yRXaSjhJzCW4Fs9oIQaMMGH2LKYB5hOVvk5NBvzO5iqACTZFe8WgJDCe5vnK8RbLmzT2Z; uid=2; sid=244; rid=1705009; agw-token=nxBaAfKWma3cglvMrsk9jLN8Yy-QNIhwyBJLQ5U9CWMyw8zX8IJOaBu1EgWZg8P8LZC2bBAN5wQlWG9Mrvo8779EIgz1t1vn4m7c9nnlO4RNeGj8On86knBrE5sH7QXlEzSfpfCc7AlLmx4; agw-rid=1705009; .fileauth=CfDJ8Dbx0ahiJDxEkpFGqJXVCY4VKl3MLqQpiyirk1F7lZH7qm1CS2-GCrvyXSE5L9LOHaMMxK6vBPGm999EcTgd3hntHD9TRLLInLrYvIjLMSJNMuEw5s1DgbUpuUzFUZqNywseJjy7lU5vm9WJpqOAu00Bz0gwHNMMGLY1yCTXHPTc_W2giljfj_IfXg_Not0tJnzklx28BWAAt9mdAxNyPLz3WwNx7CVTiHvYht-MhOIybPflk7AIgUExoZh-pffoxailVcAt-PjvnwSQmL76ffrL4tOerbMahQc0zeFf39eNFG_dasPJsDPO6cOObpauTKeSb1dCqTFGReznoT1K4iAJ1zZ2SyyQcW8Y8hVVfFSLuGsDYEpghY5x4gmiFoXmvOMw2N7Vt1AI578Z4DNK_5c2vn6GXJNlBWbpUZxA9Ya35PTBZi_HXlYke5V3WS9s_RRNWLUagaCa41FLcVWWZBGvNB3TrC6MzgAtysx1QbW8M-gdqkCA48rCoGh4-MhWkvlNzkLP9S3GOEv_2DnW-46OiKcNeOBOFv8VSf8GWItwPDpYjtgNL0O4hnM3b1K9fN1rTsAvJEiYQT3DBsDYLJrTeJX88WmyQ00RN-tQ8J9Pp5wZQcWsDUQbN7-SIhOix76mKdc_2ATepeDTgzX2O1c; _d_textservice_center_frontend_session=i8c7jHlfjNHz38ScnIjLLkpc2ngw8q8TS9e9BROOuMmTiFGeb1a5%2Bq9JkwuPjeEGfBSr1DYpADIfO%2B31lljVrhMJVsX89b5XBBjcLbpGL9sWuCQJi5%2BMW1cvoKxFNHM0DKwPDaQ%2FcSh5pSbxtE4IWFFlCYsHq2DtnJcddoovp0oyj47u9V4gRZNSIlpGmzPb6crk3TLgopAIX6ZC2INEcUURz0S9B9fdJUyRjUCXtuSp6QuhmkKQQ0DEtIaxvfN5M3R%2B%2Bkdzed46sEIMZ0tpaTB8QrH%2BjAd4KGcZgRolo0N%2BU3UDkisBjVHAtLejRDsv5V7hbW5WuDaqbAZI8rMHNgs4omciF5%2FeBFquNYi%2BHlQ0hb5wVNlJ47%2B8IJBCKd22QOuJUFCkeZASkJAe2DjFJHem%2BzLtbtJKlp2hRLjxfWTnX77NXCbO0K%2F1YfNaJFuzoh6ROMvfy%2Fww4SQQ1Tw94DouE9g9WfzrxADg%2BTcTTmyWN4jyuE%2BdA6%2BZa%2Bl1msk6O10M14sjRdW5E3Bhv4wAESbm66P4g4oT87Nanix1qVApIZw8BQLz31WefQMCDKgNUEL6MxsC8KzYFI3Wiwa6YOKNqy2aALiJeCjOQU6zkFbc6i8o8Oc2Cnx2ONO6cflMx0zObQfmzdq8qTZ30tfODJBo8CigVrTiCf9JTIER3%2BgiCsC9yQVuBOPR8vmTrBAQ0LWpLSmqlBbXViPqklLbXqToGp7KXBBnUTkTcr54KPzLV6dWjr7RncBiPiuSvo7Bbh%2FL0pmNfC%2BNBmb5lDNKSRIL%2F%2FWWUVgpZgGFR6IagklG55ulRC2zmRCImwwSeZNPSIqCV2eY1B9Wsdj3JxtPB%2Bv9EPsYq3HephJ%2F%2FDKISuXE9rakVYeZZbVS--68GXzxlIWa4fnAof--WZmk1O29737zc6SyxNou%2Bw%3D%3D",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36"
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