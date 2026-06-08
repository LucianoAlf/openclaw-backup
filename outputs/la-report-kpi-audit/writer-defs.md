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
      AND (status IN ('ativo', 'aviso_previo') OR (status = 'inativo' AND data_saida >= v_fim));

    -- Alunos pagantes (tipos que contam como pagante)
    SELECT COUNT(*) INTO v_alunos_pagantes
    FROM alunos a
    JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
    WHERE a.unidade_id = v_unidade.id
      AND a.is_segundo_curso = false
      AND tm.conta_como_pagante = true
      AND a.data_matricula < v_fim
      AND (a.status IN ('ativo', 'aviso_previo') OR (a.status = 'inativo' AND a.data_saida >= v_fim));

    -- Matrículas ativas (total incluindo segundo curso e banda)
    SELECT COUNT(*) INTO v_matriculas_ativas
    FROM alunos
    WHERE unidade_id = v_unidade.id
      AND data_matricula < v_fim
      AND (status IN ('ativo', 'aviso_previo') OR (status = 'inativo' AND data_saida >= v_fim));

    -- Matrículas banda (tipo_matricula=5 OU curso=33)
    SELECT COUNT(*) INTO v_matriculas_banda
    FROM alunos
    WHERE unidade_id = v_unidade.id
      AND (tipo_matricula_id = 5 OR curso_id = 33)
      AND data_matricula < v_fim
      AND (status IN ('ativo', 'aviso_previo') OR (status = 'inativo' AND data_saida >= v_fim));

    -- Matrículas segundo curso
    SELECT COUNT(*) INTO v_matriculas_2_curso
    FROM alunos
    WHERE unidade_id = v_unidade.id
      AND is_segundo_curso = true
      AND data_matricula < v_fim
      AND (status IN ('ativo', 'aviso_previo') OR (status = 'inativo' AND data_saida >= v_fim));

    -- Novas matrículas no mês (excluindo segundo curso e não pagantes)
    SELECT COUNT(*) INTO v_novas_matriculas
    FROM alunos a
    JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
    WHERE a.unidade_id = v_unidade.id
      AND a.data_matricula >= v_inicio AND a.data_matricula < v_fim
      AND a.is_segundo_curso = false
      AND tm.conta_como_pagante = true;

    -- Evasões no mês
    SELECT COUNT(*) INTO v_evasoes
    FROM alunos
    WHERE unidade_id = v_unidade.id
      AND data_saida >= v_inicio AND data_saida < v_fim
      AND status = 'inativo';

    -- Churn rate
    v_churn_rate := CASE 
      WHEN v_alunos_ativos > 0 THEN ROUND(v_evasoes::numeric / v_alunos_ativos * 100, 2)
      ELSE 0 
    END;

    -- Ticket médio (média das parcelas dos pagantes ativos no fim do mês)
    SELECT COALESCE(ROUND(AVG(a.valor_parcela), 2), 0) INTO v_ticket_medio
    FROM alunos a
    JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
    WHERE a.unidade_id = v_unidade.id
      AND a.is_segundo_curso = false
      AND tm.conta_como_pagante = true
      AND a.valor_parcela > 0
      AND a.data_matricula < v_fim
      AND (a.status IN ('ativo', 'aviso_previo') OR (a.status = 'inativo' AND a.data_saida >= v_fim));

    -- UPSERT (sem faturamento_estimado e saldo_liquido pois são GENERATED)
    INSERT INTO dados_mensais (
      unidade_id, ano, mes,
      alunos_ativos, alunos_pagantes, matriculas_ativas,
      matriculas_banda, matriculas_2_curso,
      novas_matriculas, evasoes, churn_rate,
      ticket_medio
    ) VALUES (
      v_unidade.id, p_ano, p_mes,
      v_alunos_ativos, v_alunos_pagantes, v_matriculas_ativas,
      v_matriculas_banda, v_matriculas_2_curso,
      v_novas_matriculas, v_evasoes, v_churn_rate,
      v_ticket_medio
    )
    ON CONFLICT (unidade_id, ano, mes)
    DO UPDATE SET
      alunos_ativos = EXCLUDED.alunos_ativos,
      alunos_pagantes = EXCLUDED.alunos_pagantes,
      matriculas_ativas = EXCLUDED.matriculas_ativas,
      matriculas_banda = EXCLUDED.matriculas_banda,
      matriculas_2_curso = EXCLUDED.matriculas_2_curso,
      novas_matriculas = EXCLUDED.novas_matriculas,
      evasoes = EXCLUDED.evasoes,
      churn_rate = EXCLUDED.churn_rate,
      ticket_medio = EXCLUDED.ticket_medio;
  END LOOP;
