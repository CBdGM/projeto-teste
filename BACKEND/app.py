from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  

load_dotenv()

db_url = os.getenv("DATABASE_URL")

# Carrega os dados no início
df = pd.read_csv("dados/Relatorio_cadop.csv", sep=";", encoding="latin1")
df = df.applymap(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)

# Renomeia as colunas
df = df.rename(columns={
    "Registro_ANS": "registro_ans",
    "Razao_Social": "razao_social",
    "Nome_Fantasia": "nome_fantasia",
    "CNPJ": "cnpj",
    "Modalidade": "modalidade",
    "UF": "uf",
    "Cidade": "municipio",
    "Data_Registro_ANS": "data_registro"
})
print(df.columns.tolist())

# Rota de busca
@app.route("/busca", methods=["GET"])
def buscar_operadoras():
    termo = request.args.get("q", "").lower()
    if not termo:
        return jsonify([])

    resultado = df[df["razao_social"].str.lower().str.contains(termo) |
                   df["nome_fantasia"].str.lower().str.contains(termo)]

    # Converter os NaN para None (incluindo colunas numéricas)
    resultado = resultado.fillna(np.nan).replace([np.nan], [None])  
    return jsonify(resultado.head(20).to_dict(orient="records"))
if __name__ == "__main__":
    app.run(debug=True)
