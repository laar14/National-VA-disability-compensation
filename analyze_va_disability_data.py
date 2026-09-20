"""
U.S. Veterans Disability Compensation Analysis Pipeline
-------------------------------------------------------
Clean raw county-level dataset and generate publication-quality figures
for GitHub repository presentation.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def run_analysis(data_path='/workspace/knowledge/export.csv', output_dir='/workspace/scratch'):
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')
    CHART_DPI = 150

    # Load dataset
    df = pd.read_csv(data_path)

    # Clean numeric columns
    num_cols = [
        'Total: Disability Compensation Recipients',
        'SCD rating: 0% to 20%', 'SCD rating: 30% to 40%',
        'SCD rating: 50% to 60%', 'SCD rating: 70% to 90%',
        'SCD rating: 100%', 'Age: 17-44', 'Age: 45-64',
        'Age: 65 or older', 'Male', 'Female'
    ]

    for col in num_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce')

    states_df = df[~df['State'].isin(['Other Foreign Countries', 'Unknown'])].groupby('State')[num_cols].sum()

    # ---------------------------------------------------------
    # Chart 1: Top 10 States Horizontal Bar Chart
    # ---------------------------------------------------------
    top10 = states_df['Total: Disability Compensation Recipients'].nlargest(10).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top10.index, top10.values / 1000, color='#1f77b4', edgecolor='none', height=0.65)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 5, bar.get_y() + bar.get_height()/2, f'{w:.1f}K', va='center', ha='left', fontweight='bold', fontsize=10, color='#222222')

    ax.set_xlim(0, max(top10.values / 1000) * 1.15)
    ax.set_title('Texas, Florida, and California Lead Nation with 1.72M VA Disability Recipients Combined', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Total Recipients (Thousands)', fontsize=11, fontweight='bold')
    ax.set_ylabel('State / Jurisdiction', fontsize=11, fontweight='bold')
    ax.text(0, -0.12, 'Source: U.S. Department of Veterans Affairs Disability Compensation Dataset', transform=ax.transAxes, fontsize=8, color='gray')
    sns.despine(top=True, right=True)
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'top_states_va_recipients.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # Chart 2: Disability Rating Severity Distribution
    # ---------------------------------------------------------
    ratings_cols = ['SCD rating: 0% to 20%', 'SCD rating: 30% to 40%', 'SCD rating: 50% to 60%', 'SCD rating: 70% to 90%', 'SCD rating: 100%']
    ratings_labels = ['0% - 20%', '30% - 40%', '50% - 60%', '70% - 90%', '100% (Total)']
    ratings_vals = df[ratings_cols].sum().values / 1000
    total_val = df['Total: Disability Compensation Recipients'].sum() / 1000

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('Blues_d', n_colors=5)
    bars = ax.bar(ratings_labels, ratings_vals, color=colors, width=0.55)

    for bar in bars:
        h = bar.get_height()
        pct = (h / total_val) * 100
        ax.text(bar.get_x() + bar.get_width()/2, h + 30, f'{h:,.0f}K\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=9.5)

    ax.set_ylim(0, max(ratings_vals) * 1.2)
    ax.set_title('Severe Ratings Dominate: 58.7% of Veterans Have 70% to 100% Disability Rating', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Service-Connected Disability (SCD) Rating Tier', fontsize=11, fontweight='bold')
    ax.set_ylabel('Recipients (Thousands)', fontsize=11, fontweight='bold')
    ax.text(0, -0.12, 'Source: U.S. Department of Veterans Affairs Disability Compensation Dataset', transform=ax.transAxes, fontsize=8, color='gray')
    sns.despine(top=True, right=True)
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'va_disability_rating_severity.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # Chart 3: Age & Gender Demographics Breakdown
    # ---------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle('Demographic Breakdown: Veterans 65+ Represent 37.8% of Recipients; Women Comprise 12.7%', fontsize=13, fontweight='bold', y=1.02)

    # Subplot 1: Age
    age_cols = ['Age: 17-44', 'Age: 45-64', 'Age: 65 or older']
    age_labels = ['17 - 44 yrs', '45 - 64 yrs', '65+ yrs']
    age_vals = df[age_cols].sum().values / 1000

    bars1 = ax1.bar(age_labels, age_vals, color=['#2b5c8f', '#4682b4', '#6baed6'], width=0.5)
    for bar in bars1:
        h = bar.get_height()
        pct = (h / total_val) * 100
        ax1.text(bar.get_x() + bar.get_width()/2, h + 30, f'{h:,.0f}K ({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=9.5)

    ax1.set_ylim(0, max(age_vals) * 1.18)
    ax1.set_title('Recipients by Age Group', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Recipients (Thousands)', fontsize=10, fontweight='bold')
    sns.despine(ax=ax1, top=True, right=True)

    # Subplot 2: Gender
    gender_cols = ['Male', 'Female']
    gender_vals = df[gender_cols].sum().values / 1000

    bars2 = ax2.bar(['Male', 'Female'], gender_vals, color=['#3182bd', '#e6550d'], width=0.45)
    for bar in bars2:
        h = bar.get_height()
        pct = (h / total_val) * 100
        ax2.text(bar.get_x() + bar.get_width()/2, h + 50, f'{h:,.0f}K ({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=9.5)

    ax2.set_ylim(0, max(gender_vals) * 1.18)
    ax2.set_title('Recipients by Gender', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Recipients (Thousands)', fontsize=10, fontweight='bold')
    sns.despine(ax=ax2, top=True, right=True)

    fig.text(0.05, -0.05, 'Source: U.S. Department of Veterans Affairs Disability Compensation Dataset', fontsize=8, color='gray')
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(output_dir, 'va_disability_demographics.png'), dpi=CHART_DPI, bbox_inches='tight')
    plt.close()

    print(f'Successfully generated all VA disability analysis charts in {output_dir}')

if __name__ == '__main__':
    run_analysis()
