# Status de Atualização — Projeto data_exploration (SIAPE)

**Data**: 2026-08-07
**Objetivo deste documento**: dar contexto completo a quem for continuar o
trabalho em outra sessão do Claude Code, sem acesso ao histórico da conversa
em que essas mudanças foram feitas. Assume que quem lê não acompanhou nada do
que está descrito abaixo.

**Contexto do projeto** (para quem não sabe): este é um piloto institucional,
não um projeto pessoal — há um relatório técnico formal sendo reportado a uma
chefia. Decisões de arquitetura e incidentes técnicos relevantes devem ser
documentados com clareza, porque podem virar conteúdo desse relatório.

---

## 1. Estado atual de cada etapa do pipeline

| Etapa | Status | Observação |
|---|---|---|
| Ingestão da base de dados | **Concluída** | Cópia em `data/raw/`, ver incidente de renomeação na seção 3. |
| Exploração/reconhecimento inicial | **Concluída** | `notebooks/00_reconhecimento.ipynb`. |
| Análise: perfil demográfico | **Concluída** | `notebooks/01_perfil_demografico.ipynb`. |
| Análise: cargos/secretarias | **Concluída** | `notebooks/02_cargos_secretarias.ipynb`. |
| Análise: situações especiais | **Concluída** | `notebooks/03_situacoes_especiais.ipynb`. |
| Análise: carreira/capacitação | **Concluída** | `notebooks/04_carreira_capacitacao.ipynb`. |
| Análise: raça/deficiência | **Concluída** | `notebooks/05_raca_deficiencia.ipynb`. |
| Relatório consolidado | **Concluída** | `reports/resumo_reconhecimento.md`, com todos os achados agregados das 6 análises acima. |
| Revisão final do usuário | **Concluída** | O usuário revisou e aprovou os 6 notebooks (00–05), os últimos três em bloco. |

Todos os 6 notebooks executam do início ao fim sem erro (validado via
`jupyter nbconvert --execute` mais de uma vez, inclusive na versão final após
os incidentes descritos na seção 3).

## 2. Notebooks concluídos

- **`00_reconhecimento.ipynb`** — Reconhecimento estrutural da base (sem
  analisar conteúdo): número de linhas/colunas, tipos de dado, contagem de
  nulos por coluna, identificação de colunas de data e seu período coberto,
  cardinalidade das colunas categóricas, e uma amostra estrutural (sem
  colunas de identificação direta). Achado principal: base com 9.991
  servidores e 62 colunas, várias delas oriundas de sistemas de origem
  diferentes (afastamentos, cessões, licenças, DB_SGC).

- **`01_perfil_demografico.ipynb`** — Distribuição por idade, sexo,
  escolaridade e UF de exercício. Achado principal: quadro concentrado no DF,
  com maioria de nível superior e distribuição de sexo equilibrada.

- **`02_cargos_secretarias.ipynb`** — Distribuição por cargo, secretaria,
  órgão de exercício e hierarquia do cargo (DAS). Achado principal: forte
  concentração num único cargo e numa única secretaria, mas dispersão maior
  entre órgãos de exercício.

- **`03_situacoes_especiais.ipynb`** — Servidores fora da situação normal de
  exercício: afastados para estudo, licenciados, cedidos a estados/municípios,
  em exercício fora do DF. Achado principal: grande maioria em situação
  normal; populações especiais são pequenas (dezenas a poucas centenas de
  pessoas).

- **`04_carreira_capacitacao.ipynb`** — Dados do sistema "DB_SGC": carreira,
  turma de ingresso, jornada de trabalho, situação funcional, tipo de
  duração do vínculo, classe e padrão salarial. Achado principal: esse
  sistema cobre só ~23% da base — a maior parte do quadro (incluindo o cargo
  mais comum) não está rastreada nele.

- **`05_raca_deficiencia.ipynb`** — Raça/cor e deficiência autodeclaradas.
  Achado principal: mesmo subconjunto de ~23% da base tem essa informação
  preenchida; entre os que informaram, perfil e proporção de deficiência
  declarada seguem o padrão esperado, sem concentração anômala.

(Números exatos e detalhados de cada análise estão em
`reports/resumo_reconhecimento.md` — não repetidos aqui.)

## 3. Decisões e incidentes técnicos

### Regra de privacidade: supressão de células pequenas (mudança de comportamento)
Durante autorrevisão dos gráficos já prontos, foi identificado que categorias
com **1 ou 2 pessoas** apareciam com contagem exata em alguns gráficos/tabelas
(ex: "Ensino Fundamental" com 1 servidor no notebook 01; "Deficiência Visual"
com 2 servidores no notebook 05). Isso é um risco real de reidentificação
mesmo sem nome/CPF. Foi criada a função `agrupar_celulas_pequenas()` em
`src/viz_style.py`, que agrupa qualquer categoria com **menos de 5 pessoas**
em um bucket "Outras (poucos casos)" antes de exibir. Essa correção foi
aplicada retroativamente nos notebooks 01, 03 e 04 (não só nos novos).
**Implicação para o futuro**: qualquer novo gráfico/tabela feito a partir
desta base deve usar essa função (ou seguir a mesma regra) antes de exibir
contagens por categoria.

