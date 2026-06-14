# International Student Support Desk DX

# 留学生部相談窓口DX

## Overview / 概要

This project is an IT consulting-style DX case study for improving international student support desk operations at a Japanese university.

It organizes common inquiries from international students, such as visa procedures, scholarships, course registration, bank accounts, student club rules, executive team participation, annual events, and academic requirements. The project provides bilingual Japanese-English guidance and redirects students to appropriate official contact points.

本プロジェクトは、日本の大学における留学生支援業務を対象とした、ITコンサルティング型のDXケーススタディです。

ビザ、奨学金、履修・授業、銀行口座、留学生部ルール、執行部参加、年間イベント、進級・卒業要件など、留学生からの問い合わせを整理し、日本語・英語の二言語で案内できる仕組みを設計しています。

---

## Purpose / 目的

The purpose of this project is not to replace official university guidance.

Instead, this project aims to:

* classify common inquiries from international students
* provide initial bilingual guidance
* identify the appropriate contact point
* separate student club information from official university procedures
* visualize academic and support-related information through a dashboard
* practice IT consulting processes such as problem definition, As-Is/To-Be analysis, data structuring, and PoC development

本プロジェクトは、大学の公式判断や正式な手続きを代替するものではありません。

目的は以下の通りです。

* 留学生からの問い合わせをカテゴリ別に整理する
* 日本語・英語で初期案内を提供する
* 適切な相談先を明確にする
* 留学生部の内部情報と大学・行政の公式手続きを区別する
* ダッシュボードで学科情報・相談カテゴリ・FAQを可視化する
* 課題定義、As-Is/To-Be分析、データ構造化、PoC開発など、ITコンサルティングの流れを実践する

---

## Features / 主な機能

### 1. Dashboard / ダッシュボード

The dashboard summarizes:

* number of faculties
* number of departments
* number of academic requirement records
* number of high-confidence records
* faculty-level department counts
* data confidence distribution

ダッシュボードでは、学部数、学科数、履修・進級要件データ数、高信頼データ数、学部別学科数、データ信頼度を確認できます。

---

### 2. Department List / 学科一覧

This section shows a bilingual list of departments by faculty.

The current dataset covers the Tokyo Senju Campus structure, including:

* School of Engineering
* School of Engineering Evening Division
* School of Science and Technology for Future Life
* School of System Design and Technology

学科一覧では、学部ごとに学科名を日本語・英語で表示します。

---

### 3. Student Support Categories / 留学生部相談カテゴリ

The project defines support categories such as:

* Visa / Residence Status
  ビザ・在留資格

* Scholarship
  奨学金

* Course Registration / Classes
  履修・授業

* Bank Account
  銀行口座

* Student Club Rules
  留学生部ルール

* Student Club Executive Team
  留学生部執行部

* Annual Events
  年間イベント

* Exchange Students
  交換留学生

* Short-term Students
  短期留学生

Each category includes:

* Japanese label
* English label
* owner type
* primary contact point
* whether official confirmation is required
* notes in Japanese and English

---

### 4. FAQ Search / FAQ検索

The FAQ search function allows users to search common questions by keyword.

Current FAQ examples include:

* residence card renewal
* scholarship information
* course registration and promotion requirements
* exchange student course registration
* bank account opening
* residence card update at banks
* student club participation rules
* attendance poll rules
* executive team participation
* annual events

FAQ検索では、キーワードを入力して、日本語・英語の質問・回答を検索できます。

---

### 5. Academic Requirements / 履修・進級要件

This section organizes academic requirement data by:

* department
* admission year
* student type
* requirement type
* academic stage
* source
* confidence level
* last verified date

The current academic requirement dataset starts with the School of System Design and Technology and can be expanded to other faculties and departments.

履修・進級要件データは、学科、入学年度、学生区分、要件種別、段階、情報源、信頼度、最終確認日ごとに管理しています。

---

## Data Design / データ設計

The project uses structured CSV datasets.

```text
data/
├── faculty_summary.csv
├── departments.csv
├── academic_requirements.csv
├── support_categories.csv
├── support_faq.csv
└── sources.csv
```

### `faculty_summary.csv`

Stores faculty-level summary information.

学部単位の概要情報を管理します。

Main columns:

```text
faculty_id
faculty_ja
faculty_en
department_count
campus_ja
campus_en
source_id
last_verified
```

---

### `departments.csv`

Stores department-level master data.

学科マスターデータを管理します。

Main columns:

```text
department_id
faculty_id
faculty_ja
faculty_en
department_ja
department_en
campus_ja
campus_en
source_id
last_verified
```

---

### `academic_requirements.csv`

Stores course registration, promotion, graduation, and academic guidance records.

履修、進級、卒業、学修案内に関するデータを管理します。

Main columns:

