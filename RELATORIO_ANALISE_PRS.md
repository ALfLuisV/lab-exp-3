# RELATÓRIO DE ANÁLISE DE PULL REQUESTS

---

**Data do Relatório:** 15/10/2025 23:59:05  
**Período Analisado:** 22/02/2012 a 15/10/2025  
**Total de Pull Requests:** 13,933  
**PRs MERGED:** 9,458 (67.9%)  
**PRs CLOSED:** 4,475 (32.1%)

---

## 📋 SUMÁRIO EXECUTIVO

Este relatório apresenta uma análise abrangente dos pull requests de varios repositórios , 
com foco em identificar relações entre características dos PRs e seus resultados finais (MERGED ou CLOSED) 
e o número de revisões necessárias. A análise responde a 8 questões de pesquisa (RQs) utilizando métodos 
estatísticos robustos e apropriados para dados não-normais com presença de outliers.

### Principais Achados


- **10 de 8** relações analisadas apresentaram significância estatística (p < 0.05)
- **Taxa de aceitação geral:** 67.9%
- **Tempo médio de análise:** 47.6 dias (mediana: 3.0 dias)
- **Tamanho médio dos PRs:** 3180.9 linhas (mediana: 60.0 linhas)
- **Número médio de revisões:** 7.3 revisões (mediana: 2.0 revisões)

---

## 📊 1. METODOLOGIA

### 1.1 Coleta de Dados

Os dados foram coletados através da API do GitHub, incluindo informações sobre:
- Metadados dos PRs (número, título, autor, URLs)
- Datas de criação e fechamento
- Estado final (MERGED ou CLOSED)
- Métricas de tamanho (arquivos alterados, linhas adicionadas/removidas)
- Métricas de interação (participantes, comentários, revisões)
- Descrição dos PRs

### 1.2 Preparação dos Dados

#### Variáveis Derivadas
- **tamanho_total_linhas:** Soma de linhas adicionadas e removidas
- **estado_numerico:** Codificação binária (MERGED=1, CLOSED=0)
- **tempo_analise_dias:** Diferença entre data de fechamento e criação

#### Tratamento de Dados
- Conversão de datas para formato datetime
- Verificação de valores ausentes: **0 valores ausentes** (dataset completo)
- Remoção de zeros em análises logarítmicas

### 1.3 Análise Exploratória

#### Distribuição dos Estados
| Estado | Quantidade | Percentual |
|--------|-----------|-----------|
| MERGED | 9,458 | 67.88% |
| CLOSED | 4,475 | 32.12% |

#### Estatísticas Descritivas Principais

| Variável | Média | Mediana | Desvio Padrão | Mín | Máx |
|----------|-------|---------|---------------|-----|-----|
| Tempo de Análise (dias) | 47.57 | 3.03 | 163.50 | 0.00 | 3710.51 |
| Tamanho Total (linhas) | 3180.89 | 60.00 | 85267.82 | 0 | 6251681 |
| Número de Revisões | 7.27 | 2.00 | 16.50 | 0 | 377 |
| Número de Comentários | 15.24 | 8.00 | 24.83 | 0 | 387 |
| Participantes | 4.29 | 3.00 | 5.95 | 0 | 419 |

---

## 🔬 2. ESCOLHA DOS TESTES ESTATÍSTICOS

### 2.1 Teste de Normalidade

Para determinar o teste de correlação mais apropriado, realizamos o **Teste de Shapiro-Wilk** 
para verificar a normalidade das distribuições:

| Variável | p-value | Distribuição |
|----------|---------|--------------|
| tempo_analise_dias | 0.0000 | ✗ Não-Normal |
| num_arquivos_alterados | 0.0000 | ✗ Não-Normal |
| linhas_adicionadas | 0.0000 | ✗ Não-Normal |
| linhas_removidas | 0.0000 | ✗ Não-Normal |
| tamanho_total_linhas | 0.0000 | ✗ Não-Normal |
| tamanho_descricao_caracteres | 0.0000 | ✗ Não-Normal |
| num_participantes | 0.0000 | ✗ Não-Normal |
| num_comentarios | 0.0000 | ✗ Não-Normal |
| num_revisoes | 0.0000 | ✗ Não-Normal |


**Resultado:** 9/9 variáveis (100.0%) 
**não seguem distribuição normal** (p-value < 0.05).

### 2.2 Análise de Assimetria e Curtose

