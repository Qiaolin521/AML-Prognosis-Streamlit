from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AML Prognosis | Research Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

# ---------- Visual style ----------
st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}
    [data-testid="stSidebar"] {border-right: 1px solid rgba(128,128,128,.18);}
    .hero {
        padding: 2rem 2.2rem; border-radius: 18px;
        background: linear-gradient(120deg, #102b46 0%, #174d68 58%, #287b83 100%);
        color: white; margin-bottom: 1.4rem;
    }
    .hero h1 {color: white; font-size: 2.35rem; margin: 0 0 .35rem 0;}
    .hero p {color: #e5f1f5; font-size: 1.02rem; margin: .25rem 0;}
    .eyebrow {text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; font-weight: 700; color: #b9d9e3;}
    .section-note {color: #64748b; font-size: .92rem;}
    .metric-card {
        border: 1px solid rgba(128,128,128,.22); border-radius: 14px;
        padding: 1rem 1.1rem; min-height: 112px;
        background: rgba(128,128,128,.035);
    }
    .metric-label {font-size: .82rem; color: #64748b; margin-bottom: .35rem;}
    .metric-value {font-size: 1.75rem; font-weight: 750; line-height: 1.15;}
    .metric-help {font-size: .78rem; color: #64748b; margin-top: .35rem;}
    .info-panel {
        border-left: 4px solid #287b83; padding: .8rem 1rem;
        background: rgba(40,123,131,.08); border-radius: 4px 10px 10px 4px;
    }
    .warning-panel {
        border-left: 4px solid #d69e36; padding: .8rem 1rem;
        background: rgba(214,158,54,.10); border-radius: 4px 10px 10px 4px;
    }
    div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.2); padding: 14px; border-radius: 12px;}
    h2 {padding-top: .6rem;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("## 🧬 AML Research")
st.sidebar.caption("GSE37642 · GPL96")
page = st.sidebar.radio(
    "页面导航",
    ["项目概览", "队列与生存分析", "预后模型", "候选基因", "方法与局限"],
    label_visibility="collapsed",
)
st.sidebar.divider()
st.sidebar.caption("Research & educational use only")

# ---------- Helpers ----------
def metric_card(label, value, help_text=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-help">{help_text}</div></div>',
        unsafe_allow_html=True,
    )

def show_figure(filename, caption, help_text=None):
    path = ASSETS / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(help_text or f"图表文件尚未添加：assets/{filename}")

def section_intro(text):
    st.markdown(f'<p class="section-note">{text}</p>', unsafe_allow_html=True)

# Values below are the verified cohort/model summary from this project.
N_TOTAL = 417
N_DEATH = 308
N_CENSORED = 109
MEDIAN_OS = 329
CINDEX_TRAIN = 0.6776
CINDEX_TEST = 0.5860

# The five coefficients below are the top examples already reported in the project.
# The full 20-gene table is loaded from data/ when supplied.
TOP_GENES = pd.DataFrame({
    "Gene": ["DDIT4", "CST3", "HOPX", "F2RL1", "ST18"],
    "Coefficient": [0.174844, -0.109641, 0.089646, 0.088470, -0.074321],
})

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Hematology · Translational bioinformatics</div>
  <h1>AML Prognosis Analysis</h1>
  <p>Gene-expression profiling and exploratory survival prediction</p>
  <p style="font-size:.86rem; opacity:.9;">GEO accession: GSE37642 &nbsp;|&nbsp; Platform: GPL96 &nbsp;|&nbsp; Cohort: 417 patients</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "本项目仅用于科研与教学展示。模型尚未经过独立队列验证，不可用于患者个体预后判断或临床决策。"
)

# ---------- Pages ----------
if page == "项目概览":
    st.subheader("项目概述")
    st.write(
        "本项目基于 Gene Expression Omnibus（GEO）公开数据集 GSE37642，"
        "围绕急性髓系白血病（acute myeloid leukemia，AML）患者的总生存期（overall survival，OS）"
        "开展探索性生存分析，并构建 LASSO-Cox 惩罚回归模型筛选候选预后相关基因。"
    )
    st.markdown("#### 核心数据")
    cols = st.columns(4)
    with cols[0]: metric_card("纳入患者", "417", "具有可用 OS 信息")
    with cols[1]: metric_card("观察到死亡", "308", "事件数")
    with cols[2]: metric_card("删失观察", "109", "随访期间未观察到死亡")
    with cols[3]: metric_card("中位 OS", "329 天", "Kaplan–Meier 估计")

    st.markdown("#### 分析流程")
    flow = st.columns(4)
    steps = [
        ("01", "数据整理", "表达矩阵与生存资料匹配"),
        ("02", "生存描述", "KM 曲线与结局分布"),
        ("03", "特征筛选", "LASSO-Cox 模型"),
        ("04", "模型评价", "训练集与测试集 C-index"),
    ]
    for col, (num, title, desc) in zip(flow, steps):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="eyebrow" style="color:#287b83">{num}</div>'
                f'<b>{title}</b><div class="metric-help">{desc}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("#### 项目摘要")
    st.markdown(
        '<div class="info-panel">分析队列共 417 例 AML 患者。当前 LASSO-Cox 模型在训练集中的 '
        'C-index 约为 0.678，在测试集中的 C-index 约为 0.586。测试集表现提示模型区分能力有限，'
        '需要进一步优化并在独立队列中验证。</div>',
        unsafe_allow_html=True,
    )

elif page == "队列与生存分析":
    st.subheader("队列特征与生存结局")
    section_intro("本页展示当前项目已核实的队列汇总数据及生存分析图。")
    a, b = st.columns([1, 1])
    with a:
        st.markdown("#### 生存结局")
        outcome = pd.DataFrame(
            {"患者数": [N_DEATH, N_CENSORED]},
            index=["死亡事件", "删失观察"],
        )
        st.bar_chart(outcome, horizontal=True)
        st.caption(f"死亡事件：{N_DEATH / N_TOTAL:.1%}；删失观察：{N_CENSORED / N_TOTAL:.1%}")
    with b:
        st.markdown("#### 队列摘要")
        st.metric("总人数", f"{N_TOTAL}")
        st.metric("中位总生存期", f"{MEDIAN_OS} 天")
        st.caption("OS = overall survival；KM = Kaplan–Meier。")

    st.divider()
    st.markdown("#### Kaplan–Meier 生存分析")
    show_figure(
        "AML_overall_KM_curve.png",
        "Overall Kaplan–Meier survival curve",
        "尚未在 GitHub 仓库中找到总生存 Kaplan–Meier 曲线。将 AML_overall_KM_curve.png 放入 assets/ 文件夹后，此处会自动显示。",
    )
    show_figure(
        "AML_test_risk_group_KM.png",
        "Test-set risk-group Kaplan–Meier curve",
        "尚未添加测试集风险分组 KM 曲线。将 AML_test_risk_group_KM.png 放入 assets/ 文件夹后，此处会自动显示。",
    )
    left, right = st.columns(2)
    with left:
        show_figure("AML_survival_outcome_distribution.png", "Survival outcome distribution")
    with right:
        show_figure("AML_survival_time_distribution.png", "Overall survival time distribution")

elif page == "预后模型":
    st.subheader("LASSO-Cox 预后模型")
    section_intro("使用 LASSO 惩罚的 Cox 比例风险回归进行特征筛选，并以 concordance index（C-index）评价区分能力。")
    x, y = st.columns(2)
    with x: metric_card("训练集 C-index", f"{CINDEX_TRAIN:.3f}", "模型拟合数据")
    with y: metric_card("测试集 C-index", f"{CINDEX_TEST:.3f}", "留出测试数据")
    st.markdown("#### 训练集与测试集表现")
    cindex = pd.DataFrame(
        {"C-index": [CINDEX_TRAIN, CINDEX_TEST]},
        index=["Training set", "Test set"],
    )
    st.bar_chart(cindex, horizontal=True)
    show_figure(
        "AML_LASSO_Cox_Cindex_comparison.png",
        "Training and test-set C-index comparison",
    )
    st.markdown(
        '<div class="warning-panel"><b>结果解读：</b>训练集 C-index 高于测试集，'
        '且测试集 C-index 约为 0.586，提示模型在当前测试集中的区分能力较有限。'
        '不应仅依据训练集表现判断模型泛化能力。</div>',
        unsafe_allow_html=True,
    )
    st.markdown("#### 模型解释")
    st.write(
        "C-index 衡量模型对患者生存时间排序的一致性。当前结果属于内部数据划分下的探索性评价；"
        "尚不能证明模型具有临床预测效能。建议后续开展重复交叉验证、校准评估、"
        "比例风险假设检查及独立外部队列验证。"
    )

elif page == "候选基因":
    st.subheader("候选预后相关基因")
    section_intro("展示 LASSO-Cox 模型系数。正系数与模型估计风险增加方向相关，负系数与风险降低方向相关；该解释不代表因果关系。")
    gene_file = DATA / "AML_LASSO_Cox_selected_genes_threshold_1e-5.csv"
    if gene_file.exists():
        try:
            genes = pd.read_csv(gene_file)
            expected = {"gene", "coefficient", "abs_coefficient"}
            if expected.issubset(genes.columns):
                genes = genes.sort_values("coefficient", ascending=False)
                st.success(f"已读取完整候选基因表：{len(genes)} 个基因")
                st.dataframe(genes, use_container_width=True, hide_index=True)
                st.download_button(
                    "下载候选基因 CSV",
                    data=genes.to_csv(index=False).encode("utf-8-sig"),
                    file_name="AML_LASSO_Cox_selected_genes.csv",
                    mime="text/csv",
                )
                plot_data = genes.set_index("gene")[["coefficient"]]
                st.bar_chart(plot_data)
            else:
                st.error("CSV 列名不符合预期，需要 gene、coefficient、abs_coefficient。")
        except Exception as exc:
            st.error(f"读取候选基因文件失败：{exc}")
    else:
        st.info("当前仓库尚未上传完整的 20 个候选基因 CSV。以下仅展示此前已核实的 5 个代表性系数，不代表完整基因列表。")
        st.dataframe(TOP_GENES, use_container_width=True, hide_index=True)
        st.bar_chart(TOP_GENES.set_index("Gene"))
    show_figure(
        "AML_LASSO_Cox_selected_gene_coefficients.png",
        "Selected-gene coefficient plot",
    )
    show_figure("AML_top20_variable_genes.png", "Top 20 variable genes")

elif page == "方法与局限":
    st.subheader("研究方法")
    st.markdown("""
    **数据来源**  
    GEO 数据集 GSE37642，GPL96 芯片平台。当前分析队列包含 417 例具有可用总生存信息的患者。

    **结局定义**  
    总生存期（OS）作为生存结局；观察到死亡记为事件，随访期间未观察到死亡者记为删失。

    **统计与建模**  
    - Kaplan–Meier 方法描述总体生存情况。
    - Cox 比例风险回归用于生存关联建模。
    - LASSO 惩罚用于特征筛选与模型拟合。
    - 使用 C-index 比较训练集与测试集的区分能力。
    """)
    st.markdown("#### 研究局限")
    st.markdown("""
    1. 当前结果基于单一公开数据集，可能受到样本构成、检测平台及临床变量可用性的影响。
    2. 测试集 C-index 约为 0.586，提示当前模型区分能力有限。
    3. 候选基因系数反映当前模型中的统计关联，不应直接解释为因果效应或临床生物标志物。
    4. 尚需独立外部队列验证、模型校准及临床变量增量价值评估。
    5. 本网页不提供个体化风险计算，也不用于临床诊疗决策。
    """)
    st.markdown("#### 数据与代码")
    st.write("数据集：GSE37642（Gene Expression Omnibus）。")
    st.write("建模框架：Python、pandas、lifelines / scikit-learn（分析环境）。")
    st.write("网页框架：Streamlit。")

st.divider()
st.caption("AML Prognosis Analysis · GSE37642 / GPL96 · Academic research demonstration")
