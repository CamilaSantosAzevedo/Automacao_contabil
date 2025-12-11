import pyautogui
import time
import winsound # Biblioteca nativa do Windows para fazer BEEP

# Lista ATUALIZADA com o aviso de conciliação
itens_para_mapear = [
    "1. Filtro CONTA (Onde digita 20001)",
    "2. Filtro HISTORICO (Onde digita mendon)",
    "3. Filtro VALOR (Campo lá em cima)",
    "4. Botão LISTAR",
    "5. GRID LINHA 1 (Onde clica no 1º resultado)",
    "6. GRID LINHA 2 (Logo abaixo do 1º resultado)",
    "7. Edição: Campo VALOR (Lá embaixo)",
    "8. Edição: Campo DEBITAR",
    "9. Edição: Campo CREDITAR",
    "10. Edição: Campo FILIAL",
    "11. Botão GRAVAR",
    "12. Botão CANCELAR / LISTAGEM",
    "13. Aviso Pop-up: Botão SIM (O aviso de conciliação)" 
]

input("🔊 Aumente o volume! Pressione ENTER para começar...")

coordenadas_finais = {}

print("\n--- INICIANDO EM 3 SEGUNDOS ---")
time.sleep(3)

for item in itens_para_mapear:
    print("\n" + "="*40)
    print(f"👉 PRÓXIMO ALVO: {item}")
    print("="*40)
    
    # Contagem Regressiva de 10 segundos
    for i in range(10, 0, -1):
        print(f"⏳ Capturando em: {i} segundos...   ", end='\r') # O \r faz atualizar na mesma linha
        
        # Faz BEEP nos últimos 3 segundos para te avisar
        if i <= 3:
            winsound.Beep(2500, 100) # (Frequência, Duração)
            
        time.sleep(1)
    
    # MOMENTO DA CAPTURA
    x, y = pyautogui.position()
    winsound.Beep(1000, 500) # Bip grave e longo confirmando captura
    
    print(f"✅ CAPTURADO: X={x}, Y={y}                      ") # Espaços para limpar a linha
    coordenadas_finais[item] = (x, y)
    
    time.sleep(0.5)

print("\n" + "="*30)
print("   RELATÓRIO FINAL (COPIE AQUI)")
print("="*30)

# Imprime formatado para ser copiado e colado diretamente no código
print(f"COORD_FILTRO_CONTA  = {coordenadas_finais[itens_para_mapear[0]]}")
print(f"COORD_FILTRO_HIST   = {coordenadas_finais[itens_para_mapear[1]]}")
print(f"COORD_FILTRO_VALOR  = {coordenadas_finais[itens_para_mapear[2]]}")
print(f"COORD_BTN_LISTAR    = {coordenadas_finais[itens_para_mapear[3]]}")
print(f"COORD_GRID_LINHA_1  = {coordenadas_finais[itens_para_mapear[4]]}")
print(f"COORD_GRID_LINHA_2  = {coordenadas_finais[itens_para_mapear[5]]}")
print(f"COORD_LANC_VALOR    = {coordenadas_finais[itens_para_mapear[6]]}")
print(f"COORD_LANC_DEBITAR  = {coordenadas_finais[itens_para_mapear[7]]}")
print(f"COORD_LANC_CREDITAR = {coordenadas_finais[itens_para_mapear[8]]}")
print(f"COORD_LANC_FILIAL   = {coordenadas_finais[itens_para_mapear[9]]}")
print(f"COORD_BTN_GRAVAR    = {coordenadas_finais[itens_para_mapear[10]]}")
print(f"COORD_BTN_CANCELAR  = {coordenadas_finais[itens_para_mapear[11]]}")
print(f"COORD_POPUP_SIM     = {coordenadas_finais[itens_para_mapear[12]]}")