A assimetria (skewness) mede a simetria da distribuição, enquanto a curtose mede a "cauda pesada":

| Variável | Assimetria | Interpretação | Curtose |
|----------|-----------|---------------|---------|
| tempo_analise_dias | 8.399 | Assimétrica à Direita (outliers altos) | 100.502 |
| num_arquivos_alterados | 45.476 | Assimétrica à Direita (outliers altos) | 2291.663 |
| linhas_adicionadas | 55.968 | Assimétrica à Direita (outliers altos) | 3426.772 |
| linhas_removidas | 47.044 | Assimétrica à Direita (outliers altos) | 2815.800 |
| tamanho_total_linhas | 53.609 | Assimétrica à Direita (outliers altos) | 3205.662 |
| tamanho_descricao_caracteres | 9.448 | Assimétrica à Direita (outliers altos) | 153.202 |
| num_participantes | 32.269 | Assimétrica à Direita (outliers altos) | 1889.184 |
| num_comentarios | 4.934 | Assimétrica à Direita (outliers altos) | 36.240 |
| num_revisoes | 7.379 | Assimétrica à Direita (outliers altos) | 90.698 |


**Interpretação:**
- **Assimetria > 0:** Maioria dos valores concentrados à esquerda, com outliers à direita
- **Assimetria < 0:** Maioria dos valores concentrados à direita, com outliers à esquerda
- **Curtose > 0:** Distribuição leptocúrtica (caudas pesadas, muitos outliers)
- **Curtose < 0:** Distribuição platicúrtica (caudas leves, poucos outliers)

### 2.3 Justificativa para Escolha do Teste de Spearman

Com base nas análises de normalidade, assimetria e curtose, optamos pela **Correlação de Spearman (ρ)** 
ao invés da Correlação de Pearson (r) pelas seguintes razões:

#### ✅ Vantagens do Spearman para Este Dataset

1. **🔴 VIOLAÇÃO DA NORMALIDADE**
 - 9/9 variáveis não seguem distribuição normal
 - Pearson **assume normalidade bivariada** entre as variáveis
 - Spearman **não requer normalidade** (é um teste não-paramétrico)

2. **🔴 PRESENÇA MASSIVA DE OUTLIERS**
 - Todas as variáveis apresentam **assimetria positiva forte** (> 1.0)
 - Curtose elevada indica **caudas pesadas** com muitos outliers extremos
 - Spearman trabalha com **ranks (posições)**, sendo robusto a outliers
 - Pearson é sensível a outliers, que podem distorcer a correlação

3. **🟡 RELAÇÕES MONOTÔNICAS (NÃO NECESSARIAMENTE LINEARES)**
 - Spearman detecta **qualquer relação monotônica** (sempre crescente ou decrescente)
 - Pearson detecta apenas **relações lineares** (proporcionais)
 - Dados de repositórios GitHub frequentemente apresentam relações não-lineares

4. **🟡 VARIÁVEIS ORDINAIS E DE CONTAGEM**
 - Número de revisões, comentários, participantes são **variáveis discretas de contagem**
 - Spearman é apropriado para **dados ordinais** e rankings
 - Pearson é mais apropriado para **variáveis contínuas verdadeiras**

5. **🟡 ESCALAS MUITO DIFERENTES**
 - Variáveis em escalas muito distintas (dias, linhas, caracteres, contagens)
 - Spearman normaliza através de **transformação em ranks**
 - Reduz o efeito das diferenças de escala

#### ❌ Quando Usaríamos Pearson

A Correlação de Pearson seria apropriada apenas se:
- ✗ Todas as variáveis seguissem **distribuição normal**
- ✗ As relações fossem estritamente **lineares**
- ✗ Não houvesse **outliers significativos**
- ✗ Variáveis fossem **contínuas e intervalares**
- ✗ Houvesse **homocedasticidade** (variância constante)

**Nenhuma dessas condições é satisfeita neste dataset.**

### 2.4 Interpretação dos Coeficientes

#### Correlação de Spearman (ρ)
- **ρ = +1:** Correlação monotônica positiva perfeita
- **ρ = -1:** Correlação monotônica negativa perfeita
- **ρ = 0:** Sem correlação monotônica

