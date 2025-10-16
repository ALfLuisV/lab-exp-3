# 📊 Análise Estatística de Pull Requests - Lab Experimental 3

Este projeto realiza uma análise estatística completa de Pull Requests de repositórios open-source, respondendo a 8 questões de pesquisa sobre os fatores que influenciam o feedback final das revisões e o número de revisões realizadas.

## 🎯 Objetivos

Analisar relações entre:
- **Dimensão A**: Características dos PRs × Feedback Final (MERGED/CLOSED)
- **Dimensão B**: Características dos PRs × Número de Revisões

## 📁 Estrutura do Projeto

```
lab-exp-3/
├── finalResults/
│   ├── dados_pull_requests.json
│   ├── dados_pull_requests2.json
│   └── dados_pull_requests3.json      # Dataset principal (13.933 PRs)
├── analise_pull_requests.py           # Script principal de análise
├── analise_completa.png               # 12 gráficos das RQs
├── correlacao_spearman.png            # Mapa de calor de correlações
├── analise_regressao.png              # Análise de regressão linear
├── resumo_analise.txt                 # Resumo executivo
├── relatorio_detalhado.md             # Relatório completo
└── requirements.txt                   # Dependências
```

## 🔬 Metodologia

### Teste Estatístico: Correlação de Spearman

**Justificativa:**
1. **Dados não-normais**: Teste de Shapiro-Wilk confirmou distribuição não-normal
2. **Robustez a outliers**: 13.8% dos dados são outliers
3. **Relações monotônicas**: Mais adequado para dados de software
4. **Variáveis discretas**: Contagens (revisões, comentários) melhor tratadas por Spearman

**Interpretação:**
- |ρ| < 0.1: Desprezível
- 0.1 ≤ |ρ| < 0.3: Fraca
- 0.3 ≤ |ρ| < 0.5: Moderada
- 0.5 ≤ |ρ| < 0.7: Forte
- |ρ| ≥ 0.7: Muito Forte

## 📊 Dataset

- **Total de PRs**: 13.933
- **PRs Aprovados (MERGED)**: 9.458 (67.88%)
- **PRs Rejeitados (CLOSED)**: 4.475 (32.12%)

### Variáveis Analisadas:
- `tamanho_total`: Linhas adicionadas + removidas
- `tempo_analise_dias`: Tempo desde criação até fechamento
- `tamanho_descricao_caracteres`: Tamanho da descrição do PR
- `num_participantes`: Número de pessoas envolvidas
- `num_comentarios`: Total de comentários
- `num_revisoes`: Número de ciclos de revisão
- `estado`: MERGED ou CLOSED

## 🔍 Questões de Pesquisa e Resultados

### Dimensão A: Feedback Final das Revisões

#### RQ 01: Tamanho dos PRs × Feedback Final
- **ρ = 0.0797** (Desprezível, mas significativa)
- **Insight**: PRs pequenos têm 35% de rejeição vs 28-30% para outros tamanhos
- **Recomendação**: Manter PRs em tamanho médio (50-500 linhas)

#### RQ 02: Tempo de Análise × Feedback Final
- **ρ = -0.1600** (Fraca negativa)
- **Insight**: PRs aprovados: 2.1 dias (mediana) vs PRs rejeitados: 6.8 dias
- **Recomendação**: Responder rapidamente a feedback

#### RQ 03: Descrição × Feedback Final
- **ρ = 0.1111** (Fraca positiva)
- **Insight CRÍTICO**: 
  - ✅ Com descrição: 69% aprovação
  - ❌ Sem descrição: 23% aprovação
- **Recomendação**: SEMPRE incluir descrição

#### RQ 04: Interações × Feedback Final
- **Participantes**: ρ = 0.1028 (Fraca)
- **Comentários**: ρ = -0.0716 (Desprezível)
- **Insight**: Mais comentários pode indicar problemas

### Dimensão B: Número de Revisões

#### RQ 05: Tamanho × Revisões
- **ρ = 0.3904** (Moderada) ⭐
- **Insight**: PRs muito grandes requerem 6x mais revisões
- **Recomendação**: Dividir PRs grandes

#### RQ 06: Tempo × Revisões
- **ρ = 0.3496** (Moderada)
- **Insight**: Mais revisões = mais tempo (processo iterativo)

#### RQ 07: Descrição × Revisões
- **ρ = 0.0197** (Desprezível)
- **Insight**: Tamanho da descrição não prediz revisões

#### RQ 08: Interações × Revisões
- **Participantes**: ρ = 0.5395 (Forte) ⭐⭐
- **Comentários**: ρ = 0.4588 (Moderada) ⭐
- **Insight**: Correlação mais forte do estudo! Processo colaborativo iterativo

## 📈 Análise de Regressão

**Modelo**: Predição do Número de Revisões
- **R² = 0.5191** (51.91% da variância explicada)

**Principais Preditores**:
1. `num_comentarios`: +0.459 revisões/comentário
2. `num_participantes`: +0.239 revisões/participante
3. Tamanho e descrição: efeito mínimo

## 🎯 Principais Conclusões

### 1. 🔑 Descrição é ESSENCIAL
- **3x mais chances** de aprovação com descrição

### 2. 📏 Tamanho Moderado é Ideal
- PRs médios têm melhor taxa de aprovação
- PRs grandes requerem 6x mais revisões

### 3. ⚡ Velocidade Importa
- Mediana de 2.1 dias para aprovação
- PRs "parados" tendem à rejeição

### 4. 👥 Engajamento Colaborativo
- Forte correlação revisões ↔ participantes (ρ = 0.54)
- Processo iterativo natural

### 5. ⚖️ Balancear Qualidade e Velocidade
- Mais revisões melhoram qualidade
- Mas aumentam tempo até merge

## 🛠️ Como Executar

### Instalação

```bash
# Clone o repositório
git clone https://github.com/ALfLuisV/lab-exp-3.git
cd lab-exp-3

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
python analise_pull_requests.py
```

### Arquivos Gerados

1. **analise_completa.png** - 12 visualizações das questões de pesquisa
2. **correlacao_spearman.png** - Mapa de calor de correlações
3. **analise_regressao.png** - Gráficos de regressão linear
4. **resumo_analise.txt** - Resumo executivo em texto
5. **relatorio_detalhado.md** - Relatório completo com interpretações

## 📦 Dependências

- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scipy >= 1.10.0
- scikit-learn >= 1.3.0

## 📚 Referências

- **Teste de Spearman**: Myers, J. L., & Well, A. D. (2003). Research Design and Statistical Analysis
- **Shapiro-Wilk**: Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality
- **Cohen's d**: Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences

## 👨‍💻 Autor

**Vinícius Luis**
- GitHub: [@ALfLuisV](https://github.com/ALfLuisV)

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Data da Análise**: 15 de outubro de 2025  
**Dataset**: 13.933 Pull Requests de repositórios open-source  
**Ferramenta**: Python + Seaborn + SciPy + Scikit-learn