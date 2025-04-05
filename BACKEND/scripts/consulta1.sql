-- Corrige a descrição corrompida no campo 'conta'
UPDATE demonstrativos
SET conta = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE MÉDICO HOSPITALAR'
WHERE conta = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÃNCIA A SAÃDE MEDICO HOSPITALAR';
-- Consulta 1 10 operadoras com maiores despesas em EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR
SELECT 
    o.registro_ans,
    o.razao_social,
    SUM(d.valor) AS total_despesa
FROM demonstrativos d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.trimestre = (
    SELECT MAX(trimestre)
    FROM demonstrativos
    WHERE conta ILIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS%'
)
AND d.conta ILIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS%'
GROUP BY o.registro_ans, o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;
