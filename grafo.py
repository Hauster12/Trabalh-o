from collections import deque
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("arestas.txt")


def carregar_grafo(caminho=ARQUIVO_PADRAO):
    grafo = {}
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            if not linha.strip():
                continue
            a, b, peso = linha.split()
            peso = int(peso)
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))
    return grafo


def conferir_grafo(grafo, origem="LABTEC"):
    num_portas = len(grafo)
    num_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2

    fila = deque([origem])
    visitados = {origem}
    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    nao_alcancadas = set(grafo.keys()) - visitados
    print(f"Número de portas: {num_portas}")
    print(f"Número de arestas: {num_arestas}")
    print(f"Portas alcançadas a partir de {origem}: {len(visitados)}/{num_portas}")
    if not nao_alcancadas:
        print("Todas as portas foram alcançadas com sucesso!")
    else:
        print(f"Faltam arestas para alcançar: {sorted(nao_alcancadas)}")


if __name__ == "__main__":
    g = carregar_grafo()
    conferir_grafo(g)
