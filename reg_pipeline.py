# %%
import os
import pandas as pd
from pathlib import Path
import numpy as np
import statsmodels.formula.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import statsmodels.graphics.api as smg
import matplotlib.pyplot as plt
from statsmodels.api import qqplot
from statsmodels.stats.diagnostic import het_white, het_breuschpagan, het_goldfeldquandt, linear_reset
from statsmodels.graphics.regressionplots import plot_fit, plot_regress_exog, influence_plot
import plotly.express as px
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import reset_ramsey
import statsmodels.api
from statistics import median_low
# %%
df = pd.read_csv('features.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Difficulty'] = df['7_plus'] + df['6tries'] + 0.5 * df['5tries']
# convert Has_Uncommon_Letters to 0/1
df['Has_Uncommon_Letters'] = df['Has_Uncommon_Letters'].astype(int)

explanatory_vars = ['Contest_Num', 'Num_Rep_Results', 'Pct_Hard_Mode', 'Has_Uncommon_Letters', 'Distance_To_Wordle_Words', 'Scrabble_Score']
quant_vars = ['Contest_Num', 'Num_Rep_Results', 'Pct_Hard_Mode', 'Distance_To_Wordle_Words', 'Scrabble_Score']
# %%

y_var = 'Difficulty'

def reg_results(df, explanatory_vars, reg_formula, summary=False, multi_col=False, het_tests=False, spec_tests=False, tornado=False):
    res = sm.wls(formula=reg_formula, data=df).fit(cov_type='HC0')
    print(f'R^2: {res.rsquared_adj:.4f}')
    if summary:
        print(res.summary())
    if multi_col:
        clean_df = df[explanatory_vars]
        print(clean_df.T)
        corr_mat = np.corrcoef(clean_df.T)
        plt.rc("figure", figsize=(18, 10))
        smg.plot_corr(corr_mat, xnames=clean_df.columns)
        plt.show()

        vif = pd.DataFrame()
        X = add_constant(clean_df)
        vif["VIF Factor"] = [variance_inflation_factor(
            X.values, i) for i in range(X.shape[1])]
        vif["features"] = X.columns
        print(vif.round(1))
    if het_tests:
        # qqplot(res.resid, line='s')
        gq_test = het_goldfeldquandt(res.resid, res.model.exog, drop=0.2)
        # # white_test = het_white(res.resid, res.model.exog)
        # bp_test = het_breuschpagan(res.resid, res.model.exog)
        # labels = ['LM Statistic', 'LM-Test p-value',
        #           'F-Statistic', 'F-Test p-value']
        print('GQ', dict(
            zip(['Test Statistic', 'p-value', 'Ordering'], gq_test)))
        print(f'Goldfeld-Quandt, p-value: {gq_test[1]:.4f}')
        # print('White', dict(zip(labels, white_test)))
        # print('BP', dict(zip(labels, bp_test)))
        # print(f'Breusch-Pagan, p-value: {bp_test[1]}')
        # for x in explanatory_vars:
        #     # plot residuals vs variable
        #     plt.figure(figsize=(6, 4))
        #     plt.plot(dropped_df[x], res.resid, 'o')
        #     plt.axhline(y=0, color='black')
        #     plt.xlabel(x)
        #     plt.ylabel('Residuals')
        #     plt.title(f'Residuals vs {x}')
    if spec_tests:
        print('Ramsey RESET', reset_ramsey(res))
    if tornado:
        reg_tornado(res, y_var)


def reg_tornado(res, y_var):
    P_VAL_MAX = 0.05
    significant_vars = res.pvalues[res.pvalues < P_VAL_MAX].index
    if 'Intercept' in significant_vars:
        significant_vars = significant_vars.drop('Intercept')
    # Beta* coefficients
    b_star_coeffs = []
    sy = df[y_var].std()
    for var in significant_vars:
        if var in quant_vars:
            sx = df[var].std()
        else:
            sx = 1
        # beta star coefficient
        b_star_coeffs.append((var, res.params[var] * sx / sy))

    b_star_coeffs.sort(key=lambda x: abs(x[1]), reverse=True)
    for line in b_star_coeffs:
        print(line)

    x = [b_star_coeffs[i][0] for i in range(len(b_star_coeffs))]
    y = [b_star_coeffs[i][1] for i in range(len(b_star_coeffs))]
    for i in range(len(b_star_coeffs) - 1, -1, -1):
        pass
        # if x[i] in quant_vars:
        #     del x[i]
        #     del y[i]

    plt.figure(figsize=(12, 8))
    plt.title(f'Beta* Coefficients for {y_var}')
    sns.barplot(x=y, y=x, orient='h')
# %%
reg_formula =  f'{y_var} ~ {" + ".join(explanatory_vars)}'
reg_results(df, explanatory_vars, reg_formula, summary=True, multi_col=True, het_tests=True, spec_tests=True, tornado=True)
# %%
