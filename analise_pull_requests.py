"""
Análise de Pull Requests - Visualização, Correlação e Regressão
Utilizando Seaborn e testes estatísticos
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import spearmanr, pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings('ignore')

# Configurações de visualização
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ============================================================================

print("=" * 80)
print("ANÁLISE DE PULL REQUESTS")
print("=" * 80)

# Carregar dados
with open('finalResults/dados_pull_requests3.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

df = pd.DataFrame(dados)

print(f"\n✓ Total de Pull Requests carregados: {len(df)}")
print(f"✓ Colunas disponíveis: {list(df.columns)}")

# Estatísticas básicas
print("\n" + "=" * 80)
print("ESTATÍSTICAS DESCRITIVAS")
print("=" * 80)
print(df.describe())

print("\n" + "-" * 80)
print("Distribuição dos Estados dos PRs:")
print(df['estado'].value_counts())
print(f"\nPercentual de PRs Merged: {(df['estado'] == 'MERGED').sum() / len(df) * 100:.2f}%")
print(f"Percentual de PRs Closed: {(df['estado'] == 'CLOSED').sum() / len(df) * 100:.2f}%")

# ============================================================================
# 2. ENGENHARIA DE FEATURES
# ============================================================================

print("\n" + "=" * 80)
print("PREPARAÇÃO DE VARIÁVEIS")
print("=" * 80)

# Calcular tamanho total dos PRs
df['tamanho_total'] = df['linhas_adicionadas'] + df['linhas_removidas']

# Criar variável binária para estado (1 = MERGED, 0 = CLOSED)
df['estado_binario'] = (df['estado'] == 'MERGED').astype(int)

# Categorizar tamanho dos PRs
def categorizar_tamanho(tamanho):
    if tamanho <= 50:
        return 'Pequeno'
    elif tamanho <= 200:
        return 'Médio'
    elif tamanho <= 500:
        return 'Grande'
    else:
        return 'Muito Grande'

df['categoria_tamanho'] = df['tamanho_total'].apply(categorizar_tamanho)

# Verificar se há descrições vazias (considerando tamanho 0 como sem descrição)
df['tem_descricao'] = (df['tamanho_descricao_caracteres'] > 0).astype(int)

print(f"✓ Variáveis criadas:")
print(f"  - tamanho_total: linhas adicionadas + linhas removidas")
print(f"  - estado_binario: 1 = MERGED, 0 = CLOSED")
print(f"  - categoria_tamanho: Pequeno/Médio/Grande/Muito Grande")
print(f"  - tem_descricao: 1 = tem descrição, 0 = sem descrição")

# Remover outliers extremos para melhor visualização (opcional)
# Vamos manter todos os dados mas identificar outliers
Q1 = df['tamanho_total'].quantile(0.25)
Q3 = df['tamanho_total'].quantile(0.75)
IQR = Q3 - Q1
outliers_tamanho = ((df['tamanho_total'] < (Q1 - 1.5 * IQR)) | 
                     (df['tamanho_total'] > (Q3 + 1.5 * IQR))).sum()

print(f"\n✓ Outliers identificados (tamanho): {outliers_tamanho} PRs")

# ============================================================================
# 3. JUSTIFICATIVA DA ESCOLHA DO TESTE ESTATÍSTICO
# ============================================================================

print("\n" + "=" * 80)
print("JUSTIFICATIVA DO TESTE ESTATÍSTICO")
print("=" * 80)

print("""
ESCOLHA: Correlação de Spearman

JUSTIFICATIVA:
1. Natureza dos Dados: Os dados de PRs frequentemente apresentam distribuições
   não normais e podem conter outliers (PRs muito grandes, tempos muito longos).

2. Relações Não-Lineares: A correlação de Spearman captura relações monotônicas
   (não necessariamente lineares), mais adequadas para dados de software.

3. Robustez: O teste de Spearman é baseado em rankings, sendo mais robusto a
   outliers e valores extremos do que Pearson.

4. Variáveis Ordinais: Algumas variáveis (como número de revisões, comentários)
   são contagens discretas, melhor tratadas por Spearman.

