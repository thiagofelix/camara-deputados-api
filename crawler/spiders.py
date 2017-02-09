# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.selector import Selector

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from datetime import date, datetime

from urlparse import urlparse, parse_qs

class ParserMixin:
    def parse_deputado_detalhes(self, res):
        self.logger.info('parsing %s', res.url)
        perfil = res.meta.get('deputado', {})
        deputados = res.xpath('//Deputado')
        item = lambda f,d: d.xpath('%s/text()' % f).extract_first('').strip()
        keys = lambda f,d: dict([(k, item(k,d)) for k in f])
        mapKeys = lambda f,d: map(lambda x: keys(f, x), d)
        foto = (
            'http://www.camara.gov.br/internet/deputado/bandep/{0}.jpg'
        )

        for deputado in deputados:
            data = {
                'matricula': perfil.get('matricula', None),
                'numLegislatura': item('numLegislatura', deputado),
                'email': item('email', deputado),
                'nomeProfissao': item('nomeProfissao', deputado),
                'dataNascimento': item('dataNascimento', deputado),
                'dataFalecimento': item('dataFalecimento', deputado),
                'ufRepresentacaoAtual': item('ufRepresentacaoAtual', deputado),
                'situacaoNaLegislaturaAtual': item('situacaoNaLegislaturaAtual', deputado),
                'ideCadastro': item('ideCadastro', deputado),
                'idParlamentarDeprecated': item('idParlamentarDeprecated', deputado),
                'nomeParlamentarAtual': item('nomeParlamentarAtual', deputado),
                'nomeCivil': item('nomeCivil', deputado),
                'sexo': item('sexo', deputado),
                'urlFoto': foto.format(item('ideCadastro', deputado)),
                'partidoAtual': keys(['idPartido','sigla','nome'], deputado.xpath('partidoAtual')),
                'gabinete': keys(['numero','anexo','telefone'], deputado.xpath('gabinete')),
                'comissoes': mapKeys([
                    'idOrgaoLegislativoCD',
                    'siglaComissao',
                    'nomeComissao',
                    'condicaoMembro',
                    'dataEntrada',
                    'dataSaida'
                ], deputado.xpath('comissoes/comissao')),
                'cargosComissoes': mapKeys([
                    'idOrgaoLegislativoCD',
                    'siglaComissao',
                    'nomeComissao',
                    'idCargo',
                    'nomeCargo',
                    'dataEntrada',
                    'dataSaida'
                ], deputado.xpath('cargosComissoes/cargoComissoes')),
                'periodosExercicio': mapKeys([
                    'siglaUFRepresentacao',
                    'situacaoExercicio',
                    'dataInicio',
                    'dataFim',
                    'idCausaFimExercicio',
                    'descricaoCausaFimExercicio',
                    'idCadastroParlamentarAnterior'
                ], deputado.xpath('periodosExercicio/periodoExercicio')),
                'historicoNomeParlamentar': item('historicoNomeParlamentar', deputado),
                'filiacoesPartidarias': item('filiacoesPartidarias', deputado),
                'historicoLider': mapKeys([
                    'idHistoricoLider',
                    'idCargoLideranca',
                    'descricaoCargoLideranca',
                    'numOrdemCargo',
                    'dataDesignacao',
                    'dataTermino',
                    'codigoUnidadeLideranca',
                    'siglaUnidadeLideranca',
                    'idBlocoPartido'
                ], deputado.xpath('historicoLider/itemHistoricoLider'))
            }

            yield data

    def parse_deputado(self, res):
        item = lambda f: res.xpath('%s/text()' % f).extract_first('').strip()

        return {
            'numLegislatura': item('numLegislatura'),
            'ideCadastro': item('ideCadastro'),
            'codOrcamento': item('codOrcamento'),
            'condicao': item('condicao'),
            'matricula': item('matricula') or item('Matricula'),
            'idParlamentar': item('idParlamentar'),
            'nome': item('nome'),
            'nomeParlamentar': item('nomeParlamentar'),
            'urlfoto': item('urlfoto'),
            'sexo': item('sexo') or item('SEXO'),
            'uf': item('uf') or item('UFEleito'),
            'partido': item('partid'),
            'gabinete': item('gabinete'),
            'anexo': item('anexo'),
            'fone': item('fone'),
            'email': item('email'),
        }

    def parse_presenca(self, res):
        self.logger.info('parsing %s', res.url)
        text = lambda f,d: d.xpath('%s/text()' % f).extract_first('').strip()
        campo = lambda f: text(f,res.xpath('/parlamentar'))
        meta = res.meta.get('deputado')

        for diaItem in res.xpath('//diasDeSessoes2/dia'):
            dia = lambda f: text(f, diaItem)

            for sessaoItem in diaItem.xpath('sessoes/sessao'):
                sessao = lambda f: text(f, sessaoItem)
                yield {
                    'ideCadastro': meta.get('ideCadastro'),
                    'matricula': meta.get('matricula'),
                    'legislatura': campo('legislatura'),
                    'carteiraParlamentar': campo('carteiraParlamentar'),
                    'nomeParlamentar': campo('nomeParlamentar'),
                    'siglaPartido': campo('siglaPartido'),
                    'siglaUF': campo('siglaUF'),
                    'data': dia('data'),
                    'frequencianoDia': dia('frequencianoDia'),
                    'justificativa': dia('justificativa'),
                    'qtdeSessoes': dia('qtdeSessoes'),
                    'descricao': sessao('descricao'),
                    'frequencia': sessao('frequencia')
                }

    def parse_votos(self, res):
        self.logger.info('parsing %s', res.url)
        deputado = res.meta.get('deputado')

        for row in res.css('.tabela-1 tr:nth-child(n+2)'):
            columns = filter(None, map(unicode.strip, row.css('td *::text').extract()))
            columns = map(lambda x: x.replace('---', ''), columns)

            if len(columns) == 3:
                proposicao = '%s %s' % (columns[0], columns[1])
                proposicao = map(unicode.strip, proposicao.split('-', 1))
                voto = columns[2]
            elif len(columns) == 2:
                proposicao = columns[0]
                voto = columns[1]

            if row.xpath('@class').extract_first() == 'even':
                sessao = columns
            else:
                [codigo, descricao] = dict(zip(['codigo', 'descricao'], proposicao))

                yield {
                    'ideCadastro'          : deputado.get('ideCadastro'),
                    'nomeParlamentarAtual' : deputado.get('nomeParlamentarAtual'),
                    'partidoAtual'         : deputado.get('partidoAtual'),
                    'numLegislatura'       : deputado.get('numLegislatura'),
                    'matricula'            : deputado.get('matricula'),
                    'data'                 : datetime.strptime(sessao[0], "%d/%m/%Y").isoformat(),
                    'sessao'               : sessao[1],
                    'frequencia'           : sessao[2],
                    'justificativa'        : sessao[3],
                    'proposicao'           : codigo,
                    'descricao'            : descricao,
                    'voto'                 : voto
                }

    def parse_votacao(self, res):
        self.logger.info('parsing %s', res.url)
        deputados = res.meta.get('deputados')
        sessao = res.css('#corpoVotacao > p *::text').extract()[2].strip()
        for deputado in deputados:
            nome = deputado.get('nomeParlamentarAtual')
            voto_xpath = "//td[contains(\
            translate(text(), 'ABCDEFGHJIKLMNOPQRSTUVWXYZ', 'abcdefghjiklmnopqrstuvwxyz'), '%s')\
            ]/../td[3]/text()" % nome.lower()

            voto = res.xpath(voto_xpath).extract_first()
            frequencia = 'Presente' if voto else 'Ausente'
            data = res.css('.grid-line .content > p::text').extract_first().strip()
            codigo, descricao = map(unicode.strip,res.css('#corpoVotacao p:nth-child(4)::text')\
                                    .extract_first('').split('-',1))

            # self.logger.info('Deputado %s' % deputado)
            yield {
                'ideCadastro'          : deputado.get('ideCadastro'),
                'nomeParlamentarAtual' : deputado.get('nomeParlamentarAtual'),
                'partidoAtual'         : deputado.get('partidoAtual'),
                'numLegislatura'       : deputado.get('numLegislatura'),
                'matricula'            : deputado.get('matricula'),
                # 'data'                 : datetime.strptime(data, "%d/%m/%Y HH:MM").isoformat(),
                'data'                 : data,
                'sessao'               : sessao,
                'frequencia'           : frequencia,
                'justificativa'        : None,
                'proposicao'           : codigo,
                'descricao'            : descricao,
                'voto'                 : voto
            }

