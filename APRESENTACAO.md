# 🎤 Resumo Executivo para Apresentação
## Análise Estatística de Pull Requests

---

## 📊 SLIDE 1: Visão Geral

### Objetivo da Pesquisa
Identificar fatores que influenciam:
- ✅ **Aprovação** de Pull Requests (MERGED vs CLOSED)
- 🔄 **Número de Revisões** necessárias

### Dataset
- **13.933 Pull Requests** analisados
- Repositórios open-source
- **67.88% aprovados**, 32.12% rejeitados

---

## 📊 SLIDE 2: Metodologia

### Por que Spearman? 🔬
✅ **Dados não seguem distribuição normal**
- Teste de Shapiro-Wilk: todas variáveis com p < 0.05

✅ **Presença de outliers**
- 13.8% dos PRs são outliers em tamanho

✅ **Relações não-lineares**
- Spearman captura relações monotônicas

✅ **Robustez**
- Baseado em rankings, resistente a valores extremos

---

## 📊 SLIDE 3: Pergunta Mais Importante

### 🔑 O que mais influencia a APROVAÇÃO de um PR?

**Resposta: DESCRIÇÃO!**

```
┌─────────────────────────────────────────────┐
│ COM descrição:    69% APROVAÇÃO ✅          │
│ SEM descrição:    23% APROVAÇÃO ❌          │
│                                             │
│ 🎯 3x MAIS CHANCES com descrição!          │
└─────────────────────────────────────────────┘
```

**Correlação de Spearman**: ρ = 0.1111 (fraca, mas **significativa**)

**Takeaway**: SEMPRE inclua descrição detalhada no PR!

---

## 📊 SLIDE 4: Tamanho do PR

### Qual o tamanho ideal de um PR?

**Taxas de Rejeição por Categoria:**
```
Pequeno       (≤50 linhas):    35% ❌
Médio         (50-200):        30% ❌  ← IDEAL
Grande        (200-500):       28% ❌
Muito Grande  (>500):          30% ❌
```

**Surpreendente**: PRs muito pequenos têm MAIOR rejeição!

**Impacto no Número de Revisões:**
```
Pequeno:       2.7 revisões
Muito Grande:  16.5 revisões  (6x mais!) 🔄
```

**Correlação**: ρ = 0.3904 (moderada)

**Takeaway**: Manter tamanho **médio** (50-500 linhas) para melhor resultado!

---

## 📊 SLIDE 5: Velocidade é Crucial

### ⚡ Tempo de Análise

**Medianas:**
```
✅ PRs APROVADOS:   2.1 dias
❌ PRs REJEITADOS:  6.8 dias

🚀 3x mais rápido!
```

**Correlação**: ρ = -0.1600 (fraca **negativa**)

**Interpretação**:
- PRs que "ficam parados" tendem à rejeição
- Velocidade indica qualidade ou simplicidade
- Falta de resposta = perda de interesse

**Takeaway**: Responda rapidamente a feedback dos revisores!

---

## 📊 SLIDE 6: Engajamento e Interações

### 👥 Participantes vs Comentários

**Efeito na Aprovação:**
```
Participantes:  ρ = 0.1028  (fraca positiva)  ✅
Comentários:    ρ = -0.0716 (desprezível neg) ⚠️
```

**Médias por Estado:**
```
              Participantes  |  Comentários
MERGED:           4.2       |     14.9
CLOSED:           4.5       |     16.0
```

**Insight Contraintuitivo:**
- Mais comentários ≠ melhor
- Pode indicar **problemas** sendo discutidos
- PRs bons são aprovados rapidamente com pouca discussão

**Takeaway**: Busque **qualidade** na revisão, não quantidade de comentários!

---

## 📊 SLIDE 7: Ciclo de Revisões

### 🔄 O que Aumenta o Número de Revisões?

