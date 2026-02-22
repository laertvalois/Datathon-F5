-- ============================================
-- SCHEMA DO BANCO DE DADOS - DATATHON F5
-- Passos Mágicos - Análise de Risco de Defasagem
-- ============================================

-- Tabela principal: dados dos alunos
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ra TEXT,
    ano INTEGER NOT NULL,
    turma TEXT,
    idade REAL,
    ano_ingresso INTEGER,
    fase TEXT,
    instituicao_ensino TEXT,
    
    -- Indicadores principais
    iaa REAL,           -- Índice de Autoavaliação
    ieg REAL,           -- Índice de Engajamento Geral
    ips REAL,           -- Índice de Perfil Psicossocial
    ipp REAL,           -- Índice de Perfil Psicopedagógico
    ida REAL,           -- Índice de Desempenho Acadêmico
    ipv REAL,           -- Índice de Ponto de Virada
    ian REAL,           -- Índice de Adequação de Nível
    
    -- Notas por disciplina
    mat REAL,           -- Matemática
    por REAL,           -- Português
    ing REAL,           -- Inglês
    
    -- Indicadores adicionais
    inde_22 REAL,       -- INDE 2022
    inde_23 REAL,       -- INDE 2023
    inde_24 REAL,       -- INDE 2024
    inde REAL,          -- INDE (consolidado)
    defasagem TEXT,     -- Categoria de defasagem
    
    -- Campos adicionais da base oficial
    pedra_20 TEXT,      -- Pedra 2020
    pedra_21 TEXT,      -- Pedra 2021
    pedra_22 TEXT,      -- Pedra 2022
    pedra_23 TEXT,      -- Pedra 2023
    pedra_24 TEXT,      -- Pedra 2024
    fase_ideal TEXT,    -- Fase ideal para idade
    destaque_ieg TEXT,  -- Destaque IEG
    destaque_ida TEXT,  -- Destaque IDA
    destaque_ipv TEXT,  -- Destaque IPV
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhorar performance de queries
CREATE INDEX IF NOT EXISTS idx_alunos_ano ON alunos(ano);
CREATE INDEX IF NOT EXISTS idx_alunos_ra ON alunos(ra);
CREATE INDEX IF NOT EXISTS idx_alunos_ian ON alunos(ian);
CREATE INDEX IF NOT EXISTS idx_alunos_fase ON alunos(fase);
CREATE INDEX IF NOT EXISTS idx_alunos_ano_ingresso ON alunos(ano_ingresso);

-- Tabela de features derivadas (calculadas)
CREATE TABLE IF NOT EXISTS features_derivadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    
    -- Features calculadas
    tempo_na_escola INTEGER,      -- Ano atual - Ano ingresso
    media_academica REAL,         -- Média de Mat, Por, Ing
    media_indicadores REAL,       -- Média de IAA, IEG, IPS, IPP, IDA, IPV
    
    -- Target
    risco_defasagem INTEGER,      -- 0 = sem risco, 1 = em risco
    nivel_ian TEXT,              -- severa, moderada, em fase
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_features_aluno_id ON features_derivadas(aluno_id);
CREATE INDEX IF NOT EXISTS idx_features_risco ON features_derivadas(risco_defasagem);

-- Tabela de metadados do modelo
CREATE TABLE IF NOT EXISTS modelos_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_modelo TEXT NOT NULL,
    versao TEXT NOT NULL,
    algoritmo TEXT NOT NULL,
    features TEXT NOT NULL,        -- JSON com lista de features
    metricas TEXT,                 -- JSON com métricas (AUC, acurácia, etc.)
    threshold REAL DEFAULT 0.70,
    caminho_arquivo TEXT,
    data_treinamento TIMESTAMP,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_modelos_versao ON modelos_metadata(versao);
CREATE INDEX IF NOT EXISTS idx_modelos_data ON modelos_metadata(data_treinamento);

-- View consolidada para facilitar queries
CREATE VIEW IF NOT EXISTS vw_alunos_completo AS
SELECT 
    a.*,
    f.tempo_na_escola,
    f.media_academica,
    f.media_indicadores,
    f.risco_defasagem,
    f.nivel_ian
FROM alunos a
LEFT JOIN features_derivadas f ON a.id = f.aluno_id;

-- View para análise exploratória
CREATE VIEW IF NOT EXISTS vw_analise_exploratoria AS
SELECT 
    ano,
    fase,
    COUNT(*) as total_alunos,
    AVG(ian) as media_ian,
    AVG(ida) as media_ida,
    AVG(ieg) as media_ieg,
    AVG(iaa) as media_iaa,
    AVG(ips) as media_ips,
    AVG(ipp) as media_ipp,
    AVG(ipv) as media_ipv,
    AVG(inde) as media_inde,
    AVG(mat) as media_mat,
    AVG(por) as media_por,
    AVG(ing) as media_ing,
    SUM(CASE WHEN risco_defasagem = 1 THEN 1 ELSE 0 END) as total_em_risco,
    SUM(CASE WHEN risco_defasagem = 0 THEN 1 ELSE 0 END) as total_sem_risco
FROM vw_alunos_completo
GROUP BY ano, fase;
