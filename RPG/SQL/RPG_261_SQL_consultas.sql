-- ==============================================================================
-- SCRIPT DE CONSULTAS SQL PARA O ECOSSISTEMA RPG
-- Este arquivo contém exemplos práticos de queries utilizando diferentes técnicas
-- de manipulação e junção de dados para a estrutura do banco jogo.db.
-- ==============================================================================

-- 1. GROUP BY / HAVING
-- Objetivo: Agrupar os personagens pelo seu nível e mostrar apenas os níveis 
-- que possuem mais de um personagem criado no servidor.
SELECT 
    Nivel, 
    COUNT(ID_Personagem) AS Qtd_Personagens
FROM 
    Personagem
GROUP BY 
    Nivel
HAVING 
    COUNT(ID_Personagem) > 1;


-- 2. JUNÇÃO INTERNA (INNER JOIN)
-- Objetivo: Listar o nome do personagem, o nome do item que ele está usando 
-- e o status de onde esse item está equipado no momento.
SELECT 
    P.Nome AS Personagem, 
    I.Nome AS Item, 
    U.Status AS Equipado_Em
FROM 
    Usa U
INNER JOIN 
    Personagem P ON U.ID_Personagem = P.ID_Personagem
INNER JOIN 
    Itens I ON U.ID_Item = I.ID_Item;


-- 3. JUNÇÃO EXTERNA (LEFT OUTER JOIN)
-- Objetivo: Listar todos os personagens do banco de dados e o nome de seus 
-- respectivos Pets. Personagens que não possuem pet trarão o valor NULL.
SELECT 
    P.Nome AS Personagem, 
    PT.Nome AS Nome_Do_Pet
FROM 
    Personagem P
LEFT JOIN 
    Pet PT ON P.ID_Personagem = PT.ID_Personagem;


-- 4. SEMI-JUNÇÃO (EXISTS)
-- Objetivo: Filtrar e retornar apenas os dados dos jogadores que efetivamente 
-- já criaram pelo menos um personagem dentro do jogo.
SELECT 
    J.ID_CPF, 
    J.Nome
FROM 
    Jogador J
WHERE EXISTS (
    SELECT 1 
    FROM Cria C 
    WHERE C.ID_CPF = J.ID_CPF
);


-- 5. ANTI-JUNÇÃO (NOT EXISTS)
-- Objetivo: Encontrar quais inventários registrados no sistema estão completamente 
-- vazios, ou seja, não possuem nenhum item associado na tabela 'Usa'.
SELECT 
    I.ID_Inventario, 
    I.Tipo_Inventario
FROM 
    Inventario I
WHERE NOT EXISTS (
    SELECT 1 
    FROM Usa U 
    WHERE U.ID_Inventario = I.ID_Inventario
);


-- 6. SUBCONSULTA DO TIPO ESCALAR
-- Objetivo: Listar o nome e o nível de todos os personagens que possuem o 
-- nível estritamente acima da média geral de todo o servidor.
SELECT 
    Nome, 
    Nivel
FROM 
    Personagem
WHERE 
    Nivel > (SELECT AVG(Nivel) FROM Personagem);


-- 7. SUBCONSULTA DO TIPO LINHA
-- Objetivo: Encontrar um registro na tabela de guerreiros que possua exatamente 
-- a mesma combinação de ID e força que um registro específico de teste (ID = 3).
SELECT 
    ID_Personagem, 
    forca
FROM 
    Guerreiro
WHERE 
    (ID_Personagem, forca) = (
        SELECT ID_Personagem, forca 
        FROM Guerreiro 
        WHERE ID_Personagem = 3
    );


-- 8. SUBCONSULTA DO TIPO TABELA
-- Objetivo: Criar uma tabela derivada contendo apenas magos de alto nível (Nível >= 50) 
-- e, a partir dessa seleção, buscar a quantidade de mana deles na tabela Mago.
SELECT 
    HighLevelMagos.Nome, 
    M.Mana
FROM (
    SELECT ID_Personagem, Nome 
    FROM Personagem 
    WHERE Nivel >= 50
) AS HighLevelMagos
INNER JOIN 
    Mago M ON HighLevelMagos.ID_Personagem = M.ID_Personagem;


-- 9. OPERAÇÃO DE CONJUNTO (UNION)
-- Objetivo: Criar uma lista unificada e consolidada de todas as subclasses 
-- especializadas do jogo (Guerreiros e Magos), identificando o ID e o tipo da classe.
SELECT ID_Personagem, 'Guerreiro' AS Classe FROM Guerreiro
UNION
SELECT ID_Personagem, 'Mago' AS Classe FROM Mago;