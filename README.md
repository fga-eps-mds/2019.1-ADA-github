# ADA GitHub API

![Ada_logo_horizontal](https://user-images.githubusercontent.com/22121504/56839465-006c8200-6859-11e9-8feb-ad76c573b844.png)
[![pipeline status](https://gitlab.com/adabot/ada-github/badges/devel/pipeline.svg)](https://gitlab.com/adabot/ada-github/commits/devel)
[![coverage report](https://gitlab.com/adabot/ada-github/badges/devel/coverage.svg)](https://gitlab.com/adabot/ada-github/commits/devel) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Maintainability](https://api.codeclimate.com/v1/badges/aad68fb92205d309e799/maintainability)](https://codeclimate.com/github/fga-eps-mds/2019.1-ADA-github/maintainability)

## Sobre o Projeto

Microsserviço responsável por realizar requisições do GitHub e encaminhá-las para o [Bot](https://github.com/fga-eps-mds/2019.1-ADA).

## Contribuindo

Para colaborar com o projeto, siga o [Guia de Contribuição](https://github.com/fga-eps-mds/2019.1-ADA/blob/master/CONTRIBUTING.md)

## Executando a API localmente
#### Pré-requisitos
##### Instale o Docker
Seguindo as instruções dos links a seguir, instale o docker conforme seu sistema operacional.

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/#install-compose) (já incluído na instalação do Docker Desktop para MacOS)


#### Exporte as variáveis de ambiente
Exporte as variáveis de ambiente conforme as instruções presentes nesse [documento](/env_vars.md).

<strong><em>Antes de seguir adiante. Importante:</strong></em> As variáveis de ambiente são necessárias para o correto funcionamento da api, por isso não esqueça de exportá-las.

##### Exporte seu token de acesso
Exporte seu token de acesso conforme o comando a seguir, substituindo-o em GITHUB_TOKEN.

```sh
export GITHUB_API_TOKEN='GITHUB_TOKEN'
```


##### Execute o Docker
Execute o Docker a partir do seguinte comando:

```sh
docker-compose up --build
```

## Equipe

| Nome | Papel | GitHub | Email |
| --- | --- | --- | --- |
| Ateldy Borges Brasil Filho | Scrum Master | ateldyfilho | ateldybfilho@gmail.com |
| Bruno Oliveira Dantas | Arquiteto de Software | Brunooliveiradantas | oliveiradantas96@gmail.com |
| João Vitor Ramos de Souza | DevOps | joaovitor3 | joaovytor0@gmail.com |
| Vítor Gomes | Product Owner | vitorandos | torandoing@gmail.com |
| Caio Vinicius Fernandes de Araújo | Desenvolvedor | caiovfernandes | caiovf13@gmail.com |
| Erick Giffoni Felicíssimo | Desenvolvedor | ErickGiffoni | giffoni.erick@gmail.com |
| Guilherme Mendes Pereira | Desenvolvedor | guilherme-mendes | guimendesp12@gmail.com |
| João Pedro José Santos da Silva Guedes | Desenvolvedor | sudjoao | isudjoao@gmail.com |
| Lucas Fellipe Carvalho Moreira | Desenvolvedor | lucasfcm9 | lucasfcm9@gmail.com |


<p align="center">Engenharia de Produto de <i>Software</i> (EPS) / Métodos de Desenvolvimento de <i>Software</i> (MDS)<br /><br />
<p align="center">2019</p>
<a href="https://fga.unb.br" target="_blank"><img width="230"src="https://4.bp.blogspot.com/-0aa6fAFnSnA/VzICtBQgciI/AAAAAAAARn4/SxVsQPFNeE0fxkCPVgMWbhd5qIEAYCMbwCLcB/s1600/unb-gama.png"></a>
</p>