## audit_dados_mensais()

```sql
CREATE OR REPLACE FUNCTION public.audit_dados_mensais()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (tabela, registro_id, acao, dados_novos)
        VALUES ('dados_mensais', NEW.id, 'INSERT', to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (tabela, registro_id, acao, dados_antigos, dados_novos)
        VALUES ('dados_mensais', NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (tabela, registro_id, acao, dados_antigos)
        VALUES ('dados_mensais', OLD.id, 'DELETE', to_jsonb(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$function$

```

## fechar_dados_mensais(p_ano integer, p_mes integer)

```sql
CREATE OR REPLACE FUNCTION public.fechar_dados_mensais(p_ano integer, p_mes integer)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
  v_inicio DATE := make_date(p_ano, p_mes, 1);
  v_fim DATE := (make_date(p_ano, p_mes, 1) + INTERVAL '1 month')::date;
  v_unidade RECORD;
  v_alunos_ativos INT;
  v_alunos_pagantes INT;
  v_matriculas_ativas INT;
  v_matriculas_banda INT;
  v_matriculas_2_curso INT;
  v_novas_matriculas INT;
  v_evasoes INT;
  v_churn_rate NUMERIC;
  v_ticket_medio NUMERIC;
BEGIN
  FOR v_unidade IN SELECT id, nome FROM unidades WHERE nome IN ('Barra', 'Campo Grande', 'Recreio')
  LOOP
    -- Alunos ativos no fim do mês (únicos, sem segundo curso)
    -- Inclui aviso_previo pois aluno ainda está matriculado
    SELECT COUNT(*) INTO v_alunos_ativos
    FROM alunos
    WHERE unidade_id = v_unidade.id
      AND is_segundo_curso = false
      AND data_matricula < v_fim
      AND (status IN ('ativo', 'aviso_previo') OR (status = 'inativo' AND data_said
```

## get_comparativo_anos(p_ano_atual integer, p_ano_anterior integer)

```sql
CREATE OR REPLACE FUNCTION public.get_comparativo_anos(p_ano_atual integer, p_ano_anterior integer)
 RETURNS TABLE(metrica character varying, valor_anterior numeric, valor_atual numeric, variacao numeric)
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_alunos_atual INTEGER;
    v_alunos_anterior INTEGER;
    v_matriculas_atual INTEGER;
    v_matriculas_anterior INTEGER;
    v_evasoes_atual INTEGER;
    v_evasoes_anterior INTEGER;
    v_churn_atual NUMERIC;
    v_churn_anterior NUMERIC;
    v_ticket_atual NUMERIC;
    v_ticket_anterior NUMERIC;
BEGIN
    -- Alunos dezembro
    SELECT SUM(alunos_pagantes) INTO v_alunos_atual FROM dados_mensais WHERE ano = p_ano_atual AND mes = 12;
    SELECT SUM(alunos_pagantes) INTO v_alunos_anterior FROM dados_mensais WHERE ano = p_ano_anterior AND mes = 12;
    
    -- Matrículas total
    SELECT SUM(novas_matriculas) INTO v_matriculas_atual FROM dados_mensais WHERE ano = p_ano_atual;
    SELECT SUM(novas_matriculas) INTO v_matriculas
```

## get_dados_relatorio_gerencial(p_unidade_id uuid, p_ano integer, p_mes integer)

```sql
CREATE OR REPLACE FUNCTION public.get_dados_relatorio_gerencial(p_unidade_id uuid DEFAULT NULL::uuid, p_ano integer DEFAULT (EXTRACT(year FROM CURRENT_DATE))::integer, p_mes integer DEFAULT (EXTRACT(month FROM CURRENT_DATE))::integer)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
  v_result JSONB;
  v_mes_anterior INTEGER;
  v_ano_mes_anterior INTEGER;
  v_unidade_nome TEXT;
  v_gerente_nome TEXT;
  v_hunter_nome TEXT;
  v_farmers_nomes TEXT[];
  v_tem_dados_mensais BOOLEAN;
  v_start_date DATE;
  v_end_date DATE;
BEGIN
  IF p_mes = 1 THEN
    v_mes_anterior := 12;
    v_ano_mes_anterior := p_ano - 1;
  ELSE
    v_mes_anterior := p_mes - 1;
    v_ano_mes_anterior := p_ano;
  END IF;

  v_start_date := MAKE_DATE(p_ano, p_mes, 1);
  v_end_date := (v_start_date + INTERVAL '1 month' - INTERVAL '1 day')::date;

  IF p_unidade_id IS NOT NULL THEN
    SELECT nome, gerente_nome, hunter_nome, farmers_nomes 
    INTO v_unidade_nome, v_gerente_nome, v_hunter_nome, v_far
```