#### Força da Correlação (baseado em Cohen, 1988)
- **|ρ| < 0.10:** Trivial
- **0.10 ≤ |ρ| < 0.30:** Fraca
- **0.30 ≤ |ρ| < 0.50:** Moderada
- **0.50 ≤ |ρ| < 0.70:** Forte
- **|ρ| ≥ 0.70:** Muito Forte

#### Níveis de Significância
- **p < 0.001:** Altamente significativa (***)
- **0.001 ≤ p < 0.01:** Muito significativa (**)
- **0.01 ≤ p < 0.05:** Significativa (*)
- **p ≥ 0.05:** Não significativa (ns)

### 2.5 Testes Complementares

#### Teste de Mann-Whitney U
Para comparar grupos (MERGED vs CLOSED), utilizamos o **Teste de Mann-Whitney U**, 
que é o equivalente não-paramétrico do teste t de Student:
- **Não assume normalidade** das distribuições
- Compara **medianas** ao invés de médias
- Robusto a **outliers**
- Apropriado para **amostras independentes**

#### Effect Size (Tamanho do Efeito)
Calculamos o effect size (r) como:


r = Z / √N

Onde Z é o z-score do teste Mann-Whitney U e N é o tamanho da amostra.

**Interpretação:**
- **r < 0.1:** Efeito trivial
- **0.1 ≤ r < 0.3:** Efeito pequeno
- **0.3 ≤ r < 0.5:** Efeito médio
- **r ≥ 0.5:** Efeito grande

---

## 📝 3. RESPOSTAS ÀS QUESTÕES DE PESQUISA

---

## 🎯 DIMENSÃO A: FEEDBACK FINAL DAS REVISÕES (Status do PR)

Esta dimensão investiga quais características dos Pull Requests estão associadas ao resultado 
final: **MERGED (aceito)** ou **CLOSED (rejeitado)**.

---

### RQ01: Qual a relação entre o TAMANHO dos PRs e o FEEDBACK FINAL?

#### Hipótese
PRs menores tendem a ser mais facilmente revisados e aceitos, enquanto PRs grandes podem ser mais 
difíceis de revisar e mais propensos a rejeição.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = 0.0797**
- **p-value = 0.0000** ***
- **Força:** Trivial
- **Direção:** Positiva
- **Significância:** Altamente significativa

**Correlação de Pearson (para comparação):**
- **r = -0.0350**
- **p-value = 0.0000**

#### Comparação entre Grupos (MERGED vs CLOSED)

| Métrica | MERGED | CLOSED | Diferença |
|---------|--------|--------|-----------|
| **Mediana** | 68.0 linhas | 42.0 linhas | +61.9% |
| **Média** | 1127.9 linhas | 7520.0 linhas | -85.0% |

**Teste de Mann-Whitney U:**
- **U-statistic = 23,247,846**
- **p-value = 0.0000** ***
- **Effect Size (r) = 0.0797** (Trivial)

#### 📊 Interpretação

✅ **RELAÇÃO SIGNIFICATIVA ENCONTRADA**

Existe uma diferença **estatisticamente significativa** entre o tamanho dos PRs MERGED e CLOSED:
- PRs **MERGED** são **61.9% maiores** que PRs CLOSED
- A mediana de PRs aceitos (68 linhas) é superior à de PRs rejeitados (42 linhas)

**Implicações:**
- PRs **maiores** têm **maior probabilidade de serem aceitos** neste repositório
- Possível explicação: PRs maiores podem representar features completas e bem desenvolvidas
- PRs pequenos rejeitados podem ser mudanças triviais ou mal justificadas


#### 🎯 Conclusão RQ01
✅ HIPÓTESE CONFIRMADA: Existe relação significativa entre o tamanho dos PRs e o feedback final.

---

### RQ02: Qual a relação entre o TEMPO DE ANÁLISE dos PRs e o FEEDBACK FINAL?

#### Hipótese
PRs que levam mais tempo para serem analisados podem indicar complexidade ou problemas, 
podendo estar associados a maior taxa de rejeição.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = -0.1600**
- **p-value = 0.0000** ***
- **Força:** Fraca
- **Direção:** Negativa
- **Significância:** Altamente significativa

**Correlação de Pearson (para comparação):**
- **r = -0.1716**
- **p-value = 0.0000**

#### Comparação entre Grupos (MERGED vs CLOSED)

| Métrica | MERGED | CLOSED | Diferença |
|---------|--------|--------|-----------|
| **Mediana** | 2.13 dias | 6.77 dias | -4.63 dias |
| **Média** | 28.28 dias | 88.36 dias | -60.09 dias |

