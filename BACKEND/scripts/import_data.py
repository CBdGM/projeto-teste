import os
import pandas as pd
import psycopg2

# Conexão com o banco
conn = psycopg2.connect(
    dbname="ans_db",
    user="postgres",
    password="senha",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Caminho da pasta com os arquivos
DATA_DIR = "dados"

# === Importar os dados cadastrais das operadoras ===
cadop_path = os.path.join(DATA_DIR, "Relatorio_cadop.csv")
cadop = pd.read_csv(cadop_path, sep=";", encoding="latin1")
cadop.columns = [col.strip() for col in cadop.columns]

cadop = cadop.rename(columns={
    "Registro_ANS": "registro_ans",
    "Razao_Social": "razao_social",
    "Nome_Fantasia": "nome_fantasia",
    "CNPJ": "cnpj",
    "Modalidade": "modalidade",
    "UF": "uf",
    "Cidade": "municipio",
    "Data_Registro_ANS": "data_registro"
})

cadop["data_registro"] = pd.to_datetime(cadop["data_registro"], errors="coerce")

for _, row in cadop.iterrows():
    try:
        cursor.execute("""
            INSERT INTO operadoras (registro_ans, razao_social, nome_fantasia, cnpj, modalidade, uf, municipio, data_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (registro_ans) DO NOTHING;
        """, tuple(row))
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir operadora {row['registro_ans']}: {e}")
    else:
        conn.commit()

print("Dados das operadoras inseridos.")

#Identificar colunas mesmo com nomes diferentes
def get_coluna(df, alternativas):
    for nome in alternativas:
        if nome in df.columns:
            return nome
    return None

# Possíveis nomes das colunas nos arquivos
colunas = {
    "registro_ans": ["Registro ANS", "REG_ANS"],
    "conta": ["Conta Contábil", "CD_CONTA_CONTABIL"],
    "valor": ["Valor", "VL_SALDO_INICIAL", "VL_SALDO_FINAL"]
}

# Importar os demonstrativos contábeis 
arquivos = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv") and f != "Relatorio_cadop.csv"]

for arquivo in arquivos:
    trimestre = arquivo.replace(".csv", "").upper()
    df = pd.read_csv(os.path.join(DATA_DIR, arquivo), sep=";", encoding="latin1")

    col_registro = get_coluna(df, colunas["registro_ans"])
    col_conta = get_coluna(df, colunas["conta"])
    col_valor = get_coluna(df, colunas["valor"])

    if not all([col_registro, col_conta, col_valor]):
        print(f"Colunas não encontradas em {arquivo}. Ignorando arquivo.")
        continue

    for _, row in df.iterrows():
        try:
            registro = str(row.get(col_registro, "")).strip()

            conta_raw = str(row.get(col_conta, "")).strip()
            try:
                conta = conta_raw.encode("latin1").decode("utf-8")
            except UnicodeDecodeError:
                conta = conta_raw

            valor_raw = str(row.get(col_valor, "0")).replace("R$", "").replace(".", "").replace(",", ".").strip()
            valor = float(valor_raw) if valor_raw else 0.0

            if not registro:
                continue

            cursor.execute("SELECT 1 FROM operadoras WHERE registro_ans = %s", (registro,))
            if cursor.fetchone() is None:
                print(f"Operadora {registro} não encontrada. Pulando.")
                continue

            cursor.execute("""
                INSERT INTO demonstrativos (trimestre, registro_ans, conta, valor)
                VALUES (%s, %s, %s, %s)
            """, (trimestre, registro, conta, valor))

        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir demonstrativo (registro {registro}): {e}")
        else:
            conn.commit()

cursor.close()
conn.close()
print("Importação finalizada com sucesso.")