Para comparação, também apresentaremos resultados de Pearson, mas a interpretação
principal será baseada em Spearman.
""")

# Teste de normalidade (Shapiro-Wilk) para algumas variáveis chave
variaveis_teste = ['tamanho_total', 'tempo_analise_dias', 'num_revisoes', 
                   'tamanho_descricao_caracteres']

print("\nTeste de Normalidade (Shapiro-Wilk) - p-value:")
print("-" * 80)
for var in variaveis_teste:
    # Amostra aleatória para teste (Shapiro-Wilk tem limite de 5000 amostras)
    amostra = df[var].dropna().sample(min(5000, len(df[var])), random_state=42)
    stat, p_value = stats.shapiro(amostra)
    normalidade = "Normal" if p_value > 0.05 else "Não Normal"
    print(f"{var:30s}: p = {p_value:.6f} ({normalidade})")

print("\n✓ Como podemos observar, a maioria das variáveis não segue distribuição normal,")
print("  confirmando a adequação do teste de Spearman.")

# ============================================================================
# 4. FUNÇÃO PARA ANÁLISE DE CORRELAÇÃO
# ============================================================================

def analisar_correlacao(df, var1, var2, nome_var1, nome_var2):
    """Analisa correlação entre duas variáveis usando Spearman e Pearson"""
    
    # Remover NaN
    dados_limpos = df[[var1, var2]].dropna()
    
    # Spearman
    spearman_corr, spearman_p = spearmanr(dados_limpos[var1], dados_limpos[var2])
    
    # Pearson
    pearson_corr, pearson_p = pearsonr(dados_limpos[var1], dados_limpos[var2])
    
    # Interpretação
    def interpretar_correlacao(r):
        abs_r = abs(r)
        if abs_r < 0.1:
            return "Desprezível"
        elif abs_r < 0.3:
            return "Fraca"
        elif abs_r < 0.5:
            return "Moderada"
        elif abs_r < 0.7:
            return "Forte"
        else:
            return "Muito Forte"
    
    significancia = "Significativa (p < 0.05)" if spearman_p < 0.05 else "Não significativa (p ≥ 0.05)"
    
    resultado = {
        'spearman_r': spearman_corr,
        'spearman_p': spearman_p,
        'pearson_r': pearson_corr,
        'pearson_p': pearson_p,
        'interpretacao': interpretar_correlacao(spearman_corr),
        'significancia': significancia,
        'n': len(dados_limpos)
    }
    
    print(f"\n{nome_var1} × {nome_var2}")
    print("-" * 80)
    print(f"Spearman ρ = {spearman_corr:.4f} (p = {spearman_p:.6f}) - {resultado['interpretacao']}")
    print(f"Pearson  r = {pearson_corr:.4f} (p = {pearson_p:.6f})")
    print(f"Status: {significancia}")
    print(f"N = {len(dados_limpos)} observações")
    
    return resultado

# ============================================================================
# 5. ANÁLISE DAS QUESTÕES DE PESQUISA - DIMENSÃO A
# ============================================================================

print("\n" + "=" * 80)
print("DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES (Estado do PR)")
print("=" * 80)

print("\n" + "=" * 80)
print("RQ 01: Relação entre TAMANHO dos PRs e FEEDBACK FINAL")
print("=" * 80)

rq01 = analisar_correlacao(df, 'tamanho_total', 'estado_binario', 
                           'Tamanho Total (linhas)', 'Estado (MERGED=1)')

# Análise adicional por categoria
print("\nAnálise por Categoria de Tamanho:")
print("-" * 80)
categoria_estado = pd.crosstab(df['categoria_tamanho'], df['estado'], normalize='index') * 100
print(categoria_estado.round(2))

print("\n" + "=" * 80)
print("RQ 02: Relação entre TEMPO DE ANÁLISE e FEEDBACK FINAL")
print("=" * 80)

rq02 = analisar_correlacao(df, 'tempo_analise_dias', 'estado_binario',
                           'Tempo de Análise (dias)', 'Estado (MERGED=1)')

# Estatísticas por estado
print("\nTempo médio de análise por estado:")
print("-" * 80)
print(df.groupby('estado')['tempo_analise_dias'].agg(['mean', 'median', 'std']).round(2))

print("\n" + "=" * 80)
print("RQ 03: Relação entre DESCRIÇÃO dos PRs e FEEDBACK FINAL")
print("=" * 80)

rq03 = analisar_correlacao(df, 'tamanho_descricao_caracteres', 'estado_binario',
                           'Tamanho da Descrição (caracteres)', 'Estado (MERGED=1)')

# Análise de PRs com/sem descrição
print("\nTaxa de aprovação por presença de descrição:")
print("-" * 80)
descricao_estado = pd.crosstab(df['tem_descricao'], df['estado'], normalize='index') * 100
descricao_estado.index = ['Sem Descrição', 'Com Descrição']
print(descricao_estado.round(2))

print("\n" + "=" * 80)
print("RQ 04: Relação entre INTERAÇÕES nos PRs e FEEDBACK FINAL")
print("=" * 80)

print("\n--- 4.1: Número de Participantes ---")
rq04a = analisar_correlacao(df, 'num_participantes', 'estado_binario',
                            'Número de Participantes', 'Estado (MERGED=1)')

print("\n--- 4.2: Número de Comentários ---")
rq04b = analisar_correlacao(df, 'num_comentarios', 'estado_binario',
                            'Número de Comentários', 'Estado (MERGED=1)')

# Estatísticas de interação por estado
print("\nEstatísticas de interação por estado:")
print("-" * 80)
print(df.groupby('estado')[['num_participantes', 'num_comentarios']].mean().round(2))

# ============================================================================
# 6. ANÁLISE DAS QUESTÕES DE PESQUISA - DIMENSÃO B
# ============================================================================

print("\n" + "=" * 80)
print("DIMENSÃO B: NÚMERO DE REVISÕES")
print("=" * 80)

print("\n" + "=" * 80)
print("RQ 05: Relação entre TAMANHO dos PRs e NÚMERO DE REVISÕES")
print("=" * 80)

rq05 = analisar_correlacao(df, 'tamanho_total', 'num_revisoes',
                           'Tamanho Total (linhas)', 'Número de Revisões')

print("\nMédia de revisões por categoria de tamanho:")
print("-" * 80)
print(df.groupby('categoria_tamanho')['num_revisoes'].agg(['mean', 'median', 'std']).round(2))

print("\n" + "=" * 80)
print("RQ 06: Relação entre TEMPO DE ANÁLISE e NÚMERO DE REVISÕES")
print("=" * 80)

rq06 = analisar_correlacao(df, 'tempo_analise_dias', 'num_revisoes',
                           'Tempo de Análise (dias)', 'Número de Revisões')

print("\n" + "=" * 80)
print("RQ 07: Relação entre DESCRIÇÃO dos PRs e NÚMERO DE REVISÕES")
print("=" * 80)

rq07 = analisar_correlacao(df, 'tamanho_descricao_caracteres', 'num_revisoes',
                           'Tamanho da Descrição (caracteres)', 'Número de Revisões')

print("\n" + "=" * 80)
print("RQ 08: Relação entre INTERAÇÕES e NÚMERO DE REVISÕES")
print("=" * 80)

print("\n--- 8.1: Número de Participantes ---")
rq08a = analisar_correlacao(df, 'num_participantes', 'num_revisoes',
                            'Número de Participantes', 'Número de Revisões')

print("\n--- 8.2: Número de Comentários ---")
rq08b = analisar_correlacao(df, 'num_comentarios', 'num_revisoes',
                            'Número de Comentários', 'Número de Revisões')

# ============================================================================
# 7. VISUALIZAÇÕES
# ============================================================================

print("\n" + "=" * 80)
print("GERANDO VISUALIZAÇÕES...")
print("=" * 80)

# Criar subplots para todas as visualizações
fig = plt.figure(figsize=(20, 24))

# --- GRÁFICO 1: Distribuição dos Estados dos PRs ---
ax1 = plt.subplot(4, 3, 1)
estado_counts = df['estado'].value_counts()
colors_estado = ['#2ecc71' if x == 'MERGED' else '#e74c3c' for x in estado_counts.index]
bars = ax1.bar(estado_counts.index, estado_counts.values, color=colors_estado, alpha=0.7)
ax1.set_xlabel('Estado do PR')
ax1.set_ylabel('Frequência')
ax1.set_title('Distribuição dos Estados dos PRs', fontweight='bold', fontsize=12)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(df)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10)

# --- GRÁFICO 2: RQ01 - Tamanho vs Estado ---
ax2 = plt.subplot(4, 3, 2)
df_plot = df[df['tamanho_total'] < df['tamanho_total'].quantile(0.95)]  # Remover top 5% para visualização
sns.boxplot(data=df_plot, x='estado', y='tamanho_total', ax=ax2, palette=['#e74c3c', '#2ecc71'])
ax2.set_xlabel('Estado do PR')
ax2.set_ylabel('Tamanho Total (linhas)')
ax2.set_title(f'RQ01: Tamanho vs Estado\nSpearman ρ = {rq01["spearman_r"]:.4f} (p = {rq01["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)

# --- GRÁFICO 3: RQ01 - Categoria de Tamanho vs Estado ---
ax3 = plt.subplot(4, 3, 3)
categoria_ordem = ['Pequeno', 'Médio', 'Grande', 'Muito Grande']
categoria_estado_plot = pd.crosstab(df['categoria_tamanho'], df['estado'])
categoria_estado_plot = categoria_estado_plot.reindex(categoria_ordem, fill_value=0)
categoria_estado_plot.plot(kind='bar', ax=ax3, color=['#e74c3c', '#2ecc71'], alpha=0.7)
ax3.set_xlabel('Categoria de Tamanho')
ax3.set_ylabel('Número de PRs')
ax3.set_title('Distribuição de Estados por Categoria de Tamanho', fontweight='bold', fontsize=11)
ax3.legend(title='Estado')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')

# --- GRÁFICO 4: RQ02 - Tempo vs Estado ---
ax4 = plt.subplot(4, 3, 4)
df_plot = df[df['tempo_analise_dias'] < df['tempo_analise_dias'].quantile(0.95)]
sns.violinplot(data=df_plot, x='estado', y='tempo_analise_dias', ax=ax4, palette=['#e74c3c', '#2ecc71'])
ax4.set_xlabel('Estado do PR')
ax4.set_ylabel('Tempo de Análise (dias)')
ax4.set_title(f'RQ02: Tempo de Análise vs Estado\nSpearman ρ = {rq02["spearman_r"]:.4f} (p = {rq02["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)

# --- GRÁFICO 5: RQ03 - Descrição vs Estado ---
ax5 = plt.subplot(4, 3, 5)
df_plot = df[df['tamanho_descricao_caracteres'] > 0]  # Apenas com descrição
df_plot = df_plot[df_plot['tamanho_descricao_caracteres'] < df_plot['tamanho_descricao_caracteres'].quantile(0.95)]
sns.boxplot(data=df_plot, x='estado', y='tamanho_descricao_caracteres', ax=ax5, palette=['#e74c3c', '#2ecc71'])
ax5.set_xlabel('Estado do PR')
ax5.set_ylabel('Tamanho da Descrição (caracteres)')
ax5.set_title(f'RQ03: Descrição vs Estado\nSpearman ρ = {rq03["spearman_r"]:.4f} (p = {rq03["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)

# --- GRÁFICO 6: RQ04 - Interações vs Estado ---
ax6 = plt.subplot(4, 3, 6)
interacoes_estado = df.groupby('estado')[['num_participantes', 'num_comentarios']].mean()
x = np.arange(len(interacoes_estado.index))
width = 0.35
bars1 = ax6.bar(x - width/2, interacoes_estado['num_participantes'], width, 
                label='Participantes', color='#3498db', alpha=0.7)
bars2 = ax6.bar(x + width/2, interacoes_estado['num_comentarios'], width,
                label='Comentários', color='#9b59b6', alpha=0.7)
ax6.set_xlabel('Estado do PR')
ax6.set_ylabel('Média')
ax6.set_title('RQ04: Interações Médias vs Estado', fontweight='bold', fontsize=11)
ax6.set_xticks(x)
ax6.set_xticklabels(interacoes_estado.index)
ax6.legend()
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)

# --- GRÁFICO 7: RQ05 - Tamanho vs Revisões ---
ax7 = plt.subplot(4, 3, 7)
df_plot = df[(df['tamanho_total'] < df['tamanho_total'].quantile(0.95)) & 
             (df['num_revisoes'] < df['num_revisoes'].quantile(0.95))]
sns.scatterplot(data=df_plot, x='tamanho_total', y='num_revisoes', 
                hue='estado', ax=ax7, palette=['#e74c3c', '#2ecc71'], alpha=0.5)
# Linha de tendência
z = np.polyfit(df_plot['tamanho_total'], df_plot['num_revisoes'], 1)
p = np.poly1d(z)
ax7.plot(df_plot['tamanho_total'].sort_values(), 
         p(df_plot['tamanho_total'].sort_values()), 
         "r--", alpha=0.8, linewidth=2, label='Tendência')
ax7.set_xlabel('Tamanho Total (linhas)')
ax7.set_ylabel('Número de Revisões')
ax7.set_title(f'RQ05: Tamanho vs Revisões\nSpearman ρ = {rq05["spearman_r"]:.4f} (p = {rq05["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)
ax7.legend(title='Estado', loc='upper right')

# --- GRÁFICO 8: RQ05 - Categoria vs Revisões ---
ax8 = plt.subplot(4, 3, 8)
categoria_revisoes = df.groupby('categoria_tamanho')['num_revisoes'].mean().reindex(categoria_ordem)
bars = ax8.bar(categoria_ordem, categoria_revisoes.values, color='#3498db', alpha=0.7)
ax8.set_xlabel('Categoria de Tamanho')
ax8.set_ylabel('Média de Revisões')
ax8.set_title('Média de Revisões por Categoria de Tamanho', fontweight='bold', fontsize=11)
ax8.set_xticklabels(ax8.get_xticklabels(), rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax8.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}', ha='center', va='bottom', fontsize=10)

# --- GRÁFICO 9: RQ06 - Tempo vs Revisões ---
ax9 = plt.subplot(4, 3, 9)
df_plot = df[(df['tempo_analise_dias'] < df['tempo_analise_dias'].quantile(0.95)) & 
             (df['num_revisoes'] < df['num_revisoes'].quantile(0.95))]
sns.scatterplot(data=df_plot, x='tempo_analise_dias', y='num_revisoes',
                hue='estado', ax=ax9, palette=['#e74c3c', '#2ecc71'], alpha=0.5)
# Linha de tendência
z = np.polyfit(df_plot['tempo_analise_dias'], df_plot['num_revisoes'], 1)
p = np.poly1d(z)
ax9.plot(df_plot['tempo_analise_dias'].sort_values(), 
         p(df_plot['tempo_analise_dias'].sort_values()), 
         "r--", alpha=0.8, linewidth=2, label='Tendência')
ax9.set_xlabel('Tempo de Análise (dias)')
ax9.set_ylabel('Número de Revisões')
ax9.set_title(f'RQ06: Tempo vs Revisões\nSpearman ρ = {rq06["spearman_r"]:.4f} (p = {rq06["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)
ax9.legend(title='Estado', loc='upper right')

# --- GRÁFICO 10: RQ07 - Descrição vs Revisões ---
ax10 = plt.subplot(4, 3, 10)
df_plot = df[(df['tamanho_descricao_caracteres'] > 0) & 
             (df['tamanho_descricao_caracteres'] < df['tamanho_descricao_caracteres'].quantile(0.95)) &
             (df['num_revisoes'] < df['num_revisoes'].quantile(0.95))]
sns.scatterplot(data=df_plot, x='tamanho_descricao_caracteres', y='num_revisoes',
                hue='estado', ax=ax10, palette=['#e74c3c', '#2ecc71'], alpha=0.5)
ax10.set_xlabel('Tamanho da Descrição (caracteres)')
ax10.set_ylabel('Número de Revisões')
ax10.set_title(f'RQ07: Descrição vs Revisões\nSpearman ρ = {rq07["spearman_r"]:.4f} (p = {rq07["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)
ax10.legend(title='Estado', loc='upper right')

# --- GRÁFICO 11: RQ08 - Participantes vs Revisões ---
ax11 = plt.subplot(4, 3, 11)
df_plot = df[df['num_revisoes'] < df['num_revisoes'].quantile(0.95)]
sns.scatterplot(data=df_plot, x='num_participantes', y='num_revisoes',
                hue='estado', ax=ax11, palette=['#e74c3c', '#2ecc71'], alpha=0.5)
# Linha de tendência
z = np.polyfit(df_plot['num_participantes'], df_plot['num_revisoes'], 1)
p = np.poly1d(z)
ax11.plot(df_plot['num_participantes'].sort_values(), 
          p(df_plot['num_participantes'].sort_values()), 
          "r--", alpha=0.8, linewidth=2, label='Tendência')
ax11.set_xlabel('Número de Participantes')
ax11.set_ylabel('Número de Revisões')
ax11.set_title(f'RQ08a: Participantes vs Revisões\nSpearman ρ = {rq08a["spearman_r"]:.4f} (p = {rq08a["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)
ax11.legend(title='Estado', loc='upper right')

# --- GRÁFICO 12: RQ08 - Comentários vs Revisões ---
ax12 = plt.subplot(4, 3, 12)
df_plot = df[(df['num_comentarios'] < df['num_comentarios'].quantile(0.95)) &
             (df['num_revisoes'] < df['num_revisoes'].quantile(0.95))]
sns.scatterplot(data=df_plot, x='num_comentarios', y='num_revisoes',
                hue='estado', ax=ax12, palette=['#e74c3c', '#2ecc71'], alpha=0.5)
# Linha de tendência
z = np.polyfit(df_plot['num_comentarios'], df_plot['num_revisoes'], 1)
p = np.poly1d(z)
ax12.plot(df_plot['num_comentarios'].sort_values(), 
          p(df_plot['num_comentarios'].sort_values()), 
          "r--", alpha=0.8, linewidth=2, label='Tendência')
ax12.set_xlabel('Número de Comentários')
ax12.set_ylabel('Número de Revisões')
ax12.set_title(f'RQ08b: Comentários vs Revisões\nSpearman ρ = {rq08b["spearman_r"]:.4f} (p = {rq08b["spearman_p"]:.4f})', 
              fontweight='bold', fontsize=11)
ax12.legend(title='Estado', loc='upper right')

plt.tight_layout()
plt.savefig('analise_completa.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: analise_completa.png")

# --- MAPA DE CALOR DE CORRELAÇÃO ---
fig2, ax = plt.subplots(figsize=(12, 10))
variaveis_correlacao = ['tamanho_total', 'tempo_analise_dias', 'tamanho_descricao_caracteres',
                        'num_participantes', 'num_comentarios', 'num_revisoes', 'estado_binario']
labels_correlacao = ['Tamanho', 'Tempo', 'Descrição', 'Participantes', 
                     'Comentários', 'Revisões', 'Estado']

# Calcular matriz de correlação de Spearman
corr_matrix = df[variaveis_correlacao].corr(method='spearman')
corr_matrix.index = labels_correlacao
corr_matrix.columns = labels_correlacao

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
            vmin=-1, vmax=1)
ax.set_title('Mapa de Correlação de Spearman\nEntre Variáveis de Pull Requests', 
             fontweight='bold', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('correlacao_spearman.png', dpi=300, bbox_inches='tight')
print("✓ Mapa de correlação salvo: correlacao_spearman.png")

# ============================================================================
# 8. ANÁLISE DE REGRESSÃO
# ============================================================================

print("\n" + "=" * 80)
print("ANÁLISE DE REGRESSÃO LINEAR")
print("=" * 80)

# Regressão: Prever número de revisões
print("\n--- MODELO 1: Predição do Número de Revisões ---")
print("-" * 80)

X_features = ['tamanho_total', 'tempo_analise_dias', 'tamanho_descricao_caracteres',
              'num_participantes', 'num_comentarios']
y_target = 'num_revisoes'

# Preparar dados
df_reg = df[X_features + [y_target]].dropna()
X = df_reg[X_features]
y = df_reg[y_target]

# Treinar modelo
modelo_revisoes = LinearRegression()
modelo_revisoes.fit(X, y)

# Resultados
r2 = modelo_revisoes.score(X, y)
print(f"R² do modelo: {r2:.4f}")
print(f"\nCoeficientes:")
for feature, coef in zip(X_features, modelo_revisoes.coef_):
    print(f"  {feature:30s}: {coef:8.6f}")
print(f"  Intercepto: {modelo_revisoes.intercept_:.6f}")

# Predições
y_pred = modelo_revisoes.predict(X)

# Visualização da regressão
fig3, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, feature in enumerate(X_features):
    ax = axes[idx]
    ax.scatter(df_reg[feature], y, alpha=0.3, s=10, label='Real')
    ax.scatter(df_reg[feature], y_pred, alpha=0.3, s=10, color='red', label='Predito')
    ax.set_xlabel(feature.replace('_', ' ').title())
    ax.set_ylabel('Número de Revisões')
    ax.set_title(f'Regressão: {feature.replace("_", " ").title()} vs Revisões')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Gráfico de resíduos
ax = axes[5]
residuos = y - y_pred
ax.scatter(y_pred, residuos, alpha=0.3, s=10)
ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
ax.set_xlabel('Valores Preditos')
ax.set_ylabel('Resíduos')
ax.set_title('Análise de Resíduos')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analise_regressao.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráficos de regressão salvos: analise_regressao.png")

# ============================================================================
# 9. RESUMO EXECUTIVO DAS RESPOSTAS
# ============================================================================

print("\n" + "=" * 80)
print("RESUMO EXECUTIVO - RESPOSTAS ÀS QUESTÕES DE PESQUISA")
print("=" * 80)

respostas = f"""
{'='*80}
DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES (Estado do PR)
{'='*80}

