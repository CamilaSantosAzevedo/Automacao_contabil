# ==============================================================================
# PROJETO: Automação RPA Contábil - Domínio Sistemas
# VERSÃO: 1.0.0 
# AUTORA: Camila (Engenheira Eletricista / Mestranda em IA)
# DATA: 29/11/2025
# 
# DESCRIÇÃO:
# Script para reclassificação automática de lançamentos contábeis via acesso
# remoto (RDP), com tratamento robusto de latência e erros de interface.
# ==============================================================================

import pyautogui
import time
import pyperclip
import winsound

# --- CONFIGURAÇÕES GERAIS ---
pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True 

# --- MAPEAMENTO DE COORDENADAS (1920x1080) ---
# Ajuste conforme a resolução do monitor
COORD_FILTRO_CONTA  = (639, 227)
COORD_FILTRO_HIST   = (785, 251)
COORD_FILTRO_VALOR  = (372, 252)
COORD_BTN_LISTAR    = (1124, 216)

COORD_GRID_LINHA_1  = (618, 321)
COORD_GRID_LINHA_2  = (613, 341)

COORD_LANC_VALOR    = (789, 516)
COORD_LANC_DEBITAR  = (266, 517)
COORD_LANC_CREDITAR = (522, 516)
COORD_LANC_FILIAL   = (1128, 517)

COORD_BTN_GRAVAR    = (1079, 669)
COORD_BTN_CANCELAR  = (991, 667)
COORD_POPUP_SIM     = (740, 433)

# --- REGRAS DE NEGÓCIO (DE-PARA: FILIAL -> BANCO) ---
tabela_filiais = {
    '101472': '26991', '101390': '26997', '101391': '26998', '101392': '26984',
    '101394': '26999', '101460': '26987', '101393': '26986', '101461': '26990',
    '101473': '26989', '101463': '26983', '101469': '26980', '101470': '26988',
    '101471': '26982'
}

# Contas Alvo
CONTA_FORNECEDOR = '20001'
CONTA_MATRIZ     = '15815'
HISTORICO_BUSCA  = 'mendon'
CAIXA_CONTA      = '1'


# --- FUNÇÕES AUXILIARES ---

def clique_longo(coordenada):
    """
    Realiza um clique longo para garantir o registro em sistemas com lag.
    """
    pyautogui.moveTo(coordenada)
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.4)       
    pyautogui.mouseUp()
    time.sleep(0.2)

def limpar_e_escrever_seguro(texto):
    """
    Limpa campos com máscara (ex: monetário) de forma segura contra input lag.
    Estratégia: Backspace inicial -> End -> Backspace lento.
    """
    pyautogui.press('backspace', presses=1, interval=0.1) 
    pyautogui.press('end')  
    time.sleep(0.1)
    
    # Intervalo maior (0.4s) para garantir que o sistema processe cada deleção
    pyautogui.press('backspace', presses=7, interval=0.4) 
    
    if texto != '':
        pyautogui.write(str(texto), interval=0.05)

def copiar_valor_seguro():
    """
    Copia valores do grid garantindo que a área de transferência foi atualizada.
    """
    pyperclip.copy("") 
    pyautogui.doubleClick()
    time.sleep(0.2) 
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    return pyperclip.paste().strip()

def salvar_com_confirmacao():
    print("   💾 Salvando registro...")
    clique_longo(COORD_BTN_GRAVAR)
    time.sleep(1.0)
    clique_longo(COORD_POPUP_SIM) 
    time.sleep(0.3)

