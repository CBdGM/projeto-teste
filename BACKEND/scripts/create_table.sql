-- Cria a tabela de operadoras
CREATE TABLE operadoras (
    registro_ans VARCHAR PRIMARY KEY,
    razao_social TEXT,
    nome_fantasia TEXT,
    cnpj VARCHAR,
    modalidade TEXT,
    uf TEXT,
    municipio TEXT,
    data_registro DATE
);

-- Cria a tabela de demonstrativos financeiros por trimestre
CREATE TABLE demonstrativos (
    id SERIAL PRIMARY KEY,
    trimestre VARCHAR,
    registro_ans VARCHAR REFERENCES operadoras(registro_ans),
    conta TEXT,
    valor NUMERIC
);
