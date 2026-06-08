const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '/root/.openclaw/workspace/.env' });
const supabase = createClient(process.env.LAREPORT_SUPABASE_URL, process.env.LAREPORT_SUPABASE_SERVICE_ROLE, { auth: { persistSession: false } });
async function q(label, sql) { console.log('\n## '+label); const {data,error}=await supabase.rpc('executar_query_auditoria',{p_sql:sql}); if(error){console.error(JSON.stringify(error,null,2)); process.exitCode=1; return;} console.log(JSON.stringify(data,null,2)); }
(async()=>{
 await q('columns historico_pagamentos/presenca', `
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema='public' AND table_name IN ('historico_pagamentos','aluno_presenca','aulas_emusys')
ORDER BY table_name, ordinal_position;
`);
 await q('historico_pagamentos dos 28 ativos sem_parcela', `
WITH alvo AS (SELECT id FROM alunos WHERE status='ativo' AND status_pagamento='sem_parcela')
SELECT a.id aluno_id, a.nome, u.nome unidade, hp.ano, hp.mes, hp.status_pagamento, hp.valor_pago, hp.valor_devido, hp.created_at, hp.updated_at
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN historico_pagamentos hp ON hp.aluno_id=a.id
ORDER BY u.nome, a.nome, hp.ano DESC, hp.mes DESC
LIMIT 300;
`);
 await q('resumo historico_pagamentos por aluno', `
WITH alvo AS (SELECT id FROM alunos WHERE status='ativo' AND status_pagamento='sem_parcela')
SELECT a.id, a.nome, u.nome unidade,
       COUNT(hp.*) qtd_hist,
       COUNT(*) FILTER (WHERE hp.status_pagamento IS NOT NULL AND hp.status_pagamento NOT IN ('sem_parcela')) qtd_status_nao_sem_parcela,
       STRING_AGG(DISTINCT hp.status_pagamento, ', ' ORDER BY hp.status_pagamento) status_hist,
       MAX(make_date(hp.ano,hp.mes,1)) ultima_competencia,
       ROUND(SUM(COALESCE(hp.valor_pago,0))::numeric,2) total_pago_hist,
       ROUND(SUM(COALESCE(hp.valor_devido,0))::numeric,2) total_devido_hist
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN historico_pagamentos hp ON hp.aluno_id=a.id
GROUP BY a.id,a.nome,u.nome
ORDER BY u.nome,a.nome;
`);
 await q('presencas/aulas dos 28 ativos sem_parcela', `
WITH alvo AS (SELECT id FROM alunos WHERE status='ativo' AND status_pagamento='sem_parcela')
SELECT a.id, a.nome, u.nome unidade,
       COUNT(ap.*) qtd_presencas_registros,
       COUNT(*) FILTER (WHERE ap.status ILIKE '%pres%' OR ap.presente=true) qtd_presentes,
       COUNT(*) FILTER (WHERE ap.status ILIKE '%falt%' OR ap.presente=false) qtd_faltas,
       MAX(ae.data) ultima_aula_emusys
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN aluno_presenca ap ON ap.aluno_id=a.id
LEFT JOIN aulas_emusys ae ON ae.id=ap.aula_emusys_id
GROUP BY a.id,a.nome,u.nome
ORDER BY u.nome,a.nome;
`);
})();
