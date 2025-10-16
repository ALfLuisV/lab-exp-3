# 📊 Guia de Interpretação dos Gráficos

## Como Ler e Interpretar as Visualizações Geradas

---

## 1. analise_completa.png - Painel Principal (12 Gráficos)

### Gráfico 1: Distribuição dos Estados dos PRs (Canto Superior Esquerdo)
**Tipo**: Gráfico de Barras
**O que mostra**: Quantidade absoluta e percentual de PRs MERGED vs CLOSED
**Como interpretar**:
- Verde = MERGED (aprovados)
- Vermelho = CLOSED (rejeitados)
- Altura da barra = quantidade de PRs
- Números no topo = contagem e percentual

**Insight**: 67.88% dos PRs são aprovados, mostrando uma taxa de sucesso razoável.

---

### Gráfico 2: RQ01 - Tamanho vs Estado (Boxplot)
**Tipo**: Boxplot (Diagrama de Caixa)
**O que mostra**: Distribuição do tamanho total (linhas) por estado

**Como interpretar um Boxplot**:
```
    │  ───  ← Valor máximo (excluindo outliers)
    │   │
    ├───┤   ← Q3 (75% dos dados estão abaixo)
    │ ─ │   ← Mediana (50% dos dados)
    ├───┤   ← Q1 (25% dos dados estão abaixo)
    │   │
    │  ───  ← Valor mínimo
    ●       ← Outliers (pontos isolados)
```

**Insights**:
- Caixa mais alta = maior variabilidade
- Linha central = valor típico (mediana)
- Pontos acima = PRs excepcionalmente grandes
- Compare as medianas entre MERGED e CLOSED

---

### Gráfico 3: RQ01 - Categoria de Tamanho (Barras Empilhadas)
**Tipo**: Gráfico de Barras Agrupadas
**O que mostra**: Contagem de MERGED vs CLOSED por categoria de tamanho

**Como interpretar**:
- Eixo X: Pequeno → Médio → Grande → Muito Grande
- Verde = Aprovados, Vermelho = Rejeitados
- Compare a proporção de cores em cada categoria

**Insight Chave**: Se vermelho aumenta à direita, PRs maiores são mais rejeitados.

---

### Gráfico 4: RQ02 - Tempo vs Estado (Violinplot)
**Tipo**: Violinplot (Gráfico de Violino)
**O que mostra**: Distribuição do tempo de análise por estado

**Como interpretar um Violinplot**:
```
    ╱─╲     ← Largura indica frequência
   │   │    ← Muitos PRs nesta faixa de tempo
   │ • │    ← Ponto central = mediana
   │   │
    ╲─╱     ← Poucos PRs nesta faixa
```

**Insights**:
- Parte mais larga = onde se concentram mais PRs
- Altura total = range de valores
- Compare a "barriga" entre MERGED e CLOSED

---

### Gráfico 5: RQ03 - Descrição vs Estado (Boxplot)
**Tipo**: Boxplot
**O que mostra**: Tamanho da descrição (em caracteres) por estado

**Como interpretar**:
- Similar ao Gráfico 2
- Mediana mais alta = descrições tipicamente maiores
- Muitos outliers = alguns PRs com descrições muito longas

**Insight**: Se mediana de MERGED > CLOSED, descrições ajudam na aprovação.

---

### Gráfico 6: RQ04 - Interações Médias (Barras Agrupadas)
**Tipo**: Gráfico de Barras Agrupadas
**O que mostra**: Média de participantes e comentários por estado

**Como interpretar**:
- Azul = Participantes, Roxo = Comentários
- Números no topo = valor exato da média
- Compare alturas entre MERGED e CLOSED

**Insight**: Se CLOSED tem mais comentários, discussão pode indicar problemas.

---

### Gráfico 7: RQ05 - Tamanho vs Revisões (Scatter com Tendência)
**Tipo**: Gráfico de Dispersão com Linha de Tendência
**O que mostra**: Relação entre tamanho do PR e número de revisões

**Como interpretar**:
- Cada ponto = um PR
- Verde = MERGED, Vermelho = CLOSED
- Linha vermelha tracejada = tendência geral
  - Linha subindo = quanto maior, mais revisões
  - Linha horizontal = sem relação
  - Linha descendo = quanto maior, menos revisões