class BaseSpider(scrapy.Spider):
    allowed_domains = ["www.camara.leg.br", "www2.camara.leg.br", "www.camara.gov.br", "www2.camara.gov.br"]
    custom_settings = {
        'RETRY_TIMES': 5
    }

    def legislatura_atual(self):
        ano_atual = datetime.now().year
        return 49 + (ano_atual-1991)/4

    def ano_legislatura(self, legislatura):
        return 2015 - ((55-int(legislatura or 55)) * 4)

    def inicio_legislatura(self, legislatura):
        return '01/02/%s' % self.ano_legislatura(legislatura)

    def fim_legislatura(self, legislatura):
        return '31/01/%s' % (self.ano_legislatura(legislatura) + 4)

    def unzip(self, filename, body):
        url = urlopen("http://www.camara.leg.br/internet/deputado/DeputadosXML_52a55.zip")
        zipfile = ZipFile(StringIO(body))
        return zipfile.open(filename).read()

class DeputadosSpider(BaseSpider, ParserMixin):
    name = "deputado"
    start_urls = [
        'http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
        'http://www.camara.leg.br/internet/deputado/DeputadosXML_52a55.zip'
    ]

    def __init__(self, nome=None, *args, **kwargs):
        self.nome = unicode(nome, 'utf-8') if nome else None
        super(DeputadosSpider, self).__init__(*args, **kwargs)

    def parse(self, res):
        self.logger.info('parsing %s', res.url)
        if '.zip' in res.url:
            xml = self.unzip('Deputados.xml', res.body)
            res = Selector(text=xml, type='xml')

        if self.nome:
            deputados = res.xpath('//*[./nomeParlamentar = "%s"]' % self.nome)
        else:
            deputados = res.xpath('//nomeParlamentar/..')

        return map(self.fetch_deputado, map(self.parse_deputado, deputados))

    def fetch_deputado(self, deputado):
        url = (
            'http://www.camara.leg.br/SitCamaraWS/'
            'deputados.asmx/ObterDetalhesDeputado'
            '?ideCadastro={0}'
            '&numLegislatura='
        )

        meta = dict(deputado=deputado)
        ideCadastro = deputado.get('ideCadastro')
        link = url.format(ideCadastro)
        return scrapy.Request(link, meta=meta,
                                callback=self.parse_deputado_detalhes)

    def parse_deputado_detalhes(self, res):
        deputados = super(DeputadosSpider, self).parse_deputado_detalhes(res)
        return map(self.process_deputado, deputados)

    def process_deputado(self, deputado):
        return deputado