END;
$function$

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
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes)
    AND tm.conta_como_pagante = true;

  SELECT COUNT(*)
  INTO v_matriculas_ativas
  FROM alunos a
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes);

  SELECT COUNT(*)
  INTO v_matriculas_banda
  FROM alunos a
  LEFT JOIN cursos c ON c.id = a.curso_id
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes)
    AND c.is_projeto_banda = true;

  SELECT COUNT(*)
  INTO v_matriculas_2_curso
  FROM alunos a
  LEFT JOIN cursos c ON c.id = a.curso_id
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes)
    AND COALESCE(a.is_segundo_curso, false) = true
    AND COALESCE(c.is_projeto_banda, false) = false;

  SELECT COUNT(*)
  INTO v_novas_matriculas
  FROM alunos a
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  LEFT JOIN cursos c ON c.id = a.curso_id
  WHERE a.unidade_id = p_unidade_id
    AND a.status IN ('ativo', 'trancado')
    AND a.data_matricula >= v_inicio_mes
    AND a.data_matricula <= v_fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > v_fim_mes)
    AND COALESCE(a.is_segundo_curso, false) = false
    AND (tm.codigo IS NULL OR tm.codigo NOT IN ('BOLSISTA_INT', 'BOLSISTA_PARC'))
    AND COALESCE(c.is_projeto_banda, false) = false
    AND (c.nome IS NULL OR c.nome NOT ILIKE '%canto coral%');

  SELECT COUNT(*)
  INTO v_evasoes
  FROM (
    SELECT DISTINCT ON (LOWER(TRIM(BOTH FROM m.aluno_nome)))
      m.id
    FROM movimentacoes_admin m
    WHERE m.unidade_id = p_unidade_id
      AND m.tipo IN ('evasao', 'nao_renovacao')
      AND m.data >= v_inicio_mes
      AND m.data < (v_fim_mes + INTERVAL '1 day')
    ORDER BY
      LOWER(TRIM(BOTH FROM m.aluno_nome)),
      m.aluno_id DESC NULLS LAST,
      m.data DESC
  ) ev;

  v_churn_rate := CASE
    WHEN COALESCE(v_alunos_pagantes, 0) > 0
    THEN ROUND((v_evasoes::numeric / v_alunos_pagantes::numeric) * 100, 2)
    ELSE 0
  END;

  INSERT INTO dados_mensais (
    unidade_id, ano, mes,
    alunos_ativos, alunos_pagantes, matriculas_ativas,
    matriculas_banda, matriculas_2_curso,
    novas_matriculas, evasoes, churn_rate,
    updated_at
  ) VALUES (
    p_unidade_id, p_ano, p_mes,
    v_alunos_ativos, v_alunos_pagantes, v_matriculas_ativas,
    v_matriculas_banda, v_matriculas_2_curso,
    v_novas_matriculas, v_evasoes, v_churn_rate,
    NOW()
  )
  ON CONFLICT (unidade_id, ano, mes) DO UPDATE SET
    alunos_ativos = EXCLUDED.alunos_ativos,
    alunos_pagantes = EXCLUDED.alunos_pagantes,
    matriculas_ativas = EXCLUDED.matriculas_ativas,
    matriculas_banda = EXCLUDED.matriculas_banda,
    matriculas_2_curso = EXCLUDED.matriculas_2_curso,
    novas_matriculas = EXCLUDED.novas_matriculas,
    evasoes = EXCLUDED.evasoes,
    churn_rate = EXCLUDED.churn_rate,
    updated_at = NOW();

  v_result := jsonb_build_object(
    'scope', 'ALUNOS_MATRICULAS_ONLY',
    'ano', p_ano,
    'mes', p_mes,
    'unidade_id', p_unidade_id,
    'alunos_ativos', v_alunos_ativos,
    'alunos_pagantes', v_alunos_pagantes,
    'matriculas_ativas', v_matriculas_ativas,
    'matriculas_banda', v_matriculas_banda,
    'matriculas_2_curso', v_matriculas_2_curso,
    'novas_matriculas', v_novas_matriculas,
    'evasoes', v_evasoes,
    'churn_rate', v_churn_rate,
    'financeiro_alterado', false
  );

  RETURN v_result;