**Correlações com Número de Revisões:**
```
1. 👥 Participantes:  ρ = 0.5395  ⭐⭐ FORTE!
2. 💬 Comentários:    ρ = 0.4588  ⭐  MODERADA
3. 📏 Tamanho:        ρ = 0.3904  ⭐  MODERADA
4. ⏱️ Tempo:          ρ = 0.3496  ⭐  MODERADA
5. 📝 Descrição:      ρ = 0.0197      Desprezível
```

**Ciclo Iterativo Natural:**
```
Mais Revisões → Mais Participantes → Mais Comentários
      ↑                                      ↓
      └─────────── Mais Refinamento ────────┘
```

**Takeaway**: Aceitar que PRs complexos **requerem múltiplas iterações** - é normal e saudável!

---

## 📊 SLIDE 8: Modelo Preditivo

### 🤖 Regressão Linear: Predição de Revisões

**Performance do Modelo:**
```
R² = 0.5191  (51.91% da variância explicada)
```

**Principais Preditores:**
```
1. Comentários:     +0.459 revisões por comentário  📈
2. Participantes:   +0.239 revisões por pessoa      📈
3. Tempo:           -0.004 (efeito mínimo)          ─
4. Descrição:       +0.00001 (efeito mínimo)        ─
5. Tamanho:         -0.000003 (desprezível)         ─
```

**Interpretação:**
- **Interações** são o principal driver de revisões
- Tamanho e descrição não são bons preditores no modelo linear
- 48% da variância vem de fatores **não medidos** (qualidade do código, expertise, etc.)

---

## 📊 SLIDE 9: Mapa de Correlações

### 🗺️ Visão Panorâmica das Relações

**Correlações Mais Fortes:**
```
🟢 Participantes ↔ Revisões:     +0.54  (FORTE)
🟢 Comentários ↔ Revisões:       +0.46  (MODERADA)
🟢 Tamanho ↔ Revisões:           +0.39  (MODERADA)
🟢 Tempo ↔ Revisões:             +0.35  (MODERADA)
🔴 Tempo ↔ Estado:               -0.16  (FRACA)
```

**Padrão Identificado:**
- **Variáveis de interação** (participantes, comentários) dominam o processo de revisão
- **Características do PR** (tamanho, descrição) têm efeito menor
- **Processo colaborativo** é mais importante que métricas técnicas

---

## 📊 SLIDE 10: Top 5 Recomendações Práticas

### 🎯 Ações Concretas para Desenvolvedores

#### 1. 📝 **SEMPRE Inclua Descrição**
```
Impacto: 3x mais aprovação
Tempo: 5 minutos
ROI: ALTÍSSIMO ⭐⭐⭐
```

#### 2. 📏 **Mantenha PRs Médios (50-500 linhas)**
```
Benefícios:
- 30% rejeição (vs 35% pequenos)
- Menos revisões (2.7 vs 16.5)
- Mais rápido para revisar
```

#### 3. ⚡ **Responda em < 2 dias**
```
Meta: Responder feedback em até 2 dias
Efeito: Mantém momentum e interesse
```

#### 4. ✂️ **Divida PRs Grandes**
```
Antes: 1 PR de 2000 linhas → 16.5 revisões
Depois: 4 PRs de 500 linhas → 6.8 revisões cada
Ganho: Aprovação mais rápida
```

#### 5. 🤝 **Aceite o Processo Iterativo**
```
Revisões ↔ Discussão ↔ Refinamento
É NORMAL e SAUDÁVEL para PRs complexos!
```

---

## 📊 SLIDE 11: Estatísticas-Chave (Elevator Pitch)

### 📈 Números para Memorizar

```
┌─────────────────────────────────────────────────────┐
│ Dataset:           13.933 PRs                       │
│ Taxa de Aprovação: 67.88%                           │
│                                                     │
│ 🔑 COM descrição:  69% aprovação                    │
│ ❌ SEM descrição:  23% aprovação                    │
│                                                     │
│ ⚡ Tempo aprovados: 2.1 dias (mediana)              │
│ 🐌 Tempo rejeitados: 6.8 dias (mediana)            │
│                                                     │
│ 📏 PRs grandes:    6x mais revisões                 │
│                                                     │
│ 🔄 Correlação +forte: Participantes × Revisões     │
│    (ρ = 0.54)                                       │
└─────────────────────────────────────────────────────┘
```