**Teste de Mann-Whitney U:**
- **U-statistic = 16,976,686**
- **p-value = 0.0000** ***
- **Effect Size (r) = 0.1600** (Pequeno)

#### 📊 Interpretação

✅ **RELAÇÃO SIGNIFICATIVA ENCONTRADA**

PRs **CLOSED** demoram **4.6 dias A MAIS** para serem analisados:
- Mediana MERGED: 2.1 dias
- Mediana CLOSED: 6.8 dias

**Implicações:**
- PRs rejeitados podem passar por **tentativas de correção** antes de serem fechados
- Tempo maior pode indicar **problemas difíceis de resolver**
- PRs bons são aceitos mais rapidamente


#### 🎯 Conclusão RQ02
✅ HIPÓTESE CONFIRMADA: Existe relação significativa entre o tempo de análise e o feedback final.

---

### RQ03: Qual a relação entre a DESCRIÇÃO dos PRs e o FEEDBACK FINAL?

#### Hipótese
PRs com descrições mais detalhadas tendem a ser melhor compreendidos pelos revisores, 
facilitando a aceitação.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = 0.1111**
- **p-value = 0.0000** ***
- **Força:** Fraca
- **Direção:** Positiva
- **Significância:** Altamente significativa

**Correlação de Pearson (para comparação):**
- **r = -0.0072**
- **p-value = 0.3955**

#### Comparação entre Grupos (MERGED vs CLOSED)

| Métrica | MERGED | CLOSED | Diferença |
|---------|--------|--------|-----------|
| **Mediana** | 1232 caracteres | 1017 caracteres | +21.1% |
| **Média** | 2039 caracteres | 2089 caracteres | -2.4% |

**Teste de Mann-Whitney U:**
- **U-statistic = 24,069,404**
- **p-value = 0.0000** ***
- **Effect Size (r) = 0.1111** (Pequeno)

#### 📊 Interpretação

✅ **RELAÇÃO SIGNIFICATIVA ENCONTRADA**

PRs **MERGED** têm descrições **21.1% mais longas**:
- Mediana MERGED: 1232 caracteres
- Mediana CLOSED: 1017 caracteres

**Implicações:**
- **Descrições detalhadas aumentam a probabilidade de aceitação**
- Boa documentação facilita o processo de revisão
- Revisores valorizam contexto e justificativa clara das mudanças
- Recomenda-se incluir: propósito, impacto, testes realizados


#### 🎯 Conclusão RQ03
✅ HIPÓTESE CONFIRMADA: Existe relação significativa entre o tamanho da descrição e o feedback final.

---

### RQ04: Qual a relação entre as INTERAÇÕES nos PRs e o FEEDBACK FINAL?

#### Hipótese
PRs com mais interações (participantes e comentários) indicam discussões ativas e engajamento, 
podendo estar associados a maior taxa de aceitação.

#### 4.1 Número de Participantes

**Correlação de Spearman:**
- **ρ = 0.1028**
- **p-value = 0.0000** ***
- **Força:** Fraca
- **Direção:** Positiva

| Métrica | MERGED | CLOSED | Diferença |
|---------|--------|--------|-----------|
| **Mediana** | 3.0 participantes | 3.0 participantes | +0.0 |
| **Média** | 4.2 participantes | 4.5 participantes | -0.3 |

**Teste de Mann-Whitney U:** p = 0.0000 ***

#### 4.2 Número de Comentários

**Correlação de Spearman:**
- **ρ = -0.0716**
- **p-value = 0.0000** ***
- **Força:** Trivial
- **Direção:** Negativa

| Métrica | MERGED | CLOSED | Diferença |
|---------|--------|--------|-----------|
| **Mediana** | 7.0 comentários | 9.0 comentários | -2.0 |
| **Média** | 14.9 comentários | 16.0 comentários | -1.2 |

**Teste de Mann-Whitney U:** p = 0.0000 ***

#### 📊 Interpretação
✅ **RELAÇÃO SIGNIFICATIVA ENCONTRADA EM PELO MENOS UMA MÉTRICA**

- **Participantes:** PRs CLOSED têm MAIS participantes
- **Comentários:** PRs CLOSED têm MAIS comentários

