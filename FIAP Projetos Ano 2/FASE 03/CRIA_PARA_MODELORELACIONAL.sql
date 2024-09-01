CREATE TABLE dim_mc_regiao (
    sk_regiao INT NOT NULL,
    nm_regiao VARCHAR(25) NOT NULL,
    PRIMARY KEY (sk_regiao)
);

CREATE TABLE dim_mc_estado (
    sk_estado               INT NOT NULL,
    dim_mc_regiao_sk_regiao INT NOT NULL,
    sg_estado               CHAR(2) NOT NULL,
    nm_estado               VARCHAR(25) NOT NULL,
    nm_gentilico            VARCHAR(40) NOT NULL,
    PRIMARY KEY (sk_estado),
    CONSTRAINT fk_mc_dim_regiao_estado FOREIGN KEY (dim_mc_regiao_sk_regiao) REFERENCES dim_mc_regiao (sk_regiao)
);

CREATE TABLE dim_mc_cliente (
    sk_cliente    INT NOT NULL,
    nm_cliente    VARCHAR(60) NOT NULL,
    nr_estrelas   INT(1),
    st_cliente    VARCHAR(8) NOT NULL,
    dt_nascimento DATE,
    PRIMARY KEY (sk_cliente)
);

CREATE TABLE dim_mc_funcionario (
    sk_funcionario INT NOT NULL,
    nm_funcionario VARCHAR(60) NOT NULL,
    ds_cargo       VARCHAR(50) NOT NULL,
    PRIMARY KEY (sk_funcionario)
);

CREATE TABLE dim_mc_tempo (
    sk_mc_tempo               INT NOT NULL,
    nr_ano                    INT,
    nr_semestre               INT,
    ds_semestre_ano           VARCHAR(20),
    ds_semestre               VARCHAR(15),
    nr_trimestre              INT,
    ds_trimestre_ano          VARCHAR(20),
    ds_trimestre              VARCHAR(15),
    nr_mes                    INT,
    nr_ano_mes                INT,
    ds_mes_ano                VARCHAR(15),
    ds_mes                    VARCHAR(15),
    ds_abv_mes                CHAR(3),
    ds_abv_mes_ano            VARCHAR(15),
    ds_dia_semana             VARCHAR(15),
    ds_data                   VARCHAR(30),
    nr_dia_mes                INT,
    nr_dia_semana             INT,
    nr_dia_ano                INT,
    ds_dia_util_feriado       VARCHAR(15),
    ds_fim_semana             VARCHAR(15),
    ds_data_extenso           VARCHAR(50),
    dt_criacao_rgt            DATE,
    PRIMARY KEY (sk_mc_tempo)
);

CREATE TABLE dim_mc_categoria_prod (
    sk_categoria_prod      INT NOT NULL,
    nm_categoria_prod      VARCHAR(60) NOT NULL,
    st_categoria           VARCHAR(8) NOT NULL,
    qt_nota_categoria_prod INT(2),
    PRIMARY KEY (sk_categoria_prod)
);

CREATE TABLE dim_mc_sub_categoria_prod (
    sk_sub_categoria_prod                   INT NOT NULL,
    dim_mc_categoria_prod_sk_categoria_prod INT NOT NULL,
    nm_sub_categoria_prod                   VARCHAR(60) NOT NULL,
    st_sub_categoria                        VARCHAR(8) NOT NULL,
    qt_nota_sub_categoria_prod              INT(2),
    PRIMARY KEY (sk_sub_categoria_prod),
    CONSTRAINT fk_mc_dim_subcateg_categ FOREIGN KEY (dim_mc_categoria_prod_sk_categoria_prod) REFERENCES dim_mc_categoria_prod (sk_categoria_prod)
);

CREATE TABLE dim_mc_produto (
    sk_produto                        INT NOT NULL,
    dim_mc_sub_categoria_prod_sk_sub_categoria_prod INT NOT NULL,
    nm_produto                        VARCHAR(90) NOT NULL,
    nm_tipo_embalagem                 VARCHAR(60) NOT NULL,
    PRIMARY KEY (sk_produto),
    CONSTRAINT fk_mc_dim_categ_prod FOREIGN KEY (dim_mc_sub_categoria_prod_sk_sub_categoria_prod) REFERENCES dim_mc_sub_categoria_prod (sk_sub_categoria_prod)
);

CREATE TABLE dim_mc_centro_distribuicao (
    sk_centro_distribuicao INT NOT NULL,
    nm_centro_distribuicao VARCHAR(60) NOT NULL,
    PRIMARY KEY (sk_centro_distribuicao)
);

CREATE TABLE dim_mc_cidade (
    sk_cidade               INT NOT NULL,
    dim_mc_estado_sk_estado INT NOT NULL,
    nm_cidade               VARCHAR(25) NOT NULL,
    nr_populacao            INT(10),
    cd_ibge                 INT(8),
    nr_altitude_mar         INT(8),
    PRIMARY KEY (sk_cidade),
    CONSTRAINT fk_mc_dim_estado_cidade FOREIGN KEY (dim_mc_estado_sk_estado) REFERENCES dim_mc_estado (sk_estado)
);

