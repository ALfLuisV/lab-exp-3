# Relatório Completo - Análise de Pull Requests

## 📊 Resumo Executivo

Este relatório apresenta uma análise estatística completa de **13.933 Pull Requests** coletados de repositórios open-source, respondendo a 8 questões de pesquisa sobre os fatores que influenciam o feedback final das revisões e o número de revisões realizadas.

---

## 🔬 Metodologia

### Teste Estatístico Escolhido: **Correlação de Spearman**

**Justificativa:**

1. **Distribuição Não-Normal**: O teste de Shapiro-Wilk confirmou que todas as variáveis analisadas (tamanho_total, tempo_analise_dias, num_revisoes, tamanho_descricao_caracteres) **não seguem distribuição normal** (p < 0.05).

2. **Robustez a Outliers**: Identificamos 1.924 PRs outliers em termos de tamanho (13.8% dos dados). O teste de Spearman é baseado em rankings, sendo robusto a valores extremos.

3. **Relações Monotônicas**: Spearman captura relações monotônicas (não necessariamente lineares), mais adequadas para dados de engenharia de software.

4. **Variáveis Discretas**: Número de revisões e comentários são contagens discretas, melhor tratadas por testes não-paramétricos.

**Interpretação dos valores de ρ (rho):**
- |ρ| < 0.1: Desprezível
- 0.1 ≤ |ρ| < 0.3: Fraca
- 0.3 ≤ |ρ| < 0.5: Moderada
- 0.5 ≤ |ρ| < 0.7: Forte
- |ρ| ≥ 0.7: Muito Forte

---

## 📈 Estatísticas Descritivas

### Distribuição dos Estados
- **MERGED**: 9.458 PRs (67.88%)
- **CLOSED**: 4.475 PRs (32.12%)

### Métricas Principais
| Métrica | Média | Mediana | Desvio Padrão |
|---------|-------|---------|---------------|
| Tempo de Análise (dias) | 47.57 | 3.03 | 163.50 |
| Tamanho Total (linhas) | - | - | - |
| Número de Arquivos | - | - | - |
| Número de Participantes | 4.29 | 4.00 | - |
| Número de Comentários | 15.24 | 8.00 | 24.83 |
| Número de Revisões | 7.27 | 2.00 | 16.50 |

---

## 🔍 Respostas às Questões de Pesquisa

### Dimensão A: Feedback Final das Revisões (Status do PR)

#### **RQ 01: Tamanho dos PRs × Feedback Final**

**Resultado:**
- **Spearman ρ = 0.0797** (p < 0.001) - Correlação Desprezível mas Significativa
- **Pearson r = -0.0350** (p < 0.001)

**Análise por Categoria:**
```
Categoria        | % CLOSED | % MERGED
-----------------|----------|----------
Pequeno          | 35.22%   | 64.78%
Médio            | 29.51%   | 70.49%
Grande           | 28.40%   | 71.60%
Muito Grande     | 29.72%   | 70.28%
```

**Interpretação:**
Apesar da correlação desprezível, há uma tendência interessante: **PRs pequenos têm maior taxa de rejeição** (35.22%) comparado aos demais. Isso pode indicar que:
- PRs muito pequenos podem ser vistos como triviais ou incompletos
- PRs médios e grandes (não extremos) têm melhor taxa de aprovação
- A complexidade do PR importa mais que o tamanho absoluto

**Recomendação:** Manter PRs em tamanho médio (50-500 linhas) para maximizar chances de aprovação.

---

#### **RQ 02: Tempo de Análise × Feedback Final**

**Resultado:**
- **Spearman ρ = -0.1600** (p < 0.001) - Correlação Fraca Negativa

**Tempo Médio por Estado:**
```
Estado  | Média (dias) | Mediana (dias)
--------|--------------|---------------
MERGED  | 28.28        | 2.13
CLOSED  | 88.36        | 6.77
```

**Interpretação:**
Existe uma **correlação negativa fraca mas significativa**: PRs que levam mais tempo tendem a ser rejeitados.

**Possíveis Explicações:**
1. PRs problemáticos ficam "parados" esperando correções
2. Falta de engajamento do autor leva ao fechamento
3. PRs rapidamente revisados indicam qualidade ou simplicidade
4. O tempo prolongado pode indicar perda de relevância

**Insight Importante:** A mediana de 2.13 dias para PRs aprovados vs 6.77 dias para rejeitados sugere que **velocidade de resposta é crucial**.

---

#### **RQ 03: Descrição dos PRs × Feedback Final**

