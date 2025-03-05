-- Ler a Temperatura e Umidade
SELECT 
    datetime AS "time", 
    MAX((value->>'value')::NUMERIC) FILTER (WHERE "point" = 'TmpAmb') AS "Temperatura",
    MAX((value->>'value')::NUMERIC) FILTER (WHERE "point" = 'RH') AS "Umidade"
FROM environmental_data
WHERE 
    "point" IN ('TmpAmb', 'RH')
    AND datetime > (${__from} / 1000) 
    AND datetime < (${__to} / 1000)
GROUP BY datetime
ORDER BY datetime;
