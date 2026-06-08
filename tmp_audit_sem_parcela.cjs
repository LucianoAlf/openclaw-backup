const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '/root/.openclaw/workspace/.env' });
const url = process.env.LAREPORT_SUPABASE_URL;
const key = process.env.LAREPORT_SUPABASE_SERVICE_ROLE || process.env.LAREPORT_SUPABASE_ANON_KEY;
if (!url || !key) throw new Error('Missing LAREPORT_SUPABASE_URL/key');
const supabase = createClient(url, key, { auth: { persistSession: false } });
async function q(label, sql) {
  console.log('\n## ' + label);
  const { data, error } = await supabase.rpc('executar_query_auditoria', { p_sql: sql });
  if (error) { console.error(JSON.stringify(error, null, 2)); process.exitCode = 1; return null; }
  console.log(JSON.stringify(data, null, 2));
  return data;
}
(async () => {
  await q('schema: tabelas/colunas financeiras e contrato candidatas', `
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema='public'
  AND (
    table_name ILIKE '%pag%' OR table_name ILIKE '%financ%' OR table_name ILIKE '%parcela%' OR table_name ILIKE '%fatura%' OR table_name ILIKE '%contrat%' OR table_name ILIKE '%moviment%'
    OR column_name ILIKE '%pag%' OR column_name ILIKE '%parcela%' OR column_name ILIKE '%fatura%' OR column_name ILIKE '%contrat%' OR column_name ILIKE '%emuses%' OR column_name ILIKE '%emusys%'
  )
ORDER BY table_name, ordinal_position
LIMIT 300;
`);

  await q('tipos_matricula', `
SELECT id, nome, codigo, conta_como_pagante, entra_ticket_medio, entra_ltv, entra_churn
FROM tipos_matricula
ORDER BY id;
`);

  await q('resumo ativos sem_parcela por unidade/contrato/tipo', `
WITH base AS (
 SELECT a.id, a.nome, u.nome unidade, c.nome curso, a.status, a.status_pagamento, a.valor_parcela,
        a.data_matricula, a.data_inicio_contrato, a.data_fim_contrato,
        CASE WHEN a.data_fim_contrato IS NULL THEN 'NULO'
             WHEN a.data_fim_contrato >= CURRENT_DATE THEN 'VIGENTE'
             ELSE 'VENCIDO' END AS status_contrato,
        tm.nome tipo_matricula, tm.codigo tipo_codigo, tm.conta_como_pagante,
        COALESCE(c.is_projeto_banda,false) is_projeto_banda,         COALESCE(a.is_segundo_curso,false) is_segundo_curso
 FROM alunos a
 LEFT JOIN unidades u ON u.id=a.unidade_id
 LEFT JOIN cursos c ON c.id=a.curso_id
 LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
 WHERE a.status='ativo' AND a.status_pagamento='sem_parcela'
)
SELECT unidade, status_contrato, tipo_matricula, conta_como_pagante,
       COUNT(*) qtd, ROUND(SUM(COALESCE(valor_parcela,0))::numeric,2) soma_valor
FROM base
GROUP BY unidade, status_contrato, tipo_matricula, conta_como_pagante
ORDER BY unidade, status_contrato, tipo_matricula;
`);

  await q('lista nominal ativos sem_parcela', `
WITH mov AS (
 SELECT aluno_id,
        COUNT(*) qtd_mov,
        STRING_AGG(DISTINCT tipo, ', ' ORDER BY tipo) tipos_mov,
        MAX(data) ultima_mov
 FROM movimentacoes_admin
 GROUP BY aluno_id
), base AS (
 SELECT a.id, a.nome, u.nome unidade, c.nome curso, p.nome professor,
        a.status, a.status_pagamento, a.valor_parcela,
        a.data_matricula, a.data_inicio_contrato, a.data_fim_contrato,
        CASE WHEN a.data_fim_contrato IS NULL THEN 'NULO'
             WHEN a.data_fim_contrato >= CURRENT_DATE THEN 'VIGENTE'
             ELSE 'VENCIDO' END AS status_contrato,
        tm.nome tipo_matricula, tm.codigo tipo_codigo, tm.conta_como_pagante, tm.entra_ticket_medio,
        COALESCE(c.is_projeto_banda,false) is_projeto_banda,         COALESCE(a.is_segundo_curso,false) is_segundo_curso,
        COALESCE(mov.qtd_mov,0) qtd_mov, mov.tipos_mov, mov.ultima_mov,
        EXISTS (SELECT 1 FROM movimentacoes_admin m WHERE m.aluno_id=a.id AND m.tipo IN ('evasao','nao_renovacao')) AS tem_saida_por_id,
        EXISTS (SELECT 1 FROM movimentacoes_admin m WHERE m.aluno_nome=a.nome AND m.tipo IN ('evasao','nao_renovacao')) AS tem_saida_por_nome
 FROM alunos a
 LEFT JOIN unidades u ON u.id=a.unidade_id
 LEFT JOIN cursos c ON c.id=a.curso_id
 LEFT JOIN professores p ON p.id=a.professor_atual_id
 LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
 LEFT JOIN mov ON mov.aluno_id=a.id
 WHERE a.status='ativo' AND a.status_pagamento='sem_parcela'
)
SELECT * FROM base ORDER BY unidade, status_contrato, nome;
`);

  await q('movimentacoes saída para ativos sem_parcela por ID exato', `
SELECT a.id aluno_id, a.nome aluno, u.nome unidade, c.nome curso,
       m.id mov_id, m.aluno_id mov_aluno_id, m.aluno_nome mov_aluno_nome, m.tipo, m.data, m.observacoes, m.created_at
FROM alunos a
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN cursos c ON c.id=a.curso_id
JOIN movimentacoes_admin m ON m.aluno_id=a.id
WHERE a.status='ativo' AND a.status_pagamento='sem_parcela'
  AND m.tipo IN ('evasao','nao_renovacao')
ORDER BY u.nome, a.nome, m.data DESC;
`);

  await q('movimentacoes saída por NOME sem aluno_id exato (diagnóstico apenas)', `
SELECT a.id aluno_id, a.nome aluno, u.nome unidade, c.nome curso,
       m.id mov_id, m.aluno_id mov_aluno_id, m.aluno_nome mov_aluno_nome, m.tipo, m.data, m.observacoes, m.created_at
FROM alunos a
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN cursos c ON c.id=a.curso_id
JOIN movimentacoes_admin m ON m.aluno_nome=a.nome AND (m.aluno_id IS DISTINCT FROM a.id)
WHERE a.status='ativo' AND a.status_pagamento='sem_parcela'
  AND m.tipo IN ('evasao','nao_renovacao')
ORDER BY u.nome, a.nome, m.data DESC;
`);

  await q('impacto potencial se sem_parcela vigente forem pagantes: por unidade', `
WITH base AS (
 SELECT u.nome unidade, a.id, a.nome, a.valor_parcela,
        CASE WHEN a.data_fim_contrato IS NULL THEN 'NULO'
             WHEN a.data_fim_contrato >= CURRENT_DATE THEN 'VIGENTE'
             ELSE 'VENCIDO' END AS status_contrato,
        COALESCE(c.is_projeto_banda,false) is_projeto_banda,         COALESCE(a.is_segundo_curso,false) is_segundo_curso,
        tm.codigo tipo_codigo, tm.nome tipo_matricula
 FROM alunos a
 LEFT JOIN unidades u ON u.id=a.unidade_id
 LEFT JOIN cursos c ON c.id=a.curso_id
 LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
 WHERE a.status='ativo' AND a.status_pagamento='sem_parcela'
)
SELECT unidade,
       COUNT(*) FILTER (WHERE status_contrato='VIGENTE') qtd_vigente,
       ROUND(SUM(valor_parcela) FILTER (WHERE status_contrato='VIGENTE')::numeric,2) valor_vigente,
       COUNT(*) FILTER (WHERE status_contrato='VENCIDO') qtd_vencido,
       ROUND(SUM(valor_parcela) FILTER (WHERE status_contrato='VENCIDO')::numeric,2) valor_vencido,
       COUNT(*) FILTER (WHERE status_contrato='NULO') qtd_nulo,
       ROUND(SUM(valor_parcela) FILTER (WHERE status_contrato='NULO')::numeric,2) valor_nulo
FROM base
GROUP BY unidade
ORDER BY unidade;
`);
})();
