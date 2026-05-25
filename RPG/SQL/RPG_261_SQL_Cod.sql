-- ==========================================
-- ENTIDADES FORTES
-- ==========================================

CREATE TABLE Jogador (
    ID_CPF BIGINT NOT NULL, -- CPF costuma ser grande para INT comum, BIGINT é mais seguro
    Nome VARCHAR(100) NOT NULL,
    Pais VARCHAR(50),
    CEP INT,
    CONSTRAINT PK_Jogador PRIMARY KEY (ID_CPF)
);

CREATE TABLE Personagem (
    ID_Personagem INT NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    Nivel INT DEFAULT 1,
    CONSTRAINT PK_Personagem PRIMARY KEY (ID_Personagem)
);

CREATE TABLE Regiao (
    ID_Regiao INT NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Regiao PRIMARY KEY (ID_Regiao)
);

CREATE TABLE Missao (
    ID_Missao INT NOT NULL,
    Status VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Missao PRIMARY KEY (ID_Missao)
);

CREATE TABLE Inventario (
    ID_Inventario INT NOT NULL,
    Tipo_Inventario VARCHAR(20) NOT NULL, -- O nosso Atributo Discriminador
    Tamanho INT NOT NULL,
    CONSTRAINT PK_Inventario PRIMARY KEY (ID_Inventario),
    CONSTRAINT CHK_Tipo_Inventario_Valido CHECK (Tipo_Inventario IN ('Individual', 'Compartilhado', 'Quest'))
);

CREATE TABLE Itens (
    ID_Item INT NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Itens PRIMARY KEY (ID_Item)
);

-- ==========================================
-- ENTIDADES COM RELACIONAMENTO 1:N / HERANÇA / FRACAS
-- ==========================================

CREATE TABLE Telefone (
    ID_CPF BIGINT NOT NULL,
    Telefone VARCHAR(20) NOT NULL, -- VARCHAR lida melhor com DDD e formatações
    CONSTRAINT PK_Telefone PRIMARY KEY (ID_CPF, Telefone),
    CONSTRAINT FK_Telefone_Jogador FOREIGN KEY (ID_CPF) REFERENCES Jogador(ID_CPF) ON DELETE CASCADE
);

-- Herança: Guerreiro
CREATE TABLE Guerreiro (
    ID_Personagem INT NOT NULL,
    forca INT NOT NULL,
    CONSTRAINT PK_Guerreiro PRIMARY KEY (ID_Personagem),
    CONSTRAINT FK_Guerreiro_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
);

-- Herança: Mago
CREATE TABLE Mago (
    ID_Personagem INT NOT NULL,
    Mana INT NOT NULL,
    CONSTRAINT PK_Mago PRIMARY KEY (ID_Personagem),
    CONSTRAINT FK_Mago_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
);

-- Guild (Possui relacionamento com Personagem/Player)
CREATE TABLE Guild (
    ID_Guild INT NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    Player INT NOT NULL,
    CONSTRAINT PK_Guild PRIMARY KEY (ID_Guild),
    CONSTRAINT FK_Guild_Personagem FOREIGN KEY (Player) REFERENCES Personagem(ID_Personagem)
);

-- Entidade Fraca: Pet
CREATE TABLE Pet (
    ID_Personagem INT NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Pet PRIMARY KEY (ID_Personagem),
    CONSTRAINT FK_Pet_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
);

-- ==========================================
-- ENTIDADES ASSOCIATIVAS E RELACIONAMENTOS N:N
-- ==========================================

-- Cria (Relacionamento entre Jogador e Personagem)
CREATE TABLE Cria (
    ID_CPF BIGINT NOT NULL,
    ID_Personagem INT NOT NULL,
    CONSTRAINT PK_Cria PRIMARY KEY (ID_CPF, ID_Personagem),
    CONSTRAINT FK_Cria_Jogador FOREIGN KEY (ID_CPF) REFERENCES Jogador(ID_CPF),
    CONSTRAINT FK_Cria_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem)
);

-- Possui (Associativa entre Inventário e Personagem)
CREATE TABLE Possui (
    ID_Inventario INT NOT NULL,
    ID_Personagem INT NOT NULL,
    Status VARCHAR(50),
    CONSTRAINT PK_Possui PRIMARY KEY (ID_Inventario, ID_Personagem),
    CONSTRAINT FK_Possui_Inventario FOREIGN KEY (ID_Inventario) REFERENCES Inventario(ID_Inventario),
    CONSTRAINT FK_Possui_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem)
);

-- Realiza (Relacionamento Ternário: Guild, Região e Missão)
CREATE TABLE Realiza (
    ID_Guild INT NOT NULL,
    ID_Regiao INT NOT NULL,
    ID_Missao INT NOT NULL,
    CONSTRAINT PK_Realiza PRIMARY KEY (ID_Guild, ID_Regiao, ID_Missao),
    CONSTRAINT FK_Realiza_Guild FOREIGN KEY (ID_Guild) REFERENCES Guild(ID_Guild),
    CONSTRAINT FK_Realiza_Regiao FOREIGN KEY (ID_Regiao) REFERENCES Regiao(ID_Regiao),
    CONSTRAINT FK_Realiza_Missao FOREIGN KEY (ID_Missao) REFERENCES Missao(ID_Missao)
);

-- Rivaliza (Relacionamento Auto-relacionamento N:N de Guilds)
CREATE TABLE Rivaliza (
    Guild1 INT NOT NULL,
    Guild2 INT NOT NULL,
    CONSTRAINT PK_Rivaliza PRIMARY KEY (Guild1, Guild2),
    CONSTRAINT FK_Rivaliza_Guild1 FOREIGN KEY (Guild1) REFERENCES Guild(ID_Guild),
    CONSTRAINT FK_Rivaliza_Guild2 FOREIGN KEY (Guild2) REFERENCES Guild(ID_Guild),
    CONSTRAINT CHK_Nao_Rivalizar_Si_Mesmo CHECK (Guild1 <> Guild2) -- Evita que uma guild seja rival dela mesma
);

-- Usa (Relacionamento que conecta Personagem, Inventario e Itens)
CREATE TABLE Usa (
    ID_Personagem INT NOT NULL,
    ID_Inventario INT NOT NULL,
    ID_Item INT NOT NULL,
    Status VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Usa PRIMARY KEY (ID_Personagem, ID_Inventario, ID_Item, Status),
    CONSTRAINT FK_Usa_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem),
    CONSTRAINT FK_Usa_Inventario FOREIGN KEY (ID_Inventario) REFERENCES Inventario(ID_Inventario),
    CONSTRAINT FK_Usa_Itens FOREIGN KEY (ID_Item) REFERENCES Itens(ID_Item)
);
