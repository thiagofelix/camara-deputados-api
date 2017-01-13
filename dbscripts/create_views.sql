
DROP MATERIALIZED VIEW IF EXISTS deputados;
CREATE MATERIALIZED VIEW deputados AS
 SELECT scrap_items.id,
    (scrap_items.doc ->> 'matricula'::text) AS matricula,
    (scrap_items.doc ->> 'numLegislatura'::text) AS "numLegislatura",
    (scrap_items.doc ->> 'email'::text) AS email,
    (scrap_items.doc ->> 'nomeProfissao'::text) AS "nomeProfissao",
    (scrap_items.doc ->> 'dataNascimento'::text) AS "dataNascimento",
    (scrap_items.doc ->> 'dataFalecimento'::text) AS "dataFalecimento",
    (scrap_items.doc ->> 'ufRepresentacaoAtual'::text) AS "ufRepresentacaoAtual",
    (scrap_items.doc ->> 'situacaoNaLegislaturaAtual'::text) AS "situacaoNaLegislaturaAtual",
    (scrap_items.doc ->> 'ideCadastro'::text) AS "ideCadastro",
    (scrap_items.doc ->> 'idParlamentarDeprecated'::text) AS "idParlamentarDeprecated",
    (scrap_items.doc ->> 'nomeParlamentarAtual'::text) AS "nomeParlamentarAtual",
    (scrap_items.doc ->> 'nomeCivil'::text) AS "nomeCivil",
    (scrap_items.doc ->> 'sexo'::text) AS sexo,
    (scrap_items.doc ->> 'urlFoto'::text) AS "urlFoto",
    (scrap_items.doc -> 'partidoAtual'::text) AS "partidoAtual",
    (scrap_items.doc -> 'gabinete'::text) AS gabinete,
    (scrap_items.doc -> 'comissoes'::text) AS comissoes,
    (scrap_items.doc -> 'cargosComissoes'::text) AS "cargosComissoes",
    (scrap_items.doc -> 'periodosExercicio'::text) AS "periodosExercicio",
    (scrap_items.doc -> 'historicoNomeParlamentar'::text) AS "historicoNomeParlamentar",
    (scrap_items.doc -> 'filiacoesPartidarias'::text) AS "filiacoesPartidarias",
    (scrap_items.doc -> 'historicoLider'::text) AS "historicoLider"
   FROM scrap_items
  WHERE ((scrap_items.kind)::text = 'deputado'::text);


DROP MATERIALIZED VIEW IF EXISTS presencas;
CREATE MATERIALIZED VIEW presencas AS
 SELECT presencas.id,
    (presencas.doc ->> 'ideCadastro'::text) AS "ideCadastro",
    (presencas.doc ->> 'matricula'::text) AS matricula,
    (presencas.doc ->> 'legislatura'::text) AS legislatura,
    (presencas.doc ->> 'carteiraParlamentar'::text) AS "carteiraParlamentar",
    (presencas.doc ->> 'nomeParlamentar'::text) AS "nomeParlamentar",
    (presencas.doc ->> 'siglaPartido'::text) AS "siglaPartido",
    (presencas.doc ->> 'siglaUF'::text) AS "siglaUF",
    (presencas.doc ->> 'data'::text) AS data,
    (presencas.doc ->> 'frequencianoDia'::text) AS "frequencianoDia",
    (presencas.doc ->> 'justificativa'::text) AS justificativa,
    (presencas.doc ->> 'qtdeSessoes'::text) AS "qtdeSessoes",
    (presencas.doc ->> 'descricao'::text) AS descricao,
    (presencas.doc ->> 'frequencia'::text) AS frequencia
   FROM scrap_items presencas
  WHERE ((presencas.kind)::text = 'presenca'::text);


DROP MATERIALIZED VIEW IF EXISTS votos;
CREATE MATERIALIZED VIEW votos AS
 SELECT votos.id,
    (votos.doc ->> 'ideCadastro'::text) AS "ideCadastro",
    (votos.doc ->> 'numLegislatura'::text) AS "numLegislatura",
    (votos.doc ->> 'matricula'::text) AS matricula,
    (votos.doc ->> 'nomeParlamentarAtual'::text) AS "nomeParlamentar",
    (votos.doc ->> 'justificativa'::text) AS justificativa,
    (votos.doc ->> 'proposicao'::text) AS proposicao,
    (votos.doc ->> 'descricao'::text) AS descricao,
    (votos.doc -> 'partidoAtual'::text) AS "partidoAtual",
    (votos.doc ->> 'sessao'::text) AS sessao,
    (votos.doc ->> 'url'::text) AS url,
    (votos.doc ->> 'voto'::text) AS voto,
    (votos.doc ->> 'frequencia'::text) AS frequencia,
    (votos.doc ->> 'data'::text) AS data
   FROM scrap_items votos
  WHERE ((votos.kind)::text = 'voto'::text);

