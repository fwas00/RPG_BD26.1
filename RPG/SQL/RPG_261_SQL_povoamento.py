import sqlite3

def povoar_banco():
    # Conecta ao banco de dados (se o arquivo não existir, ele será criado)
    conn = sqlite3.connect('jogo.db')
    cursor = conn.cursor()

    print("Criando tabelas...")

    # Ativa o suporte a chaves estrangeiras no SQLite (por padrão vem desativado)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. CRIÇÃO DAS TABELAS
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Jogador (
        ID_CPF BIGINT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        Pais VARCHAR(50),
        CEP INT,
        CONSTRAINT PK_Jogador PRIMARY KEY (ID_CPF)
    );

    CREATE TABLE IF NOT EXISTS Personagem (
        ID_Personagem INT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        Nivel INT DEFAULT 1,
        CONSTRAINT PK_Personagem PRIMARY KEY (ID_Personagem)
    );

    CREATE TABLE IF NOT EXISTS Regiao (
        ID_Regiao INT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        CONSTRAINT PK_Regiao PRIMARY KEY (ID_Regiao)
    );

    CREATE TABLE IF NOT EXISTS Missao (
        ID_Missao INT NOT NULL,
        Status VARCHAR(50) NOT NULL,
        CONSTRAINT PK_Missao PRIMARY KEY (ID_Missao)
    );

    CREATE TABLE IF NOT EXISTS Inventario (
        ID_Inventario INT NOT NULL,
        Tipo_Inventario VARCHAR(50) NOT NULL,
        Tamanho INT NOT NULL,
        CONSTRAINT PK_Inventario PRIMARY KEY (ID_Inventario)
    );

    CREATE TABLE IF NOT EXISTS Itens (
        ID_Item INT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        CONSTRAINT PK_Itens PRIMARY KEY (ID_Item)
    );

    CREATE TABLE IF NOT EXISTS Telefone (
        ID_CPF BIGINT NOT NULL,
        Telefone VARCHAR(20) NOT NULL,
        CONSTRAINT PK_Telefone PRIMARY KEY (ID_CPF, Telefone),
        CONSTRAINT FK_Telefone_Jogador FOREIGN KEY (ID_CPF) REFERENCES Jogador(ID_CPF) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Guerreiro (
        ID_Personagem INT NOT NULL,
        forca INT NOT NULL,
        CONSTRAINT PK_Guerreiro PRIMARY KEY (ID_Personagem),
        CONSTRAINT FK_Guerreiro_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Mago (
        ID_Personagem INT NOT NULL,
        Mana INT NOT NULL,
        CONSTRAINT PK_Mago PRIMARY KEY (ID_Personagem),
        CONSTRAINT FK_Mago_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Guild (
        ID_Guild INT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        Player INT NOT NULL,
        CONSTRAINT PK_Guild PRIMARY KEY (ID_Guild),
        CONSTRAINT FK_Guild_Personagem FOREIGN KEY (Player) REFERENCES Personagem(ID_Personagem)
    );

    CREATE TABLE IF NOT EXISTS Pet (
        ID_Personagem INT NOT NULL,
        Nome VARCHAR(100) NOT NULL,
        CONSTRAINT PK_Pet PRIMARY KEY (ID_Personagem),
        CONSTRAINT FK_Pet_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Cria (
        ID_CPF BIGINT NOT NULL,
        ID_Personagem INT NOT NULL,
        CONSTRAINT PK_Cria PRIMARY KEY (ID_CPF, ID_Personagem),
        CONSTRAINT FK_Cria_Jogador FOREIGN KEY (ID_CPF) REFERENCES Jogador(ID_CPF),
        CONSTRAINT FK_Cria_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem)
    );

    CREATE TABLE IF NOT EXISTS Possui (
        ID_Inventario INT NOT NULL,
        ID_Personagem INT NOT NULL,
        Status VARCHAR(50),
        CONSTRAINT PK_Possui PRIMARY KEY (ID_Inventario, ID_Personagem),
        CONSTRAINT FK_Possui_Inventario FOREIGN KEY (ID_Inventario) REFERENCES Inventario(ID_Inventario),
        CONSTRAINT FK_Possui_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem)
    );

    CREATE TABLE IF NOT EXISTS Realiza (
        ID_Guild INT NOT NULL,
        ID_Regiao INT NOT NULL,
        ID_Missao INT NOT NULL,
        CONSTRAINT PK_Realiza PRIMARY KEY (ID_Guild, ID_Regiao, ID_Missao),
        CONSTRAINT FK_Realiza_Guild FOREIGN KEY (ID_Guild) REFERENCES Guild(ID_Guild),
        CONSTRAINT FK_Realiza_Regiao FOREIGN KEY (ID_Regiao) REFERENCES Regiao(ID_Regiao),
        CONSTRAINT FK_Realiza_Missao FOREIGN KEY (ID_Missao) REFERENCES Missao(ID_Missao)
    );

    CREATE TABLE IF NOT EXISTS Rivaliza (
        Guild1 INT NOT NULL,
        Guild2 INT NOT NULL,
        CONSTRAINT PK_Rivaliza PRIMARY KEY (Guild1, Guild2),
        CONSTRAINT FK_Rivaliza_Guild1 FOREIGN KEY (Guild1) REFERENCES Guild(ID_Guild),
        CONSTRAINT FK_Rivaliza_Guild2 FOREIGN KEY (Guild2) REFERENCES Guild(ID_Guild)
    );
    
    CREATE TABLE IF NOT EXISTS Usa (
        ID_Personagem INT NOT NULL,
        ID_Inventario INT NOT NULL,
        ID_Item INT NOT NULL,
        Status VARCHAR(50) NOT NULL,
        CONSTRAINT PK_Usa PRIMARY KEY (ID_Personagem, ID_Inventario, ID_Item, Status),
        CONSTRAINT FK_Usa_Personagem FOREIGN KEY (ID_Personagem) REFERENCES Personagem(ID_Personagem),
        CONSTRAINT FK_Usa_Inventario FOREIGN KEY (ID_Inventario) REFERENCES Inventario(ID_Inventario),
        CONSTRAINT FK_Usa_Itens FOREIGN KEY (ID_Item) REFERENCES Itens(ID_Item)
    );
    ''')

    print("Inserindo dados fictícios...")

    # 2. INSERÇÃO DOS DADOS (Respeitando a ordem das chaves estrangeiras)
    
    # Jogadores
    jogadores = [
        (12345678901, 'Fábio Silva', 'Brasil', 50000000),
        (98765432100, 'Arthur Pendragon', 'Reino Unido', 1234567)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Jogador VALUES (?, ?, ?, ?);", jogadores)

    # Telefones
    telefones = [
        (12345678901, '81999998888'),
        (12345678901, '8135331122'),
        (98765432100, '447911122233')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Telefone VALUES (?, ?);", telefones)

    # Personagens
    personagens = [
        (1, 'Guga_O_Esmagador', 45),
        (2, 'Merlin_Dourado', 50),
        (3, 'Grid_Overgeared', 99)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Personagem VALUES (?, ?, ?);", personagens)

    # Classes Filhas (Guerreiro / Mago)
    guerreiros = [(1, 85), (3, 99)] # ID_Personagem, Força
    magos = [(2, 95)] # ID_Personagem, Mana
    cursor.executemany("INSERT OR IGNORE INTO Guerreiro VALUES (?, ?);", guerreiros)
    cursor.executemany("INSERT OR IGNORE INTO Mago VALUES (?, ?);", magos)

    # Pets
    pets = [
        (1, 'Fenrir'),
        (2, 'Corujinha')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Pet VALUES (?, ?);", pets)

    # Guilds (Lembrando que o campo Player aponta para um líder/personagem existente)
    guilds = [
        (10, 'Cavaleiros de Prata', 1),
        (20, 'Guilda Overgeared', 3)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Guild VALUES (?, ?, ?);", guilds)

    # Regiões
    regioes = [
        (100, 'Floresta de Elwynn'),
        (201, 'Deserto de Kalahari')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Regiao VALUES (?, ?);", regioes)

    # Missões
    missoes = [
        (501, 'Em Andamento'),
        (502, 'Concluída')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Missao VALUES (?, ?);", missoes)

    # Inventários
    inventarios = [
        (1001, 'Mochila Principal', 30),
        (1002, 'Baú de Guilda Compartilhado', 200),
        (1003, 'Alforge de Montaria', 15)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Inventario VALUES (?, ?, ?);", inventarios)

    # Itens
    itens = [
        (9001, 'Espada Longa de Ferro'),
        (9002, 'Cajado de Cristal'),
        (9003, 'Poção de Mana Maior')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Itens VALUES (?, ?);", itens)

    # 3. POVOAMENTO DAS TABELAS ASSOCIATIVAS E RELACIONAMENTOS N:N

    # Cria (Ligação Jogador -> Personagem)
    relacao_cria = [
        (12345678901, 1), # Fábio criou Guga
        (12345678901, 3), # Fábio criou Grid
        (98765432100, 2)  # Arthur criou Merlin
    ]
    cursor.executemany("INSERT OR IGNORE INTO Cria VALUES (?, ?);", relacao_cria)

    # Possui (Ligação Personagem -> Inventário)
    relacao_possui = [
        (1001, 1, 'Ativo'), # Guga possui Mochila Principal
        (1002, 1, 'Compartilhado'), # Guga tem acesso ao Baú de Guilda
        (1002, 3, 'Compartilhado'), # Grid também tem acesso ao mesmo Baú de Guilda
        (1003, 2, 'Ativo')  # Merlin possui Alforge
    ]
    cursor.executemany("INSERT OR IGNORE INTO Possui VALUES (?, ?, ?);", relacao_possui)

    # Realiza (Ternário: Guild realiza Missão em uma Região)
    relacao_realiza = [
        (10, 100, 501), # Cavaleiros de Prata realizam Missão 501 na Floresta
        (20, 201, 502)  # Guilda Overgeared realizou Missão 502 no Deserto
    ]
    cursor.executemany("INSERT OR IGNORE INTO Realiza VALUES (?, ?, ?);", relacao_realiza)

    # Rivaliza (Auto-relacionamento N:N de Guilds)
    relacao_rivaliza = [
        (10, 20), # Guilda 10 rivaliza com a Guilda 20
        (20, 10)  # Rivalidade mútua/bidirecional
    ]
    cursor.executemany("INSERT OR IGNORE INTO Rivaliza VALUES (?, ?);", relacao_rivaliza)

    # Usa (Relacionamento quádruplo conectando Personagem, Inventário e Item)
    relacao_usa = [
        (1, 1001, 9001, 'Equipado na Mão Direita'), # Guga usa Espada da sua Mochila
        (2, 1003, 9002, 'Equipado no Slot Principal'), # Merlin usa Cajado do seu Alforge
        (3, 1002, 9003, 'Pronto na Barra de Atalho') # Grid usa Poção do Baú de Guilda
    ]
    cursor.executemany("INSERT OR IGNORE INTO Usa VALUES (?, ?, ?, ?);", relacao_usa)

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()
    print("Banco de dados 'jogo.db' criado e povoado com sucesso!")

if __name__ == '__main__':
    povoar_banco()