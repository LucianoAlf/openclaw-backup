const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '/root/.openclaw/workspace/.env' });
const supabase = createClient(process.env.LAREPORT_SUPABASE_URL, process.env.LAREPORT_SUPABASE_SERVICE_ROLE, { auth: { persistSession: false } });
async function q(label, sql) { console.log('\n## '+label); const {data,error}=await supabase.rpc('executar_query_auditoria',{p_sql:sql}); if(error){console.error(JSON.stringify(error,null,2)); process.exitCode=1; return;} console.log(JSON.stringify(data,null,2)); }
(async()=>{
 await q('resumo historico_pagamentos por aluno', `
WITH alvo AS (SELECT id FROM alunos WHERE status='ativo' AND status_pagamento='sem_parcela')
SELECT a.id, a.nome, u.nome unidade,
       COUNT(hp.*) qtd_hist,
       COUNT(*) FILTER (WHERE hp.status_pagamento IS NOT NULL AND hp.status_pagamento NOT IN ('sem_parcela')) qtd_status_nao_sem_parcela,
       STRING_AGG(DISTINCT hp.status_pagamento, ', ' ORDER BY hp.status_pagamento) status_hist,
       MAX(make_date(hp.ano,hp.mes,1)) ultima_competencia,
       ROUND(SUM(COALESCE(hp.valor_parcela,0))::numeric,2) soma_valor_hist
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN historico_pagamentos hp ON hp.aluno_id=a.id
GROUP BY a.id,a.nome,u.nome
ORDER BY u.nome,a.nome;
`);
 await q('historico_pagamentos últimos dos casos regulares', `
WITH alvo AS (
 SELECT a.id FROM alunos a JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
 WHERE a.status='ativo' AND a.status_pagamento='sem_parcela' AND tm.codigo='REGULAR'
)
SELECT a.id aluno_id, a.nome, u.nome unidade, hp.ano, hp.mes, hp.status_pagamento, hp.valor_parcela, hp.created_at
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN historico_pagamentos hp ON hp.aluno_id=a.id
ORDER BY u.nome, a.nome, hp.ano DESC NULLS LAST, hp.mes DESC NULLS LAST
LIMIT 200;
`);
 await q('presencas dos 28 ativos sem_parcela', `
WITH alvo AS (SELECT id FROM alunos WHERE status='ativo' AND status_pagamento='sem_parcela')
SELECT a.id, a.nome, u.nome unidade,
       COUNT(ap.*) qtd_presencas_registros,
       COUNT(*) FILTER (WHERE lower(ap.status) IN ('presente','presença','presenca')) qtd_presentes,
       COUNT(*) FILTER (WHERE lower(ap.status) LIKE '%falt%') qtd_faltas,
       MAX(ap.data_aula) ultima_aula_report,
       STRING_AGG(DISTINCT ap.status, ', ' ORDER BY ap.status) status_presenca
FROM alvo
JOIN alunos a ON a.id=alvo.id
LEFT JOIN unidades u ON u.id=a.unidade_id
LEFT JOIN aluno_presenca ap ON ap.aluno_id=a.id
GROUP BY a.id,a.nome,u.nome
ORDER BY u.nome,a.nome;
`);
})();
