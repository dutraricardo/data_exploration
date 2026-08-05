"""Estilo e helpers de grafico compartilhados entre os notebooks de exploracao."""

import matplotlib.pyplot as plt
import pandas as pd

COR_PRINCIPAL = "#2a78d6"
COR_OUTROS = "#898781"
COR_TEXTO_PRIMARIA = "#0b0b0b"
COR_TEXTO_SECUNDARIA = "#52514e"
COR_TEXTO_MUTED = "#898781"
COR_GRADE = "#e1e0d9"
COR_BASELINE = "#c3c2b7"


def aplicar_estilo_global() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = COR_BASELINE
    plt.rcParams["text.color"] = COR_TEXTO_PRIMARIA
    plt.rcParams["axes.labelcolor"] = COR_TEXTO_SECUNDARIA
    plt.rcParams["xtick.color"] = COR_TEXTO_MUTED
    plt.rcParams["ytick.color"] = COR_TEXTO_MUTED


def estilizar_eixos(ax, grade_x: bool = False, grade_y: bool = False) -> None:
    """Remove bordas desnecessarias e aplica grade discreta quando pedido."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(COR_BASELINE)
    ax.tick_params(length=0)
    if grade_x:
        ax.xaxis.grid(True, color=COR_GRADE, linewidth=0.8)
        ax.set_axisbelow(True)
    if grade_y:
        ax.yaxis.grid(True, color=COR_GRADE, linewidth=0.8)
        ax.set_axisbelow(True)


def grafico_barra_horizontal(contagem: pd.Series, total: int, titulo: str,
                              xlabel: str = "Quantidade de servidores",
                              figsize: tuple = (8, 5),
                              destacar_neutro: str | None = None) -> None:
    """Grafico de barras horizontais ordenado por valor, com rotulos de valor e percentual.

    Use quando TODAS as categorias sao mostradas (sem agrupamento em "Outros").

    `destacar_neutro`: rotulo de uma categoria "nao-informativa" (ex: "NI") que deve
    ser fixada na base do grafico e pintada em cinza, para nao competir visualmente
    com as categorias reais.
    """
    percentual = (contagem / total * 100).round(1)

    if destacar_neutro is not None and destacar_neutro in contagem.index:
        reais = contagem.drop(index=destacar_neutro).sort_values(ascending=True)
        ordem = pd.concat([contagem[[destacar_neutro]], reais])
        cores = [COR_OUTROS] + [COR_PRINCIPAL] * len(reais)
    else:
        ordem = contagem.sort_values(ascending=True)
        cores = COR_PRINCIPAL

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(ordem.index, ordem.values, color=cores, height=0.6)
    estilizar_eixos(ax, grade_x=True)
    ax.set_title(titulo, loc="left", fontsize=13, color=COR_TEXTO_PRIMARIA, pad=12)
    ax.set_xlabel(xlabel)

    for nome, valor in ordem.items():
        pct = percentual[nome]
        ax.text(valor, nome, f"  {valor} ({pct}%)", va="center", fontsize=10, color=COR_TEXTO_PRIMARIA)

    plt.tight_layout()
    plt.show()


def grafico_top_n_outros(serie: pd.Series, total: int, titulo: str, n: int = 10,
                          xlabel: str = "Quantidade de servidores",
                          figsize: tuple = (8, 5)) -> pd.Series:
    """Grafico de barras horizontais com as N categorias mais frequentes, agrupando
    o restante em "Outros".

    "Outros" e sempre fixado na base do grafico (nunca ordenado por valor junto com
    as categorias nomeadas) e desenhado em cinza neutro, para nao ser confundido com
    uma categoria real que por acaso e a maior do grafico.

    Retorna a serie completa de contagem (todas as categorias, sem agrupar), para uso
    em tabelas ou no resumo consolidado.
    """
    contagem_completa = serie.value_counts()
    n_total_categorias = len(contagem_completa)
    topo = contagem_completa.head(n).sort_values(ascending=True)

    nomes = list(topo.index)
    valores = list(topo.values)
    cores = [COR_PRINCIPAL] * len(topo)

    if n_total_categorias > n:
        n_outras = n_total_categorias - n
        valor_outros = int(contagem_completa.iloc[n:].sum())
        rotulo_outros = f"Outros ({n_outras} categorias)"
        nomes = [rotulo_outros] + nomes
        valores = [valor_outros] + valores
        cores = [COR_OUTROS] + cores

    percentual = {nome: round(valor / total * 100, 1) for nome, valor in zip(nomes, valores)}

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(nomes, valores, color=cores, height=0.6)
    estilizar_eixos(ax, grade_x=True)
    ax.set_title(titulo, loc="left", fontsize=13, color=COR_TEXTO_PRIMARIA, pad=12)
    ax.set_xlabel(xlabel)

    for nome, valor in zip(nomes, valores):
        ax.text(valor, nome, f"  {valor} ({percentual[nome]}%)", va="center", fontsize=10, color=COR_TEXTO_PRIMARIA)

    plt.tight_layout()
    plt.show()

    return contagem_completa


def resumo_informado(serie: pd.Series, total: int, valor_neutro: str = "NI") -> tuple[pd.Series, float]:
    """Separa uma coluna categorica em (categorias com valor real, % da base que tem
    valor informado). Util para colunas onde a maioria dos registros e "NI" (nao
    informado / nao se aplica) e a analise interessante esta no subconjunto restante.
    """
    contagem = serie.value_counts()
    contagem_informada = contagem.drop(index=valor_neutro, errors="ignore")
    pct_informado = round(contagem_informada.sum() / total * 100, 1)
    return contagem_informada, pct_informado


def agrupar_celulas_pequenas(contagem: pd.Series, minimo: int = 5) -> tuple[pd.Series, str | None]:
    """Agrupa categorias com contagem abaixo de `minimo` em um unico grupo neutro.

    Celulas muito pequenas (poucas pessoas em uma categoria sensivel, como tipo de
    deficiencia) podem, na pratica, identificar indivíduos mesmo sem nome ou CPF.
    Retorna a serie agrupada e o rotulo do grupo (ou None se nada precisou ser
    agrupado) para uso com `destacar_neutro` em `grafico_barra_horizontal`.
    """
    grandes = contagem[contagem >= minimo]
    pequenas = contagem[contagem < minimo]

    if len(pequenas) == 0:
        return contagem, None

    rotulo = f"Outras (poucos casos, {len(pequenas)} categorias agrupadas)"
    agrupada = pd.concat([grandes, pd.Series({rotulo: int(pequenas.sum())})])
    return agrupada, rotulo
