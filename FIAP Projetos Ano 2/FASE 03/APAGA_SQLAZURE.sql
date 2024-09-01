-- Desativa as verificações de chave estrangeira temporariamente
DECLARE @disableConstraints NVARCHAR(MAX) = '';

SELECT @disableConstraints = @disableConstraints + 'ALTER TABLE ' + QUOTENAME(table_name) + ' NOCHECK CONSTRAINT ALL;' + CHAR(13)
FROM information_schema.tables
WHERE table_schema = 'melhorescomprasfiapfase03';

EXEC sp_executesql @disableConstraints;

-- Exclui as tabelas, se existirem
DECLARE @tableName NVARCHAR(MAX);

DECLARE tableCursor CURSOR FOR
SELECT QUOTENAME(table_name) 
FROM information_schema.tables 
WHERE table_schema = 'melhorescomprasfiapfase03'; 

OPEN tableCursor;
FETCH NEXT FROM tableCursor INTO @tableName;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC('DROP TABLE IF EXISTS ' + @tableName);
    FETCH NEXT FROM tableCursor INTO @tableName;
END;

CLOSE tableCursor;
DEALLOCATE tableCursor;

-- Reactiva as verificações de chave estrangeira
DECLARE @enableConstraints NVARCHAR(MAX) = '';

SELECT @enableConstraints = @enableConstraints + 'ALTER TABLE ' + QUOTENAME(table_name) + ' WITH CHECK CHECK CONSTRAINT ALL;' + CHAR(13)
FROM information_schema.tables
WHERE table_schema = 'melhorescomprasfiapfase03';
EXEC sp_executesql @enableConstraints;
