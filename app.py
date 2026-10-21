import pandas as pd
import streamlit as st
from src.data_utils import filter_requirements, load_table, search_faq

st.set_page_config(
    page_title="International Student Support Desk DX",
    layout="wide"
)

def load_csv(name: str) -> pd.DataFrame:
    try:
        return load_table(name)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        st.error(f"データを読み込めません / Unable to load {name}: {exc}")
        st.stop()

requirements = load_csv("academic_requirements.csv")
departments = load_csv("departments.csv")
faculties = load_csv("faculty_summary.csv")
sources = load_csv("sources.csv")
support_categories = load_csv("support_categories.csv")
support_faq = load_csv("support_faq.csv")

st.title("留学生部相談窓口DX / International Student Support Desk DX")
st.caption(
    "大学の公式判断を代替するものではなく、学生の問い合わせを整理し、適切な相談先へ案内するためのPoCです。 "
    "/ This PoC does not replace official university guidance. It organizes inquiries and redirects students to the appropriate office."
)

tab_dashboard, tab_departments, tab_support, tab_faq, tab_academic, tab_sources = st.tabs(
    [
        "Dashboard / ダッシュボード",
        "Departments / 学科一覧",
        "Student Support / 留学生部相談",
        "FAQ Search / FAQ検索",
        "Academic Requirements / 履修・進級要件",
        "Sources / 情報源"
    ]
)

with tab_dashboard:
    st.subheader("Overview / 概要")

    col1, col2, col3, col4 = st.columns(4)

    total_faculties = faculties["faculty_id"].nunique() if not faculties.empty else 0
    total_departments = departments["department_id"].nunique() if not departments.empty else 0
    total_requirements = len(requirements) if not requirements.empty else 0
    high_conf = len(requirements[requirements["confidence"] == "high"]) if not requirements.empty and "confidence" in requirements.columns else 0

    col1.metric("Faculties / 学部数", total_faculties)
    col2.metric("Departments / 学科数", total_departments)
    col3.metric("Requirement records / 要件データ数", total_requirements)
    col4.metric("High confidence / 高信頼データ", high_conf)

    st.markdown("### Faculty Summary / 学部別サマリー")
    if not faculties.empty:
        st.dataframe(
            faculties[
                [
                    "faculty_ja",
                    "faculty_en",
                    "department_count",
                    "campus_ja",
                    "campus_en",
                    "last_verified"
                ]
            ],
            use_container_width=True
        )

        chart_df = faculties.set_index("faculty_en")["department_count"]
        st.bar_chart(chart_df)
    else:
        st.info("faculty_summary.csv is not found.")

    st.markdown("### Data Confidence / データ信頼度")
    if not requirements.empty and "confidence" in requirements.columns:
        confidence_counts = requirements["confidence"].value_counts()
        st.bar_chart(confidence_counts)

with tab_departments:
    st.subheader("Departments / 学科一覧")

    if departments.empty:
        st.warning("departments.csv がありません。")
    else:
        faculty_options = ["all"] + departments["faculty_ja"].dropna().unique().tolist()
        selected_faculty = st.selectbox("Faculty / 学部", faculty_options)

        dept_view = departments.copy()

        if selected_faculty != "all":
            dept_view = dept_view[dept_view["faculty_ja"] == selected_faculty]

        st.write(f"Departments / 学科数: {len(dept_view)}")

        for _, row in dept_view.iterrows():
            st.markdown(f"### {row['faculty_ja']} / {row['faculty_en']}")
            st.write(f"**{row['department_ja']}** / {row['department_en']}")
            st.write(
                f"Department ID: `{row['department_id']}` | "
                f"Campus: {row['campus_ja']} / {row['campus_en']}"
            )
            st.divider()

with tab_support:
    st.subheader("Student Support Categories / 留学生部相談カテゴリ")

    if support_categories.empty:
        st.warning("support_categories.csv がありません。")
    else:
        selected_category = st.selectbox(
            "Category / カテゴリ",
            support_categories["category_id"].tolist()
        )

        category_row = support_categories[
            support_categories["category_id"] == selected_category
        ].iloc[0]

        left, right = st.columns(2)

        with left:
            st.markdown("### 日本語")
            st.write(f"**カテゴリ:** {category_row['category_ja']}")
            st.write(f"**担当種別:** {category_row['owner_type']}")
            st.write(f"**相談先:** {category_row['primary_contact_ja']}")
            st.write(f"**公式確認が必要:** {category_row['official_check_required']}")
            st.write(category_row["notes_ja"])

        with right:
            st.markdown("### English")
            st.write(f"**Category:** {category_row['category_en']}")
            st.write(f"**Owner type:** {category_row['owner_type']}")
            st.write(f"**Contact:** {category_row['primary_contact_en']}")
            st.write(f"**Official check required:** {category_row['official_check_required']}")
            st.write(category_row["notes_en"])

        st.divider()

        st.markdown("### Related FAQ / 関連FAQ")

        if support_faq.empty:
            st.info("support_faq.csv がありません。")
        else:
            related = support_faq[support_faq["category_id"] == selected_category]

            if related.empty:
                st.info("No related FAQ found. / 関連FAQはまだ登録されていません。")
            else:
                for _, row in related.iterrows():
                    st.markdown(f"#### {row['question_ja']} / {row['question_en']}")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.markdown("**日本語**")
                        st.write(row["answer_ja"])
                        st.write(f"**相談先:** {row['contact_ja']}")

                    with c2:
                        st.markdown("**English**")
                        st.write(row["answer_en"])
                        st.write(f"**Contact:** {row['contact_en']}")

                    st.write(f"Confidence / 信頼度: {row['confidence']}")
                    st.divider()

