# Bot de Automação Contábil (RPA)

Versão: 1.0.0

## Resumo do Projeto

Este projeto consiste em um script de **Automação Robótica de Processos (RPA)** desenvolvido para reclassificar automaticamente lançamentos contábeis no sistema **Domínio**, operando sobre uma interface de **Área de Trabalho Remota (RDP)**.

O sistema atua identificando padrões de lançamentos (únicos ou múltiplos), capturando dados de filiais e aplicando regras de negócio para correção de contas contábeis (Débito/Crédito) e códigos de filiais bancárias.

## Lógica de Operação

O robô executa um ciclo contínuo (loop) seguindo este fluxograma lógico:

INÍCIO DO CICLO  
  ├── 1. Filtra lançamentos pendentes na conta (variavel: CONTA_FORNECEDOR) e com o historico (variavel: HISTORICO_BUSCA)  
  ├── 2. Abre o detalhamento do lançamento (Captura valor e refiltra)  
  ├── 3. ANÁLISE DO GRID (Leitura comparativa):  
  │    ├── SE (Débito da Linha 1 != Débito da Linha 2):  
  │    │    # Cenário: Múltiplo (2 Lançamentos)  
  │    │    -> Identifica qual linha é o Fornecedor  
  │    │    -> Corrige para Conta Matriz (variavel: CONTA_MATRIZ)  
  │    │    -> Captura a Filial  
  │    │    -> Busca o Banco correspondente no Hash Map  
  │    │    -> Corrige a segunda linha com o Banco  
  │    │    -> Salva  
  │    │  
  │    └── SENÃO (Débitos iguais ou Linha 2 vazia):  
  │         # Cenário: Lançamento Único  
  │         -> Altera a conta de crédito para '1' (variavel: CAIXA_CONTA)  
  │         -> Salva  
  │  
  └── 4. Retorna ao filtro e repete  
FIM SE lista vazia  

## Arquitetura e Soluções de Engenharia

A versão atual foi desenhada com foco em **estabilidade em ambientes de alta latência (RDP)**.

* Linguagem: Python 3.12
* Core: `pyautogui` para interação de interface.
* Configuração: Variáveis de ambiente (`CONTA_FORNECEDOR`, `CAIXA_CONTA`, `CONTA_MATRIZ`, `HISTORICO_BUSCA` ) e coordenadas centralizadas.
* Segurança: Implementação de Fail-Safe (movimento de mouse para abortar).

### Desafios Superados

1. Latência e Inputs "Fantasmas" (Erro do "11")
   * Problema: Comandos rápidos de seleção (`Ctrl+A`) falhavam devido ao lag, fazendo o robô digitar "1" sem apagar o "20001" anterior, gerando "11".
   * Solução ("Limpeza Nuclear"): Implementação de uma função que não depende de seleção visual. Ela move o cursor para o final (`End`) e executa deleções massivas (`Backspace` + `Delete`), garantindo o campo limpo.

2. Falha no Registro de Cliques
   * *Problema:* O sistema remoto frequentemente ignorava cliques rápidos (`.click()`), impedindo a seleção da segunda linha do grid.
   * *Solução ("Clique longo"):* Desenvolvimento de uma função wrapper que simula um clique humano com retenção (`mouseDown` + `sleep 0.4s` + `mouseUp`), forçando o sistema remoto a registrar o evento de foco.


## 🚀 Roadmap: Melhorias Futuras (v2.0.0)

Como plano de evolução para tornar a aplicação agnóstica à resolução de tela, as seguintes melhorias estão mapeadas:

## 1. Visão Computacional (Computer Vision)
* Biblioteca Alvo: `OpenCV` + `pyautogui.locateOnScreen`.
* Objetivo: Substituir as coordenadas fixas `(X, Y)` por reconhecimento de imagem dos botões. Isso permitirá que o robô funcione em qualquer monitor sem re-mapeamento.

### 2. OCR (Reconhecimento Óptico de Caracteres)
* Biblioteca Alvo: `Tesseract`.
* Objetivo: Ler os valores diretamente da tela via screenshot, eliminando a dependência do `Clipboard`, que pode ser instável em conexões remotas.

### 3. Arquivos de Configuração Externos
* Objetivo: Mover a tabela de filiais (`tabela_filiais`) para um arquivo `.json` externo, permitindo manutenção das regras de negócio sem alteração no código fonte.

## Estrutura do Projeto

O projeto é composto por dois módulos principais:

1. **`rastreamento.py` (Utilitário de Calibração):**
   Script auxiliar responsável por mapear as coordenadas `(X, Y)` dos botões e campos na tela do usuário. Ele guia o operador passo a passo para clicar nos elementos da interface, gerando o arquivo de configuração necessário para o robô.

2. **`robo_main.py` (Core):**
   O script principal que contém a lógica de negócio, as funções de segurança (limpeza nuclear, clique reforçado) e o loop de execução da automação.

## 📦 Como Executar

1. Clone este repositório.
2. Instale as dependências: `pip install pyautogui pyperclip`
3. Abra o sistema Domínio na conexão remota (Maximize a tela).
4. **Passo 1 (Configuração):** Execute o script de mapeamento para calibrar o robô para o seu monitor:

   python rastreamento.py

   Siga as instruções do terminal para capturar as coordenadas e cole o resultado no início do arquivo `robo_main.py`.

5. **Passo 2 (Execução):** Inicie o robô:

   python robo_main.py

6. Alterne rapidamente para a janela remota (você tem 5 segundos).
7. **Para parar:** Mova o mouse bruscamente para o canto superior esquerdo da tela (Fail-Safe).


Desenvolvido por Camila Azevedo  
Engenheira Eletricista & Mestranda em IA  
email: camila.azevedo.eng@gmail.com  