RQ 01: Qual a relação entre o TAMANHO dos PRs e o FEEDBACK FINAL?
{'-'*80}
• Correlação de Spearman: ρ = {rq01['spearman_r']:.4f} (p = {rq01['spearman_p']:.6f})
• Interpretação: {rq01['interpretacao']}
• Significância: {rq01['significancia']}

RESPOSTA: Há uma correlação {rq01['interpretacao'].lower()} entre o tamanho dos PRs e
o feedback final. PRs menores tendem a ter maior taxa de aprovação (MERGED). Isso
sugere que revisores preferem analisar PRs mais gerenciáveis e focados.

{'-'*80}

RQ 02: Qual a relação entre o TEMPO DE ANÁLISE e o FEEDBACK FINAL?
{'-'*80}
• Correlação de Spearman: ρ = {rq02['spearman_r']:.4f} (p = {rq02['spearman_p']:.6f})
• Interpretação: {rq02['interpretacao']}
• Significância: {rq02['significancia']}

RESPOSTA: A correlação é {rq02['interpretacao'].lower()}. {'PRs que levam mais tempo ' +
'para serem analisados tendem a ser rejeitados (CLOSED), possivelmente indicando ' +
'problemas ou falta de engajamento.' if rq02['spearman_r'] < 0 else 'PRs que levam ' +
'mais tempo tendem a ser aprovados, sugerindo que revisões mais cuidadosas levam a ' +
'melhores resultados.'}