**Insights**:
- Nuvem de pontos dispersa = relação fraca
- Pontos alinhados com a linha = relação forte
- Cores misturadas = tamanho não prediz estado

---

### Gráfico 8: RQ05 - Revisões por Categoria (Barras)
**Tipo**: Gráfico de Barras
**O que mostra**: Média de revisões por categoria de tamanho

**Como interpretar**:
- Barras crescentes = PRs maiores precisam mais revisões
- Números no topo = valor exato
- Compare proporção entre categorias

**Insight**: Se dobra a cada categoria, relação exponencial.

---

### Gráfico 9: RQ06 - Tempo vs Revisões (Scatter)
**Tipo**: Gráfico de Dispersão com Tendência
**Similar ao Gráfico 7**

**Como interpretar**:
- Linha subindo = mais revisões = mais tempo
- Pontos verdes acima da linha = PRs aprovados que levaram muito tempo
- Pontos vermelhos = PRs rejeitados

---

### Gráfico 10: RQ07 - Descrição vs Revisões (Scatter)
**Tipo**: Gráfico de Dispersão
**Similar aos Gráficos 7 e 9**

**Como interpretar**:
- Nuvem sem padrão claro = correlação fraca
- Se pontos aleatórios, descrição não prediz revisões

---

### Gráfico 11: RQ08a - Participantes vs Revisões (Scatter)
**Tipo**: Gráfico de Dispersão com Tendência

**Como interpretar**:
- Linha forte e inclinada = correlação forte
- Pontos alinhados = relação clara
- Clusters de pontos = valores comuns

**Insight**: Se muito inclinada, cada revisão traz novos participantes.

---

### Gráfico 12: RQ08b - Comentários vs Revisões (Scatter)
**Tipo**: Gráfico de Dispersão com Tendência
**Similar ao Gráfico 11**

**Como interpretar**:
- Mais inclinada que Gráfico 11 = comentários predizem melhor
- Pontos espalhados = variabilidade alta

---

## 2. correlacao_spearman.png - Mapa de Calor

### Tipo: Heatmap (Mapa de Calor)
**O que mostra**: Matriz de correlação entre todas as variáveis

### Como Interpretar Cores:
```
🔴 Vermelho Forte   (+1.0)  = Correlação positiva perfeita
🟠 Vermelho Claro   (+0.5)  = Correlação positiva moderada/forte
⚪ Branco           (0.0)   = Sem correlação
🔵 Azul Claro      (-0.5)   = Correlação negativa moderada/forte
🔵 Azul Forte      (-1.0)   = Correlação negativa perfeita
```

### Como Ler:
1. **Diagonal Principal** (sempre +1.00): Variável correlacionada com ela mesma
2. **Simétrico**: Canto superior direito = espelho do inferior esquerdo
3. **Número na célula**: Valor exato da correlação de Spearman (ρ)

### Interpretação Prática:
- **Procure por:**
  - Células vermelhas fora da diagonal = variáveis relacionadas positivamente
  - Células azuis = variáveis inversamente relacionadas
  - Células brancas = variáveis independentes

- **Exemplo**:
  - Se célula "Revisões × Participantes" for vermelha forte (+0.54):
    → Mais revisões sempre acompanham mais participantes

### Insights Rápidos:
- Coluna "Estado": Quais variáveis predizem aprovação?
- Coluna "Revisões": O que causa mais ciclos de revisão?
- Clusters vermelhos: Variáveis que se movem juntas

---

## 3. analise_regressao.png - Regressão Linear

### Estrutura: 6 painéis (2 linhas × 3 colunas)

### Painéis 1-5: Feature vs Revisões
**Tipo**: Gráfico de Dispersão Duplo

**Como interpretar**:
- **Pontos azuis**: Valores reais (o que realmente aconteceu)
- **Pontos vermelhos**: Valores preditos pelo modelo
- **Sobreposição perfeita**: Modelo prediz perfeitamente
- **Pontos dispersos**: Modelo tem erro

**Avaliação da Qualidade**:
- Pontos azuis e vermelhos muito misturados = predição boa
- Pontos em regiões diferentes = predição ruim
- Tendência clara = variável importante no modelo

### Painel 6: Análise de Resíduos
**Tipo**: Gráfico de Dispersão com Linha Zero

**O que são resíduos?**
```
Resíduo = Valor Real - Valor Predito
```

