# EDX UniText Downloader

このリポジトリは、連番で配置された SVG ページを自動でダウンロードし、PDF に結合するシンプルなスクリプトです。

**Project**: `EDX UniText Downloader`

**Main script**: `EDX_unitext_downloader.py`

---

**概要**:

- **目的**: Web 上にある連番 SVG（例: .../pages/1/page.svg, .../pages/2/page.svg ...）を順に取得し、各 SVG を PDF に変換して 1 つの PDF に結合します。
- **動作**: `BASE_URL` にページ番号のプレースホルダ `{}` を入れておくと、スクリプトが 1 ページ目から順にアクセスして存在しなくなるまでダウンロードを続けます。

---

**注意 (重要)**:

- このスクリプトはブラウザで取得した `Cookie` と `User-Agent` を使ってアクセスします。対象サイトの利用規約・著作権を必ず確認し、ダウンロードが許可されているコンテンツのみを扱ってください。

---

**要件 (最低限)**:

- Python 3.8+
- 必要な Python パッケージ:

```
requests
svglib
reportlab
PyPDF2
```

インストール例:

```bash
python -m pip install --upgrade pip
pip install requests svglib reportlab PyPDF2
```

（`svglib` は `reportlab` に依存します。Windows 環境ではビルドツールが必要になる場合があります。）

---

**設定方法**:

1. `EDX_unitext_downloader.py` をテキストエディタで開きます。
2. 上部の設定セクションを編集します:
   - `BASE_URL` : ページ番号の位置を `{}` に置き換えた URL を指定します。例:

```
BASE_URL = "https://example.com/book/pages/{}/page.svg"
```

- `output_name` : 出力される PDF ファイル名（例: `mybook.pdf`）。
- `HEADERS` : ブラウザからコピーした `Cookie` と `User-Agent` を貼り付けます。

例:

```python
BASE_URL = "https://example.com/book/pages/{}/page.svg"
output_name = "mybook.pdf"
HEADERS = {
    "Cookie": "SESSION=xxxxx; other=yyy",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
}
```

---

**実行方法 (Windows cmd)**:

```cmd
cd "c:\Users\<あなたのユーザ>\OneDrive\Documents\EDX UniText Downloader"
python EDX_unitext_downloader.py
```

スクリプトは `images/` フォルダや一時的な `temp_page_*.svg/pdf` を作成します。処理終了後に一時ファイルは削除されます。

---

**トラブルシューティング**:

- 取得できるページが 0 枚の場合: `BASE_URL`、`Cookie`、`User-Agent` を確認してください。ログにステータスコードが表示されます。
- `svg2rlg` や `reportlab` のエラー: 依存パッケージが正しくインストールされているか確認してください。特に Windows ではビルド環境が必要になることがあります。
- 画像（JPG 等）が正しく表示されない場合: スクリプトは SVG 内の `images/...` リンクを相対パスから取得します。必要に応じて `BASE_URL` のパス部分が正しいか確認してください。

---

**ライセンス**:
このリポジトリには明示的なライセンスが含まれていません。利用・配布条件を明示する必要がある場合は、`LICENSE` ファイルを追加してください。個人的に使う場合は注意してお使いください。

---

**貢献**:

- バグや改善案があれば Issue を立ててください。

---

作成: `EDX_unitext_downloader.py` と同じディレクトリに配置しています。
