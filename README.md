  # Rotas do Prédio com Grafos

Trabalho de Algoritmos e Estruturas de Dados II 
Professor: Pablo De Chiaro

## Integrantes
- Tiago Santos
- Henrique Serpa
- Gabriel Schug

## Unidade de medida
Usamos passos para medir a distância entre cada porta/local do prédio, começando a contagem a partir do `LABTEC` (ponto zero). Ao todo ficaram 38 locais e 39 conexões mapeadas no arquivo `arestas.txt`.

## Como rodar o projeto

Primeiro, instale o FastAPI e o Uvicorn:
```bash
pip install fastapi uvicorn
```

Para conferir se o grafo está carregando todas as portas e arestas certinho (Passo 3):
```bash
python grafo.py
```

Para usar o menu pelo terminal:
```bash
python Grafo_dusgu.py
```

Para subir a API:
```bash
python -m uvicorn Grafo_dusgu:app --reload
```
*(também funciona rodando `uvicorn Grafo_dusgu:app --reload`)*

Com a API rodando, é só abrir `http://127.0.0.1:8000/docs` no navegador para testar os endpoints `/portas`, `/vizinhos/{porta}`, `/rota` e `/comparar`.

## Diferença entre BFS e Dijkstra no nosso grafo

Testando as rotas do prédio, um exemplo claro onde a BFS e o Dijkstra dão caminhos diferentes é saindo de **`LABTEC`** até **`BIBLIOTECAINTERNO`** (ou saindo de **`RUAINTERNODOIS`** até **`BIBLIOTECAINTERNO`**):

- **Caminho pela BFS:**  
  `LABTEC -> RUAINTERNO -> LANCHERIADOIS -> LANCHERIAUM -> BIBLIOTECARUA -> BIBLIOTECAINTERNO`  
  Passa por 6 locais (5 arestas), mas dá um custo total de 87 passos (`18 + 8 + 25 + 29 + 7`).

- **Caminho pelo Dijkstra:**  
  `LABTEC -> SALA201 -> SALA202 -> SALA203 -> RUAINTERNODOIS -> BF -> BM -> SECAO -> COORDENACAO -> LIDERACAO -> DR -> PROFESSORES -> BIBLIOTECAINTERNO`  
  Passa por 13 locais (12 arestas), mas o custo total cai para 77 passos (`4 + 5 + 21 + 9 + 2 + 11 + 9 + 3 + 1 + 3 + 5 + 4`).

**Por que deu diferente?**  
A BFS só olha para a quantidade de portas no caminho (ela não liga para o peso das arestas), então ela escolhe ir pela Lancheria porque tem menos paradas até a Biblioteca, mesmo tendo corredores bem mais longos no meio do caminho (25 e 29 passos). Já o Dijkstra soma os passos de cada trecho usando a fila de prioridade e prefere passar pelo corredor da Seção/Coordenação/Professores: apesar de passar na frente de mais portas, elas ficam bem grudadas umas nas outras (1 a 5 passos de distância), economizando 10 passos no final.