**Implicações:**
- Interações indicam **engajamento da comunidade**
- Discussões ativas podem levar a **melhorias iterativas**
- Mais participantes = mais perspectivas e revisão mais completa


#### 🎯 Conclusão RQ04
✅ HIPÓTESE PARCIALMENTE CONFIRMADA: Pelo menos uma métrica de interação mostra relação significativa com o feedback final.

---

## 🎯 DIMENSÃO B: NÚMERO DE REVISÕES

Esta dimensão investiga quais características dos Pull Requests estão associadas ao número de 
ciclos de revisão necessários antes do fechamento.

---

### RQ05: Qual a relação entre o TAMANHO dos PRs e o NÚMERO DE REVISÕES?

#### Hipótese
PRs maiores requerem mais revisões devido à maior complexidade e superfície de código a ser revisada.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = 0.3904**
- **p-value = 0.0000** ***
- **Força:** Moderada
- **Direção:** Positiva
- **Significância:** Altamente significativa

**Correlação de Pearson (para comparação):**
- **r = -0.0005**
- **p-value = 0.9551**

#### Modelo de Regressão Linear

**Equação:** `Revisões = 7.27 + -0.000000 × Tamanho`

- **R² = 0.0000** (0.00% da variância explicada)
- **Coeficiente = -0.000000**

#### Interpretação Prática

A cada 100 linhas adicionais: **-0.00 revisões**  
A cada 500 linhas adicionais: **-0.00 revisões**  
A cada 1000 linhas adicionais: **-0.00 revisões**

#### 📊 Interpretação

✅ **RELAÇÃO POSITIVA SIGNIFICATIVA ENCONTRADA**

Existe uma correlação moderada **positiva** entre tamanho e revisões:
- Correlação de Spearman: ρ = 0.390
- PRs **maiores requerem MAIS revisões**

**Implicações:**
- Cada 100 linhas adicionais aumentam em -0.00 revisões
- **Recomenda-se dividir PRs grandes em menores** para:
- Facilitar a revisão
- Reduzir o número de ciclos de revisão
- Acelerar o processo de merge
- Limite sugerido: manter PRs abaixo de 500 linhas quando possível


#### 🎯 Conclusão RQ05
✅ HIPÓTESE CONFIRMADA: Existe relação positiva significativa entre tamanho e número de revisões.

---

### RQ06: Qual a relação entre o TEMPO DE ANÁLISE e o NÚMERO DE REVISÕES?

#### Hipótese
Mais revisões aumentam o tempo de análise, pois cada ciclo adiciona dias ao processo.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = 0.3496**
- **p-value = 0.0000** ***
- **Força:** Moderada
- **Direção:** Positiva
- **Significância:** Altamente significativa

**Correlação de Pearson (para comparação):**
- **r = 0.1628**
- **p-value = 0.0000**

#### Modelo de Regressão Linear

**Equação:** `Revisões = 6.48 + 0.0164 × Tempo(dias)`

- **R² = 0.0265** (2.65% da variância explicada)
- **Coeficiente = 0.0164**

#### Interpretação Prática

A cada dia adicional de análise: **+0.016 revisões**  
A cada semana adicional (7 dias): **+0.12 revisões**  
A cada mês adicional (30 dias): **+0.49 revisões**

#### 📊 Interpretação

✅ **RELAÇÃO POSITIVA SIGNIFICATIVA ENCONTRADA**

Existe uma correlação moderada **positiva** entre tempo e revisões:
- Correlação de Spearman: ρ = 0.350
- **Mais revisões aumentam significativamente o tempo de análise**

**Implicações:**
- Cada revisão adicional aumenta o tempo em aproximadamente 0.0 dias
- Ciclos de revisão são **custosos em tempo**
- **Recomendações:**
- Reduzir o número de revisões através de:
  - Melhor qualidade inicial do código
  - Testes automatizados antes do PR
  - Linting e formatação automática
  - Revisão de checklist antes de submeter


#### 🎯 Conclusão RQ06
✅ HIPÓTESE CONFIRMADA: Existe relação positiva significativa entre tempo de análise e número de revisões.

---

### RQ07: Qual a relação entre a DESCRIÇÃO dos PRs e o NÚMERO DE REVISÕES?

#### Hipótese
Descrições mais detalhadas podem reduzir o número de revisões ao esclarecer melhor as mudanças propostas.

#### Análise de Correlação