class PresencaSpider(DeputadosSpider):
    name = "presenca"

    def __init__(self, data=None, dataInicio=None, dataFim=None, *args, **kwargs):
        if data == 'hoje':
            data = date.strftime(date.today(), '%d/%m/%Y')

        self.dataInicio = dataInicio or data
        self.dataFim = dataFim or data

        if data:
            data = data.split('/')
            data[0] = str(int(data[0]) + 1)
            self.dataFim = '/'.join(data)

        super(PresencaSpider, self).__init__(*args, **kwargs)

    def process_deputado(self, deputado):
        url = (
            'http://www.camara.leg.br/SitCamaraWS/'
            'sessoesreunioes.asmx/ListarPresencasParlamentar'
            '?numMatriculaParlamentar={0}'
            '&dataIni={1}'
            '&dataFim={2}'
        )

        matricula = deputado.get('matricula')
        legislatura = deputado.get('numLegislatura')
        dataInicio = self.dataInicio or self.inicio_legislatura(legislatura)
        dataFim = self.dataFim or self.fim_legislatura(legislatura)
        link = url.format(matricula, dataInicio, dataFim)
        meta = dict(deputado=deputado)
        return scrapy.Request(link, meta=meta, callback=self.parse_presenca)

class VotosSpider(DeputadosSpider):
    name = "voto"
    custom_settings = {
        'RETRY_TIMES': 5
    }

    def __init__(self, data=None, dataInicio=None, dataFim=None, *args, **kwargs):
        if data == 'hoje':
            data = date.strftime(date.today(), '%d/%m/%Y')

        self.dataInicio = dataInicio or data
        self.dataFim = dataFim or data
        super(VotosSpider, self).__init__(*args, **kwargs)

    def process_deputado(self, deputado):
        url = (
            'http://www.camara.leg.br/'
            'internet/deputado/RelVotacoes.asp'
            '?nuLegislatura={0}'
            '&nuMatricula={1}'
            '&dtInicio={2}'
            '&dtFim={3}'
        )

        matricula= deputado.get('matricula')
        legislatura = deputado.get('numLegislatura')
        dataInicio = self.dataInicio or self.inicio_legislatura(legislatura)
        dataFim = self.dataFim or self.fim_legislatura(legislatura)

        meta = dict(deputado=deputado)
        link = url.format(legislatura, matricula, dataInicio, dataFim)
        return scrapy.Request(link, meta=meta, callback=self.parse_votos)

