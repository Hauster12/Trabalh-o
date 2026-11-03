from collections import deque
import heapq
from pathlib import Path
import unicodedata

NOMES_ORIGINAIS = {
    0: "Labtec",
    1: "Sala 201",
    2: "Sala 202",
    3: "Rua Interno",
    4: "Sala 203",
    5: "Rua Interno Dois",
    6: "BF",
    7: "BM",
    8: "Sala 204",
    9: "Sala 205",
    10: "Sala 102",
    11: "Saída",
    12: "Massagista",
    13: "Apoio Tec",
    14: "Copa",
    15: "Saída Creche",
    16: "Lancheria Um",
    17: "Lancheria Dois",
    18: "Recepção",
    19: "Entrada",
    20: "Biblioteca Rua",
    21: "Coordenação",
    22: "Seção",
    23: "Lideração",
    24: "D.R",
    25: "Professores",
    26: "Biblioteca Interno",
    27: "S2",
    28: "S1",
    29: "S3",
    30: "Prédio 2",
    31: "Sala 210",
    32: "Sala 209",
    33: "Idiomas",
    34: "Sala 208",
    35: "Sala 207",
    36: "Sala 206",
    37: "Saída Prédio 2",
}

PORTAS_POR_ID = {
    0: "LABTEC",
    1: "SALA201",
    2: "SALA202",
    3: "RUAINTERNO",
    4: "SALA203",
    5: "RUAINTERNODOIS",
    6: "BF",
    7: "BM",
    8: "SALA204",
    9: "SALA205",
    10: "SALA102",
    11: "SAIDA",
    12: "MASSAGISTA",
    13: "APOIOTEC",
    14: "COPA",
    15: "SAIDACRECHE",
    16: "LANCHERIAUM",
    17: "LANCHERIADOIS",
    18: "RECEPCAO",
    19: "ENTRADA",
    20: "BIBLIOTECARUA",
    21: "COORDENACAO",
    22: "SECAO",
    23: "LIDERACAO",
    24: "DR",
    25: "PROFESSORES",
    26: "BIBLIOTECAINTERNO",
    27: "S2",
    28: "S1",
    29: "S3",
    30: "PREDIO2",
    31: "SALA210",
    32: "SALA209",
    33: "IDIOMAS",
    34: "SALA208",
    35: "SALA207",
    36: "SALA206",
    37: "SAIDAPREDIO2",
}

ID_POR_PORTA = {porta: id_no for id_no, porta in PORTAS_POR_ID.items()}

# Ligações entre as portas e quantidade de passos
ARESTAS_PADRAO = [
    (0, 1, 4),
    (1, 2, 5),
    (2, 4, 21),
    (4, 5, 9),
    (5, 6, 2),
    (6, 7, 11),
    (7, 8, 9),
    (8, 9, 9),
    (9, 10, 18),
    (10, 11, 2),
    (10, 12, 3),
    (12, 13, 12),
    (13, 14, 4),
    (14, 15, 1),
    (7, 22, 9),
    (22, 21, 3),
    (21, 23, 1),
    (23, 24, 3),
    (24, 25, 5),
    (25, 26, 4),
    (5, 16, 12),
    (16, 20, 29),
    (20, 26, 7),
    (26, 27, 36),
    (27, 28, 3),
    (27, 29, 1),
    (0, 3, 18),
    (3, 18, 8),
    (18, 19, 12),
    (3, 17, 8),
    (16, 17, 25),
    (17, 30, 68),
    (30, 31, 6),
    (31, 32, 4),
    (32, 33, 6),
    (33, 34, 6),
    (33, 35, 11),
    (35, 36, 13),
    (36, 37, 8),
]

ARQUIVO_ARESTAS = Path(__file__).with_name("arestas.txt")


def garantir_arquivo_arestas(caminho=ARQUIVO_ARESTAS):
    caminho = Path(caminho)
    if not caminho.exists():
        linhas = [
            f"{PORTAS_POR_ID[a]} {PORTAS_POR_ID[b]} {peso}"
            for a, b, peso in ARESTAS_PADRAO
        ]
        caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")


