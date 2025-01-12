-- Script para apagar todas as tabelas e suas constraints

-- Desabilitar verificação de chave estrangeira temporariamente
SET FOREIGN_KEY_CHECKS = 0;

-- Apagar tabelas
DROP TABLE IF EXISTS mc_fiap.F_PEDIDOS;
DROP TABLE IF EXISTS mc_fiap.D_ESTOQUE;
DROP TABLE IF EXISTS mc_fiap.D_PRODUTO;
DROP TABLE IF EXISTS mc_fiap.D_FORNECEDOR;
DROP TABLE IF EXISTS mc_fiap.D_CENTRODISTRIBUICAO;
DROP TABLE IF EXISTS mc_fiap.D_MUNICIPIO;
DROP TABLE IF EXISTS mc_fiap.D_UF;

-- Restaurar verificação de chave estrangeira
SET FOREIGN_KEY_CHECKS = 1;