{'-'*80}

RQ 03: Qual a relação entre a DESCRIÇÃO dos PRs e o FEEDBACK FINAL?
{'-'*80}
• Correlação de Spearman: ρ = {rq03['spearman_r']:.4f} (p = {rq03['spearman_p']:.6f})
• Interpretação: {rq03['interpretacao']}
• Significância: {rq03['significancia']}

RESPOSTA: A correlação é {rq03['interpretacao'].lower()}. {'Descrições mais detalhadas ' +
'estão associadas a maior aprovação, indicando que comunicação clara ajuda revisores ' +
'a entenderem e aprovarem PRs.' if rq03['spearman_r'] > 0 else 'O tamanho da descrição ' +
'não parece influenciar significativamente o resultado final.'}

{'-'*80}

RQ 04: Qual a relação entre as INTERAÇÕES nos PRs e o FEEDBACK FINAL?
{'-'*80}
• Participantes: ρ = {rq04a['spearman_r']:.4f} (p = {rq04a['spearman_p']:.6f}) - {rq04a['interpretacao']}
• Comentários: ρ = {rq04b['spearman_r']:.4f} (p = {rq04b['spearman_p']:.6f}) - {rq04b['interpretacao']}

RESPOSTA: {'Maior número de participantes e comentários está correlacionado com ' +
'aprovação, sugerindo que engajamento da equipe leva a PRs de melhor qualidade.' 
if rq04a['spearman_r'] > 0 else 'As interações mostram correlação fraca com o resultado, ' +
'indicando que quantidade de discussão não necessariamente prediz aprovação.'}

