# Câmara dos Deputados API

Este projeto implementa uma API REST alternativa aos serviços atualmente
publicados pelo governo brasileiro.

> Portabilidade dos dados em andamento. Se voce não encontrar o que procura considere abrindo um
> [ticket/issue](https://github.com/thiagofelix/camara-deputados-api/issues)
> aqui no repositório explicando o caso de uso

# Como utilizar?

Atualmente a API está publicada diretamente na plataforma [Heroku](heroku.com)
acessível pelo endereço [api-camara-deputados.herokuapp.com](https://api-camara-deputados.herokuapp.com/)

Através deste endereço você pode acompanhar quais conjuntos de dados
disponibilizados atté o momento. Novos dados serão adicionados nesta página
a medida que os mesmos forem incorporados.

### Deputados

Informações detalhadas sobre todos os deputados eleitos a partir de 2003 até
data atual. Os dados são apresentados por legislatura, portanto se um deputado
foi eleito em mais de um mandato certifique-se de indicar qual legislatura você
está interessado em obter os dados

**Exemplo**

Obtem informações sobre o deputado Eduardo Cunha em todos seus mandatos:  
https://api-camara-deputados.herokuapp.com/deputados?nomeParlamentarAtual=eq.EDUARDO+CUNHA

### Presenças

Informações sobre presença dos deputados no plenário individualizado por cada
sessão. Você pode utilizar este conjunto de dados para acompanhar se o deputado
este presente ou ausente em uma determinada sessão, dia ou período de dias.

**Exemplo**

Histórico de presenca dos deputados cujo nome contendo a palavra *POPÓ*:  
https://api-camara-deputados.herokuapp.com/presencas?nomeParlamentar=like.*Popó*

### Votos

Informações sobre como o deputado votou para uma determinada proposição. 

**Exemplo**

Obtem histórico de votos todos efetuados pelo deputado Rodrigo Maia:  
https://api-camara-deputados.herokuapp.com/votos?nomeParlamentar=eq.RODRIGO+MAIA


### Buscas avançadas

Os dados acima são servidos através da ferramenta [Postgrest](postgrest.com),
para saber mais sobre os operadores de consulta e todas suas opções consulte
a [documentação oficial](http://postgrest.com/api/reading/)

## Como dados são obtidos

Os dados originais da camara dos deputados são obtidos através de dois
consumidores distintos, um dedicado ao site e outro dedicado as apis. Voce pode
encontrar o código dentro da pasta camara_deputados/spiders

## Frequência de atualizacão

Os dados serão atualizados uma vez ao dia no fim do dia. Portanto se você
precisa de uma atualização mais rápida eu sugiro utilizar os webservices
originais

## Por que uma nova API?

Apesar destes serviços representarem um grande avanço na transparência dos
dados as suas limitações listadas abaixo foram o motivo para criação da API
 Brasil Como Vota:

* Os webservices originais ocasionalmente ficam fora do ar.
* Expor os dados no formato JSON e não XML como apresentado nos webservices
  originais.
* Possibilitar uma capacidade de consulta mais avançada com novos filtros.
* Incluir dados apresentados somente no site e não nos webservices. Por
  exemplo, os dados do deputado Acelino Popó [retornados via webservice](http://www.camara.leg.br/SitCamaraWS/deputados.asmx/ObterDetalhesDeputado?ideCadastro=161907&numLegislatura=54) não contém a profissão do parlamentar,
  entretanto é possível ver a profissão através da [página do próprio
  deputado](http://www2.camara.leg.br/deputados/pesquisa/layouts_deputados_biografia?pk=193046&tipo=0)
* Aliviar carga de requisições feitas para os webservices originais. A API
  Brasil Como Vota replica os dados em um Banco de Dados próprio não sendo
  necessário chamar os serviços originais a todo momento

###Serviços originais da Camara dos Deputados

Atualmente alguns dados da camara dos deputados [são publicados na forma de
webservices](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/dados-abertos-legislativo) sendo possível acessar os seguintes banco de dados

* [Deputados](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/deputados/deputados): Disponibiliza serviços de acesso aos dados de deputados federais
* [Orgaos](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/orgaos): Disponibiliza serviços de acesso aos dados dos órgãos legislativos da Câmara dos Deputados
* [Proposicoes](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/proposicoes-1/proposicoes): Disponibiliza serviços de acesso aos dados das proposições que tramitaram ou que estão em tramitação na Câmara dos Deputados
* [SessoesReunioes](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/sessoesreunioes-2/sessoesreunioes-1): Disponibiliza serviços de acesso aos dados das sessões plenárias e das reuniões de comissões realizadas na Câmara dos Deputados
* [Comissoes](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/comissoes/comissoes): Obsoleto (Deprecated)