## get_dados_retencao_ia(p_unidade_id uuid, p_ano integer, p_mes integer)

```sql
CREATE OR REPLACE FUNCTION public.get_dados_retencao_ia(p_unidade_id uuid, p_ano integer, p_mes integer)
 RETURNS json
 LANGUAGE plpgsql
AS $function$
DECLARE
  resultado JSON;
  mes_anterior INT;
  ano_anterior INT;
  ano_passado INT;
BEGIN
  IF p_mes = 1 THEN
    mes_anterior := 12;
    ano_anterior := p_ano - 1;
  ELSE
    mes_anterior := p_mes - 1;
    ano_anterior := p_ano;
  END IF;
  ano_passado := p_ano - 1;

  SELECT json_build_object(
    'periodo', json_build_object('ano', p_ano, 'mes', p_mes, 'mes_nome', TRIM(TO_CHAR(TO_DATE(p_mes::text, 'MM'), 'Month'))),
    'kpis_gestao', (
      SELECT COALESCE(json_agg(json_build_object(
        'unidade_id', kg.unidade_id, 'unidade_nome', kg.unidade_nome,
        'total_alunos_ativos', COALESCE(kg.total_alunos_ativos, 0),
        'total_alunos_pagantes', COALESCE(kg.total_alunos_pagantes, 0),
        'ticket_medio', COALESCE(kg.ticket_medio, 0), 'mrr', COALESCE(kg.mrr, 0),
        'tempo_permanencia_medio', COALESCE(kg.tempo_permanenc
```

## get_heatmap_data(p_ano integer, p_metrica character varying)

```sql
CREATE OR REPLACE FUNCTION public.get_heatmap_data(p_ano integer, p_metrica character varying)
 RETURNS TABLE(unidade character varying, codigo character varying, mes integer, valor integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF p_metrica = 'evasoes' THEN
        RETURN QUERY
        SELECT u.nome::VARCHAR, u.codigo::VARCHAR, dm.mes, dm.evasoes::INTEGER
        FROM dados_mensais dm
        JOIN unidades u ON dm.unidade_id = u.id
        WHERE dm.ano = p_ano
        ORDER BY u.nome, dm.mes;
    ELSIF p_metrica = 'matriculas' THEN
        RETURN QUERY
        SELECT u.nome::VARCHAR, u.codigo::VARCHAR, dm.mes, dm.novas_matriculas::INTEGER
        FROM dados_mensais dm
        JOIN unidades u ON dm.unidade_id = u.id
        WHERE dm.ano = p_ano
        ORDER BY u.nome, dm.mes;
    ELSE
        RETURN QUERY
        SELECT u.nome::VARCHAR, u.codigo::VARCHAR, dm.mes, dm.alunos_pagantes::INTEGER
        FROM dados_mensais dm
        JOIN unidades u ON dm.unidade_id 
```

## get_heatmap_totais(p_ano integer, p_metrica character varying)

```sql
CREATE OR REPLACE FUNCTION public.get_heatmap_totais(p_ano integer, p_metrica character varying)
 RETURNS TABLE(mes integer, total integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF p_metrica = 'evasoes' THEN
        RETURN QUERY
        SELECT dm.mes, SUM(dm.evasoes)::INTEGER as total
        FROM dados_mensais dm
        WHERE dm.ano = p_ano
        GROUP BY dm.mes
        ORDER BY dm.mes;
    ELSIF p_metrica = 'matriculas' THEN
        RETURN QUERY
        SELECT dm.mes, SUM(dm.novas_matriculas)::INTEGER as total
        FROM dados_mensais dm
        WHERE dm.ano = p_ano
        GROUP BY dm.mes
        ORDER BY dm.mes;
    ELSE
        RETURN QUERY
        SELECT dm.mes, SUM(dm.alunos_pagantes)::INTEGER as total
        FROM dados_mensais dm
        WHERE dm.ano = p_ano
        GROUP BY dm.mes
        ORDER BY dm.mes;
    END IF;
END;
$function$

```

## get_kpis_consolidados(p_ano integer)

