# ADA GitHub API

![Ada_logo_horizontal](https://user-images.githubusercontent.com/22121504/56839465-006c8200-6859-11e9-8feb-ad76c573b844.png)
[![pipeline status](https://gitlab.com/adabot/ada-github/badges/master/pipeline.svg)](https://gitlab.com/adabot/ada-github/commits/master)
[![coverage report](https://gitlab.com/adabot/ada-github/badges/master/coverage.svg)](https://gitlab.com/adabot/ada-github/commits/master) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


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

##### Exporte seu token de acesso
Exporte seu token de acesso conforme o comando a seguir, substituindo-o em GITHUB_TOKEN.

```sh
export GITHUB_API_TOKEN='GITHUB_TOKEN'
```

##### Exporte as variáveis do banco

```sh
export DB_NAME=api
export DB_URL=mongodb://mongo-github:27009/api
```

##### Execute o Docker
Execute o Docker a partir do seguinte comando:

```sh
docker-compose -f docker-compose.yml up --build
```

## Licença

[GPL](https://opensource.org/licenses/GPL-3.0)
