-- Desativa as verificações de chave estrangeira temporariamente
SET FOREIGN_KEY_CHECKS = 0;

-- Variável para armazenar o nome das tabelas
SET @tables = NULL;

-- Consulta para obter uma lista de todas as tabelas no banco de dados específico
SELECT GROUP_CONCAT(table_name) INTO @tables
FROM information_schema.tables
WHERE table_schema = 'mc_fiap'; -- Substitua 'mc_fiap' pelo nome do seu banco de dados

-- Consulta para excluir todas as tabelas listadas na variável @tables
SET @drop_query = CONCAT('DROP TABLE IF EXISTS ', @tables);
PREPARE stmt FROM @drop_query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Reactiva as verificações de chave estrangeira
SET FOREIGN_KEY_CHECKS = 1;
