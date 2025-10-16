import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import spearmanr, pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import json
import warnings
warnings.filterwarnings('ignore')

# Configurações visuais
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("ANÁLISE DE PULL REQUESTS")
print("="*80)

# ============================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ============================================

print("\n📂 Carregando dados de: dados_pull_requests3.json")

with open('dados_pull_requests3.json', 'r', encoding='utf-8') as file:
 dados_json = json.load(file)

df = pd.DataFrame(dados_json)

print(f"✓ Dados carregados com sucesso!")
print(f"✓ Total de registros: {len(df):,}")
print(f"✓ Total de colunas: {len(df.columns)}")

print("\n" + "="*80)
print("INFORMAÇÕES DO DATASET")
print("="*80)
print(df.info())

print("\n" + "="*80)
print("PRIMEIRAS LINHAS DO DATASET")
print("="*80)
print(df.head())

print("\n" + "="*80)
print("VALORES AUSENTES")
print("="*80)
missing = df.isnull().sum()
if missing.sum() > 0:
 print(missing[missing > 0])
 print(f"\n⚠️  Total de valores ausentes: {missing.sum()}")
else:
 print("✓ Não há valores ausentes no dataset!")

# Converter datas
df['data_criacao'] = pd.to_datetime(df['data_criacao'])
df['data_fechamento'] = pd.to_datetime(df['data_fechamento'])

# Criar variáveis derivadas
df['tamanho_total_linhas'] = df['linhas_adicionadas'] + df['linhas_removidas']
df['estado_numerico'] = (df['estado'] == 'MERGED').astype(int)
df['ano'] = df['data_criacao'].dt.year
df['mes'] = df['data_criacao'].dt.month
df['ano_mes'] = df['data_criacao'].dt.to_period('M')

# Adicionar +1 para permitir log (evitar log(0))
df['tamanho_total_linhas_log'] = np.log1p(df['tamanho_total_linhas'])
df['tempo_analise_dias_log'] = np.log1p(df['tempo_analise_dias'])
df['num_comentarios_log'] = np.log1p(df['num_comentarios'])
df['num_revisoes_log'] = np.log1p(df['num_revisoes'])

print("\n" + "="*80)
print("ESTATÍSTICAS DESCRITIVAS")
print("="*80)
print(df.describe())

print("\n" + "="*80)
print("DISTRIBUIÇÃO DE ESTADOS DOS PRs")
print("="*80)
print(df['estado'].value_counts())
print(f"\nPercentuais:")
print(df['estado'].value_counts(normalize=True) * 100)

# ============================================
# 2. ANÁLISE DE NORMALIDADE
# ============================================

print("\n" + "="*80)
print("TESTE DE NORMALIDADE (Shapiro-Wilk)")
print("="*80)
print("Testando se as variáveis seguem distribuição normal...")
print("-" * 80)

variaveis_continuas = [
 'tempo_analise_dias', 
 'num_arquivos_alterados', 
 'linhas_adicionadas',
 'linhas_removidas',
 'tamanho_total_linhas',
 'tamanho_descricao_caracteres',
 'num_participantes', 
 'num_comentarios', 
 'num_revisoes'
]

normais = 0

for var in variaveis_continuas:
 if len(df[var]) > 5000:
     amostra = df[var].sample(n=5000, random_state=42)
     stat, p_value = stats.shapiro(amostra)
 else:
     stat, p_value = stats.shapiro(df[var])
 
 ks_stat, ks_p = stats.kstest(df[var], 'norm', args=(df[var].mean(), df[var].std()))
 is_normal = p_value > 0.05
 status = "✓ NORMAL" if is_normal else "✗ NÃO-NORMAL"
 print(f"{var:35s} | Shapiro p={p_value:.4f} | KS p={ks_p:.4f} | {status}")
 
 if is_normal:
     normais += 1

print("\n" + "="*80)
print("ANÁLISE DE ASSIMETRIA E CURTOSE")
print("="*80)

for var in variaveis_continuas:
 skewness = df[var].skew()
 kurtosis = df[var].kurtosis()
 
 if abs(skewness) < 0.5:
     skew_interp = "Simétrica"
 elif skewness > 0:
     skew_interp = "Assimétrica à direita"
 else:
     skew_interp = "Assimétrica à esquerda"
 
 print(f"{var:35s} | Assimetria: {skewness:7.3f} ({skew_interp:25s}) | Curtose: {kurtosis:7.3f}")

percentual_normal = (normais / len(variaveis_continuas)) * 100

print("\n" + "="*80)
print("DECISÃO: CORRELAÇÃO DE SPEARMAN")
print("="*80)
print(f"""
JUSTIFICATIVA: {len(variaveis_continuas) - normais}/{len(variaveis_continuas)} variáveis não seguem distribuição normal.
Spearman é robusto a outliers e apropriado para relações monotônicas.
""")

# ============================================
# 3. VISUALIZAÇÕES EXPLORATÓRIAS - MELHORADAS
# ============================================

print("\n" + "="*80)
print("GERANDO VISUALIZAÇÕES COM ESCALA LOGARÍTMICA...")
print("="*80)

# ============================================
# GRÁFICO 1: DISTRIBUIÇÕES (ESCALA LINEAR E LOG)
# ============================================

fig, axes = plt.subplots(3, 3, figsize=(22, 18))
fig.suptitle('Distribuições das Variáveis Principais (Escala Logarítmica)', 
          fontsize=20, fontweight='bold', y=0.995)

variaveis_plot = [
 ('tempo_analise_dias', 'Tempo de Análise (dias)', 'steelblue'),
 ('num_arquivos_alterados', 'Arquivos Alterados', 'coral'),
 ('tamanho_total_linhas', 'Tamanho Total (linhas)', 'green'),
 ('tamanho_descricao_caracteres', 'Descrição (caracteres)', 'purple'),
 ('num_participantes', 'Participantes', 'orange'),
 ('num_comentarios', 'Comentários', 'red'),
 ('num_revisoes', 'Revisões', 'brown'),
 ('linhas_adicionadas', 'Linhas Adicionadas', 'teal'),
 ('linhas_removidas', 'Linhas Removidas', 'pink')
]

