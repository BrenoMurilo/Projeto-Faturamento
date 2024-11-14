from Drivers.Documents_Drivers.Excel import Excel


wb = Excel(r"C:\Users\breno\Downloads\Parâmetros.xlsx")
dict = wb.Gerar_Dicionario_de_Grupos_de_Colunas('Parâmetros',
            r'C:\Users\breno\OneDrive\Documentos\Projeto Faturamento\Config_Parâmetros.json', True, True)
print(dict)