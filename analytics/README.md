## Module 2 — Analytics Pipeline

### Overview

The Analytics module implements an end-to-end data analysis and machine
learning workflow using the Titanic dataset.

The workflow is:

**Data Loading → Profiling → Cleaning → EDA → Preprocessing →
Classification → Model Evaluation → Imbalance Analysis →
Hyperparameter Tuning → Regression**

The module is organized into two notebooks:

- `analytics/01_eda.ipynb`
- `analytics/02_modeling.ipynb`

The Titanic dataset is loaded once in the EDA notebook and saved as
`analytics/titanic.csv`. The modeling notebook continues from this saved
dataset rather than independently loading the raw dataset again.

### Install packages
Before starting we should install requirements.txt file for packages
which could be used in notebooks as (import pandas as pd,etc)

### Data Loading and Profiling

The Titanic dataset is loaded using:

`sns.load_dataset("titanic")`

The initial analysis includes:

- Dataset information
- Descriptive statistics
- Dataset shape
- Missing-value percentages
- Data quality inspection

The original dataset is also saved as `titanic.csv` as an offline
fallback.

### Missing-Value Handling

Missing values are handled using the percentage-based strategy required
by the project:

- Less than 5% missing → affected rows are dropped.
- 5% to 30% missing → values are imputed.
- Columns with very high missingness are evaluated separately and a
  documented decision is made rather than blindly imputing them.

The missing-value percentage is reported before applying the selected
strategy.

** After cleaning the missing data the file is saved as `titanic_clean.csv`.
Here on own we use this cleaned dataset as working data.

*** Note:After imputation the missing values basically we detect the duplicates in data
and delete by ".drop_duplicates()".But as per project instructions duplication is not
mention to do.So i won't perform the duplication for cleaned data.

### Exploratory Data Analysis

The EDA includes:

- Histograms for age and fare
- Box plots for age and fare
- IQR-based outlier analysis
- Mean, median and mode analysis for fare
- Survival-rate analysis by sex
- Survival-rate analysis by passenger class
- Survival-rate analysis by sex and passenger class
- Correlation analysis
- Correlation heatmap
- Multivariate visualizations

The correlation matrix uses the required six columns:

- survived
- pclass
- age
- sibsp
- parch
- fare

The EDA visualizations are accompanied by written interpretations.

### Standardization Check

Age and fare are standardized during the exploratory analysis to verify
the effect of standardization.

The before-and-after distributions/statistics are compared to confirm
that the transformed variables have approximately zero mean and unit
standard deviation.

### Classification Modeling

The classification target is:

`survived`

A stratified train/test split is used so that the class distribution is
preserved between the training and testing datasets.

Three classifiers are trained on the same train/test split:

1. Logistic Regression
2. Decision Tree
3. Random Forest

The Decision Tree is also visualized using `plot_tree`.

### Preprocessing

Preprocessing is performed only using the training data.

The workflow includes:

- Missing-value imputation (this uses clean data so imputation is optional)
- Categorical encoding
- Numerical feature scaling using `StandardScaler`

The preprocessing steps are applied through the modeling pipeline so that
test-set information does not leak into training.

### Model Evaluation

The classifiers are evaluated using:

- Confusion matrix
- Accuracy
- Precision
- Recall
- F1 score
- ROC curve
- ROC-AUC

The results are presented together for comparison.

### Class Imbalance Analysis

The survived/not-survived class distribution is examined.

A classification model is compared using three approaches:

1. Baseline without imbalance handling
2. `class_weight="balanced"`
3. SMOTE oversampling

SMOTE is applied only to the training fold to avoid test-data leakage.

Precision, recall and F1 score are compared across the three approaches.

### Random Forest Hyperparameter Tuning

`GridSearchCV` is used to tune the Random Forest.

The search includes:

- `n_estimators`
- `max_depth`
- `max_features`

The tuned Random Forest is configured with `oob_score=True`, allowing
the out-of-bag score to be reported.

### Regression Side Task

A multivariate linear regression model is used to predict `fare` from the
available features.

The regression model is evaluated using:

- MAE
- RMSE
- R²
- Adjusted R²

A residual plot is also produced and interpreted to assess whether the
residuals show heteroscedasticity.

### Model Comparison

The final analysis contains a model comparison table.

Classification metrics are reported separately from regression metrics
because they measure different types of predictive performance.

The classification models are compared using:

- Accuracy
- Precision
- Recall
- F1
- AUC

The regression model is reported using:

- MAE
- RMSE
- R²
- Adjusted R²

### Saved Model

The complete fitted preprocessing and modeling pipeline is saved as a
single artifact using `joblib`.

The saved pipeline includes the preprocessing steps together with the
final estimator so that it can be reused with raw input data.

The saved artifact is also reloaded and tested to confirm that it can
produce predictions successfully.

### Design Decisions

1. **The Titanic dataset is loaded only once** and then saved as
   `titanic.csv` after cleaning the data it saved as 
   `titanic_clean.csv` so that the rest of the workflow can run from 
   the same dataset.
2. **A stratified train/test split** is used because the classification
   target has two classes and stratification preserves their distribution.
3. **Pipeline-based preprocessing** is used to ensure that imputers,
   encoders and scalers are fitted only on training data.
4. **Three classifiers** are trained on the same split to make their
   evaluation comparable.
5. **SMOTE is applied only to the training fold** to prevent data leakage.
6. **GridSearchCV** is used to tune Random Forest hyperparameters.
7. **The complete preprocessing + estimator pipeline** is saved with
   `joblib` so that predictions can be made directly from raw input data.