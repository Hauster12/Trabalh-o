from collections import deque
import heapq


def _calcular_custo(grafo, caminho):
    if len(caminho) < 2:
        return 0
    total = 0
    for a, b in zip(caminho, caminho[1:]):
        pesos = [peso for vizinho, peso in grafo[a] if vizinho == b]
        if not pesos:
            return float("inf")
        total += min(pesos)
    return total


# Monta a rota voltando pelos nós anteriores
def _reconstruir_caminho(anterior, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


# Percorre por níveis com uma fila
def bfs(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    fila = deque([origem])
    descobertos = {origem}
    anterior = {}
    visitados = 0

    while fila:
        atual = fila.popleft()
        visitados += 1

        if atual == destino:
            caminho = _reconstruir_caminho(anterior, origem, destino)
            custo = _calcular_custo(grafo, caminho)
            return caminho, custo, visitados

        for vizinho, _ in grafo[atual]:
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                anterior[vizinho] = atual
                fila.append(vizinho)

    return [], float("inf"), visitados


# Percorre usando uma pilha
def dfs(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    pilha = [origem]
    visitados_set = set()
    anterior = {}
    visitados = 0

    while pilha:
        atual = pilha.pop()
        if atual in visitados_set:
            continue
        visitados_set.add(atual)
        visitados += 1

        if atual == destino:
            caminho = _reconstruir_caminho(anterior, origem, destino)
            custo = _calcular_custo(grafo, caminho)
            return caminho, custo, visitados

        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in visitados_set:
                anterior[vizinho] = atual
                pilha.append(vizinho)

    return [], float("inf"), visitados


# Testa primeiro as ligações mais leves
def gulosa(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    visitados_set = set()
    visitados = 0
    caminho = []

    def buscar(atual):
        nonlocal visitados
        visitados_set.add(atual)
        visitados += 1
        caminho.append(atual)

        if atual == destino:
            return True

        vizinhos_ordenados = sorted(grafo[atual], key=lambda item: item[1])
        for vizinho, _ in vizinhos_ordenados:
            if vizinho not in visitados_set:
                if buscar(vizinho):
                    return True

        caminho.pop()
        return False

    if buscar(origem):
        custo = _calcular_custo(grafo, caminho)
        return caminho, custo, visitados

    return [], float("inf"), visitados


# Soma os pesos para achar a menor rota
def dijkstra(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        return [], float("inf"), 0

    distancia = {p: float("inf") for p in grafo}
    anterior = {}
    distancia[origem] = 0
    fila = [(0, origem)]
    finalizadas = set()

    while fila:
        d, atual = heapq.heappop(fila)
        if atual in finalizadas:
            continue
        finalizadas.add(atual)

        if atual == destino:
            caminho = _reconstruir_caminho(anterior, origem, destino)
            return caminho, distancia[destino], len(finalizadas)

        for vizinho, peso in grafo[atual]:
            if vizinho not in finalizadas:
                nova = d + peso
                if nova < distancia[vizinho]:
                    distancia[vizinho] = nova
                    anterior[vizinho] = atual
                    heapq.heappush(fila, (nova, vizinho))

    return [], float("inf"), len(finalizadas)