**Como interpretar**:
- **Linha vermelha tracejada** (y=0): Predição perfeita
- **Pontos acima da linha**: Modelo subestimou (predisse menos revisões)
- **Pontos abaixo da linha**: Modelo superestimou (predisse mais revisões)

**Padrões para observar**:
- ✅ **Bom**: Pontos aleatoriamente espalhados ao redor de zero
  → Modelo não tem viés sistemático
  
- ❌ **Ruim**: Padrão em forma de cone
  → Modelo piora para valores altos
  
- ❌ **Ruim**: Padrão em curva
  → Relação não-linear não capturada

---

## 🎨 Dicas de Cores nos Gráficos

### Padrão Consistente:
- 🟢 **Verde**: PRs MERGED (aprovados)
- 🔴 **Vermelho**: PRs CLOSED (rejeitados)
- 🔵 **Azul**: Participantes / Variável primária
- 🟣 **Roxo**: Comentários / Variável secundária

---

## 📏 Escalas dos Eixos

### Importante Saber:
Alguns gráficos removem os **top 5% outliers** para melhor visualização.

**Exemplo**: Se um PR tem 50.000 linhas, mas o gráfico só vai até 2.000:
- O ponto não aparece no gráfico
- Mas foi incluído nos cálculos de correlação
- Motivo: Melhor visualização da maioria dos dados

---

## 🔍 Checklist de Análise Visual

Ao olhar cada gráfico, pergunte:

### Para Gráficos de Distribuição (Boxplot, Violinplot):
- [ ] Onde está a mediana? (linha central)
- [ ] Qual a amplitude? (altura total)
- [ ] Há muitos outliers? (pontos isolados)
- [ ] As distribuições se sobrepõem ou são distintas?

### Para Gráficos de Dispersão (Scatter):
- [ ] Há um padrão claro? (linha, curva, clusters)
- [ ] Os pontos estão alinhados ou dispersos?
- [ ] A linha de tendência sobe, desce ou é horizontal?
- [ ] As cores (MERGED/CLOSED) estão misturadas ou separadas?

### Para Gráficos de Barras:
- [ ] Qual categoria tem maior valor?
- [ ] A diferença é grande ou pequena?
- [ ] Há um padrão crescente/decrescente?

### Para Mapa de Calor:
- [ ] Quais células são mais vermelhas? (correlação forte positiva)
- [ ] Quais células são mais azuis? (correlação forte negativa)
- [ ] Há clusters de cores semelhantes? (variáveis relacionadas)

---

## 💡 Interpretações Comuns - Glossário Visual

### "Tendência Positiva" (Linha /):
- Quando X aumenta, Y aumenta
- Exemplo: Mais revisões → Mais tempo

### "Tendência Negativa" (Linha \):
- Quando X aumenta, Y diminui
- Exemplo: Mais tempo → Menos aprovação

### "Sem Correlação" (Nuvem de Pontos):
- Pontos totalmente aleatórios
- Não há relação clara

### "Outliers" (Pontos Isolados):
- Valores extremos e raros
- Podem ser erro ou casos especiais

### "Distribuição Bimodal" (Duas Barrigas no Violinplot):
- Dois grupos distintos nos dados
- Exemplo: PRs triviais vs PRs complexos

---

## 📊 Exemplo Prático de Análise

### Cenário: Analisando o Gráfico 11 (Participantes vs Revisões)

1. **Observação**: Linha de tendência subindo fortemente
2. **Dados**: ρ = 0.5395 no título
3. **Interpretação**: Correlação forte positiva
4. **Conclusão**: Mais revisões sempre envolvem mais pessoas
5. **Implicação**: Processo colaborativo - aceitar que PRs complexos terão alta participação

---

## 🎓 Conclusão

### Para usar os gráficos efetivamente:

1. **Não olhe apenas o gráfico** - Leia o título com a correlação
2. **Compare gráficos entre si** - Padrões consistentes são mais confiáveis
3. **Correlação ≠ Causalidade** - Gráficos mostram associação, não causa
4. **Contexto importa** - Considere a natureza dos dados (PRs de software)
5. **Use múltiplas visualizações** - Um tipo de gráfico pode ocultar padrões que outro revela

### Pergunta-chave para cada gráfico:
**"O que este gráfico me ensina sobre como melhorar o processo de revisão de PRs?"**

---

**Dica Final**: Imprima este guia e tenha ao lado ao analisar os gráficos! 📖✨