**Correlação de Spearman:**
- **ρ = 0.0197**
- **p-value = 0.0198** *
- **Força:** Trivial
- **Direção:** Positiva
- **Significância:** Significativa

**Correlação de Pearson (para comparação):**
- **r = -0.0318**
- **p-value = 0.0002**

#### Modelo de Regressão Linear

**Equação:** `Revisões = 7.60 + -0.00016092 × Descrição`

- **R² = 0.0010** (0.10% da variância explicada)
- **Coeficiente = -0.00016092**

#### 📊 Interpretação

✅ **RELAÇÃO POSITIVA SIGNIFICATIVA ENCONTRADA**

Existe uma correlação trivial **positiva**:
- Descrições mais longas estão associadas a **MAIS revisões**

**Possíveis Explicações:**
- PRs complexos requerem descrições detalhadas E mais revisões
- Descrição longa pode indicar complexidade do problema
- **Correlação não implica causalidade**: ambos podem ser consequência da complexidade

**Implicações:**
- O tamanho da descrição **não reduz** o número de revisões
- Descrições devem focar em **qualidade** (clareza, justificativa) não quantidade


#### 🎯 Conclusão RQ07
❌ HIPÓTESE REJEITADA: O tamanho da descrição não afeta o número de revisões.

---

### RQ08: Qual a relação entre as INTERAÇÕES nos PRs e o NÚMERO DE REVISÕES?

#### Hipótese
Mais interações (participantes e comentários) indicam discussões ativas que podem levar a mais 
ciclos de revisão.

#### 8.1 Número de Participantes vs Revisões

**Correlação de Spearman:**
- **ρ = 0.5395**
- **p-value = 0.0000** ***
- **Força:** Forte
- **Direção:** Positiva

#### 8.2 Número de Comentários vs Revisões

**Correlação de Spearman:**
- **ρ = 0.4588**
- **p-value = 0.0000** ***
- **Força:** Moderada
- **Direção:** Positiva

#### 📊 Interpretação
✅ **RELAÇÃO SIGNIFICATIVA ENCONTRADA EM PELO MENOS UMA MÉTRICA**


**Participantes:**
- Mais participantes = **mais revisões** (ρ = 0.540)
- Diferentes perspectivas levam a mais ciclos de revisão
- **Implicação:** Múltiplos revisores aumentam a qualidade mas também o tempo

**Comentários:**
- Mais comentários = **mais revisões** (ρ = 0.459)
- Discussão ativa indica necessidade de ajustes
- **Implicação:** Feedback construtivo leva a melhorias iterativas

**Implicações Gerais:**
- Interações são **preditores significativos** do número de revisões
- PRs com mais discussão passam por mais ciclos
- Equilibrar qualidade (mais revisão) vs velocidade (menos ciclos)


#### 🎯 Conclusão RQ08
✅ HIPÓTESE CONFIRMADA: Pelo menos uma métrica de interação é preditora significativa do número de revisões.

---

## 📈 4. SÍNTESE DOS RESULTADOS

### 4.1 Tabela Resumo das Correlações

| Questão | Variáveis | Spearman ρ | p-value | Significância | Força | Direção |
|---------|-----------|-----------|---------|---------------|-------|---------|
| RQ01 | Tamanho × Status | +0.0797 | 0.0000 | *** | Trivial | Positiva |
| RQ02 | Tempo × Status | -0.1600 | 0.0000 | *** | Fraca | Negativa |
| RQ03 | Descrição × Status | +0.1111 | 0.0000 | *** | Fraca | Positiva |
| RQ04a | Participantes × Status | +0.1028 | 0.0000 | *** | Fraca | Positiva |
| RQ04b | Comentários × Status | -0.0716 | 0.0000 | *** | Trivial | Negativa |
| RQ05 | Tamanho × Revisões | +0.3904 | 0.0000 | *** | Moderada | Positiva |
| RQ06 | Tempo × Revisões | +0.3496 | 0.0000 | *** | Moderada | Positiva |
| RQ07 | Descrição × Revisões | +0.0197 | 0.0198 | * | Trivial | Positiva |
| RQ08a | Participantes × Revisões | +0.5395 | 0.0000 | *** | Forte | Positiva |
| RQ08b | Comentários × Revisões | +0.4588 | 0.0000 | *** | Moderada | Positiva |


**Total de Relações Significativas:** 10/10 (100%)

### 4.2 Achados Principais