# Lê as conexões do arquivo
def carregar_grafo(caminho=ARQUIVO_ARESTAS):
    garantir_arquivo_arestas(caminho)
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


def normalizar_chave(texto):
    texto = unicodedata.normalize("NFD", str(texto).strip().upper())
    sem_acento = "".join(c for c in texto if not unicodedata.combining(c))
    return "".join(c for c in sem_acento if c.isalnum())


def identificar_porta(entrada, grafo):
    texto = str(entrada).strip()
    if texto.isdigit() and int(texto) in PORTAS_POR_ID:
        return PORTAS_POR_ID[int(texto)]

    chave = normalizar_chave(texto)
    if chave in grafo:
        return chave
    if f"SALA{chave}" in grafo:
        return f"SALA{chave}"

    for id_no, nome in NOMES_ORIGINAIS.items():
        if normalizar_chave(nome) == chave:
            return PORTAS_POR_ID[id_no]

    raise ValueError(f"Porta '{entrada}' não encontrada.")


def rotulo_porta(porta):
    if porta in ID_POR_PORTA:
        id_no = ID_POR_PORTA[porta]
        return f"{id_no} - {porta} ({NOMES_ORIGINAIS[id_no]})"
    return porta


def calcular_custo_caminho(grafo, caminho):
    if len(caminho) < 2:
        return 0
    total = 0
    for a, b in zip(caminho, caminho[1:]):
        pesos = [peso for vizinho, peso in grafo[a] if vizinho == b]
        if not pesos:
            return float("inf")
        total += min(pesos)
    return total