```sql
CREATE OR REPLACE FUNCTION public.get_kpis_consolidados(p_ano integer)
 RETURNS TABLE(alunos_total integer, matriculas_total integer, evasoes_total integer, churn_medio numeric, ticket_medio numeric, renovacao_media numeric, permanencia_media integer, inadimplencia_media numeric, faturamento_estimado numeric)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT SUM(dm2.alunos_pagantes)::INTEGER FROM dados_mensais dm2 WHERE dm2.ano = p_ano AND dm2.mes = 12),
        SUM(dm.novas_matriculas)::INTEGER,
        SUM(dm.evasoes)::INTEGER,
        ROUND(AVG(dm.churn_rate), 2),
        ROUND(AVG(dm.ticket_medio), 2),
        ROUND(AVG(dm.taxa_renovacao), 2),
        ROUND(AVG(dm.tempo_permanencia))::INTEGER,
        ROUND(AVG(dm.inadimplencia), 2),
        SUM(dm.faturamento_estimado)
    FROM dados_mensais dm
    WHERE dm.ano = p_ano;
END;
$function$

```

## get_kpis_evolucao_mensal(p_unidade_id text, p_meses integer)

```sql
CREATE OR REPLACE FUNCTION public.get_kpis_evolucao_mensal(p_unidade_id text DEFAULT NULL::text, p_meses integer DEFAULT 6)
 RETURNS TABLE(ano integer, mes integer, mes_nome text, alunos_ativos integer, novas_matriculas integer, evasoes integer, churn_rate numeric, ticket_medio numeric, mrr numeric)
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN QUERY
  SELECT 
    dm.ano,
    dm.mes,
    TO_CHAR(TO_DATE(dm.mes::text, 'MM'), 'Mon') as mes_nome,
    dm.alunos_pagantes as alunos_ativos,
    dm.novas_matriculas,
    dm.evasoes,
    dm.churn_rate::numeric,
    dm.ticket_medio::numeric,
    (dm.alunos_pagantes * dm.ticket_medio)::numeric as mrr
  FROM dados_mensais dm
  WHERE (p_unidade_id IS NULL OR dm.unidade_id::text = p_unidade_id)
  ORDER BY dm.ano DESC, dm.mes DESC
  LIMIT p_meses;
END;
$function$

```

## get_kpis_unidade(p_unidade_codigo character varying, p_ano integer)

```sql
CREATE OR REPLACE FUNCTION public.get_kpis_unidade(p_unidade_codigo character varying, p_ano integer)
 RETURNS TABLE(alunos_dezembro integer, alunos_janeiro integer, matriculas_total integer, evasoes_total integer, churn_medio numeric, ticket_medio numeric, renovacao_media numeric, permanencia integer, inadimplencia_media numeric, faturamento_dezembro numeric)
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_unidade_id UUID;
BEGIN
    SELECT id INTO v_unidade_id FROM unidades WHERE codigo = p_unidade_codigo;
    
    RETURN QUERY
    SELECT 
        (SELECT dm2.alunos_pagantes FROM dados_mensais dm2 WHERE dm2.unidade_id = v_unidade_id AND dm2.ano = p_ano AND dm2.mes = 12),
        (SELECT dm2.alunos_pagantes FROM dados_mensais dm2 WHERE dm2.unidade_id = v_unidade_id AND dm2.ano = p_ano AND dm2.mes = 1),
        SUM(dm.novas_matriculas)::INTEGER,
        SUM(dm.evasoes)::INTEGER,
        ROUND(AVG(dm.churn_rate), 2),
        ROUND(AVG(dm.ticket_medio), 2),
        ROUND(AVG(d
```

## get_metas_vs_realizado(p_ano integer)

```sql
CREATE OR REPLACE FUNCTION public.get_metas_vs_realizado(p_ano integer)
 RETURNS TABLE(unidade character varying, codigo character varying, metrica character varying, meta numeric, realizado numeric, percentual_atingido numeric, status character varying)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT 
        u.nome::VARCHAR,
        u.codigo::VARCHAR,
        'alunos'::VARCHAR,
        m.meta_alunos::NUMERIC,
        MAX(CASE WHEN dm.mes = 12 THEN dm.alunos_pagantes ELSE 0 END)::NUMERIC,
        ROUND((MAX(CASE WHEN dm.mes = 12 THEN dm.alunos_pagantes ELSE 0 END)::NUMERIC / NULLIF(m.meta_alunos, 0) * 100), 1),
        CASE 
            WHEN MAX(CASE WHEN dm.mes = 12 THEN dm.alunos_pagantes ELSE 0 END) >= m.meta_alunos THEN 'atingida'
            WHEN MAX(CASE WHEN dm.mes = 12 THEN dm.alunos_pagantes ELSE 0 END) >= m.meta_alunos * 0.9 THEN 'proximo'
            ELSE 'nao_atingida'
        END::VARCHAR
    FROM metas m
    JOIN unidades u ON m.unidade_
```

