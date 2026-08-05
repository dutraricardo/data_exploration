# Projeto: data_exploration

Ambiente gerenciado por uv. Nao usar pip diretamente.

Comandos padrao:
- Instalar dependencia: uv add <pacote>
- Rodar script: uv run python <arquivo>.py
- Rodar notebook: uv run jupyter lab
- Rodar testes: uv run pytest
- Lint: uv run ruff check .

Ambiente: Python 3.13, Windows.

Estrutura:
- notebooks/ -> exploracao
- src/ -> funcoes reutilizaveis
- data/ -> dados (nao versionar arquivos grandes)
- reports/ -> saidas finais
