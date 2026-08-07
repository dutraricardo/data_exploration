# Resumo do Reconhecimento — Base SIAPE

**Base analisada**: `data/raw/DB_SIAPE_processado_20260729_v2.xlsx`
**Tamanho**: 9.991 servidores, 62 colunas
**Notebooks de origem**: `notebooks/00_reconhecimento.ipynb` a `notebooks/05_raca_deficiencia.ipynb`

Este documento consolida os achados de todas as análises feitas até agora, para
servir de contexto rápido em conversas futuras. Todos os números aqui são
agregados (contagens e percentuais) — nenhum servidor é identificado
individualmente em nenhum ponto deste resumo.

---

## 1. Perfil demográfico

*(fonte: `01_perfil_demografico.ipynb`)*

- **Idade**: média de 45 anos, concentração maior entre 40 e 50 anos.
- **Sexo**: 53% masculino, 47% feminino — quadro equilibrado.
- **Escolaridade**: 84,7% têm ensino superior; mestrado (11,7%) e doutorado
  (3,6%) somam praticamente todo o restante. Um grupo residual de 2 servidores
  com ensino fundamental/médio foi agrupado por privacidade (ver seção 8).
- **UF de exercício**: 96,4% dos servidores estão lotados no DF — esperado por
  ser um órgão federal sediado em Brasília. Os 3,6% restantes se espalham por
  vários estados, sem nenhum concentrar mais que 1,2% (RJ é o segundo maior).

## 2. Cargos e estrutura organizacional

*(fonte: `02_cargos_secretarias.ipynb`)*

- **Cargo**: quadro muito concentrado — 54% dos servidores são "Analista Técnico
  Executivo". Os 6 cargos mais comuns somam quase 99% da base; os outros 9
  cargos têm pouquíssimos ocupantes cada.
- **Secretaria**: 78,7% dos servidores estão na "MGI/SE" (Secretaria-Executiva
  do Ministério da Gestão), muito à frente das demais.
- **Órgão de exercício**: mais disperso que secretaria — o maior órgão
  individual concentra só 18,6% (Min. Gestão e Inovação em Serviços Públicos);
  133 outros órgãos somam 38,2% da base, mostrando que esses servidores estão
  espalhados por vários ministérios diferentes.
- **Hierarquia do cargo**: 86,7% não têm cargo de comissão (DAS) registrado;
  os 13,3% restantes se distribuem entre DAS-1 e DAS-6 e Natureza Especial.

## 3. Situações especiais e movimentações

*(fonte: `03_situacoes_especiais.ipynb`)*

- **76,7%** dos servidores estão em situação normal de exercício (sem nenhuma
  movimentação especial registrada). Os **23,3%** restantes têm algum tipo de
  movimentação — a mais comum é "exercício descentralizado no DF" (10,6% da
  base).
- **29 servidores** estão afastados para estudo (a maioria para doutorado).
- **105 servidores** estão licenciados (maioria por licença para tratar de
  interesses particulares).
- **17 servidores** estão cedidos a estados/municípios — população pequena
  demais para detalhar destino sem risco de identificação individual.
- **354 servidores** exercem funções fora do DF, com destaque para o Rio de
  Janeiro (74 pessoas, o maior grupo estadual).

## 4. Carreira e capacitação (DB_SGC)

*(fonte: `04_carreira_capacitacao.ipynb`)*

- Apenas **23,3%** da base está vinculada ao sistema de acompanhamento de
  carreira "DB_SGC" — o cargo mais comum do quadro (Analista Técnico
  Executivo) **não** faz parte desse sistema, então a maioria dos servidores
  aparece como "não informado" (NI) aqui.
- Entre os rastreados: carreira mais comum é **EPPGG**; regime de trabalho
  predominante é **40 horas semanais**; a maioria tem vínculo por **prazo
  indeterminado**; classe funcional mais comum é **Classe B** e padrão salarial
  mais comum é **Padrão IV**.

## 5. Raça e deficiência

*(fonte: `05_raca_deficiencia.ipynb`)*