## get_programa_fideliza_dados(p_ano integer, p_trimestre integer, p_unidade_id uuid)

```sql
CREATE OR REPLACE FUNCTION public.get_programa_fideliza_dados(p_ano integer DEFAULT 2026, p_trimestre integer DEFAULT NULL::integer, p_unidade_id uuid DEFAULT NULL::uuid)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
  v_config JSONB;
  v_farmers JSONB;
  v_penalidades JSONB;
  v_historico JSONB;
  v_experiencias JSONB;
  v_trim_atual INTEGER;
BEGIN
  IF p_trimestre IS NULL THEN
    v_trim_atual := CEIL(EXTRACT(MONTH FROM CURRENT_DATE)::numeric / 3);
  ELSE
    v_trim_atual := p_trimestre;
  END IF;

  SELECT jsonb_build_object(
    'ano', c.ano,
    'metas', jsonb_build_object(
      'churn_maximo', c.meta_churn_maximo, 'inadimplencia_maxima', c.meta_inadimplencia_maxima,
      'renovacao_minima', c.meta_renovacao_minima, 'reajuste_minimo', c.meta_reajuste_minimo,
      'lojinha_campo_grande', (c.metas_lojinha->>'2ec861f6-023f-4d7b-9927-3960ad8c2a92')::numeric,
      'lojinha_recreio', (c.metas_lojinha->>'95553e96-971b-4590-a6eb-0201d013c14d')::numeric,
    
```

## recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)

```sql
CREATE OR REPLACE FUNCTION public.recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
  v_result jsonb;
  v_inicio_mes date;
  v_fim_mes date;
  v_alunos_ativos integer;
  v_alunos_pagantes integer;
  v_matriculas_ativas integer;
  v_matriculas_banda integer;
  v_matriculas_2_curso integer;
  v_novas_matriculas integer;
  v_evasoes integer;
  v_churn_rate numeric;
BEGIN
  v_inicio_mes := DATE_TRUNC('month', MAKE_DATE(p_ano, p_mes, 1))::date;
  v_fim_mes := (v_inicio_mes + INTERVAL '1 month - 1 day')::date;

  SELECT COUNT(DISTINCT a.nome)
  INTO v_alunos_ativos
  FROM alunos a
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes);

  SELECT COUNT(DISTINCT a.nome)
  INTO v_alunos_pagantes
  FROM alunos a
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  WHERE a
```

## salvar_historico_trimestral_fideliza(p_ano integer, p_trimestre integer)

```sql
CREATE OR REPLACE FUNCTION public.salvar_historico_trimestral_fideliza(p_ano integer, p_trimestre integer)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
  v_config programa_fideliza_config%ROWTYPE;
BEGIN
  SELECT * INTO v_config FROM programa_fideliza_config WHERE ano = p_ano;
  
  INSERT INTO programa_fideliza_historico (
    ano, trimestre, unidade_id, 
    churn_rate, inadimplencia_pct, taxa_renovacao, reajuste_medio, vendas_lojinha,
    bateu_churn, bateu_inadimplencia, bateu_renovacao, bateu_reajuste, bateu_lojinha,
    pontos_base, pontos_penalidades, pontos_total
  )
  SELECT 
    p_ano,
    p_trimestre,
    u.id,
    COALESCE(AVG(dm.churn_rate), 0),
    COALESCE(AVG(dm.inadimplencia), 0),
    COALESCE(AVG(dm.taxa_renovacao), 0),
    COALESCE(AVG(dm.reajuste_parcelas), 0),
    0,
    COALESCE(AVG(dm.churn_rate), 100) <= v_config.meta_churn_maximo,
    COALESCE(AVG(dm.inadimplencia), 100) <= v_config.meta_inadimplencia_maxima,
    COALESCE(AVG(dm.taxa_r
```

