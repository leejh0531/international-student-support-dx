# 留学生部相談窓口DX / International Student Support Desk DX

留学生向けの相談先、FAQ、学科情報、履修・進級要件を、日本語と英語で参照するための個人学習用プロトタイプです。Python、Streamlit、pandasを使い、CSVに整理した情報を画面に表示します。

相談内容に応じた案内先を探しやすくすることが目的です。現在の実装は情報の閲覧・絞り込み・検索が中心で、問い合わせの自動分類や生成AIによる回答は実装していません。大学への正式導入、利用者評価、問い合わせ削減などの効果を示す記録は本リポジトリに含まれていません。

A personal learning prototype for browsing international-student support information in Japanese and English. It reads structured CSV files and provides tables, filters, FAQ search, and summary charts. Automatic inquiry classification and AI-generated answers are not implemented. This repository does not provide evidence of institutional deployment or measured operational benefits.

## 現在の機能 / Implemented features

| 画面 | 実装内容 |
| --- | --- |
| Dashboard | 学部数・学科数・学修要件レコード数の集計、学部別学科数と登録済み信頼度ラベルのグラフ |
| Departments | 学部による学科一覧の絞り込み、日本語・英語名称の表示 |
| Student Support | 相談カテゴリごとの案内先・注意事項・関連FAQの表示 |
| FAQ Search | 登録済みの質問・回答・カテゴリIDを対象とした文字列検索 |
| Academic Requirements | 学科・学生区分・要件種別・段階による情報の絞り込み |
| Sources | CSVに登録した情報源メタデータの一覧表示 |

二言語の文章はCSVに登録済みのものを表示します。実行時の自動翻訳や、大学のWebサイト・UNIPAからの自動取得は行いません。

Bilingual text is stored in the CSV files; there is no live translation or automatic synchronization with university systems.

## データの対象範囲 / Data scope

- 学科一覧：東京千住キャンパスの工学部、工学部第二部、未来科学部、システムデザイン工学部。
- 学修要件：主に2026年度のシステムデザイン工学部に関する登録データ。学科一覧にある全学科の要件を網羅しているわけではありません。
- FAQ：在留資格、奨学金、履修、銀行、留学生部の活動などに関する初期案内。
- 入学年度はCSVに保存していますが、現在の画面には入学年度による絞り込みがありません。

The department directory has broader coverage than the academic-requirement dataset. A listed department does not imply that its academic requirements are available.

## 情報源と確認状況 / Sources and verification

[情報源一覧](data/sources.csv)と[FAQ](data/support_faq.csv)には、公式資料、学内情報、学生団体の内部情報、個人ブログなど、性質の異なる情報が含まれます。

- **source_type / access_level**：出典の種類と参照方法を示すメタデータです。
- **confidence**：登録時に付与された high / medium / low のラベルです。現在のデータでは内部の部活動情報にも high が使われており、**high は大学の公式確認済みという意味ではありません**。
- **last_verified**：CSVに記録された確認日です。アプリが最新性を自動確認しているわけではありません。
- 一部の **source_url** は studentdoc3.pdf のようなローカルファイル名で、その資料は本リポジトリに含まれていません。公開URLや根拠ページの追跡性は未整備です。

Confidence labels are dataset annotations, not independently validated reliability scores. Some source references are local filenames unavailable to repository readers. Source categories, supporting pages, and verification records need further standardization.

本アプリは大学公式の案内や個別の履修・在留資格等の判断を代替しません。実際の手続きには、該当年度の公式資料と担当窓口の案内を確認してください。

## 既知の制約 / Known limitations

1. **学科フィルタの適用範囲**  
   現在は学科を選択すると、department_id が all_ で始まる共通レコードを学部に関係なく含めます。そのため、システムデザイン工学部以外の学科にも同学部の共通要件が表示される場合があります。学部との対応付けの修正が必要です。

2. **FAQ検索の入力処理**  
   検索はpandasの str.contains を使用し、現在は入力を正規表現として扱います。[ などの不完全なパターンではエラーが発生する場合があります。意味検索や検索精度の評価は未実装です。

3. **データ検証の範囲**  
   検証スクリプトは一部のファイルの存在、学修要件の必須列・信頼度ラベル・出典IDを確認します。情報の正確性、翻訳品質、全CSVの整合性、画面の動作を保証するものではありません。

The department filter currently includes all shared records regardless of faculty. FAQ input is interpreted as a regular expression and can raise errors for invalid patterns. The validator checks selected structural properties only.

## セットアップ / Run locally

以下はmacOS/Linuxのシェルで、リポジトリのルートから実行する例です。

~~~bash
git clone https://github.com/leejh0531/international-student-support-dx.git
cd international-student-support-dx
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/validate_dataset.py
python -m streamlit run app.py
~~~

Windowsでは仮想環境の有効化コマンドを利用するシェルに合わせて変更してください。依存ライブラリは [requirements.txt](requirements.txt) に記載しています。バージョンは固定していません。

## ファイル構成 / Repository contents

| ファイル | 用途 |
| --- | --- |
| [app.py](app.py) | Streamlitの画面とデータ読込・検索・フィルタ処理 |
| [src/validate_dataset.py](src/validate_dataset.py) | 一部のデータ構造と出典IDの検証 |
| [data/faculty_summary.csv](data/faculty_summary.csv) | 学部別概要 |
| [data/departments.csv](data/departments.csv) | 学科マスタ |
| [data/academic_requirements.csv](data/academic_requirements.csv) | 履修・進級・卒業等に関する登録情報 |
| [data/support_categories.csv](data/support_categories.csv) | 相談カテゴリと案内先 |
| [data/support_faq.csv](data/support_faq.csv) | 日英FAQ |
| [data/sources.csv](data/sources.csv) | 出典のメタデータ |
| [data/course_categories.csv](data/course_categories.csv) | 補助データ。現在のアプリでは未使用 |
| [data/student_advice_rules.csv](data/student_advice_rules.csv) | 補助データ。現在のアプリでは未使用 |

## 今後の改善候補 / Next improvements

- 学部・学科・入学年度に対応した要件の表示と検証。
- FAQ検索入力の文字列処理の修正と、検索例による動作確認。
- 公式情報と部活動情報の確認基準の分離、公開出典とページ番号の追加。
- 利用者に試してもらい、案内先の探しやすさや不足情報を評価。

これらは今後の改善候補であり、実装・評価済みの成果ではありません。