END;
$function$

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
       AND COALESCE(is_segundo_curso, false) = false)::INTEGER,
      (SELECT COUNT(*) FROM alunos 
       WHERE unidade_id = v_unidade.id AND status = 'ativo')::INTEGER,
      (SELECT COUNT(*) FROM alunos 
       WHERE unidade_id = v_unidade.id AND status = 'ativo' 
       AND COALESCE(is_segundo_curso, false) = true)::INTEGER,
      (SELECT COUNT(*) FROM alunos a2
       LEFT JOIN cursos c ON c.id = a2.curso_id
       WHERE a2.unidade_id = v_unidade.id AND a2.status = 'ativo' 
       AND c.is_projeto_banda = true)::INTEGER,
      (SELECT COALESCE(SUM(COALESCE(quantidade, 1)), 0) FROM leads 
       WHERE unidade_id = v_unidade.id AND status IN ('matriculado','convertido')
       AND EXTRACT(YEAR FROM data_contato) = p_ano AND EXTRACT(MONTH FROM data_contato) = p_mes)::INTEGER,
      (SELECT COUNT(*) FROM movimentacoes_admin WHERE unidade_id = v_unidade.id
       AND tipo IN ('evasao', 'nao_renovacao')
       AND EXTRACT(YEAR FROM data) = p_ano AND EXTRACT(MONTH FROM data) = p_mes)::INTEGER,
      COALESCE((SELECT CASE WHEN dm_ant.alunos_pagantes > 0 
        THEN ROUND(((SELECT COUNT(*) FROM movimentacoes_admin WHERE unidade_id = v_unidade.id 
                     AND tipo IN ('evasao', 'nao_renovacao')
                     AND EXTRACT(YEAR FROM data) = p_ano AND EXTRACT(MONTH FROM data) = p_mes)::NUMERIC 
                    / dm_ant.alunos_pagantes) * 100, 2) ELSE 0 END
        FROM dados_mensais dm_ant WHERE dm_ant.unidade_id = v_unidade.id 
        AND ((dm_ant.ano = p_ano AND dm_ant.mes = p_mes - 1) OR (dm_ant.ano = p_ano - 1 AND dm_ant.mes = 12 AND p_mes = 1))
        LIMIT 1), 0),
      (SELECT COALESCE(ROUND(AVG(a3.valor_parcela), 2), 0) FROM alunos a3
       LEFT JOIN tipos_matricula tm ON tm.id = a3.tipo_matricula_id
       WHERE a3.unidade_id = v_unidade.id AND a3.status = 'ativo' 
       AND COALESCE(a3.is_segundo_curso, false) = false
       AND (tm.entra_ticket_medio = true OR tm.id IS NULL)),
      0,
      (SELECT COALESCE(ROUND(AVG(tempo_permanencia_meses), 1), 0) FROM alunos 
       WHERE unidade_id = v_unidade.id AND status = 'ativo'),
      0
    ON CONFLICT (unidade_id, ano, mes) DO UPDATE SET
      alunos_pagantes = EXCLUDED.alunos_pagantes, 
      alunos_ativos = EXCLUDED.alunos_ativos,
      matriculas_ativas = EXCLUDED.matriculas_ativas,
      matriculas_2_curso = EXCLUDED.matriculas_2_curso,
      matriculas_banda = EXCLUDED.matriculas_banda,
      novas_matriculas = EXCLUDED.novas_matriculas,
      evasoes = EXCLUDED.evasoes, churn_rate = EXCLUDED.churn_rate, 
      ticket_medio = EXCLUDED.ticket_medio,
      tempo_permanencia = EXCLUDED.tempo_permanencia, 
      updated_at = NOW();
    
    unidade_nome := v_unidade.nome;
    registros_afetados := 1;
    RETURN NEXT;
  END LOOP;
  RETURN;
END;
$function$

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
    AND ((ano = v_ano AND mes = v_mes - 1) OR (ano = v_ano - 1 AND mes = 12 AND v_mes = 1))
  LIMIT 1;

  UPDATE dados_mensais
  SET evasoes = v_count,
      churn_rate = CASE WHEN COALESCE(v_pagantes, 0) > 0 THEN ROUND((v_count::NUMERIC / v_pagantes) * 100, 2) ELSE 0 END,
      updated_at = NOW()
  WHERE unidade_id = v_unidade AND ano = v_ano AND mes = v_mes;

  RETURN COALESCE(NEW, OLD);
END;
$function$

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
        v_unidade_id, p_ano, p_mes, 
        COALESCE(p_alunos_pagantes, 0),
        COALESCE(p_novas_matriculas, 0),
        COALESCE(p_evasoes, 0),
        COALESCE(p_churn_rate, 0),
        COALESCE(p_ticket_medio, 0),
        COALESCE(p_taxa_renovacao, 0),
        COALESCE(p_tempo_permanencia, 0),
        COALESCE(p_inadimplencia, 0),
        COALESCE(p_reajuste_parcelas, 0)
    )
    ON CONFLICT (unidade_id, ano, mes) DO UPDATE SET
        alunos_pagantes = COALESCE(p_alunos_pagantes, dados_mensais.alunos_pagantes),
        novas_matriculas = COALESCE(p_novas_matriculas, dados_mensais.novas_matriculas),
        evasoes = COALESCE(p_evasoes, dados_mensais.evasoes),
        churn_rate = COALESCE(p_churn_rate, dados_mensais.churn_rate),
        ticket_medio = COALESCE(p_ticket_medio, dados_mensais.ticket_medio),
        taxa_renovacao = COALESCE(p_taxa_renovacao, dados_mensais.taxa_renovacao),
        tempo_permanencia = COALESCE(p_tempo_permanencia, dados_mensais.tempo_permanencia),
        inadimplencia = COALESCE(p_inadimplencia, dados_mensais.inadimplencia),
        reajuste_parcelas = COALESCE(p_reajuste_parcelas, dados_mensais.reajuste_parcelas),
        updated_at = NOW()
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$function$

```