```text
requirement_id
department_id
admission_year
student_type
requirement_type
stage
title_ja
title_en
detail_ja
detail_en
primary_contact_ja
primary_contact_en
source_id
confidence
last_verified
```

---

### `support_categories.csv`

Stores support desk category data.

留学生部相談カテゴリを管理します。

Main columns:

```text
category_id
category_ja
category_en
owner_type
primary_contact_ja
primary_contact_en
official_check_required
notes_ja
notes_en
```

---

### `support_faq.csv`

Stores bilingual FAQ data.

日本語・英語のFAQデータを管理します。

Main columns:

```text
faq_id
category_id
question_ja
question_en
answer_ja
answer_en
contact_ja
contact_en
source_type
confidence
last_verified
```

---

### `sources.csv`

Stores source metadata.

情報源を管理します。

Main columns:

```text
source_id
source_name
source_type
source_url
access_level
last_verified
notes
```

---

## Source and Confidence Policy / 情報源と信頼度の方針

This project separates information by reliability.

本プロジェクトでは、情報の信頼度を区別して管理します。

### High Confidence

Information confirmed from official handbooks or official university documents.

学生要覧や大学の公式資料で確認した情報。

### Medium Confidence

Information based on internal university portals such as UNIPA or information that requires additional confirmation.

UNIPAなどの学内ポータル情報、または追加確認が必要な情報。

### Low Confidence

Information based on personal experience, student interviews, blogs, or unofficial references.

個人の経験、学生からの聞き取り、ブログなど、公式根拠ではない参考情報。

---

## Important Disclaimer / 注意事項

This system does not provide legal, immigration, academic, or administrative final judgments.

For important matters, students must confirm with the official university office, International Center, Academic Affairs Office, UNIPA, Immigration Services Agency, or relevant external institution.

本システムは、法律、在留資格、履修、進級、卒業、大学手続きに関する最終判断を行うものではありません。

重要な事項については、必ず大学の担当窓口、国際センター、教務担当窓口、UNIPA、出入国在留管理庁、または関連する公式機関で確認してください。

---

## Tech Stack / 使用技術

* Python
* Streamlit
* Pandas
* CSV-based structured dataset

---

## Setup / セットアップ

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/international-student-support-dx.git
cd international-student-support-dx
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## Requirements / 必要ライブラリ

```text
streamlit
pandas
```

---

## Project Structure / プロジェクト構成

```text
international-student-support-dx/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── faculty_summary.csv
│   ├── departments.csv
│   ├── academic_requirements.csv
│   ├── support_categories.csv
│   ├── support_faq.csv
│   └── sources.csv
└── docs/
    └── future_documents.md
```

---

## Current Scope / 現在の対象範囲

The current version focuses on a proof-of-concept for international student support operations.

現在のバージョンは、留学生支援業務を対象としたPoCです。

Current scope:

* Tokyo Senju Campus department structure
* Student support categories
* Bilingual FAQ
* Initial academic requirement dataset
* Source and confidence tracking

---

## Future Work / 今後の拡張予定

Planned improvements include:

* Add more academic requirement data by faculty and department
* Add course-level datasets
* Add student-type-specific guidance for exchange students and short-term students
* Add visa and bank account guidance with official source links
* Add event participation dashboard
* Add inquiry classification logic
* Add FAQ search improvement
* Add As-Is / To-Be process diagrams
* Add consulting report documentation

今後の拡張予定：

* 学部・学科ごとの履修・進級要件データ追加
* 科目単位のデータセット追加
* 交換留学生・短期留学生向け案内の拡充
* ビザ・銀行口座に関する公式情報リンクの追加
* イベント参加状況ダッシュボードの追加
* 問い合わせ分類ロジックの追加
* FAQ検索機能の改善
* As-Is / To-Be業務フロー図の追加
* コンサルティングレポートの作成

---

## Consulting Perspective / コンサルティング観点

This project is designed not only as a software prototype, but also as an IT consulting case study.

It demonstrates:

* problem identification
* stakeholder and contact point analysis
* information classification
* bilingual user support design
* data source management
* risk separation between official and internal information
* dashboard-based visualization
* PoC implementation

本プロジェクトは、単なるアプリ開発ではなく、ITコンサルティング型ケーススタディとして設計しています。

以下の観点を重視しています。

* 課題定義
* 関係者・相談先の整理
* 情報分類
* 日本語・英語の二言語対応設計
* 情報源管理
* 公式情報と内部情報のリスク分離
* ダッシュボードによる可視化
* PoC実装

---

## Author / 作成者

This project was created as a personal portfolio project to understand and practice IT consulting, DX proposal design, and data-driven student support operations.

本プロジェクトは、ITコンサルティング、DX提案設計、データに基づく学生支援業務改善を理解・実践するための個人ポートフォリオプロジェクトです。