with tab_faq:
    st.subheader("FAQ Search / FAQ検索")

    if support_faq.empty:
        st.warning("support_faq.csv がありません。")
    else:
        keyword = st.text_input("Keyword / キーワード", "")

        results = search_faq(support_faq, keyword)

        st.write(f"Results / 検索結果: {len(results)}")

        for _, row in results.iterrows():
            st.markdown(f"### {row['question_ja']} / {row['question_en']}")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**日本語**")
                st.write(row["answer_ja"])
                st.write(f"**相談先:** {row['contact_ja']}")

            with c2:
                st.markdown("**English**")
                st.write(row["answer_en"])
                st.write(f"**Contact:** {row['contact_en']}")

            st.write(
                f"**Category:** {row['category_id']} | "
                f"**Confidence:** {row['confidence']} | "
                f"**Last verified:** {row['last_verified']}"
            )
            st.divider()

with tab_academic:
    st.subheader("Academic Requirements / 履修・進級要件")

    if requirements.empty:
        st.warning("No academic requirement data found. / 履修・進級要件データがありません。")
    else:
        c1, c2, c3, c4 = st.columns(4)

        if not departments.empty:
            department_options = ["all"] + departments["department_id"].dropna().tolist()
        else:
            department_options = ["all"] + sorted(requirements["department_id"].dropna().unique())

        student_type_options = ["all"] + sorted(requirements["student_type"].dropna().unique())
        requirement_type_options = ["all"] + sorted(requirements["requirement_type"].dropna().unique())
        stage_options = ["all"] + sorted(requirements["stage"].dropna().unique())

        selected_department = c1.selectbox("Department / 学科", department_options)
        selected_student_type = c2.selectbox("Student Type / 学生区分", student_type_options)
        selected_requirement_type = c3.selectbox("Requirement Type / 要件種別", requirement_type_options)
        selected_stage = c4.selectbox("Stage / 段階", stage_options)

        selected_year = st.selectbox(
            "Admission Year / 入学年度",
            ["all"] + sorted(requirements["admission_year"].dropna().astype(str).unique())
        )
        filtered = filter_requirements(
            requirements, departments, selected_department, selected_student_type,
            selected_requirement_type, selected_stage, selected_year
        )

        st.write(f"Results / 検索結果: {len(filtered)}")

        if filtered.empty:
            st.info(
                "この学科の履修・進級要件データはまだ登録されていません。"
                " / Academic requirement data for this department has not been registered yet."
            )
        else:
            for _, row in filtered.iterrows():
                st.markdown(f"### {row['title_ja']} / {row['title_en']}")

                left, right = st.columns(2)

                with left:
                    st.markdown("**日本語**")
                    st.write(row["detail_ja"])
                    st.write(f"**相談先:** {row['primary_contact_ja']}")

                with right:
                    st.markdown("**English**")
                    st.write(row["detail_en"])
                    st.write(f"**Contact:** {row['primary_contact_en']}")

                st.write(
                    f"**Type / 種別:** {row['requirement_type']} | "
                    f"**Stage / 段階:** {row['stage']}"
                )
                st.write(
                    f"**Confidence / 信頼度:** {row['confidence']} | "
                    f"**Last verified / 最終確認:** {row['last_verified']}"
                )

                if not sources.empty and "source_id" in row:
                    src = sources[sources["source_id"] == row["source_id"]]
                    if not src.empty:
                        src_row = src.iloc[0]
                        st.write(f"**Source / 情報源:** {src_row['source_name']}")
                        if src_row["source_url"] != "not_public":
                            st.write(src_row["source_url"])

                st.divider()

with tab_sources:
    st.subheader("Sources / 情報源")

    if sources.empty:
        st.warning("No source data found. / 情報源データがありません。")
    else:
        st.dataframe(sources, use_container_width=True)