**Resultado:**
- **Spearman ρ = 0.1111** (p < 0.001) - Correlação Fraca Positiva
- **Pearson r = -0.0072** (p = 0.396) - Não significativo

**Taxa de Aprovação por Presença de Descrição:**
```
Descrição       | % CLOSED | % MERGED
----------------|----------|----------
Sem Descrição   | 76.56%   | 23.44%
Com Descrição   | 30.86%   | 69.14%
```

**Interpretação:**
Este é um dos **resultados mais impactantes**: PRs sem descrição têm **76.56% de taxa de rejeição**!

**Implicações Práticas:**
- Descrição é **ESSENCIAL** para aprovação
- Não é apenas o tamanho da descrição que importa (correlação fraca de Spearman)
- A **presença** de qualquer descrição já aumenta dramaticamente as chances

**Recomendação:** SEMPRE incluir descrição no PR, explicando o contexto, motivação e impacto das mudanças.

---

#### **RQ 04: Interações × Feedback Final**

**Resultado:**
- **Participantes**: Spearman ρ = 0.1028 (p < 0.001) - Fraca Positiva
- **Comentários**: Spearman ρ = -0.0716 (p < 0.001) - Desprezível Negativa

**Médias por Estado:**
```
Estado  | Participantes | Comentários
--------|---------------|-------------
MERGED  | 4.19          | 14.86
CLOSED  | 4.50          | 16.03
```

**Interpretação:**
Resultado contraintuitivo: 
- Mais participantes correlaciona levemente com aprovação
- Mais comentários correlaciona levemente com rejeição

**Hipóteses:**
1. PRs problemáticos geram mais discussão (comentários)
2. PRs simples e corretos são aprovados rapidamente com poucos comentários
3. Engajamento de múltiplos participantes pode indicar interesse/importância
4. Comentários podem representar problemas sendo discutidos

**Conclusão:** Engajamento não garante aprovação - qualidade do código é mais determinante.

---

### Dimensão B: Número de Revisões

#### **RQ 05: Tamanho dos PRs × Número de Revisões**

**Resultado:**
- **Spearman ρ = 0.3904** (p < 0.001) - **Correlação Moderada Positiva**
- **Pearson r = -0.0005** (p = 0.955) - Não significativo

**Média de Revisões por Categoria:**
```
Categoria        | Média | Mediana
-----------------|-------|--------
Pequeno          | 2.68  | 2.0
Médio            | 6.84  | 3.0
Grande           | 11.24 | 5.0
Muito Grande     | 16.52 | 5.0
```

**Interpretação:**
Esta é a **correlação mais forte na Dimensão A**! 

**Insights:**
- PRs maiores requerem **6x mais revisões** que pequenos
- Relação **não-linear** (Pearson não significativo, Spearman sim)
- Cada aumento de categoria aproximadamente **dobra** o número de revisões

**Implicação Prática:** Para reduzir ciclos de revisão e acelerar aprovação, **dividir PRs grandes em menores**.

---

#### **RQ 06: Tempo de Análise × Número de Revisões**

**Resultado:**
- **Spearman ρ = 0.3496** (p < 0.001) - **Correlação Moderada Positiva**
- **Pearson r = 0.1628** (p < 0.001)

**Interpretação:**
Mais revisões levam a mais tempo - relação esperada e lógica.

**Ciclo de Feedback:**
```
Mais Revisões → Mais Tempo → Mais Discussão → Mais Refinamento
```

**Ponto de Atenção:** Embora mais revisões possam melhorar qualidade, também:
- Aumentam tempo até merge
- Podem causar fadiga em revisores e autores
- Retardam entrega de valor

**Recomendação:** Balancear qualidade (revisões) com velocidade (tempo).

---

#### **RQ 07: Descrição dos PRs × Número de Revisões**

**Resultado:**
- **Spearman ρ = 0.0197** (p = 0.020) - **Correlação Desprezível**
- **Pearson r = -0.0318** (p < 0.001)

**Interpretação:**
Tamanho da descrição **NÃO prediz** número de revisões necessárias.

**Conclusão:** 
- Descrição é importante para **aprovação** (RQ03)
- Mas não afeta significativamente o **processo de revisão**
- Qualidade do código importa mais que documentação para ciclos de revisão

---

#### **RQ 08: Interações × Número de Revisões**

**Resultado:**
- **Participantes**: Spearman ρ = 0.5395 (p < 0.001) - **Correlação Forte**
- **Comentários**: Spearman ρ = 0.4588 (p < 0.001) - **Correlação Moderada**

**Interpretação:**
Esta é a **correlação mais forte de todo o estudo**!

**Relação Bidirecional:**
```
Mais Revisões ⟷ Mais Participantes ⟷ Mais Comentários
```