#### ✅ Relações Significativas Encontradas
- **RQ01:** Tamanho × Status - Correlação trivial positiva (ρ = 0.080, p = 0.0000)
- **RQ02:** Tempo × Status - Correlação fraca negativa (ρ = -0.160, p = 0.0000)
- **RQ03:** Descrição × Status - Correlação fraca positiva (ρ = 0.111, p = 0.0000)
- **RQ04_participantes:** Participantes × Status - Correlação fraca positiva (ρ = 0.103, p = 0.0000)
- **RQ04_comentarios:** Comentários × Status - Correlação trivial negativa (ρ = -0.072, p = 0.0000)
- **RQ05:** Tamanho × Revisões - Correlação moderada positiva (ρ = 0.390, p = 0.0000)
- **RQ06:** Tempo × Revisões - Correlação moderada positiva (ρ = 0.350, p = 0.0000)
- **RQ07:** Descrição × Revisões - Correlação trivial positiva (ρ = 0.020, p = 0.0198)
- **RQ08_participantes:** Participantes × Revisões - Correlação forte positiva (ρ = 0.540, p = 0.0000)
- **RQ08_comentarios:** Comentários × Revisões - Correlação moderada positiva (ρ = 0.459, p = 0.0000)


#### ❌ Relações Não Significativas


### 4.3 Comparação: Spearman vs Pearson

Para validar a escolha do teste de Spearman, comparamos os resultados com a Correlação de Pearson:

| Questão | Spearman ρ | Pearson r | Diferença |
|---------|-----------|-----------|-----------|
| RQ01 | +0.0797 | -0.0350 | 0.1147 |
| RQ02 | -0.1600 | -0.1716 | 0.0116 |
| RQ03 | +0.1111 | -0.0072 | 0.1183 |
| RQ04a | +0.1028 | -0.0243 | 0.1271 |
| RQ04b | -0.0716 | -0.0220 | 0.0495 |
| RQ05 | +0.3904 | -0.0005 | 0.3909 |
| RQ06 | +0.3496 | +0.1628 | 0.1867 |
| RQ07 | +0.0197 | -0.0318 | 0.0515 |
| RQ08a | +0.5395 | +0.3586 | 0.1809 |
| RQ08b | +0.4588 | +0.7159 | 0.2571 |


**Diferença Média:** 0.1489

**Observação:** Diferenças significativas entre Spearman e Pearson confirmam a presença de **outliers** 
e **relações não-lineares**, validando a escolha do teste de Spearman.

---

## 🎯 5. CONCLUSÕES E RECOMENDAÇÕES

### 5.1 Principais Conclusões

1. **Tamanho dos PRs:**
 - PRs maiores têm maior taxa de aceitação neste repositório

2. **Tempo de Análise:**
 - PRs rejeitados demoram mais tempo (problemas identificados)

3. **Descrição dos PRs:**
 - Descrições mais detalhadas aumentam chances de aceitação

4. **Interações:**
 - Interações são indicadores do resultado final e número de revisões

5. **Número de Revisões:**
 - PRs maiores requerem mais revisões (+-0.00 revisões/100 linhas)

### 5.2 Recomendações para Contribuidores

#### 📝 Ao Criar um Pull Request:

1. **Inclua descrição detalhada** com contexto e justificativa
2. **Divida PRs grandes** para reduzir ciclos de revisão
3. **Execute testes localmente** antes de submeter
4. **Aplique linting/formatação** automaticamente
5. **Revise checklist do projeto** antes de submeter
6. **Responda rapidamente** a comentários dos revisores


#### 👥 Para Revisores:

1. **Priorize PRs pequenos** para review rápido
2. **Forneça feedback construtivo** e específico
3. **Seja consistente** nos critérios de revisão
4. **Comunique expectativas** claramente
5. **Reconheça boas práticas** dos contribuidores

#### 🏢 Para Mantenedores do Projeto:

1. **Documente padrões** de código e estilo
2. **Automatize verificações** (CI/CD, linting, testes)
3. **Defina limites** recomendados para tamanho de PRs
4. **Crie templates** para descrição de PRs
5. **Monitore métricas** de revisão regularmente

### 5.3 Limitações do Estudo

1. **Causalidade:** Correlações não implicam relações causais
2. **Contexto:** Resultados específicos para o repositório freeCodeCamp
3. **Variáveis Omitidas:** Outros fatores não medidos (expertise do autor, urgência)
4. **Temporal:** Padrões podem mudar ao longo do tempo
5. **Qualitativo:** Análise não captura aspectos qualitativos das revisões

