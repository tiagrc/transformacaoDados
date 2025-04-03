import pdfplumber
import pandas as pd
import zipfile
import os

# Nome do usuário para personalizar o arquivo zip
usuario_nome = "tiago"

# Caminho do arquivo PDF
pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

# Lista para armazenar os dados extraídos
dados_tabela = []

# Mapeamento das abreviações para suas descrições completas
substituicoes = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

# Extração dos dados


def extrair_tabelas(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tabela = page.extract_table()
            if tabela:
                dados_tabela.extend(tabela[1:])  # Ignora cabeçalho repetido


extrair_tabelas(pdf_path)

# Criar DataFrame
df = pd.DataFrame(dados_tabela)

# Substituir abreviações
if not df.empty:
    df = df.applymap(lambda x: substituicoes.get(x, x))

# Caminhos dos arquivos
csv_filename = "Teste_Tiago.csv"
zip_filename = "Teste_Tiago.zip"

# Salvar CSV
df.to_csv(csv_filename, index=False, header=False, encoding='utf-8')

# Compactar em ZIP
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename)

# Remover o CSV após compactação
os.remove(csv_filename)

print(f"Processo concluído. Arquivo salvo como {zip_filename}")