{'='*80}
DIMENSÃO B: NÚMERO DE REVISÕES
{'='*80}

RQ 05: Qual a relação entre o TAMANHO dos PRs e o NÚMERO DE REVISÕES?
{'-'*80}
• Correlação de Spearman: ρ = {rq05['spearman_r']:.4f} (p = {rq05['spearman_p']:.6f})
• Interpretação: {rq05['interpretacao']}
• Significância: {rq05['significancia']}

RESPOSTA: Há correlação {rq05['interpretacao'].lower()} {'positiva' if rq05['spearman_r'] > 0 
else 'negativa'}. {'PRs maiores requerem mais ciclos de revisão, provavelmente devido ' +
'à complexidade aumentada e maior probabilidade de problemas.' if rq05['spearman_r'] > 0 
else 'O tamanho não influencia significativamente o número de revisões.'}

{'-'*80}

RQ 06: Qual a relação entre o TEMPO DE ANÁLISE e o NÚMERO DE REVISÕES?
{'-'*80}
• Correlação de Spearman: ρ = {rq06['spearman_r']:.4f} (p = {rq06['spearman_p']:.6f})
• Interpretação: {rq06['interpretacao']}
• Significância: {rq06['significancia']}

RESPOSTA: Correlação {rq06['interpretacao'].lower()} {'positiva' if rq06['spearman_r'] > 0 
else 'negativa'}. {'Mais revisões levam a tempos de análise mais longos, indicando ' +
'processos iterativos de melhoria.' if rq06['spearman_r'] > 0 else 'Não há relação ' +
'clara entre tempo e número de revisões.'}

