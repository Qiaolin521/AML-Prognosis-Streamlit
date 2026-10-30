# AML Prognosis Analysis

An interactive research dashboard for exploratory overall-survival analysis in acute myeloid leukemia (AML), based on GEO dataset **GSE37642** and platform **GPL96**.

## Dashboard

The Streamlit application presents:
- Cohort overview (417 patients; 308 observed deaths; 109 censored observations)
- Kaplan–Meier survival analysis figures
- Exploratory LASSO-Cox model performance (training C-index ≈ 0.678; test C-index ≈ 0.586)
- Candidate prognostic-gene coefficients
- Methods, interpretation, and study limitations

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Optional result files

To display the original analysis figures, create an `assets/` folder and add the corresponding PNG files:

- `AML_overall_KM_curve.png`
- `AML_test_risk_group_KM.png`
- `AML_survival_outcome_distribution.png`
- `AML_survival_time_distribution.png`
- `AML_LASSO_Cox_Cindex_comparison.png`
- `AML_LASSO_Cox_selected_gene_coefficients.png`
- `AML_top20_variable_genes.png`

To display the complete selected-gene table, place
`AML_LASSO_Cox_selected_genes_threshold_1e-5.csv` in the `data/` folder.
The CSV should contain columns: `gene`, `coefficient`, and `abs_coefficient`.

Only aggregate results and figures should be published. Do not upload raw expression matrices or patient-level clinical data to a public repository.

## Important notice

This is an academic and educational demonstration. The model is exploratory, has limited discrimination in the current test set, and has not undergone independent external validation. It must not be used for individual patient prognosis or clinical decision-making.