# --- FLUXO PRINCIPAL ---
def automacao_final():
    print("\n🚀 ROBÔ INICIADO: MODO DE RECLASSIFICAÇÃO")
    print("Atenção: Mude para a tela remota em 5 segundos...")
    winsound.Beep(1000, 200)
    time.sleep(5)

    contador_sucesso = 0

    while True:
        try:
            print(f"\n--- Ciclo {contador_sucesso + 1} ---")

            # 1. FILTRAGEM
            pyautogui.click(COORD_FILTRO_HIST)
            limpar_e_escrever_seguro(HISTORICO_BUSCA) 
            
            clique_longo(COORD_BTN_LISTAR)
            time.sleep(1.5) 
            
            # 2. CAPTURA DO VALOR ALVO
            pyautogui.click(COORD_LANC_VALOR) 
            valor_copiado = copiar_valor_seguro()
            
            if not valor_copiado:
                print("🏁 Lista vazia ou fim do processo.")
                winsound.Beep(500, 1000)
                break

            print(f"   💰 Valor em processamento: {valor_copiado}")
            
            pyautogui.click(COORD_BTN_CANCELAR)
            time.sleep(1.0)
            
            # 3. ISOLAMENTO DO LANÇAMENTO (RE-FILTRO)
            pyautogui.click(COORD_FILTRO_VALOR)
            limpar_e_escrever_seguro(valor_copiado)
            
            pyautogui.click(COORD_FILTRO_HIST)
            limpar_e_escrever_seguro('') 
            
            clique_longo(COORD_BTN_LISTAR)
            time.sleep(1.5)
            
            # 4. ANÁLISE DE CENÁRIO (TRIAGEM)
            print("   🔍 Analisando estrutura do lançamento...")
            clique_longo(COORD_GRID_LINHA_1)
            pyautogui.click(COORD_LANC_DEBITAR)
            debito_1 = copiar_valor_seguro()
   
            pyautogui.click(COORD_BTN_CANCELAR)
            time.sleep(0.8)

            clique_longo(COORD_GRID_LINHA_2)
            pyautogui.click(COORD_LANC_DEBITAR)
            debito_2 = copiar_valor_seguro()

            pyautogui.click(COORD_BTN_CANCELAR)
            time.sleep(0.8)
            
            sao_iguais = (debito_1 == debito_2)
            
            # 5. EXECUÇÃO DA CORREÇÃO
            if not sao_iguais:
                # CENÁRIO A: CORREÇÃO DE FILIAL
                print(f"   📊 Cenário Identificado: Múltiplo (Filial)")
                filial_capturada = None
                
                # Identifica qual linha possui a conta incorreta (20001)
                if debito_1 == CONTA_FORNECEDOR:
                    print("   -> Editando Linha 1...")
                    clique_longo(COORD_GRID_LINHA_1)
                    
                    pyautogui.click(COORD_LANC_DEBITAR)
                    limpar_e_escrever_seguro(CONTA_MATRIZ) # Conta Matriz
                    pyautogui.press('tab') 
                    time.sleep(0.5)
                    
                    pyautogui.click(COORD_LANC_FILIAL)
                    filial_capturada = copiar_valor_seguro()
                    salvar_com_confirmacao()
                    
                elif debito_2 == CONTA_FORNECEDOR:
                    print("   -> Editando Linha 2...")
                    clique_longo(COORD_GRID_LINHA_2)
                    
                    pyautogui.click(COORD_LANC_DEBITAR)
                    limpar_e_escrever_seguro(CONTA_MATRIZ) # Conta Matriz
                    pyautogui.press('tab') 
                    time.sleep(0.05)
                    
                    pyautogui.click(COORD_LANC_FILIAL)
                    filial_capturada = copiar_valor_seguro()
                    salvar_com_confirmacao()
                
                # Ajuste do Banco baseado na Filial
                if filial_capturada:
                    print(f"   -> Filial {filial_capturada} detectada. Ajustando Banco...")
                    clique_longo(COORD_GRID_LINHA_1)
                    time.sleep(0.5)
                    
                    novo_credito = tabela_filiais.get(filial_capturada)
                    if novo_credito:
                        pyautogui.click(COORD_LANC_CREDITAR)
                        limpar_e_escrever_seguro(novo_credito)
                        pyautogui.press('tab')
                        time.sleep(0.5)
                        salvar_com_confirmacao()

            else:
                # CENÁRIO B: LANÇAMENTO ÚNICO (CAIXA)
                print(f"   📊 Cenário Identificado: Único (Caixa)")
                clique_longo(COORD_GRID_LINHA_1)
                
                print("   -> Ajustando para Conta 1...")
                pyautogui.click(COORD_LANC_CREDITAR) 
                limpar_e_escrever_seguro(CAIXA_CONTA)
                pyautogui.press('tab')
                time.sleep(0.5)
                salvar_com_confirmacao()

            # FINALIZA CICLO
            pyautogui.click(COORD_FILTRO_VALOR)
            limpar_e_escrever_seguro('')
            
            contador_sucesso += 1
            print(f"✅ Sucesso! Ciclos concluídos: {contador_sucesso}")
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            break

if __name__ == "__main__":
    automacao_final()