### Bug de visualização: "Outros" podia parecer a maior categoria
Em gráficos de barra com muitas categorias (UF, secretaria, órgão), a
categoria "Outros" (soma das categorias menores) era ordenada por valor junto
com as categorias reais — em um caso (Órgão de Exercício), "Outros" virou a
maior barra do gráfico, passando a impressão errada de que era um órgão
específico gigante. Corrigido fixando "Outros" (e categorias "neutras" como
"NI") sempre na base do gráfico, em cinza, nunca competindo por posição com
as categorias reais. Implementado em `grafico_top_n_outros()` e no parâmetro
`destacar_neutro` de `grafico_barra_horizontal()`, ambos em `src/viz_style.py`.

### Extração de `src/viz_style.py`
Depois da 3ª repetição do mesmo bloco de estilo de gráfico entre notebooks,
o código foi extraído para um módulo compartilhado (`src/viz_style.py`), que
concentra: paleta de cores, estilo de eixos, e as duas regras de privacidade
acima (`agrupar_celulas_pequenas`, `destacar_neutro`, `resumo_informado`).
**Todo notebook novo deve importar desse módulo** em vez de recriar a lógica.

### Incidente: bloqueio de acesso ao arquivo de dados pelo Avast
O arquivo `data/raw/DB_SIAPE_processado_20260729.xlsx` passou a ser bloqueado
(`PermissionError`) especificamente para processos `python.exe`, mesmo após
reiniciar o computador e adicionar exceções na tela de "Exceções" do Avast
(não resolveu). Diagnóstico confirmado por eliminação: outros arquivos na
mesma pasta abriam normalmente; uma cópia com conteúdo idêntico mas nome
diferente abria normalmente; renomear essa cópia de volta ao nome original
voltava a bloquear na hora. Conclusão: o Avast (provavelmente Escudo de
Comportamento/Ransomware) marcou o **caminho exato do arquivo** como
suspeito, possivelmente por causa de muitas leituras repetidas em sequência
pelo mesmo processo não reconhecido (`python.exe` gerenciado por `uv`) — um
padrão parecido com comportamento de ransomware.

**Correção aplicada**: o arquivo foi renomeado para
`data/raw/DB_SIAPE_processado_20260729_v2.xlsx` (mesmo conteúdo, nome novo).
Todas as referências em `notebooks/*.ipynb`, `reports/resumo_reconhecimento.md`
e `src/load_data.py` foram atualizadas para o novo nome. O arquivo original
bloqueado foi preservado como backup em
`data/raw/DB_SIAPE_processado_20260729.xlsx.bloqueado_bkp` (fora do git).
**Implicação para o futuro**: se um `PermissionError` parecido aparecer de
novo (mesmo arquivo ou outro), não vale a pena insistir na tela de exceções
do Avast — o caminho mais rápido é renomear o arquivo e atualizar as
referências.

### Incidente correlato (mas distinto): kernel do Cursor segurando o arquivo aberto
Antes do incidente do Avast ter sido isolado como causa, um sintoma parecido
(`PermissionError` ao rodar `nbconvert --execute` pelo terminal) tinha uma
causa diferente e mais simples: havia um kernel Jupyter vivo, iniciado pelo
Cursor ao abrir o notebook, com o arquivo em uso. Resolvido encerrando o
processo do kernel. **Importante**: os dois incidentes têm o mesmo sintoma
(`PermissionError` no mesmo arquivo) mas causas diferentes — se reaparecer,
checar primeiro se há um kernel vivo (`tasklist` / `Get-Process`) antes de
suspeitar do Avast.

### Incidente menor: célula desatualizada no editor após a correção do nome do arquivo
Depois de corrigir o nome do arquivo em disco, o usuário ainda viu um erro
(`FileNotFoundError` com o nome antigo) ao rodar uma célula no Cursor — porque
o editor tinha o conteúdo antigo da célula em memória, não recarregado do
disco. Resolvido fechando o arquivo **sem salvar** e reabrindo. Não é um bug
de código; é um cuidado a ter sempre que um arquivo for editado por fora do
editor enquanto ele está aberto.

