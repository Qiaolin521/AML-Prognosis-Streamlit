from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AML Prognosis Analysis",
    page_icon="🧬",
    layout="wide"
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

st.title("AML Prognosis Analysis")
st.caption("GSE37642 · GPL96 · Bioinformatics Course Project")

st.markdown("""
This project explores overall survival in acute myeloid leukemia (AML) using
the GSE37642 gene-expression dataset. The webpage summarizes cohort
characteristics, Kaplan–Meier survival analyses, a LASSO-Cox model, and
candidate prognostic genes.
""")

st.warning(
    "For research and educational demonstration only. This exploratory model "
    "is not validated for clinical decision-making. Independent validation is required."
)

st.header("1. Dataset overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Patients analyzed", "417")
c2.metric("Observed deaths", "308")
c3.metric("Censored observations", "109")
c4.metric("Median overall survival", "329 days")

st.write(
    "The analysis cohort included 417 patients with available overall-survival "
    "information. There were 308 observed death events and 109 censored observations."
)

def show_figure(filename, caption):
    image_path = ASSETS / filename
    if image_path.exists():
        st.image(str(image_path), caption=caption, use_container_width=True)
    else:
        st.info(f"Figure pending upload: assets/{filename}")

st.header("2. Survival analysis")
left, right = st.columns(2)
with left:
    show_figure("AML_overall_KM_curve.png", "Overall Kaplan–Meier survival curve")
with right:
    show_figure("AML_test_risk_group_KM.png", "Test-set risk-group Kaplan–Meier curve")

show_figure("AML_survival_outcome_distribution.png", "Distribution of survival outcomes")
show_figure("AML_survival_time_distribution.png", "Distribution of overall survival time")

st.header("3. LASSO-Cox prognostic model")
st.markdown("""
The LASSO-Cox model was developed using a training/test split. The concordance
index (C-index) was approximately **0.678 in the training set** and
**0.586 in the test set**. The lower test-set C-index indicates limited
discrimination in this evaluation and suggests that further model development
and independent validation are necessary.
""")
show_figure("AML_LASSO_Cox_Cindex_comparison.png", "Training and test-set C-index comparison")

st.header("4. Candidate genes")
st.write(
    "The following table will display the 20 genes selected using the "
    "coefficient threshold of 1e-5 once the result CSV is added to the data folder."
)

gene_csv = DATA / "AML_LASSO_Cox_selected_genes_threshold_1e-5.csv"
if gene_csv.exists():
    try:
        genes = pd.read_csv(gene_csv)
        if {"gene", "coefficient", "abs_coefficient"}.issubset(genes.columns):
            genes = genes.sort_values("coefficient", ascending=False)
            st.dataframe(genes, use_container_width=True, hide_index=True)
            st.download_button(
                "Download candidate-gene table",
                data=genes.to_csv(index=False).encode("utf-8-sig"),
                file_name="AML_candidate_genes.csv",
                mime="text/csv"
            )
        else:
            st.error("The candidate-gene CSV does not contain the expected columns.")
    except Exception as error:
        st.error(f"Unable to read the candidate-gene CSV: {error}")
else:
    st.info("Upload the selected-gene CSV to data/ to display the complete table.")

show_figure(
    "AML_LASSO_Cox_selected_gene_coefficients.png",
    "Selected-gene coefficient plot"
)

st.header("5. Methods and limitations")
st.markdown("""
- **Dataset:** GSE37642, GPL96 platform.
- **Outcome:** Overall survival; death was treated as the event and follow-up
  without an observed death was treated as censored.
- **Model:** LASSO-penalized Cox proportional hazards model.
- **Interpretation:** Model coefficients describe associations within this
  fitted model and do not establish causality.
- **Limitations:** Test-set discrimination was modest. The candidate genes and
  model require further statistical assessment, biological interpretation,
  and independent-cohort validation.
""")

st.caption("Built with Streamlit · Academic demonstration only")
