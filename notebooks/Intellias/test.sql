DROP TABLE clientes
CREATE TABLE clientes (
    id INT
    ,nome VARCHAR(100)
    ,idade INT
);

INSERT INTO clientes (id, nome, idade)
VALUES
    (1,'Rafael', 10)
    ,(2,'Maria', 18)
    ,(3,'Ana', 32)
    ,(4,'Rafael', 35);

SHOW TABLES;

DROP TABLE geracao
CREATE TABLE geracao (
    start_date date
    ,end_date date
    ,nome_geracao VARCHAR(100)
);

INSERT INTO geracao (start_date, end_date, nome_geracao)
VALUES
    ('1990-01-01','2000-01-01', 'adulto')
    ,('2000-01-01','2015-01-01', 'jovem')
    ,('2015-01-01','2030-01-01', 'crianca');

SELECT
*
FROM clientes

SELECT
*
,DATE_DIFF('year', start_date, CURRENT_DATE) as top_old
,DATE_DIFF('year', end_date, CURRENT_DATE) as bottom_old
FROM geracao

SELECT
c.id
,c.nome
,c.idade
,g.nome_geracao
FROM clientes c
LEFT JOIN (
    SELECT
    *
    ,DATE_DIFF('year', start_date, CURRENT_DATE) as top_old
    ,DATE_DIFF('year', end_date, CURRENT_DATE) as bottom_old
    FROM geracao
) g ON (c.idade > g.bottom_old AND c.idade < g.top_old)

-- Storing the table
CREATE OR REPLACE VIEW test_data AS
SELECT *
FROM read_csv_auto('notebooks/Intellias/test_data.csv');

SELECT
*
,LEFT(nome,3) as esquerda
,RIGHT(nome, 3) as direita
FROM test_data