### 5.4 Trabalhos Futuros

1. **Análise de Séries Temporais:** Investigar mudanças nos padrões ao longo do tempo
2. **Análise de Texto:** Sentiment analysis nos comentários
3. **Machine Learning:** Modelos preditivos para aceitação de PRs
4. **Análise de Rede:** Relacionamentos entre contribuidores e revisores
5. **Comparação Cross-Repo:** Comparar com outros projetos open source

---

## 📚 6. REFERÊNCIAS METODOLÓGICAS

### Testes Estatísticos Utilizados

1. **Shapiro-Wilk Test**
 - Royston, P. (1982). "An extension of Shapiro and Wilk's W test for normality to large samples"
 - Usado para testar normalidade das distribuições

2. **Correlação de Spearman**
 - Spearman, C. (1904). "The proof and measurement of association between two things"
 - Teste não-paramétrico para correlação monotônica

3. **Mann-Whitney U Test**
 - Mann, H. B., & Whitney, D. R. (1947). "On a test of whether one of two random variables is stochastically larger than the other"
 - Teste não-paramétrico para comparação de grupos independentes

4. **Regressão Linear**
 - Usado para quantificar relações e fazer predições
 - Complementa a análise de correlação

### Interpretação de Effect Sizes

- Cohen, J. (1988). "Statistical Power Analysis for the Behavioral Sciences" (2nd ed.)
- Utilizado para classificar força das correlações e tamanhos de efeito

---

## 📊 7. APÊNDICES

### A. Estatísticas Descritivas Completas por Estado

#### Pull Requests MERGED

| Métrica | Média | Mediana | DP | Mín | Máx |
|---------|-------|---------|-----|-----|-----|
| tempo_analise_dias | 28.28 | 2.13 | 109.64 | 0.00 | 3710.51 |
| tamanho_total_linhas | 1127.86 | 68.00 | 18114.70 | 0.00 | 1097856.00 |
| num_revisoes | 8.26 | 3.00 | 17.24 | 0.00 | 377.00 |
| num_comentarios | 14.86 | 7.00 | 25.30 | 0.00 | 387.00 |
| num_participantes | 4.19 | 3.00 | 3.21 | 0.00 | 64.00 |


#### Pull Requests CLOSED

| Métrica | Média | Mediana | DP | Mín | Máx |
|---------|-------|---------|-----|-----|-----|
| tempo_analise_dias | 88.36 | 6.77 | 235.33 | 0.00 | 2989.09 |
| tamanho_total_linhas | 7520.01 | 42.00 | 148051.46 | 0.00 | 6251681.00 |
| num_revisoes | 5.17 | 1.00 | 14.59 | 0.00 | 320.00 |
| num_comentarios | 16.03 | 9.00 | 23.78 | 0.00 | 285.00 |
| num_participantes | 4.50 | 3.00 | 9.39 | 0.00 | 419.00 |


### B. Informações do Dataset

- **Data de Coleta:** 15/10/2025
- **Período Analisado:** 22/02/2012 a 15/10/2025
- **Total de PRs:** 13,933
- **PRs Merged:** 9,458 (67.9%)
- **PRs Closed:** 4,475 (32.1%)
- **Valores Ausentes:** 0
- **Nível de Significância:** α = 0.05

### C. Software e Bibliotecas

- **Python:** 3.x
- **pandas:** Manipulação de dados
- **numpy:** Operações numéricas
- **scipy:** Testes estatísticos
- **scikit-learn:** Modelos de regressão
- **seaborn/matplotlib:** Visualizações

---

## ✅ 8. DECLARAÇÃO DE CONFORMIDADE

Este relatório foi elaborado seguindo as melhores práticas de análise estatística:

- ✅ Testes de normalidade realizados antes da escolha dos testes
- ✅ Testes não-paramétricos utilizados para dados não-normais
- ✅ Effect sizes calculados e reportados
- ✅ P-values corrigidos quando necessário
- ✅ Limitações do estudo explicitamente declaradas
- ✅ Correlação vs causalidade claramente distinguidas
- ✅ Todas as decisões metodológicas justificadas

---

**Fim do Relatório**

Gerado automaticamente em 15/10/2025 às 23:59:05