for idx, (var, titulo, cor) in enumerate(variaveis_plot):
 ax = axes[idx // 3, idx % 3]
 
 # Remover zeros para log
 data_plot = df[df[var] > 0][var]
 
 # Histograma com escala log
 sns.histplot(data=data_plot, ax=ax, color=cor, bins=50, kde=True, log_scale=True)
 
 mediana = data_plot.median()
 media = data_plot.mean()
 
 ax.axvline(mediana, color='red', linestyle='--', linewidth=2.5, 
            label=f'Mediana: {mediana:.1f}', alpha=0.8)
 ax.axvline(media, color='darkblue', linestyle=':', linewidth=2.5, 
            label=f'Média: {media:.1f}', alpha=0.8)
 
 ax.set_title(titulo, fontweight='bold', fontsize=13)
 ax.set_xlabel('Valor (escala log)', fontsize=11)
 ax.set_ylabel('Frequência', fontsize=11)
 ax.legend(fontsize=10, loc='upper right')
 
 # Estatísticas
 q25, q75 = data_plot.quantile([0.25, 0.75])
 textstr = f'Q1: {q25:.1f}\nQ3: {q75:.1f}\nSkew: {data_plot.skew():.2f}'
 ax.text(0.03, 0.97, textstr, transform=ax.transAxes, fontsize=9,
         verticalalignment='top', bbox=dict(boxstyle='round', 
         facecolor='wheat', alpha=0.7))

plt.tight_layout()
plt.savefig('01_distribuicoes_log.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 01_distribuicoes_log.png")
plt.close()

# ============================================
# GRÁFICO 2: COMPARAÇÃO MERGED vs CLOSED (ESCALA LOG)
# ============================================

fig, axes = plt.subplots(2, 4, figsize=(24, 12))
fig.suptitle('Comparação: Pull Requests MERGED vs CLOSED (Escala Logarítmica)', 
          fontsize=20, fontweight='bold')

variaveis_comparacao = [
 ('tempo_analise_dias', 'Tempo de Análise (dias)'),
 ('tamanho_total_linhas', 'Tamanho Total (linhas)'),
 ('tamanho_descricao_caracteres', 'Descrição (caracteres)'),
 ('num_participantes', 'Participantes'),
 ('num_comentarios', 'Comentários'),
 ('num_revisoes', 'Revisões'),
 ('num_arquivos_alterados', 'Arquivos Alterados'),
 ('linhas_adicionadas', 'Linhas Adicionadas')
]

resultados_testes = {}

for idx, (var, titulo) in enumerate(variaveis_comparacao):
 ax = axes[idx // 4, idx % 4]
 
 # Preparar dados (remover zeros para log)
 df_plot = df[df[var] > 0].copy()
 
 # Violinplot + Boxplot
 sns.violinplot(data=df_plot, x='estado', y=var, ax=ax, 
                palette='Set2', alpha=0.4, inner=None)
 sns.boxplot(data=df_plot, x='estado', y=var, ax=ax, 
             palette='Set2', width=0.3, showcaps=True, 
             boxprops=dict(alpha=0.8), showfliers=False)
 
 # Escala logarítmica no eixo Y
 ax.set_yscale('log')
 
 # Teste estatístico
 merged = df[df['estado'] == 'MERGED'][var]
 closed = df[df['estado'] == 'CLOSED'][var]
 
 u_stat, p_val = stats.mannwhitneyu(merged, closed, alternative='two-sided')
 z_score = abs(stats.norm.ppf(p_val / 2))
 effect_size = z_score / np.sqrt(len(df))
 
 resultados_testes[var] = {
     'u_stat': u_stat,
     'p_value': p_val,
     'effect_size': effect_size,
     'merged_median': merged.median(),
     'closed_median': closed.median()
 }
 
 if p_val < 0.001:
     sig = "***"
     sig_text = "p < 0.001"
 elif p_val < 0.01:
     sig = "**"
     sig_text = f"p = {p_val:.3f}"
 elif p_val < 0.05:
     sig = "*"
     sig_text = f"p = {p_val:.3f}"
 else:
     sig = "ns"
     sig_text = f"p = {p_val:.3f}"
 
 ax.set_title(f'{titulo}\n{sig_text} {sig}', fontweight='bold', fontsize=11)
 ax.set_xlabel('Status', fontsize=10)
 ax.set_ylabel(f'{titulo} (log)', fontsize=10)
 
 # Adicionar medianas
 textstr = f'MERGED: {merged.median():.1f}\nCLOSED: {closed.median():.1f}\nEffect size: {effect_size:.3f}'
 ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('02_merged_vs_closed_log.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 02_merged_vs_closed_log.png")
plt.close()

# ============================================
# GRÁFICO 3: SÉRIES TEMPORAIS
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('Análise Temporal dos Pull Requests', fontsize=20, fontweight='bold')

# 3.1: Volume de PRs por mês
ax = axes[0, 0]
prs_por_mes = df.groupby(['ano_mes', 'estado']).size().unstack(fill_value=0)
prs_por_mes.plot(kind='line', ax=ax, marker='o', linewidth=2.5, markersize=6)
ax.set_title('Volume de PRs por Mês', fontweight='bold', fontsize=14)
ax.set_xlabel('Período', fontsize=12)
ax.set_ylabel('Número de PRs', fontsize=12)
ax.legend(title='Status', fontsize=11)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 3.2: Tempo médio de análise por mês
ax = axes[0, 1]
tempo_por_mes = df.groupby('ano_mes')['tempo_analise_dias'].agg(['mean', 'median'])
ax.plot(tempo_por_mes.index.astype(str), tempo_por_mes['mean'], 
     marker='o', linewidth=2.5, markersize=6, label='Média', color='steelblue')
ax.plot(tempo_por_mes.index.astype(str), tempo_por_mes['median'], 
     marker='s', linewidth=2.5, markersize=6, label='Mediana', color='coral')
ax.set_title('Tempo de Análise ao Longo do Tempo', fontweight='bold', fontsize=14)
ax.set_xlabel('Período', fontsize=12)
ax.set_ylabel('Dias', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 3.3: Taxa de aceitação por mês
ax = axes[1, 0]
taxa_por_mes = df.groupby('ano_mes')['estado_numerico'].agg(['mean', 'count'])
taxa_por_mes['taxa_merged'] = taxa_por_mes['mean'] * 100
ax.bar(range(len(taxa_por_mes)), taxa_por_mes['taxa_merged'], 
    color='green', alpha=0.7, edgecolor='black')
ax.axhline(y=taxa_por_mes['taxa_merged'].mean(), color='red', 
        linestyle='--', linewidth=2, label=f"Média: {taxa_por_mes['taxa_merged'].mean():.1f}%")
ax.set_title('Taxa de Aceitação (MERGED) por Mês', fontweight='bold', fontsize=14)
ax.set_xlabel('Período', fontsize=12)
ax.set_ylabel('% de PRs Merged', fontsize=12)
ax.set_xticks(range(len(taxa_por_mes)))
ax.set_xticklabels(taxa_por_mes.index.astype(str), rotation=45)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# 3.4: Número médio de revisões por mês
ax = axes[1, 1]
revisoes_por_mes = df.groupby(['ano_mes', 'estado'])['num_revisoes'].mean().unstack(fill_value=0)
revisoes_por_mes.plot(kind='line', ax=ax, marker='o', linewidth=2.5, markersize=6)
ax.set_title('Número Médio de Revisões por Mês', fontweight='bold', fontsize=14)
ax.set_xlabel('Período', fontsize=12)
ax.set_ylabel('Média de Revisões', fontsize=12)
ax.legend(title='Status', fontsize=11)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('03_series_temporais.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 03_series_temporais.png")
plt.close()

# ============================================
# GRÁFICO 4: SCATTERPLOT MATRIX (CORRELAÇÕES VISUAIS)
# ============================================

print("\nCalculando matriz de correlação de Spearman...")

variaveis_correlacao = [
 'tempo_analise_dias',
 'num_arquivos_alterados',
 'tamanho_total_linhas',
 'tamanho_descricao_caracteres',
 'num_participantes',
 'num_comentarios',
 'num_revisoes',
 'estado_numerico'
]

rename_dict = {
 'tempo_analise_dias': 'Tempo',
 'num_arquivos_alterados': 'Arquivos',
 'tamanho_total_linhas': 'Tamanho',
 'tamanho_descricao_caracteres': 'Descrição',
 'num_participantes': 'Participantes',
 'num_comentarios': 'Comentários',
 'num_revisoes': 'Revisões',
 'estado_numerico': 'Merged'
}

df_corr = df[variaveis_correlacao].copy()
df_corr.columns = [rename_dict[col] for col in df_corr.columns]

correlacao_spearman = df_corr.corr(method='spearman')

# Calcular p-values
p_values = pd.DataFrame(np.zeros_like(correlacao_spearman), 
                    columns=correlacao_spearman.columns,
                    index=correlacao_spearman.index)

for i, col1 in enumerate(df_corr.columns):
 for j, col2 in enumerate(df_corr.columns):
     if i != j:
         _, p_val = spearmanr(df_corr[col1], df_corr[col2])
         p_values.iloc[i, j] = p_val

fig, ax = plt.subplots(figsize=(16, 14))
mask = np.triu(np.ones_like(correlacao_spearman, dtype=bool))

# Heatmap melhorado
sns.heatmap(correlacao_spearman, mask=mask, annot=True, fmt='.3f', 
         cmap='RdBu_r', center=0, square=True, linewidths=2,
         cbar_kws={"shrink": 0.8, "label": "Correlação de Spearman (ρ)"},
         vmin=-1, vmax=1, ax=ax, annot_kws={"size": 11, "weight": "bold"})

plt.title('Matriz de Correlação de Spearman\n(Valores mais fortes em cores intensas)', 
       fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('04_correlacao_spearman.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 04_correlacao_spearman.png")
plt.close()

# Exibir correlações fortes
print("\n" + "="*80)
print("CORRELAÇÕES MAIS FORTES (|ρ| > 0.3)")
print("="*80)

correlacoes_fortes = []
for i in range(len(correlacao_spearman.columns)):
 for j in range(i+1, len(correlacao_spearman.columns)):
     corr_val = correlacao_spearman.iloc[i, j]
     p_val = p_values.iloc[i, j]
     if abs(corr_val) > 0.3:
         correlacoes_fortes.append({
             'var1': correlacao_spearman.columns[i],
             'var2': correlacao_spearman.columns[j],
             'rho': corr_val,
             'p_value': p_val
         })

correlacoes_fortes.sort(key=lambda x: abs(x['rho']), reverse=True)

for item in correlacoes_fortes:
 sig = "***" if item['p_value'] < 0.001 else "**" if item['p_value'] < 0.01 else "*" if item['p_value'] < 0.05 else "ns"
 print(f"{item['var1']:15s} ↔ {item['var2']:15s} | ρ = {item['rho']:7.3f} | p = {item['p_value']:.4f} {sig}")

# ============================================
# GRÁFICO 5: SCATTERPLOTS DE REGRESSÃO (ESCALA LOG)
# ============================================

print("\n" + "="*80)
print("ANÁLISES DE REGRESSÃO COM ESCALA LOGARÍTMICA")
print("="*80)

fig, axes = plt.subplots(2, 3, figsize=(22, 14))
fig.suptitle('Regressão: Preditores do Número de Revisões (Escala Log)', 
          fontsize=20, fontweight='bold')

preditores_revisoes = [
 ('tamanho_total_linhas', 'Tamanho Total (linhas)', 'steelblue'),
 ('tamanho_descricao_caracteres', 'Descrição (caracteres)', 'green'),
 ('num_participantes', 'Participantes', 'purple'),
 ('num_comentarios', 'Comentários', 'orange'),
 ('tempo_analise_dias', 'Tempo de Análise (dias)', 'red'),
 ('num_arquivos_alterados', 'Arquivos Alterados', 'brown')
]

resultados_regressao_revisoes = {}

for idx, (var, titulo, cor) in enumerate(preditores_revisoes):
 ax = axes[idx // 3, idx % 3]
 
 # Remover zeros e outliers extremos
 df_plot = df[(df[var] > 0) & (df['num_revisoes'] > 0)].copy()
 df_plot = df_plot[(df_plot[var] <= df_plot[var].quantile(0.99)) & 
                   (df_plot['num_revisoes'] <= df_plot['num_revisoes'].quantile(0.99))]
 
 # Amostra para visualização
 if len(df_plot) > 1000:
     df_sample = df_plot.sample(n=1000, random_state=42)
 else:
     df_sample = df_plot
 
 # Scatter plot com alpha para densidade
 ax.scatter(df_sample[var], df_sample['num_revisoes'], 
            alpha=0.4, s=40, color=cor, edgecolors='black', linewidth=0.5)
 
 # Regressão linear
 x = df[var].values.reshape(-1, 1)
 y = df['num_revisoes'].values
 model = LinearRegression().fit(x, y)
 y_pred = model.predict(x)
 
 # Linha de regressão
 x_range = np.linspace(df_plot[var].min(), df_plot[var].max(), 100).reshape(-1, 1)
 y_range = model.predict(x_range)
 ax.plot(x_range, y_range, color='red', linewidth=3, 
         label='Regressão Linear', alpha=0.8)
 
 # Escala log
 ax.set_xscale('log')
 ax.set_yscale('log')
 
 # Métricas
 r2 = r2_score(y, y_pred)
 rho, p_spearman = spearmanr(df[var], df['num_revisoes'])
 
 resultados_regressao_revisoes[var] = {
     'coef': model.coef_[0],
     'intercept': model.intercept_,
     'r2': r2,
     'spearman_rho': rho,
     'spearman_p': p_spearman
 }
 
 sig = "***" if p_spearman < 0.001 else "**" if p_spearman < 0.01 else "*" if p_spearman < 0.05 else "ns"
 ax.set_title(f'{titulo}\nρ={rho:.3f} {sig} | R²={r2:.3f}',
             fontweight='bold', fontsize=12)
 
 ax.set_xlabel(f'{titulo} (log)', fontsize=11)
 ax.set_ylabel('Número de Revisões (log)', fontsize=11)
 ax.legend(fontsize=10, loc='best')
 ax.grid(True, alpha=0.3, which='both', linestyle='--')

plt.tight_layout()
plt.savefig('05_regressao_revisoes_log.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 05_regressao_revisoes_log.png")
plt.close()

# ============================================
# GRÁFICO 6: COMPARATIVO DE DENSIDADES
# ============================================

fig, axes = plt.subplots(2, 3, figsize=(22, 12))
fig.suptitle('Comparação de Densidades: MERGED vs CLOSED', 
          fontsize=20, fontweight='bold')

variaveis_densidade = [
 ('tempo_analise_dias', 'Tempo de Análise'),
 ('tamanho_total_linhas', 'Tamanho Total'),
 ('num_revisoes', 'Número de Revisões'),
 ('num_comentarios', 'Número de Comentários'),
 ('num_participantes', 'Número de Participantes'),
 ('tamanho_descricao_caracteres', 'Tamanho Descrição')
]

for idx, (var, titulo) in enumerate(variaveis_densidade):
 ax = axes[idx // 3, idx % 3]
 
 merged_data = df[df['estado'] == 'MERGED'][var]
 closed_data = df[df['estado'] == 'CLOSED'][var]
 
 # KDE plots
 merged_data[merged_data > 0].plot(kind='density', ax=ax, 
                                   color='green', linewidth=3, 
                                   label='MERGED', alpha=0.7)
 closed_data[closed_data > 0].plot(kind='density', ax=ax, 
                                   color='red', linewidth=3, 
                                   label='CLOSED', alpha=0.7)
 
 ax.set_xscale('log')
 ax.set_title(titulo, fontweight='bold', fontsize=13)
 ax.set_xlabel(f'{titulo} (log)', fontsize=11)
 ax.set_ylabel('Densidade', fontsize=11)
 ax.legend(fontsize=11, loc='best')
 ax.grid(True, alpha=0.3)
 
 # Adicionar medianas
 ax.axvline(merged_data.median(), color='green', linestyle='--', 
            linewidth=2, alpha=0.6)
 ax.axvline(closed_data.median(), color='red', linestyle='--', 
            linewidth=2, alpha=0.6)

plt.tight_layout()
plt.savefig('06_densidades_comparativas.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 06_densidades_comparativas.png")
plt.close()

# ============================================
# GRÁFICO 7: ANÁLISE DE OUTLIERS E QUANTIS
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('Análise de Distribuição por Quantis', fontsize=20, fontweight='bold')

# 7.1: Distribuição de tamanho por quantis
ax = axes[0, 0]
quantis = df['tamanho_total_linhas'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
merged_quantis = df[df['estado'] == 'MERGED']['tamanho_total_linhas'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
closed_quantis = df[df['estado'] == 'CLOSED']['tamanho_total_linhas'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

x_pos = np.arange(len(quantis))
width = 0.35

ax.bar(x_pos - width/2, merged_quantis.values, width, label='MERGED', color='green', alpha=0.7)
ax.bar(x_pos + width/2, closed_quantis.values, width, label='CLOSED', color='red', alpha=0.7)

ax.set_xlabel('Quantis', fontsize=12)
ax.set_ylabel('Tamanho (linhas)', fontsize=12)
ax.set_title('Distribuição de Tamanho por Quantis', fontweight='bold', fontsize=14)
ax.set_xticks(x_pos)
ax.set_xticklabels(['Q25', 'Q50', 'Q75', 'Q90', 'Q95', 'Q99'])
ax.set_yscale('log')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# 7.2: Tempo de análise por quantis
ax = axes[0, 1]
merged_tempo_q = df[df['estado'] == 'MERGED']['tempo_analise_dias'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
closed_tempo_q = df[df['estado'] == 'CLOSED']['tempo_analise_dias'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])

ax.bar(x_pos - width/2, merged_tempo_q.values, width, label='MERGED', color='green', alpha=0.7)
ax.bar(x_pos + width/2, closed_tempo_q.values, width, label='CLOSED', color='red', alpha=0.7)

ax.set_xlabel('Quantis', fontsize=12)
ax.set_ylabel('Tempo (dias)', fontsize=12)
ax.set_title('Tempo de Análise por Quantis', fontweight='bold', fontsize=14)
ax.set_xticks(x_pos)
ax.set_xticklabels(['Q25', 'Q50', 'Q75', 'Q90', 'Q95', 'Q99'])
ax.set_yscale('log')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# 7.3: Box plot comparativo tamanho
ax = axes[1, 0]
data_box = [
 df[df['estado'] == 'MERGED']['tamanho_total_linhas'],
 df[df['estado'] == 'CLOSED']['tamanho_total_linhas']
]
bp = ax.boxplot(data_box, labels=['MERGED', 'CLOSED'], patch_artist=True,
             showfliers=False, widths=0.6)
bp['boxes'][0].set_facecolor('green')
bp['boxes'][1].set_facecolor('red')
for patch in bp['boxes']:
 patch.set_alpha(0.7)
ax.set_yscale('log')
ax.set_ylabel('Tamanho Total (linhas, log)', fontsize=12)
ax.set_title('Boxplot: Tamanho Total', fontweight='bold', fontsize=14)
ax.grid(True, alpha=0.3, axis='y')

# 7.4: Box plot comparativo revisões
ax = axes[1, 1]
data_box = [
 df[df['estado'] == 'MERGED']['num_revisoes'],
 df[df['estado'] == 'CLOSED']['num_revisoes']
]
bp = ax.boxplot(data_box, labels=['MERGED', 'CLOSED'], patch_artist=True,
             showfliers=False, widths=0.6)
bp['boxes'][0].set_facecolor('green')
bp['boxes'][1].set_facecolor('red')
for patch in bp['boxes']:
 patch.set_alpha(0.7)
ax.set_yscale('log')
ax.set_ylabel('Número de Revisões (log)', fontsize=12)
ax.set_title('Boxplot: Número de Revisões', fontweight='bold', fontsize=14)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('07_analise_quantis.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 07_analise_quantis.png")
plt.close()

# ============================================
# GRÁFICO 8: HEATMAP DE MÉTRICAS POR CATEGORIA
# ============================================

fig, axes = plt.subplots(1, 2, figsize=(20, 8))
fig.suptitle('Comparação de Métricas Médias: MERGED vs CLOSED', 
          fontsize=20, fontweight='bold')

# Calcular médias por grupo
metricas = ['tempo_analise_dias', 'tamanho_total_linhas', 'num_revisoes', 
         'num_comentarios', 'num_participantes', 'num_arquivos_alterados']

medias_merged = df[df['estado'] == 'MERGED'][metricas].mean()
medias_closed = df[df['estado'] == 'CLOSED'][metricas].mean()

# Normalizar para comparação
matriz_comparacao = pd.DataFrame({
 'MERGED': medias_merged,
 'CLOSED': medias_closed
}).T

# Normalizar por coluna (z-score)
matriz_norm = (matriz_comparacao - matriz_comparacao.mean()) / matriz_comparacao.std()

# Heatmap normalizado
ax = axes[0]
sns.heatmap(matriz_norm, annot=matriz_comparacao.values, fmt='.1f', 
         cmap='RdYlGn', center=0, ax=ax, cbar_kws={"label": "Z-score"},
         linewidths=2, square=False, annot_kws={"size": 11, "weight": "bold"})
ax.set_title('Valores Médios (Z-score normalizado)', fontweight='bold', fontsize=14)
ax.set_xlabel('')
ax.set_ylabel('Status', fontsize=12)

# Diferença percentual
ax = axes[1]
diff_perc = ((medias_merged - medias_closed) / medias_closed * 100).values.reshape(1, -1)
sns.heatmap(diff_perc, annot=True, fmt='.1f', cmap='RdBu_r', center=0,
         xticklabels=matriz_comparacao.columns, yticklabels=['Diferença %'],
         ax=ax, cbar_kws={"label": "% Diferença (MERGED vs CLOSED)"},
         linewidths=2, square=False, annot_kws={"size": 11, "weight": "bold"})
ax.set_title('Diferença Percentual (MERGED vs CLOSED)', fontweight='bold', fontsize=14)
ax.set_xlabel('Métricas', fontsize=12)

plt.tight_layout()
plt.savefig('08_heatmap_comparativo.png', dpi=300, bbox_inches='tight')
print("✓ Salvo: 08_heatmap_comparativo.png")
plt.close()

# ============================================
# CONTINUAR COM AS ANÁLISES DAS RQs...
# ============================================

def analise_correlacao_completa(var1_name, var2_name, dados):
 var1 = dados[var1_name]
 var2 = dados[var2_name]
 
 rho, p_spearman = spearmanr(var1, var2)
 r, p_pearson = pearsonr(var1, var2)
 
 abs_rho = abs(rho)
 if abs_rho < 0.1:
     forca = "Trivial"
 elif abs_rho < 0.3:
     forca = "Fraca"
 elif abs_rho < 0.5:
     forca = "Moderada"
 elif abs_rho < 0.7:
     forca = "Forte"
 else:
     forca = "Muito Forte"
 
 direcao = "Positiva" if rho > 0 else "Negativa"
 
 if p_spearman < 0.001:
     sig = "***"
     sig_text = "Altamente significativa"
 elif p_spearman < 0.01:
     sig = "**"
     sig_text = "Muito significativa"
 elif p_spearman < 0.05:
     sig = "*"
     sig_text = "Significativa"
 else:
     sig = "ns"
     sig_text = "Não significativa"
 
 return {
     'spearman_rho': rho,
     'spearman_p': p_spearman,
     'pearson_r': r,
     'pearson_p': p_pearson,
     'forca': forca,
     'direcao': direcao,
     'significancia': sig,
     'sig_text': sig_text
 }

# ============================================
# RESPOSTAS ÀS QUESTÕES DE PESQUISA
# ============================================

print("\n" + "="*80)
print("RESPOSTAS ÀS QUESTÕES DE PESQUISA")
print("="*80)

respostas_rq = {}

print("\n" + "┏" + "━"*78 + "┓")
print("┃" + " "*20 + "DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES" + " "*19 + "┃")
print("┗" + "━"*78 + "┛")

# RQ01
print("\n" + "─"*80)
print("📌 RQ01: Qual a relação entre o TAMANHO dos PRs e o FEEDBACK FINAL?")
print("─"*80)

resultado = analise_correlacao_completa('tamanho_total_linhas', 'estado_numerico', df)
respostas_rq['RQ01'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f"   Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

merged_tamanho = df[df['estado'] == 'MERGED']['tamanho_total_linhas']
closed_tamanho = df[df['estado'] == 'CLOSED']['tamanho_total_linhas']

print(f"\n🔹 Estatísticas Descritivas:")
print(f"   MERGED: Mediana = {merged_tamanho.median():.0f} | Média = {merged_tamanho.mean():.0f} | DP = {merged_tamanho.std():.0f}")
print(f"   CLOSED: Mediana = {closed_tamanho.median():.0f} | Média = {closed_tamanho.mean():.0f} | DP = {closed_tamanho.std():.0f}")

u_stat, p_val = stats.mannwhitneyu(merged_tamanho, closed_tamanho, alternative='two-sided')
print(f"\n🔹 Teste Mann-Whitney U: U = {u_stat:,.0f}, p = {p_val:.4f}")

z_score = abs(stats.norm.ppf(p_val / 2)) if p_val > 0 else 0
effect_size = z_score / np.sqrt(len(df)) if z_score > 0 else 0
print(f"   Effect Size (r): {effect_size:.4f}", end="")

if effect_size < 0.1:
 print(" (Trivial)")
elif effect_size < 0.3:
 print(" (Pequeno)")
elif effect_size < 0.5:
 print(" (Médio)")
else:
 print(" (Grande)")

print(f"\n📊 INTERPRETAÇÃO:")
if p_val < 0.05:
 if closed_tamanho.median() > 0:
     diferenca = ((merged_tamanho.median() - closed_tamanho.median()) / closed_tamanho.median()) * 100
 else:
     diferenca = 0
 if merged_tamanho.median() > closed_tamanho.median():
     print(f"   ✓ PRs MERGED são significativamente MAIORES ({diferenca:+.1f}%) que PRs CLOSED")
     print(f"   → PRs maiores têm maior probabilidade de serem aceitos")
 else:
     print(f"   ✓ PRs CLOSED são significativamente MAIORES ({-diferenca:+.1f}%) que PRs MERGED")
     print(f"   → PRs menores têm maior probabilidade de serem aceitos")
else:
 print(f"   ✗ Não há diferença significativa no tamanho entre PRs MERGED e CLOSED")
 print(f"   → O tamanho não é um fator determinante para aceitação")

#RQ02: Tempo de Análise e Feedback Final
print("\n" + "─"*80) 
print("📌 RQ02: Qual a relação entre o TEMPO DE ANÁLISE e o FEEDBACK FINAL?")
print("─"*80)

resultado = analise_correlacao_completa('tempo_analise_dias', 'estado_numerico', df)
respostas_rq['RQ02'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f" Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

merged_tempo = df[df['estado'] == 'MERGED']['tempo_analise_dias']
closed_tempo = df[df['estado'] == 'CLOSED']['tempo_analise_dias']

print(f"\n🔹 Estatísticas Descritivas:")
print(f" MERGED: Mediana = {merged_tempo.median():.1f} dias | Média = {merged_tempo.mean():.1f} | DP = {merged_tempo.std():.1f}")
print(f" CLOSED: Mediana = {closed_tempo.median():.1f} dias | Média = {closed_tempo.mean():.1f} | DP = {closed_tempo.std():.1f}")

u_stat, p_val = stats.mannwhitneyu(merged_tempo, closed_tempo, alternative='two-sided')
print(f"\n🔹 Teste Mann-Whitney U: U = {u_stat:,.0f}, p = {p_val:.4f}")

z_score = abs(stats.norm.ppf(p_val / 2))
effect_size = z_score / np.sqrt(len(df))
print(f" Effect Size (r): {effect_size:.4f}", end="")

if effect_size < 0.1: print(" (Trivial)")
elif effect_size < 0.3: print(" (Pequeno)")
elif effect_size < 0.5: print(" (Médio)")
else: print(" (Grande)")

print(f"\n📊 INTERPRETAÇÃO:") 
if p_val < 0.05: 
   diferenca_dias = merged_tempo.median() - closed_tempo.median() if merged_tempo.median() > closed_tempo.median() else closed_tempo.median() - merged_tempo.median()
   if merged_tempo.median() > closed_tempo.median():
       print(f" ✓ PRs MERGED demoram {diferenca_dias:.1f} dias A MAIS para serem analisados")
       print(f" → PRs aceitos passam por análise mais cuidadosa e demorada")
   else:
       print(f" ✓ PRs CLOSED demoram {-diferenca_dias:.1f} dias A MAIS para serem analisados")
       print(f" → PRs rejeitados podem levar mais tempo devido a problemas identificados")
else:
   print(f" ✗ Não há diferença significativa no tempo entre PRs MERGED e CLOSED")
   print(f" → O tempo de análise não é um indicador do resultado final")

#RQ03: Descrição dos PRs e Feedback Final
print("\n" + "─"*80)
print("📌 RQ03: Qual a relação entre a DESCRIÇÃO dos PRs e o FEEDBACK FINAL?")
print("─"*80)

resultado = analise_correlacao_completa('tamanho_descricao_caracteres', 'estado_numerico', df)
respostas_rq['RQ03'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f" Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

merged_desc = df[df['estado'] == 'MERGED']['tamanho_descricao_caracteres']
closed_desc = df[df['estado'] == 'CLOSED']['tamanho_descricao_caracteres']

print(f"\n🔹 Estatísticas Descritivas:")
print(f" MERGED: Mediana = {merged_desc.median():.0f} caracteres | Média = {merged_desc.mean():.0f} | DP = {merged_desc.std():.0f}")
print(f" CLOSED: Mediana = {closed_desc.median():.0f} caracteres | Média = {closed_desc.mean():.0f} | DP = {closed_desc.std():.0f}")

u_stat, p_val = stats.mannwhitneyu(merged_desc, closed_desc, alternative='two-sided')
print(f"\n🔹 Teste Mann-Whitney U: U = {u_stat:,.0f}, p = {p_val:.4f}")

z_score = abs(stats.norm.ppf(p_val / 2))
effect_size = z_score / np.sqrt(len(df))
print(f" Effect Size (r): {effect_size:.4f}", end="")

if effect_size < 0.1: 
   print(" (Trivial)")
elif effect_size < 0.3: 
   print(" (Pequeno)")
elif effect_size < 0.5: 
   print(" (Médio)")
else: 
   print(" (Grande)")

print(f"\n📊 INTERPRETAÇÃO:")
if p_val < 0.05:
   diferenca_perc = ((merged_desc.median() - closed_desc.median()) / closed_desc.median()) * 100 if merged_desc.median() > closed_desc.median() else ((closed_desc.median() - merged_desc.median()) / merged_desc.median()) * 100
   if merged_desc.median() > closed_desc.median():
       print(f" ✓ PRs MERGED têm descrições {diferenca_perc:+.1f}% MAIS LONGAS")
       print(f" → Descrições detalhadas aumentam a probabilidade de aceitação")
       print(f" → Boa documentação facilita o processo de revisão")
   else:
       print(f" ✓ PRs CLOSED têm descrições {-diferenca_perc:+.1f}% MAIS LONGAS")
       print(f" → Descrições longas podem indicar complexidade excessiva")
else:
   print(f" ✗ Não há diferença significativa na descrição entre PRs MERGED e CLOSED")
   print(f" → O tamanho da descrição não é um fator determinante")

#RQ04: Interações nos PRs e Feedback Final
print("\n" + "─"*80)
print("📌 RQ04: Qual a relação entre as INTERAÇÕES nos PRs e o FEEDBACK FINAL?")
print("─"*80)

# Analisar participantes

print("\n🔸 Número de Participantes:")
resultado_part = analise_correlacao_completa('num_participantes', 'estado_numerico', df)
respostas_rq['RQ04_participantes'] = resultado_part

print(f" Correlação: ρ = {resultado_part['spearman_rho']:.4f} (p = {resultado_part['spearman_p']:.4f}) {resultado_part['significancia']}")
print(f" {resultado_part['forca']} | {resultado_part['direcao']}")

merged_part = df[df['estado'] == 'MERGED']['num_participantes']
closed_part = df[df['estado'] == 'CLOSED']['num_participantes']

print(f" MERGED: Mediana = {merged_part.median():.1f} | CLOSED: Mediana = {closed_part.median():.1f}")

u_stat, p_val = stats.mannwhitneyu(merged_part, closed_part)
if p_val < 0.05:
    if merged_part.median() > closed_part.median():
        print(f" ✓ PRs MERGED têm MAIS participantes (p = {p_val:.4f})")
    else:
        print(f" ✓ PRs CLOSED têm MAIS participantes (p = {p_val:.4f})")
else:
    print(f" ✗ Sem diferença significativa (p = {p_val:.4f})")

# Analisar comentários

print("\n🔸 Número de Comentários:")
resultado_com = analise_correlacao_completa('num_comentarios', 'estado_numerico', df)
respostas_rq['RQ04_comentarios'] = resultado_com

print(f" Correlação: ρ = {resultado_com['spearman_rho']:.4f} (p = {resultado_com['spearman_p']:.4f}) {resultado_com['significancia']}")
print(f" {resultado_com['forca']} | {resultado_com['direcao']}")

merged_com = df[df['estado'] == 'MERGED']['num_comentarios']
closed_com = df[df['estado'] == 'CLOSED']['num_comentarios']

print(f" MERGED: Mediana = {merged_com.median():.1f} | CLOSED: Mediana = {closed_com.median():.1f}")

u_stat, p_val = stats.mannwhitneyu(merged_com, closed_com)
if p_val < 0.05:
    if merged_com.median() > closed_com.median():
        print(f" ✓ PRs MERGED têm MAIS comentários (p = {p_val:.4f})")
    else:
        print(f" ✓ PRs CLOSED têm MAIS comentários (p = {p_val:.4f})")
else:
    print(f" ✗ Sem diferença significativa (p = {p_val:.4f})")

print(f"\n📊 INTERPRETAÇÃO GERAL:")
print(f" As interações (participantes e comentários) {'são' if (resultado_part['spearman_p'] < 0.05 or resultado_com['spearman_p'] < 0.05) else 'não são'} indicadores significativos do feedback final.")

# DIMENSÃO B: NÚMERO DE REVISÕES
print("\n" + "┏" + "━"*78 + "┓")
print("┃" + " "*25 + "DIMENSÃO B: NÚMERO DE REVISÕES" + " "*23 + "┃")
print("┗" + "━"*78 + "┛")

# RQ05: Tamanho dos PRs e Número de Revisões
print("\n" + "─"*80)
print("📌 RQ05: Qual a relação entre o TAMANHO dos PRs e o NÚMERO DE REVISÕES?")
print("─"*80)

resultado = analise_correlacao_completa('tamanho_total_linhas', 'num_revisoes', df)
respostas_rq['RQ05'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f" Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

# Regressão Linear

x = df['tamanho_total_linhas'].values.reshape(-1, 1)
y = df['num_revisoes'].values
model = LinearRegression().fit(x, y)
r2 = r2_score(y, model.predict(x))

print(f"\n🔹 Modelo de Regressão Linear:")
print(f" R² = {r2:.4f} ({r2*100:.2f}% da variância explicada)")
print(f" Coeficiente: {model.coef_[0]:.6f}")
print(f" Intercepto: {model.intercept_:.4f}")
print(f" Equação: Revisões = {model.intercept_:.2f} + {model.coef_[0]:.6f} × Tamanho")

# Interpretação prática

revisoes_100_linhas = model.coef_[0] * 100
revisoes_500_linhas = model.coef_[0] * 500

print(f"\n🔹 Interpretação Prática:")
print(f" • A cada 100 linhas adicionais: +{revisoes_100_linhas:.2f} revisões")
print(f" • A cada 500 linhas adicionais: +{revisoes_500_linhas:.2f} revisões")

print(f"\n📊 INTERPRETAÇÃO:")
if resultado['spearman_p'] < 0.05:
    if resultado['spearman_rho'] > 0:
        print(f" ✓ Existe relação {resultado['forca'].lower()} POSITIVA entre tamanho e revisões")
        print(f" → PRs maiores requerem MAIS revisões")
        print(f" → Recomenda-se dividir PRs grandes em menores")
    else:
        print(f" ✓ Existe relação {resultado['forca'].lower()} NEGATIVA entre tamanho e revisões")
        print(f" → PRs maiores requerem MENOS revisões (incomum)")
else:
    print(f" ✗ Não há relação significativa entre tamanho e número de revisões")

# RQ06: Tempo de Análise e Número de Revisões
print("\n" + "─"*80)
print("📌 RQ06: Qual a relação entre o TEMPO DE ANÁLISE e o NÚMERO DE REVISÕES?")
print("─"*80)

resultado = analise_correlacao_completa('tempo_analise_dias', 'num_revisoes', df)
respostas_rq['RQ06'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f" Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

#Regressão Linear

x = df['tempo_analise_dias'].values.reshape(-1, 1)
y = df['num_revisoes'].values
model = LinearRegression().fit(x, y)
r2 = r2_score(y, model.predict(x))

print(f"\n🔹 Modelo de Regressão Linear:")
print(f" R² = {r2:.4f} ({r2*100:.2f}% da variância explicada)") 
print(f" Coeficiente: {model.coef_[0]:.6f}") 
print(f" Equação: Revisões = {model.intercept_:.2f} + {model.coef_[0]:.4f} × Tempo(dias)")

print(f"\n🔹 Interpretação Prática:") 
print(f" • A cada dia adicional de análise: +{model.coef_[0]:.3f} revisões") 
print(f" • A cada semana adicional: +{model.coef_[0]*7:.2f} revisões")

print(f"\n📊 INTERPRETAÇÃO:") 
if resultado['spearman_p'] < 0.05:
    if resultado['spearman_rho'] > 0: 
        print(f" ✓ Existe relação {resultado['forca'].lower()} POSITIVA entre tempo e revisões")
        print(f" → Mais revisões aumentam o tempo de análise") 
        print(f" → Cada ciclo de revisão adiciona dias ao processo") 
    else: 
        print(f" ✓ Existe relação {resultado['forca'].lower()} NEGATIVA entre tempo e revisões") 
else:
    print(f" ✗ Não há relação significativa entre tempo e número de revisões")

# RQ07: Descrição dos PRs e Número de Revisões
print("\n" + "─"*80) 
print("📌 RQ07: Qual a relação entre a DESCRIÇÃO dos PRs e o NÚMERO DE REVISÕES?")
print("─"*80)

resultado = analise_correlacao_completa('tamanho_descricao_caracteres', 'num_revisoes', df)
respostas_rq['RQ07'] = resultado

print(f"\n🔹 Correlação de Spearman: ρ = {resultado['spearman_rho']:.4f} (p = {resultado['spearman_p']:.4f}) {resultado['significancia']}")
print(f" Força: {resultado['forca']} | Direção: {resultado['direcao']} | {resultado['sig_text']}")

# Regressão Linear
x = df['tamanho_descricao_caracteres'].values.reshape(-1, 1)
y = df['num_revisoes'].values
model = LinearRegression().fit(x, y)
r2 = r2_score(y, model.predict(x))

print(f"\n🔹 Modelo de Regressão Linear:")
print(f" R² = {r2:.4f} ({r2*100:.2f}% da variância explicada)")
print(f" Coeficiente: {model.coef_[0]:.8f}")

print(f"\n📊 INTERPRETAÇÃO:")
if resultado['spearman_p'] < 0.05:
    if resultado['spearman_rho'] > 0:
        print(f" ✓ Existe relação {resultado['forca'].lower()} POSITIVA")
        print(f" → Descrições mais longas estão associadas a MAIS revisões")
        print(f" → Pode indicar PRs mais complexos que requerem documentação detalhada")
    else:
        print(f" ✓ Existe relação {resultado['forca'].lower()} NEGATIVA")
        print(f" → Descrições mais longas estão associadas a MENOS revisões")
        print(f" → Boa documentação pode facilitar o processo de revisão")
else:
    print(f" ✗ Não há relação significativa entre descrição e número de revisões")
    print(f" → O tamanho da descrição não afeta o número de revisões necessárias")

# RQ08: Interações nos PRs e Número de Revisões
print("\n" + "─"*80) 
print("📌 RQ08: Qual a relação entre as INTERAÇÕES nos PRs e o NÚMERO DE REVISÕES?")
print("─"*80)

#Participantes

print("\n🔸 Número de Participantes vs Revisões:") 
resultado_part = analise_correlacao_completa('num_participantes', 'num_revisoes', df) 
respostas_rq['RQ08_participantes'] = resultado_part

print(f" Correlação: ρ = {resultado_part['spearman_rho']:.4f} (p = {resultado_part['spearman_p']:.4f}) {resultado_part['significancia']}") 
print(f" {resultado_part['forca']} | {resultado_part['direcao']}")

x = df['num_participantes'].values.reshape(-1, 1)
y = df['num_revisoes'].values
model = LinearRegression().fit(x, y)
r2 = r2_score(y, model.predict(x))
print(f" R² = {r2:.4f} | Coeficiente = {model.coef_[0]:.4f}")

if resultado_part['spearman_p'] < 0.05: print(f" ✓ Relação significativa: cada participante adicional → +{model.coef_[0]:.2f} revisões")

#Comentários

print("\n🔸 Número de Comentários vs Revisões:") 
resultado_com = analise_correlacao_completa('num_comentarios', 'num_revisoes', df) 
respostas_rq['RQ08_comentarios'] = resultado_com

print(f" Correlação: ρ = {resultado_com['spearman_rho']:.4f} (p = {resultado_com['spearman_p']:.4f}) {resultado_com['significancia']}") 
print(f" {resultado_com['forca']} | {resultado_com['direcao']}")

x = df['num_comentarios'].values.reshape(-1, 1) 
y = df['num_revisoes'].values 
model = LinearRegression().fit(x, y) 
r2 = r2_score(y, model.predict(x))
print(f" R² = {r2:.4f} | Coeficiente = {model.coef_[0]:.4f}")

if resultado_com['spearman_p'] < 0.05: print(f" ✓ Relação significativa: cada comentário adicional → +{model.coef_[0]:.3f} revisões")

print(f"\n📊 INTERPRETAÇÃO GERAL:") 
if resultado_part['spearman_p'] < 0.05 or resultado_com['spearman_p'] < 0.05: 
    print(f" ✓ As interações SÃO preditores significativos do número de revisões") 
if resultado_part['spearman_rho'] > 0: 
    print(f" → Mais participantes = mais revisões (diferentes perspectivas)") 
if resultado_com['spearman_rho'] > 0: 
   print(f" → Mais comentários = mais revisões (discussão ativa)") 
else: 
    print(f" ✗ As interações NÃO são preditores significativos do número de revisões")

print("\n" + "="*80)
print("SUMÁRIO EXECUTIVO")
print("="*80)
print(f"""
📊 VISUALIZAÇÕES GERADAS:
════════════════════════
✓ 01_distribuicoes_log.png - Distribuições com escala logarítmica
✓ 02_merged_vs_closed_log.png - Comparação com escala log
✓ 03_series_temporais.png - Análise temporal
✓ 04_correlacao_spearman.png - Matriz de correlação
✓ 05_regressao_revisoes_log.png - Regressões com escala log
✓ 06_densidades_comparativas.png - Comparação de densidades
✓ 07_analise_quantis.png - Análise por quantis
✓ 08_heatmap_comparativo.png - Heatmap de métricas

Dataset: {len(df):,} Pull Requests
Período: {df['data_criacao'].min().strftime('%Y-%m-%d')} a {df['data_criacao'].max().strftime('%Y-%m-%d')}
""")

print("="*80)
print("ANÁLISE CONCLUÍDA COM SUCESSO! ✅")
print("="*80)

# Exportar resultados
print("\n📁 Exportando resultados...")

stats_por_grupo = pd.DataFrame({
 'Variavel': [var for var, _ in variaveis_comparacao],
 'MERGED_Mediana': [df[df['estado'] == 'MERGED'][var].median() for var, _ in variaveis_comparacao],
 'CLOSED_Mediana': [df[df['estado'] == 'CLOSED'][var].median() for var, _ in variaveis_comparacao],
 'MannWhitney_U': [resultados_testes[var]['u_stat'] for var, _ in variaveis_comparacao],
 'p_value': [resultados_testes[var]['p_value'] for var, _ in variaveis_comparacao]
})

stats_por_grupo.to_csv('estatisticas_por_grupo.csv', index=False)
print("✓ Salvo: estatisticas_por_grupo.csv")

print("\n✅ Todos os arquivos foram gerados com sucesso!")