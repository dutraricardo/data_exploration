# data_exploration

Projeto piloto de exploração de dados. Analisa a base de servidores do SIAPE em
`data/raw/DB_SIAPE_processado_20260729_v2.xlsx` e gera relatórios de apoio em
`reports/`.

Todas as análises seguem uma regra permanente: **nenhum registro individual
(nome, CPF, matrícula, e-mail, ou categorias com poucas pessoas) é reproduzido
em nenhum notebook ou relatório** — apenas agregados, contagens e percentuais.
Ver `reports/resumo_reconhecimento.md` para o resumo consolidado dos achados.

## Ambiente

Gerenciado com [uv](https://docs.astral.sh/uv/) — não usar `pip` diretamente.
Python 3.13, Windows.

```
uv add <pacote>          # instalar dependência
uv run python <arquivo>.py   # rodar script
uv run jupyter lab        # rodar notebooks
uv run pytest              # rodar testes
uv run ruff check .        # lint
```

## Estrutura

```
data/            # dados (não versionado; ver .gitignore)
notebooks/        # exploração, uma dimensão de análise por arquivo
src/               # funções e estilos reutilizáveis (ex: viz_style.py)
reports/           # saídas finais (resumos, relatórios)
```

### Notebooks

| Notebook | Conteúdo |
|---|---|
| `00_reconhecimento.ipynb` | Estrutura da base: colunas, tipos, valores ausentes, período de datas |
| `01_perfil_demografico.ipynb` | Idade, sexo, escolaridade, UF |
| `02_cargos_secretarias.ipynb` | Cargo, secretaria, órgão de exercício, hierarquia |
| `03_situacoes_especiais.ipynb` | Afastamentos, licenças, cessões, exercício fora do DF |
| `04_carreira_capacitacao.ipynb` | Carreira, turma, jornada, classe e padrão salarial (DB_SGC) |
| `05_raca_deficiencia.ipynb` | Raça/cor e deficiência autodeclaradas |

## Privacidade

Regras aplicadas em todos os notebooks, implementadas em `src/viz_style.py`:

- Colunas identificadoras diretas (Nome, CPF, Matrícula SIAPE, E-mail, Data de
  Nascimento) nunca têm valores exibidos.
- Categorias de cauda longa (muitas categorias com poucos casos cada) são
  agrupadas em "Outros" nos gráficos.
- Categorias com menos de 5 pessoas são agrupadas em "Outras (poucos casos)",
  em gráfico ou tabela, para evitar identificação individual.