## snapshot_dados_mensais(p_ano integer, p_mes integer)

```sql
CREATE OR REPLACE FUNCTION public.snapshot_dados_mensais(p_ano integer, p_mes integer)
 RETURNS TABLE(unidade_nome text, registros_afetados integer)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_unidade RECORD;
BEGIN
  FOR v_unidade IN SELECT id, nome FROM unidades WHERE ativo = true LOOP
    INSERT INTO dados_mensais (
      unidade_id, ano, mes, alunos_pagantes, alunos_ativos, matriculas_ativas,
      matriculas_2_curso, matriculas_banda,
      novas_matriculas, evasoes,
      churn_rate, ticket_medio, taxa_renovacao, tempo_permanencia, inadimplencia
    )
    SELECT 
      v_unidade.id, p_ano, p_mes,
      (SELECT COUNT(*) FROM alunos a 
       LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
       WHERE a.unidade_id = v_unidade.id AND a.status = 'ativo' 
       AND COALESCE(a.is_segundo_curso, false) = false
       AND (tm.conta_como_pagante = true OR tm.id IS NULL))::INTEGER,
      (SELECT COUNT(*) FROM alunos 
       WHERE unidade_id = v_unidade.id AND status = 'ativo' 
```

## sync_evasao_to_dados_mensais()

```sql
CREATE OR REPLACE FUNCTION public.sync_evasao_to_dados_mensais()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_ano INT; v_mes INT; v_unidade UUID; v_count INT; v_pagantes INT;
BEGIN
  IF TG_OP = 'DELETE' THEN
    IF OLD.tipo NOT IN ('evasao', 'nao_renovacao', 'aviso_previo') THEN RETURN OLD; END IF;
    v_ano := EXTRACT(YEAR FROM OLD.data); v_mes := EXTRACT(MONTH FROM OLD.data); v_unidade := OLD.unidade_id;
  ELSE
    IF NEW.tipo NOT IN ('evasao', 'nao_renovacao', 'aviso_previo') THEN RETURN NEW; END IF;
    v_ano := EXTRACT(YEAR FROM NEW.data); v_mes := EXTRACT(MONTH FROM NEW.data); v_unidade := NEW.unidade_id;
  END IF;

  SELECT COUNT(*) INTO v_count FROM movimentacoes_admin
  WHERE unidade_id = v_unidade AND tipo IN ('evasao', 'nao_renovacao')
    AND EXTRACT(YEAR FROM data) = v_ano AND EXTRACT(MONTH FROM data) = v_mes;

  SELECT alunos_pagantes INTO v_pagantes FROM dados_mensais
  WHERE unidade_id = v_unidade
    AND ((ano = v_ano AND mes = v_mes - 1) OR (ano = v_an
```

## upsert_dados_mensais(p_unidade_codigo character varying, p_ano integer, p_mes integer, p_alunos_pagantes integer, p_novas_matriculas integer, p_evasoes integer, p_churn_rate numeric, p_ticket_medio numeric, p_taxa_renovacao numeric, p_tempo_permanencia integer, p_inadimplencia numeric, p_reajuste_parcelas numeric)

```sql
CREATE OR REPLACE FUNCTION public.upsert_dados_mensais(p_unidade_codigo character varying, p_ano integer, p_mes integer, p_alunos_pagantes integer DEFAULT NULL::integer, p_novas_matriculas integer DEFAULT NULL::integer, p_evasoes integer DEFAULT NULL::integer, p_churn_rate numeric DEFAULT NULL::numeric, p_ticket_medio numeric DEFAULT NULL::numeric, p_taxa_renovacao numeric DEFAULT NULL::numeric, p_tempo_permanencia integer DEFAULT NULL::integer, p_inadimplencia numeric DEFAULT NULL::numeric, p_reajuste_parcelas numeric DEFAULT NULL::numeric)
 RETURNS uuid
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_unidade_id UUID;
    v_id UUID;
BEGIN
    SELECT id INTO v_unidade_id FROM unidades WHERE codigo = p_unidade_codigo;
    
    INSERT INTO dados_mensais (
        unidade_id, ano, mes, alunos_pagantes, novas_matriculas, evasoes,
        churn_rate, ticket_medio, taxa_renovacao, tempo_permanencia,
        inadimplencia, reajuste_parcelas
    ) VALUES (
        v_unidade_id, p_ano
```