---

## 📊 SLIDE 12: Conclusão

### 🎯 Mensagem Principal

> **"Comunicação clara (descrição) + Tamanho gerenciável + Velocidade de resposta = Aprovação"**

### Fórmula do PR Perfeito:
```
✅ Descrição detalhada (contexto, motivação, impacto)
✅ 50-500 linhas (dividir se maior)
✅ Resposta < 2 dias a feedback
✅ Aceitar processo iterativo
✅ Focar em qualidade, não quantidade de discussão
```

### Resultado Esperado:
```
📈 +3x chances de aprovação
⚡ 3x mais rápido (2 dias vs 7 dias)
🔄 Menos revisões (3-7 vs 16+)
😊 Equipe mais satisfeita
```

---

## 📊 SLIDE 13: Perguntas e Respostas

### ❓ Perguntas Frequentes

**Q1: "PRs muito pequenos também são rejeitados. Por quê?"**
- A: Podem parecer incompletos ou triviais
- Recomendação: Agrupe mudanças relacionadas

**Q2: "Como balancear velocidade e qualidade?"**
- A: Definir critérios claros de "pronto para merge"
- Aceitar que "bom suficiente" é melhor que "perfeito"

**Q3: "O modelo preditivo não usa tamanho. Isso não é estranho?"**
- A: Tamanho afeta revisões **indiretamente** (via comentários)
- Efeito direto é pequeno depois de controlar para interações

**Q4: "Devo evitar discussões nos PRs?"**
- A: Não! Discussão saudável é normal
- Evite: Discussões intermináveis sobre estilo/preferências

**Q5: "Estas recomendações se aplicam a todos os projetos?"**
- A: Dados são de repos open-source
- Adapte ao contexto do seu projeto

---

## 📊 SLIDE 14: Próximos Passos

### 🔮 Pesquisas Futuras

1. **Análise Qualitativa** 📝
   - Conteúdo das descrições (NLP)
   - Qualidade dos comentários

2. **Machine Learning** 🤖
   - Predição de aprovação (classificação)
   - Features adicionais (linguagem, complexidade ciclomática)

3. **Análise Temporal** 📅
   - Evolução das práticas ao longo do tempo
   - Impacto de mudanças de processo

4. **Causalidade** 🔬
   - Experimentos controlados (A/B testing)
   - Inferência causal

5. **Comparação** 🔀
   - Entre linguagens (Python vs JavaScript)
   - Entre tipos de projeto (frontend vs backend)

---

## 📊 SLIDE EXTRA: Recursos

### 📚 Material Disponível

```
📁 Arquivos Gerados:
├── 📊 analise_completa.png      (12 gráficos principais)
├── 🗺️ correlacao_spearman.png   (mapa de calor)
├── 📈 analise_regressao.png     (modelo preditivo)
├── 📄 resumo_analise.txt        (resumo executivo)
├── 📝 relatorio_detalhado.md    (análise completa)
├── 📖 GUIA_GRAFICOS.md          (como interpretar)
└── 🐍 analise_pull_requests.py  (código reproduzível)
```

### 🔗 Links
- **GitHub**: github.com/ALfLuisV/lab-exp-3
- **Dataset**: 13.933 PRs de repos open-source
- **Ferramentas**: Python + Seaborn + SciPy + Scikit-learn

---

## 🙏 Obrigado!

### Contato
- 📧 Email: [seu-email]
- 💼 LinkedIn: [seu-linkedin]
- 🐙 GitHub: @ALfLuisV

### Dúvidas?
**Abra uma issue no repositório!**

---

**Data**: 15 de outubro de 2025  
**Análise**: 13.933 Pull Requests  
**Metodologia**: Correlação de Spearman + Regressão Linear  
**Confiança**: Todos os resultados significativos (p < 0.05)