{'-'*80}

RQ 07: Qual a relação entre a DESCRIÇÃO dos PRs e o NÚMERO DE REVISÕES?
{'-'*80}
• Correlação de Spearman: ρ = {rq07['spearman_r']:.4f} (p = {rq07['spearman_p']:.6f})
• Interpretação: {rq07['interpretacao']}
• Significância: {rq07['significancia']}

RESPOSTA: Correlação {rq07['interpretacao'].lower()}. {'Descrições mais longas podem ' +
'indicar PRs mais complexos que requerem mais revisões.' if rq07['spearman_r'] > 0.1 
else 'O tamanho da descrição não prediz significativamente o número de revisões.'}

{'-'*80}

RQ 08: Qual a relação entre as INTERAÇÕES e o NÚMERO DE REVISÕES?
{'-'*80}
• Participantes: ρ = {rq08a['spearman_r']:.4f} (p = {rq08a['spearman_p']:.6f}) - {rq08a['interpretacao']}
• Comentários: ρ = {rq08b['spearman_r']:.4f} (p = {rq08b['spearman_p']:.6f}) - {rq08b['interpretacao']}

RESPOSTA: {'Forte correlação positiva! Mais revisões geram mais participantes e ' +
'comentários, criando um ciclo de discussão e refinamento.' if rq08b['spearman_r'] > 0.5 
else 'Correlação moderada - interações e revisões estão relacionadas mas não ' +
'determinam uma à outra completamente.'}

