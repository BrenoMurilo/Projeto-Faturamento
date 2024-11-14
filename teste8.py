caminho_arquivo = r"C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\Planilhas de faturamento\Faturamento - GPA - 12.11.2024.xlsx"

# Abre o arquivo no modo binário e lê seu conteúdo
with open(caminho_arquivo, "rb") as arquivo:
    conteudo_binario = arquivo.read()
    print(conteudo_binario)