class VotacaoSpider(DeputadosSpider):
    name = "votacao"
    kinkd = "voto"

    def __init__(self, data=None, dataInicio=None, dataFim=None, *args, **kwargs):
        if data == 'hoje':
            data = date.strftime(date.today(), '%d/%m/%Y')

        legislatura = self.legislatura_atual()
        dataInicio = dataInicio or data or self.inicio_legislatura(legislatura)
        dataFim = dataFim or data or self.fim_legislatura(legislatura)

        url = (
            'http://www.camara.leg.br/'
            'internet/votacao/default.asp'
            '?datInicial={0}'
            '&datFinal={1}'
        ).format(dataInicio, dataFim)
        self.start_urls = [url]

        super(VotacaoSpider, self).__init__(*args, **kwargs)

    def parse(self, res):
        self.logger.info('parsing %s', res.url)
        votacoes = res.css('a[href*="tipo=partido"]').xpath('@href').extract()
        votacoes = map(lambda href: 'http://www.camara.leg.br/internet/votacao/%s' % href, votacoes)
        if (len(votacoes) > 0):
            return GetDeputadosAtuais(callback=self.parse_votacoes, meta=dict(votacoes=votacoes))

    def parse_votacoes(self, deputados, meta):
        for link in meta.get('votacoes'):
            meta=dict(deputados=deputados)
            yield scrapy.Request(link, meta=meta, callback=self.parse_votacao)


class GetDeputadosAtuais(scrapy.Request, ParserMixin):
    def __init__(self, callback=None, meta=None, *args, **kwargs):
        self.client_callback=callback
        self.client_meta=meta
        super(GetDeputadosAtuais, self).__init__('http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
                                              callback=self.parse_deputados,
                                              *args, **kwargs)
    def parse_deputados(self, res):
        deputados = map(self.parse_deputado, res.xpath('//nomeParlamentar/..'))
        url = (
            'http://www.camara.leg.br/SitCamaraWS/'
            'deputados.asmx/ObterDetalhesDeputado'
            '?ideCadastro={0}'
            '&numLegislatura='
        )

        self.total_requests = 0
        self.deputados = []
        self.logger = logging.getLogger()
        requests = []

        for deputado in deputados:
            meta = dict(deputado=deputado)
            ideCadastro = deputado.get('ideCadastro')
            link = url.format(ideCadastro)
            self.total_requests += 1
            requests.append(
                scrapy.Request(link,
                               meta=meta,
                               callback=self.parse_deputado_detalhes,
                               errback=self.errback)
            )

        return requests

    def errback(self):
        self.total_requests -= 1
        if (self.total_requests== 0):
            return self.client_callback(self.deputados, self.client_meta)

    def parse_deputado_detalhes(self, res):
        deputados = super(GetDeputadosAtuais, self).parse_deputado_detalhes(res)
        for deputado in deputados:
            self.deputados.append(deputado)

        self.total_requests -= 1
        if (self.total_requests== 0):
            return self.client_callback(self.deputados, self.client_meta)
