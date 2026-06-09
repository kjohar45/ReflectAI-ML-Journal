import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

# Set a clean, print-friendly style
plt.style.use('grayscale')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8

OUTPUT_DIR = "/Users/sy/IdeaProjects/AI Journal Companion/paper_graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate Heavy Data (30 Days)
np.random.seed(42)
days = np.arange(1, 31)

# Base sentiment starting somewhat positive, drifting down, then recovering
raw_trend = np.sin(days / 4.0) * 0.4 + 0.1
noise = np.random.normal(0, 0.15, 30)
sentiment_scores = np.clip(raw_trend + noise, -1.0, 1.0)

# Calculate EDS natively
mean_stable = 0.3
std_stable = 0.15
eds_scores = np.abs(sentiment_scores - mean_stable) / std_stable
# smooth EDS slightly for visual clarity
eds_scores = np.convolve(eds_scores, np.ones(3)/3, mode='same')
eds_scores = np.clip(eds_scores, 0, 3.5)


def generate_figure2():
    plt.figure(figsize=(10, 6))
    
    plt.plot(days, sentiment_scores, marker='o', color='black', markerfacecolor='white', markeredgewidth=1.5)
    
    # Shade decline period (e.g. Days 10 to 20 where score drops below 0)
    decline_mask = sentiment_scores < 0
    plt.fill_between(days, sentiment_scores, 0, where=decline_mask, color='lightgray', alpha=0.5)

    # Drift Point Line around Day 12
    plt.axvline(x=12, color='gray', linestyle='--')
    plt.text(12, 0.9, r'$\leftarrow$ Drift Point $\rightarrow$', ha='center', fontsize=10, color='black')

    # Highlight a specific low point
    min_idx = np.argmin(sentiment_scores)
    plt.plot(days[min_idx], sentiment_scores[min_idx], marker='o', color='black', markersize=10)

    plt.ylim(-1.0, 1.0)
    plt.xlim(1, 30)
    plt.xlabel('Time (Days)', fontsize=12)
    plt.ylabel('Sentiment Score', fontsize=12)
    plt.title('FIGURE 2 — Emotional Trend Over 30-Day Period', fontsize=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'FIGURE_2_Trend.png'), dpi=300)
    plt.close()


def generate_figure3():
    plt.figure(figsize=(10, 6))

    plt.plot(days, eds_scores, marker='o', color='black', markerfacecolor='white', markeredgewidth=1.5)

    # Threshold line at EDS = 2.0
    plt.axhline(y=2.0, color='black', linestyle='--', linewidth=2)
    plt.text(26, 2.1, 'Threshold (EDS = 2.0)', ha='center', fontsize=10)

    # Shade where EDS > 2.0
    spike_mask = eds_scores > 2.0
    plt.fill_between(days, eds_scores, 0, where=spike_mask, color='lightgray', alpha=0.6)

    # Highlight max EDS
    max_idx = np.argmax(eds_scores)
    plt.plot(days[max_idx], eds_scores[max_idx], marker='o', color='black', markersize=10)

    plt.ylim(0, 3.5)
    plt.xlim(1, 30)
    plt.xlabel('Time (Days)', fontsize=12)
    plt.ylabel('Drift Score (EDS)', fontsize=12)
    plt.title('FIGURE 3 — Emotional Drift Detection (EDS)', fontsize=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'FIGURE_3_EDS.png'), dpi=300)
    plt.close()


def generate_figure5():
    # Heavy sample state transitions matrix (3x3)
    # Rows: From State (Positive, Neutral, Negative)
    # Cols: To State (Positive, Neutral, Negative)
    # Using specific probabilities
    data = np.array([
        [0.65, 0.25, 0.10],
        [0.20, 0.55, 0.25],
        [0.10, 0.35, 0.55]
    ])
    
    plt.figure(figsize=(8, 6))
    
    sns.heatmap(data, annot=True, fmt=".2f", cmap="Greys", 
                xticklabels=["Positive", "Neutral", "Negative"],
                yticklabels=["Positive", "Neutral", "Negative"],
                cbar_kws={'label': 'Intensity: Low probability ⟶ High probability'},
                linewidths=1, linecolor='black')

    plt.xlabel('To State \u2192', fontsize=12, labelpad=10)
    plt.ylabel('\u2190 From State', fontsize=12, labelpad=10)
    plt.title('FIGURE 5 — Emotional State Transition Matrix (Heavy Sample)', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'FIGURE_5_Matrix.png'), dpi=300)
    plt.close()


def export_datasets():
    # Folder 1: Trend Data
    trend_dir = os.path.join(OUTPUT_DIR, "Dataset_Trend")
    os.makedirs(trend_dir, exist_ok=True)
    df_trend = pd.DataFrame({
        'Day': days,
        'Raw_Trend': raw_trend,
        'Noise': noise,
        'Final_Sentiment_Score': sentiment_scores
    })
    df_trend.to_csv(os.path.join(trend_dir, 'figure2_trend_data.csv'), index=False)

    # Folder 2: EDS Data
    eds_dir = os.path.join(OUTPUT_DIR, "Dataset_EDS")
    os.makedirs(eds_dir, exist_ok=True)
    df_eds = pd.DataFrame({
        'Day': days,
        'Base_Sentiment': sentiment_scores,
        'Calculated_EDS': eds_scores,
        'EDS_Threshold_Exceeded': eds_scores > 2.0
    })
    df_eds.to_csv(os.path.join(eds_dir, 'figure3_eds_data.csv'), index=False)

    # Folder 3: Transition Matrix Data
    matrix_dir = os.path.join(OUTPUT_DIR, "Dataset_Transition_Matrix")
    os.makedirs(matrix_dir, exist_ok=True)
    
    data = np.array([
        [0.65, 0.25, 0.10],
        [0.20, 0.55, 0.25],
        [0.10, 0.35, 0.55]
    ])
    df_matrix = pd.DataFrame(data, 
                             index=["From_Positive", "From_Neutral", "From_Negative"],
                             columns=["To_Positive", "To_Neutral", "To_Negative"])
    df_matrix.to_csv(os.path.join(matrix_dir, 'figure5_transition_probabilities.csv'))


if __name__ == "__main__":
    generate_figure2()
    generate_figure3()
    generate_figure5()
    export_datasets()
    print(f"✅ Generated all 3 high-resolution paper graphs in: {OUTPUT_DIR}")
    print(f"✅ Exported 3 datasets into discrete subfolders within {OUTPUT_DIR}/")
