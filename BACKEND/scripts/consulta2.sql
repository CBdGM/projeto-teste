-- Mapear automaticamente os últimos trimestres
WITH trimestres_ordenados AS (
    SELECT 
        DISTINCT trimestre,
        CAST(SUBSTRING(trimestre FROM 3 FOR 4) AS INTEGER) AS ano,
        CAST(SUBSTRING(trimestre FROM 1 FOR 1) AS INTEGER) AS numero_trimestre
    FROM demonstrativos
),
ultimos_trimestres AS (
    SELECT trimestre
    FROM trimestres_ordenados
    ORDER BY ano DESC, numero_trimestre DESC
    LIMIT 4
)
-- Contulta 2: 10 operadoras com maiores despesas nessa categoria no último ano
SELECT 
    o.registro_ans,
    o.razao_social,
    SUM(d.valor) AS total_despesa
FROM demonstrativos d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.trimestre IN (SELECT trimestre FROM ultimos_trimestres)
  AND d.conta ILIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS%'
GROUP BY o.registro_ans, o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;