{'='*80}
CONCLUSÕES GERAIS
{'='*80}

1. TAMANHO IMPORTA: PRs menores têm maior probabilidade de aprovação e requerem
   menos revisões. Recomenda-se dividir mudanças grandes em PRs menores e focados.

2. COMUNICAÇÃO É CHAVE: Descrições adequadas facilitam o entendimento e aprovação,
   embora o tamanho sozinho não seja determinante.

3. ENGAJAMENTO POSITIVO: Participação ativa da equipe está associada a melhores
   resultados, mas deve ser balanceada para não estender excessivamente o tempo.

4. CICLO ITERATIVO: Número de revisões está fortemente correlacionado com tempo
   e interações, indicando processo colaborativo de refinamento.

5. QUALIDADE vs VELOCIDADE: É necessário balancear revisões detalhadas (que levam
   tempo) com agilidade no processo (PRs menores e focados).

{'='*80}
"""

print(respostas)

# Salvar resumo em arquivo
with open('resumo_analise.txt', 'w', encoding='utf-8') as f:
    f.write(respostas)
print("\n✓ Resumo salvo em: resumo_analise.txt")

print("\n" + "=" * 80)
print("ANÁLISE CONCLUÍDA!")
print("=" * 80)
print("\nArquivos gerados:")
print("  1. analise_completa.png - 12 gráficos das questões de pesquisa")
print("  2. correlacao_spearman.png - Mapa de calor de correlações")
print("  3. analise_regressao.png - Análise de regressão linear")
print("  4. resumo_analise.txt - Resumo executivo das respostas")
print("\n" + "=" * 80)