def reconstruir_caminho(anterior, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


# Busca por largura usando fila
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
            caminho = reconstruir_caminho(anterior, origem, destino)
            custo = calcular_custo_caminho(grafo, caminho)
            return caminho, custo, visitados

        for vizinho, _ in grafo[atual]:
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                anterior[vizinho] = atual
                fila.append(vizinho)

    return [], float("inf"), visitados


# Busca por profundidade usando pilha
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
            caminho = reconstruir_caminho(anterior, origem, destino)
            custo = calcular_custo_caminho(grafo, caminho)
            return caminho, custo, visitados

        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in visitados_set:
                anterior[vizinho] = atual
                pilha.append(vizinho)

    return [], float("inf"), visitados


# Prioriza a ligação com menor peso
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
        custo = calcular_custo_caminho(grafo, caminho)
        return caminho, custo, visitados

    return [], float("inf"), visitados


# Calcula o caminho de menor custo
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
            caminho = reconstruir_caminho(anterior, origem, destino)
            return caminho, distancia[destino], len(finalizadas)

        for vizinho, peso in grafo[atual]:
            if vizinho not in finalizadas:
                nova = d + peso
                if nova < distancia[vizinho]:
                    distancia[vizinho] = nova
                    anterior[vizinho] = atual
                    heapq.heappush(fila, (nova, vizinho))

    return [], float("inf"), len(finalizadas)


ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


def conferir_grafo(grafo, origem_inicial="LABTEC"):
    num_portas = len(grafo)
    num_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2

    fila = deque([origem_inicial])
    alcancadas = {origem_inicial}
    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in alcancadas:
                alcancadas.add(vizinho)
                fila.append(vizinho)

    faltando = set(grafo.keys()) - alcancadas
    print(f"Total de portas: {num_portas}")
    print(f"Total de arestas: {num_arestas}")
    print(f"Portas alcançadas via BFS a partir de {origem_inicial}: {len(alcancadas)}/{num_portas}")
    if not faltando:
        print("Grafo conexo! Todas as portas foram alcançadas a partir do LABTEC.")
    else:
        print(f"Atenção! Portas não alcançadas: {sorted(faltando)}")


try:
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Rotas do Prédio com Grafos - UNISENAC")
    grafo_api = carregar_grafo(ARQUIVO_ARESTAS)

    @app.get("/portas")
    def listar_portas():
        return list(grafo_api.keys())

    @app.get("/vizinhos/{porta}")
    def vizinhos(porta: str):
        porta_norm = porta.strip().upper()
        if porta_norm not in grafo_api:
            raise HTTPException(404, "Porta não encontrada")
        return [{"porta": p, "peso": w} for p, w in grafo_api[porta_norm]]

    @app.get("/rota")
    def calcular_rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
        origem_norm = origem.strip().upper()
        destino_norm = destino.strip().upper()
        alg_norm = algoritmo.strip().lower()

        if origem_norm not in grafo_api or destino_norm not in grafo_api:
            raise HTTPException(404, "Porta não encontrada")
        if alg_norm not in ALGORITMOS:
            raise HTTPException(
                400, "Algoritmo inválido. Use: bfs, dfs, gulosa ou dijkstra"
            )

        caminho, custo, visitados = ALGORITMOS[alg_norm](
            grafo_api, origem_norm, destino_norm
        )
        return {
            "algoritmo": alg_norm,
            "caminho": caminho,
            "custo": custo,
            "unidade": "passos",
            "visitados": visitados,
        }

    @app.get("/comparar")
    def comparar_algoritmos(origem: str, destino: str):
        origem_norm = origem.strip().upper()
        destino_norm = destino.strip().upper()

        if origem_norm not in grafo_api or destino_norm not in grafo_api:
            raise HTTPException(404, "Porta não encontrada")

        resultado = {}
        for nome_alg, func in ALGORITMOS.items():
            caminho, custo, visitados = func(grafo_api, origem_norm, destino_norm)
            resultado[nome_alg] = {
                "caminho": caminho,
                "custo": custo,
                "unidade": "passos",
                "visitados": visitados,
            }
        return resultado

except ImportError:
    app = None


# Menu principal do programa
def main():
    grafo = carregar_grafo(ARQUIVO_ARESTAS)
    while True:
        print("\n=== GRAFO DA FACULDADE (Grafo_dusgu) ===")
        print("1 - Mostrar todas as portas")
        print("2 - Mostrar lista de adjacência")
        print("3 - Conferir grafo (Passo 3: portas, arestas e conectividade via BFS)")
        print("4 - Calcular rota com um algoritmo (BFS, DFS, Gulosa ou Dijkstra)")
        print("5 - Comparar os 4 algoritmos lado a lado")
        print("0 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "0":
            break
        elif opcao == "1":
            for id_no, porta in PORTAS_POR_ID.items():
                print(f"{id_no:2d} - {porta:<18} ({NOMES_ORIGINAIS[id_no]})")
        elif opcao == "2":
            for porta, lista_vizinhos in grafo.items():
                destinos = "; ".join(f"{v} ({p} passos)" for v, p in lista_vizinhos)
                print(f"{porta} -> {destinos}")
        elif opcao == "3":
            conferir_grafo(grafo)
        elif opcao == "4":
            try:
                origem = identificar_porta(input("Origem (ID ou nome): "), grafo)
                destino = identificar_porta(input("Destino (ID ou nome): "), grafo)
                alg = input("Algoritmo (bfs, dfs, gulosa, dijkstra): ").strip().lower()
                if alg not in ALGORITMOS:
                    print("Algoritmo inválido! Escolha entre: bfs, dfs, gulosa, dijkstra.")
                    continue
                caminho, custo, visitados = ALGORITMOS[alg](grafo, origem, destino)
                print(f"\nAlgoritmo: {alg.upper()}")
                print(f"Caminho ({len(caminho)} portas): {' -> '.join(caminho)}")
                print(f"Custo total: {custo} passos")
                print(f"Portas visitadas: {visitados}")
            except ValueError as erro:
                print(erro)
        elif opcao == "5":
            try:
                origem = identificar_porta(input("Origem (ID ou nome): "), grafo)
                destino = identificar_porta(input("Destino (ID ou nome): "), grafo)
                print(f"\nComparativo de {origem} até {destino}:")
                print(f"{'Algoritmo':<10} | {'Custo':<12} | {'Portas':<7} | {'Visitados':<9} | Caminho")
                print("-" * 80)
                for nome_alg, func in ALGORITMOS.items():
                    caminho, custo, visitados = func(grafo, origem, destino)
                    rota_str = " -> ".join(caminho)
                    print(
                        f"{nome_alg.upper():<10} | {f'{custo} passos':<12} | {len(caminho):<7} | {visitados:<9} | {rota_str}"
                    )
            except ValueError as erro:
                print(erro)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")
