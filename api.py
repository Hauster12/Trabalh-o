from pathlib import Path
from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

app = FastAPI(title="Rotas do Prédio com Grafos - UNISENAC")
grafo = carregar_grafo(Path(__file__).with_name("arestas.txt"))

ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


# Lista as portas disponíveis
@app.get("/portas")
def portas():
    return list(grafo.keys())


@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    porta = porta.strip().upper()
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada")
    return [{"porta": p, "peso": w} for p, w in grafo[porta]]


# Busca uma rota com o algoritmo escolhido
@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
    origem = origem.strip().upper()
    destino = destino.strip().upper()
    algoritmo = algoritmo.strip().lower()

    if origem not in grafo or destino not in grafo:
        raise HTTPException(404, "Porta não encontrada")
    if algoritmo not in ALGORITMOS:
        raise HTTPException(
            400, "Algoritmo inválido. Use: bfs, dfs, gulosa ou dijkstra"
        )

    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": "passos",
        "visitados": visitados,
    }


# Compara os resultados das buscas
@app.get("/comparar")
def comparar(origem: str, destino: str):
    origem = origem.strip().upper()
    destino = destino.strip().upper()

    if origem not in grafo or destino not in grafo:
        raise HTTPException(404, "Porta não encontrada")

    resultado = {}
    for nome, func in ALGORITMOS.items():
        caminho, custo, visitados = func(grafo, origem, destino)
        resultado[nome] = {
            "caminho": caminho,
            "custo": custo,
            "unidade": "passos",
            "visitados": visitados,
        }
    return resultado