- Também apenas **23,4%** da base tem raça/cor e deficiência autodeclaradas
  registradas (aparentemente o mesmo subconjunto de servidores do item 4).
- Entre os que informaram: **16,8%** da base total se declara branca, **5,1%**
  parda, e os demais grupos (preta, amarela, indígena) somam menos de 1,5% da
  base total.
- Entre os que informaram deficiência, a grande maioria (22,9% da base total)
  declarou **não ter deficiência**. Os tipos específicos de deficiência somam
  menos de 0,5% da base total e foram agrupados por privacidade (ver seção 8).

## 6. Qualidade dos dados — pontos de atenção

Achados que podem indicar erro de preenchimento na base original (não
investigados a fundo, pois isso exigiria olhar registros individuais):

- **Data futura inconsistente**: a coluna "Data de início_DB_SGC" tem um valor
  máximo em **2103** — quase certamente um erro de digitação (dígito a mais no
  ano).
- **Escolaridade muito baixa**: 2 servidores aparecem com "Ensino
  Fundamental"/"Ensino Médio" num quadro onde 84,7% tem nível superior. Pode
  ser dado real (cargo mais antigo, sem exigência de diploma) ou erro de
  preenchimento.
- **Colunas possivelmente redundantes**: "Tipo de movimentação_DB_SGC" e "Tipo
  de movimentação_Situação atual por tipo de movimentação" têm categorias e
  contagens quase idênticas — parecem ser a mesma informação duplicada em dois
  sistemas de origem diferentes.
- **Coluna vazia**: "Unnamed: 16" está 100% vazia (resíduo da planilha
  original, sem uso).
- **Coluna constante**: "Total" tem sempre o valor 1 em todas as linhas (sem
  informação útil).

## 7. Regras de privacidade aplicadas

Todas as análises seguiram estas regras, implementadas em `src/viz_style.py`:

- Nenhuma linha/registro individual é exibida — apenas contagens e agregados.
- Colunas identificadoras diretas (Nome, CPF, Matrícula SIAPE, E-mail, Data de
  Nascimento) nunca têm valores exibidos, nem em amostras estruturais.
- Categorias "cauda longa" em colunas de muitas categorias (UF, secretaria,
  órgão, turma) são agrupadas em "Outros" nos gráficos, sempre destacadas em
  cinza e fixadas à parte — para não serem confundidas com uma categoria real.
- **Supressão de células pequenas**: qualquer categoria com **menos de 5
  servidores** é agrupada em "Outras (poucos casos)" antes de ser exibida, em
  gráfico ou tabela — mostrar uma contagem exata de 1 ou 2 pessoas poderia, na
  prática, identificar alguém.

## 8. Estrutura de arquivos

```
data/raw/DB_SIAPE_processado_20260729_v2.xlsx   # dado bruto, fora do git
src/viz_style.py                             # paleta e helpers de gráfico/privacidade compartilhados
notebooks/00_reconhecimento.ipynb            # estrutura da base (colunas, tipos, nulos, datas)
notebooks/01_perfil_demografico.ipynb        # idade, sexo, escolaridade, UF
notebooks/02_cargos_secretarias.ipynb        # cargo, secretaria, órgão, hierarquia
notebooks/03_situacoes_especiais.ipynb       # afastamentos, licenças, cessões, exercício fora do DF
notebooks/04_carreira_capacitacao.ipynb      # DB_SGC: carreira, turma, jornada, classe, padrão
notebooks/05_raca_deficiencia.ipynb          # raça/cor e deficiência autodeclaradas
```

## 9. Possíveis próximos passos

- Investigar (com cautela, sem expor indivíduos) as inconsistências listadas na
  seção 6, junto à área responsável pelos dados de origem.
- Cruzar dimensões (ex: idade x cargo, escolaridade x hierarquia) se houver uma
  pergunta de negócio específica que justifique isso.
- Definir se os relatórios devem ser atualizados periodicamente conforme a base
  SIAPE for reprocessada.