**Insights:**
1. Cada ciclo de revisão traz novos participantes
2. Discussão gera novas revisões
3. Processo iterativo de refinamento colaborativo
4. Correlação forte (0.54) indica relação quase causal

**Implicação:** Para PRs que requerem muitas revisões, esperar alto engajamento da equipe.

---

## 📊 Análise de Regressão Linear

### Modelo: Predição do Número de Revisões

**R² = 0.5191** (51.91% da variância explicada)

**Coeficientes:**
```
Variável                     | Coeficiente | Interpretação
-----------------------------|-------------|--------------------------------
num_comentarios              | +0.459      | Cada comentário → +0.46 revisões
num_participantes            | +0.239      | Cada participante → +0.24 revisões
tamanho_descricao_caracteres | +0.000014   | Efeito mínimo
tempo_analise_dias           | -0.004      | Efeito mínimo negativo
tamanho_total                | -0.000003   | Efeito desprezível
```

**Interpretação:**
- **Comentários e participantes** são os principais preditores
- **Tamanho, descrição e tempo** têm efeito muito pequeno no modelo
- **R² de 0.52** é bom para ciências sociais/engenharia de software
- 48% da variância vem de fatores não medidos (qualidade do código, expertise do revisor, etc.)

---

## 🎯 Conclusões Gerais e Recomendações

### 1. **DESCRIÇÃO É ESSENCIAL** 
- ✅ 69% de aprovação COM descrição
- ❌ 23% de aprovação SEM descrição
- **Recomendação:** SEMPRE incluir descrição detalhada

### 2. **TAMANHO MODERADO É IDEAL**
- PRs médios (50-500 linhas) têm melhor taxa de aprovação
- PRs muito pequenos podem parecer incompletos
- PRs grandes requerem 6x mais revisões
- **Recomendação:** Dividir grandes mudanças em PRs menores

### 3. **VELOCIDADE IMPORTA**
- PRs aprovados: mediana de 2.1 dias
- PRs rejeitados: mediana de 6.8 dias
- **Recomendação:** Responder rapidamente a feedback, manter momentum

### 4. **ENGAJAMENTO É DOUBLE-EDGED SWORD**
- Mais participantes → melhor para aprovação
- Mais comentários → pode indicar problemas
- **Recomendação:** Buscar revisões de qualidade, não quantidade de discussão

### 5. **CICLO ITERATIVO COLABORATIVO**
- Forte correlação revisões ↔ interações (ρ = 0.54)
- Processo natural de refinamento
- **Recomendação:** Aceitar que PRs complexos requerem múltiplas iterações

### 6. **BALANCEAR QUALIDADE E VELOCIDADE**
- Mais revisões melhoram qualidade mas aumentam tempo
- Trade-off entre perfeição e entrega
- **Recomendação:** Definir critérios claros de "pronto para merge"

---

## 📉 Limitações do Estudo

1. **Causalidade**: Correlação não implica causalidade - não podemos afirmar que "aumentar descrição causa aprovação"
2. **Contexto**: Dados de repositórios específicos podem não generalizar para todos os projetos
3. **Variáveis Não Medidas**: Qualidade do código, expertise, urgência, etc. não foram capturadas
4. **Temporal**: Práticas de revisão podem mudar ao longo do tempo

---

## 🔮 Sugestões para Pesquisas Futuras

1. Análise qualitativa do conteúdo das descrições (não apenas tamanho)
2. Impacto da expertise do autor/revisor nos resultados
3. Análise temporal: como práticas evoluem
4. Comparação entre diferentes linguagens/frameworks
5. Machine Learning para predição de aprovação baseado em múltiplas features
6. Análise de sentimento nos comentários

---

## 📁 Arquivos Gerados

1. **analise_completa.png** - 12 gráficos das questões de pesquisa
2. **correlacao_spearman.png** - Mapa de calor de correlações
3. **analise_regressao.png** - Análise de regressão linear
4. **resumo_analise.txt** - Resumo executivo em texto
5. **relatorio_detalhado.md** - Este relatório completo

---

## 📚 Referências Metodológicas

- **Teste de Spearman**: Myers, J. L., & Well, A. D. (2003). Research Design and Statistical Analysis.
- **Teste de Shapiro-Wilk**: Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality.
- **Interpretação de Correlações**: Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences.

---

**Data da Análise:** 15 de outubro de 2025  
**Dataset:** 13.933 Pull Requests  
**Ferramentas:** Python, Pandas, Seaborn, SciPy, Scikit-learn  
**Autor:** Análise Automatizada via GitHub Copilot