### Divisão de papéis Cursor / Claude Code
Ficou estabelecido que o Claude Code é o executor principal das tarefas
analíticas (exploração, scripts, execução, iteração), e o Cursor é usado pelo
usuário como camada de revisão visual e navegação de arquivos/diffs — evitando
ter dois agentes de IA operando os mesmos arquivos ao mesmo tempo. Esta sessão
foi encerrada sem novas edições em notebooks/relatórios exatamente para
respeitar esse princípio, já que a continuação será em outra instância.

### Commits realizados nesta sessão
- `a8f7999` — correção da supressão de células pequenas e do bloqueio de
  arquivo pelo Avast (10 arquivos: notebooks, `README.md`,
  `reports/resumo_reconhecimento.md`, `src/load_data.py`,
  `.claude/settings.json`).
- `748d141` — commit de acompanhamento só com uma permissão registrada
  automaticamente em `.claude/settings.json`.
- Estado do `git status` no momento em que este arquivo foi escrito: apenas
  `.claude/settings.json` modificado (nova permissão registrada
  automaticamente pela sessão atual) — nada relacionado a notebooks ou dados.

### `README.md`
Estava vazio desde o commit inicial (0 bytes, nunca teve conteúdo). Foi
preenchido nesta sessão com visão geral do projeto, comandos `uv`, estrutura
de pastas e tabela dos notebooks.

### Remoção de artefatos superados (`reports/summary.txt` e `src/load_data.py`)
Os dois arquivos eram de uma versão inicial/anterior do projeto, anterior às
análises estruturadas em notebooks. Antes de decidir, foi confirmado que
nada mais no projeto importava `src/load_data.py` (`grep` sem resultado fora
do próprio arquivo) — ou seja, código morto. Além do problema de privacidade
já conhecido (calculava `describe()` sobre CPF e Matrícula SIAPE, tratando
identificadores como quantidade), o script também apontava para um caminho
de dado que não existe mais (`data/DB_SIAPE_processado_20260729_v2.xlsx`, na
raiz de `data/`, em vez de `data/raw/`) — ou seja, já estava quebrado, não só
inconsistente. Por ser código morto, quebrado e substituído em funcionalidade
pelo `notebooks/00_reconhecimento.ipynb` + `reports/resumo_reconhecimento.md`,
optei por **remover** em vez de corrigir. O cache `src/__pycache__` associado
também foi removido.

### Limpeza do backup do incidente do Avast
`data/raw/DB_SIAPE_processado_20260729.xlsx.bloqueado_bkp` foi removido
(estava fora do git, sem risco). O arquivo de dados ativo continua sendo
`data/raw/DB_SIAPE_processado_20260729_v2.xlsx`.

## 4. Pendências reais

- **Investigar as inconsistências de qualidade de dado** listadas na seção 6
  de `reports/resumo_reconhecimento.md` (data de 2103, 2 registros com
  escolaridade muito baixa, colunas aparentemente duplicadas) junto à área
  responsável pela base de origem — não investigado a fundo intencionalmente,
  para não expor registros individuais. **Depende de terceiros.**
- **Decidir se este relatório vai ser atualizado periodicamente** conforme a
  base SIAPE for reprocessada, ou se é uma entrega única do piloto. **Decisão
  do usuário, ainda não tomada.**

## 5. Riscos ou ressalvas

- **Cobertura parcial em duas análises**: as análises de carreira/capacitação
  (notebook 04) e raça/deficiência (notebook 05) cobrem só **~23% da base**
  (o sistema "DB_SGC" e o cadastro de dados pessoais não abrangem todos os
  servidores — inclusive o cargo mais comum da base fica de fora). Qualquer
  número desses dois notebooks citado no relatório institucional deve deixar
  claro que representa um subconjunto, não o quadro completo.
- **Limiar de supressão de células pequenas (5) é uma escolha própria**, não
  um limiar legal/normativo conhecido. Se este relatório for usado de forma
  mais formal (ex: anexado ao relatório institucional), vale ter esse número
  validado por alguém com conhecimento de LGPD/privacidade de dados, em vez
  de aceitar como está.
- **Qualidade de dado não validada com a fonte**: os achados da seção 6 do
  `resumo_reconhecimento.md` (data de 2103, escolaridade muito baixa, colunas
  duplicadas) são inferências da exploração, não confirmadas com quem mantém
  a base original — tratar como hipótese, não fato, em qualquer comunicação
  mais formal.
- **Risco de ambiente (Avast)**: fica registrado que o antivírus desta
  máquina pode bloquear silenciosamente a leitura de um arquivo específico
  por processos Python após muitas execuções repetidas em sequência. Se isso
  se repetir com o arquivo `_v2` atual (ou com outro arquivo no futuro), a
  causa mais provável é essa, não um problema de código.
- **`data/` já está corretamente no `.gitignore`** — a base bruta do SIAPE
  nunca foi versionada no Git em nenhum momento deste projeto.
