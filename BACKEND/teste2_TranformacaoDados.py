import os
import pdfplumber
import pandas as pd
import zipfile

# Configurações
PDF_FILE = os.path.join("downloads", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
CSV_FILE = "rol_procedimentos.csv"
ZIP_FILE = "Teste_CaioMontenegro.zip"

def extract_tables(file_path):
    """Extrai e limpa as tabelas do PDF."""
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                # Remove linhas vazias
                clean = [row for row in table if any((cell or "").strip() for cell in row)]
                if clean:
                    tables.append(clean)
    return tables

def combine_tables(tables):
    """Usa a primeira linha da primeira tabela como cabeçalho e junta os dados."""
    if not tables:
        print("Nenhuma tabela encontrada.")
        return None
    header = tables[0][0]
    rows = []
    for table in tables:
        if table[0] == header:
            rows.extend(table[1:])
        else:
            rows.extend(table)
    df = pd.DataFrame(rows, columns=header)
    df.dropna(how="all", inplace=True)
    return df

def rename_columns(df):
    """Renomeia 'OD' para 'Seg. Odontológica' e 'AMB' para 'Seg. Ambulatorial'."""
    mapping = {}
    for col in df.columns:
        if col.strip().upper() == "OD":
            mapping[col] = "Seg. Odontológica"
        elif col.strip().upper() == "AMB":
            mapping[col] = "Seg. Ambulatorial"
    df.rename(columns=mapping, inplace=True)
    return df

def save_csv(df, csv_file):
    """Salva o DataFrame em CSV."""
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print("CSV salvo em", csv_file)

def zip_csv(csv_file, zip_file):
    """Compacta o CSV em um arquivo ZIP."""
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(csv_file, arcname=os.path.basename(csv_file))
    print("CSV compactado em", zip_file)

def main():
    print("Extraindo tabelas do PDF...")
    tables = extract_tables(PDF_FILE)
    df = combine_tables(tables)
    if df is None:
        return
    df = rename_columns(df)
    print("Colunas:", df.columns.tolist())
    save_csv(df, CSV_FILE)
    zip_csv(CSV_FILE, ZIP_FILE)

if __name__ == "__main__":
    main()
