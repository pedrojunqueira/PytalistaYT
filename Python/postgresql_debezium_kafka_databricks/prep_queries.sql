-- create database kafka_cdc;

-- ALTER ROLE pedrojunqueira WITH REPLICATION;

CREATE TABLE basic (id INTEGER NOT NULL PRIMARY KEY, fruit TEXT);
INSERT INTO basic VALUES (1, 'apple');
INSERT INTO basic VALUES (2, 'banana');

SELECT * from basic

-- ALTER TABLE basic REPLICA IDENTITY FULL;

INSERT INTO basic VALUES (3, 'mandarin');
INSERT INTO basic VALUES (4, 'pineapple');

INSERT INTO basic VALUES (5, 'raspberry');
INSERT INTO basic VALUES (6, 'morango');

-- CREATE PUBLICATION pub FOR TABLE basic;

select * from basic;

delete from basic where id = 2;

UPDATE basic set fruit = 'strawberry' where id = 6
UPDATE basic set fruit = 'framboesa' where id = 5

delete from basic where id = 6;

-- ALTER TABLE basic REPLICA IDENTITY FULL