CREATE TABLE dim_mc_bairro (
    sk_bairro               INT NOT NULL,
    dim_mc_cidade_sk_cidade INT NOT NULL,
    nm_bairro               VARCHAR(25) NOT NULL,
    nr_populacao            INT(10),
    nr_nivel_seguranca      INT(1),
    PRIMARY KEY (sk_bairro),
    CONSTRAINT fk_mc_dim_cidade_bairro FOREIGN KEY (dim_mc_cidade_sk_cidade) REFERENCES dim_mc_cidade (sk_cidade)
);

CREATE TABLE dim_mc_pedido_venda (
    sk_pedido_venda       INT NOT NULL,
    nr_pedido_origem      INT NOT NULL,
    nr_item_pedido_origem INT NOT NULL,
    PRIMARY KEY (sk_pedido_venda)
);

CREATE TABLE dim_mc_forma_pagto (
    sk_forma_pagto INT NOT NULL,
    ds_forma_pagto VARCHAR(35) NOT NULL,
    PRIMARY KEY (sk_forma_pagto)
);

CREATE TABLE dim_mc_origem_vda (
    sk_origem_vda INT NOT NULL,
    ds_origem_vda VARCHAR(30) NOT NULL,
    PRIMARY KEY (sk_origem_vda)
);

CREATE TABLE dim_mc_status_venda (
    sk_status_venda INT NOT NULL,
    ds_status_venda VARCHAR(40) NOT NULL,
    PRIMARY KEY (sk_status_venda)
);

CREATE TABLE dim_mc_tipo_venda (
    sk_tipo_venda INT NOT NULL,
    ds_tipo_venda  VARCHAR(30) NOT NULL,
    PRIMARY KEY (sk_tipo_venda)
);

CREATE TABLE dim_mc_colecao_status (
    sk_colecao_status INT NOT NULL AUTO_INCREMENT,
    sk_forma_pagto    INT NOT NULL,
    sk_origem_vda     INT NOT NULL,
    sk_status_venda   INT NOT NULL,
    sk_tipo_venda     INT NOT NULL,
    PRIMARY KEY (sk_colecao_status),
    CONSTRAINT fk_dim_mc_colecao_status_forma_pagto FOREIGN KEY (sk_forma_pagto) REFERENCES dim_mc_forma_pagto (sk_forma_pagto),
    CONSTRAINT fk_dim_mc_colecao_status_origem_vda FOREIGN KEY (sk_origem_vda) REFERENCES dim_mc_origem_vda (sk_origem_vda),
    CONSTRAINT fk_dim_mc_colecao_status_status_venda FOREIGN KEY (sk_status_venda) REFERENCES dim_mc_status_venda (sk_status_venda),
    CONSTRAINT fk_dim_mc_colecao_status_tipo_venda FOREIGN KEY (sk_tipo_venda) REFERENCES dim_mc_tipo_venda (sk_tipo_venda)
);

CREATE TABLE fto_entrega_prd_pesq_satisf_cd (
    sk_mc_pesq_satisf_prod                           INT NOT NULL,
    dim_mc_tempo_sk_mc_tempo                         INT NOT NULL,
    dim_mc_cliente_sk_cliente                        INT NOT NULL,
    dim_mc_centro_distribuicao_sk_centro_distribuicao INT NOT NULL,
    dim_mc_produto_sk_produto                        INT NOT NULL,
    dim_mc_colecao_status_sk_colecao_status          INT NOT NULL,
    dim_mc_funcionario_sk_funcionario                INT NOT NULL,
    dim_mc_pedido_venda_sk_pedido_venda              INT NOT NULL,
    nr_pedido_venda                                  INT NOT NULL,
    nr_item_pedido_venda                             INT NOT NULL,
    qt_vendas_cliente                                INT,
    vl_desconto                                      DECIMAL(10,2),
    vl_venda_unitaria                                DECIMAL(10,2),
    vl_venda_bruta                                   DECIMAL(10,2),
    vl_venda_liquida                                 DECIMAL(10,2),
    PRIMARY KEY (sk_mc_pesq_satisf_prod),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_tempo FOREIGN KEY (dim_mc_tempo_sk_mc_tempo) REFERENCES dim_mc_tempo (sk_mc_tempo),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_cliente FOREIGN KEY (dim_mc_cliente_sk_cliente) REFERENCES dim_mc_cliente (sk_cliente),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_centro_distribuicao FOREIGN KEY (dim_mc_centro_distribuicao_sk_centro_distribuicao) REFERENCES dim_mc_centro_distribuicao (sk_centro_distribuicao),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_produto FOREIGN KEY (dim_mc_produto_sk_produto) REFERENCES dim_mc_produto (sk_produto),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_colecao_status FOREIGN KEY (dim_mc_colecao_status_sk_colecao_status) REFERENCES dim_mc_colecao_status (sk_colecao_status),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_funcionario FOREIGN KEY (dim_mc_funcionario_sk_funcionario) REFERENCES dim_mc_funcionario (sk_funcionario),
    CONSTRAINT fk_fto_entrega_prd_pesq_satisf_cd_dim_mc_pedido_venda FOREIGN KEY (dim_mc_pedido_venda_sk_pedido_venda) REFERENCES dim_mc_pedido_venda (sk_pedido_venda)
);
