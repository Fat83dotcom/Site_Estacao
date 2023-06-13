-- Active: 1686355749375@@129.148.57.149@5432@dados_estacao

select current_database();

create database dados_estacao;

create table
    dado_diario (
        codigo serial not null primary key,
        dia timestamp not null unique,
        media_umidade double precision not null,
        minimo_umidade double precision not null,
        maximo_umidade double precision not null,
        mediana_umidade double precision not null,
        moda_umidade double precision not null,
        media_pressao double precision not null,
        minimo_pressao double precision not null,
        maximo_pressao double precision not null,
        mediana_pressao double precision not null,
        moda_pressao double precision not null,
        media_temp_int double precision not null,
        minimo_temp_int double precision not null,
        maximo_temp_int double precision not null,
        mediana_temp_int double precision not null,
        moda_temp_int double precision not null,
        media_temp_ext double precision not null,
        minimo_temp_ext double precision not null,
        maximo_temp_ext double precision not null,
        mediana_temp_ext double precision not null,
        moda_temp_ext double precision not null
    );

CREATE OR REPLACE VIEW MEDIAS_DIARIAS 
	as
	select
	    dia,
	    media_umidade,
	    media_pressao,
	    media_temp_int,
	    media_temp_ext
	from dado_diario
; 

CREATE OR REPLACE VIEW MEDIAS_MIN_MAX_TEMP 
	as
	select
	    dia,
	    media_temp_int,
	    minimo_temp_int,
	    maximo_temp_int,
	    media_temp_ext,
	    minimo_temp_ext,
	    maximo_temp_ext
	from
DADO_DIARIO; 

CREATE OR REPLACE VIEW MINIMAS_TOTAIS 
	as
	select
	    codigo,
	    dia,
	    minimo_umidade,
	    minimo_pressao,
	    minimo_temp_int,
	    minimo_temp_ext
	from dado_diario
	order by dia
DESC; 

CREATE OR REPLACE VIEW MAXIMAS_TOTAIS as
	select
	    codigo,
	    dia,
	    maximo_umidade,
	    maximo_pressao,
	    maximo_temp_int,
	    maximo_temp_ext
	from dado_diario
	order by dia
DESC; 

CREATE OR REPLACE VIEW MEDIANAS_TOTAIS 
	as
	select
	    codigo,
	    dia,
	    mediana_umidade,
	    mediana_pressao,
	    mediana_temp_int,
	    mediana_temp_ext
	from dado_diario
	order by dia
DESC; 

CREATE OR REPLACE VIEW MODAS_TOTAIS 
	as
	select
	    codigo,
	    dia,
	    moda_umidade,
	    moda_pressao,
	    moda_temp_int,
	    moda_temp_ext
	from dado_diario
	order by dia
DESC; 

CREATE OR REPLACE VIEW MEDIAS_TOTAIS 
	as
	select
	    codigo,
	    dia,
	    media_umidade,
	    media_pressao,
	    media_temp_int,
	    media_temp_ext
	from dado_diario
	order by dia
DESC; 

CREATE OR REPLACE VIEW label_datas AS
SELECT codigo, dia FROM dado_diario
ORDER BY dia DESC;

SELECT dia, maximo_umidade FROM dado_diario
WHERE maximo_umidade = (SELECT MAX(maximo_umidade) FROM dado_diario)
AND
EXTRACT(YEAR FROM(SELECT dia))='2023' 
ORDER BY dia DESC;

SELECT dia, minimo_umidade FROM dado_diario
WHERE minimo_umidade = (SELECT MAX(minimo_umidade) FROM dado_diario)
AND
EXTRACT(YEAR FROM(SELECT dia))='2023';

SELECT dia, maximo_temp_ext FROM dado_diario
WHERE maximo_temp_ext = (SELECT MAX(maximo_temp_ext) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023')
AND
EXTRACT(YEAR FROM(SELECT dia))='2023' 
ORDER BY dia DESC;

SELECT dia, minimo_temp_ext FROM dado_diario
WHERE minimo_temp_ext = 
(SELECT MIN(minimo_temp_ext) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023')
AND
EXTRACT(YEAR FROM(SELECT dia))='2023' 

ORDER BY dia DESC;SELECT dia, maximo_pressao FROM dado_diario
WHERE maximo_pressao = (SELECT MAX(maximo_pressao) FROM dado_diario)
AND
EXTRACT(YEAR FROM(SELECT dia))='2023' 
ORDER BY dia DESC;

SELECT dia, minimo_pressao FROM dado_diario
WHERE minimo_pressao = (SELECT MAX(minimo_pressao) FROM dado_diario)
AND
EXTRACT(YEAR FROM(SELECT dia))='2023' 
ORDER BY dia DESC;

SELECT AVG(media_temp_ext) FROM
dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023';
SELECT AVG(media_umidade) FROM
dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023';
SELECT AVG(media_pressao) FROM
dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023';

select * from maximas_totais;

-- drop view medias_totais;

select minimo_pressao
from medias_diarias
where
    dia between '2022-1-1' and '2022-12-31'
    -- and media_temp_int <= 28
order by dia;

select *
from medias_min_max_temp
where
    dia between '2023-1-1' and '2023-6-2'
    and minimo_temp_int <= 20
order by dia;

select min(minimo_temp_int) from medias_min_max_temp;

select * from dado_diario where maximo_temp_int >= 60;

select * from dado_diario where dia BETWEEN '2022-01-01' AND '2022-04-01';

-- truncate table dado_diario;

-- drop table dado_diario cascade;

show datastyle;

SELECT 0 AS id, AVG(maximo_umidade) FROM
dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))='2023';