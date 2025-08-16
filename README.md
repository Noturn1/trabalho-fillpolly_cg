# Editor de Polígonos com Preenchimento Gouraud (Fillpoly)

## 📜 Sobre o Projeto

Este projeto é uma aplicação gráfica desenvolvida em Python com a biblioteca Tkinter, criada como parte de um trabalho acadêmico para a disciplina de Computação Gráfica. O objetivo principal é demonstrar a implementação do algoritmo de preenchimento de polígonos **Scanline**, com a interpolação de cores através do método de sombreamento de **Gouraud**.

A aplicação permite que o usuário desenhe múltiplos polígonos em uma tela, definindo cores distintas para cada vértice, e visualize o preenchimento suave e interpolado em tempo real.

---

## ✨ Funcionalidades

* **Criação de Múltiplos Polígonos**: Desenhe quantos polígonos desejar na mesma tela.
* **Sombreamento de Gouraud**: Preenchimento com gradiente de cores suaves, interpoladas a partir das cores definidas nos vértices.
* **Seleção de Cores**: Um seletor de cores permite escolher a cor de cada vértice individualmente antes de adicioná-lo.
* **Interface Interativa**:
    * Adicione vértices com o **clique esquerdo** do mouse.
    * Finalize e preencha um polígono pressionando a **barra de espaço**.
    * Selecione um polígono existente com o **clique direito** do mouse.
* **Gerenciamento de Polígonos**:
    * Remova polígonos selecionados.
    * Limpe toda a tela para recomeçar.
    * Mostre ou esconda as arestas dos polígonos.

---

## 🚀 Como Usar

### Pré-requisitos

* Python 3.x instalado.
* A biblioteca Tkinter (geralmente já vem inclusa na instalação padrão do Python).

### Execução

1.  Certifique-se de que os dois arquivos, `interface_fillpoly.py` e `fillpoly.py`, estejam no mesmo diretório.
2.  Execute o arquivo da interface através do terminal:
    ```bash
    python interface_fillpoly.py
    ```
3.  A janela da aplicação será aberta e você poderá começar a desenhar.

### Controles

| Ação | Comando |
| :--- | :--- |
| **Adicionar Vértice** | Clique com o **botão esquerdo** do mouse |
| **Finalizar Polígono** | Pressione a **Barra de Espaço** |
| **Selecionar Polígono**| Clique com o **botão direito** do mouse sobre ele |
| **Escolher Cor** | Clique no botão "Escolher Cor do Vértice" |

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3
* **Interface Gráfica**: Tkinter

---

## 📂 Estrutura do Projeto

O código foi modularizado em dois arquivos para separar as responsabilidades, seguindo boas práticas de desenvolvimento:

* `fillpoly.py`: Contém toda a lógica matemática e as estruturas de dados do projeto.
    * **Classes `Cor` e `Vertice`**: Estruturas para armazenar os dados.
    * **Classe `Poligono`**: Entidade que representa um polígono, responsável por calcular e armazenar os pixels do seu preenchimento.
    * **Função `preenchimento_gourand`**: A implementação pura do algoritmo Scanline com Gouraud.

* `interface_fillpoly.py`: Responsável por toda a parte visual e pela interação com o usuário.
    * **Classe `TelaDesenho`**: Gerencia o canvas, os botões, os eventos de mouse/teclado e o ciclo de renderização. Ela utiliza os objetos da classe `Poligono` para desenhar os resultados na tela.
