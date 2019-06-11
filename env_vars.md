## Setando variáveis de ambiente

##### Crie um bot no Telegram

<strong></strong>Observação:</strong></em> Caso você já tenha criado a application conforme o [readme do repositório da AdaBot](https://github.com/fga-eps-mds/2019.1-ADA), não é necessário criar outro. Apenas siga para o passo de exportações de variáveis do bot.

Converse com o [@BotFather do Telegram](https://t.me/BotFather) e crie um bot de teste unicamente seu seguindo as instruções dele.


##### Exporte as variáveis do seu bot

Após escolher um nome para seu bot, o @BotFather lhe dará um token para utilizar para acessar a API do Telegram. Exporte ambos no terminal como a seguir. Substitua o TELEGRAM_ACESS_TOKEN pelo token lhe enviado pelo @BotFather e TELEGRAM_BOT_NAME pelo nome do seu bot.

```sh
export ACCESS_TOKEN='TELEGRAM_ACCESS_TOKEN'
export BOT_NAME='TELEGRAM_BOT_NAME'
```
##### Exporte as variáveis do banco
Variáveis para utilização do banco de dados localmente.

```sh
export DB_NAME=api
export DB_URL=mongodb://mongo-github:27009/api
```

##### Exporte a variável para o webhook do github ser setado

Importe o seu domínio que irá receber posts do github quando pull requests, revisões de pull requests e issues ocorrerem em repositórios cadastrados no bot. Para isso é recomendado um protocolo https por razões de segurança, porém caso você não possua um domínio você também pode colocar essa variável de acordo com a rota do serviço, no caso ``` http://localhost:5000/```. Por exemplo se o seu domínio é ```https://github.meubot.com/```, a exportação ficará assim:
 
 ```sh
export GITHUB_WEBHOOK_URL=https://github.meubot.com/
```

##### Exporte o seu personal access token

Gere um personal access token, seguindo os passos a seguir:
- No seu perfil do github clique em **Developer Settings** > **Personal access tokens** e selecione **generate new token**.
- Selecione **admin:repo_hook**
- Após clique em **Generate token**

Para mais informações visite a [documntação do github](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)

Com o token gerado, realize a exportação da variável GITHUB_API_TOKEN, substituindo GITHUB_TOKEN, pelo seu token.
 
 ```sh
export GITHUB_API_TOKEN='GITHUB_TOKEN'
```

##### Crie um OAuth App no github
<strong></strong>Observação:</strong></em> Caso você já tenha criado a application conforme o [readme do repositório da AdaBot](https://github.com/fga-eps-mds/2019.1-ADA), não é necessário criar outro. Apenas siga para o passo de exportações de variáveis do app.

Crie um OAuth app no github para a Ada realizar autenticação junto aos usuários, seguindo os passos a seguir:
- No seu perfil do github clique em **Developer Settings** > **OAuth Apps** e selecione **New OAuth app**.
- No formulário de registro do app, escolha o nome do seu app e preencha os campos **Homepage URL** com as urls ```http://localhost:5015/user``` e ```http://localhost:5000/user/github/authorize``` respectivamente.
- Ao clicar em **Register application** o github irá retornar os tokens _Client id_ e _Client secret_.

Agora seu app está pronto.

Para maiores informações clique nesse [link da documentação do github](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/).


##### Exporte as variáveis do seu app
Após cadastrar um app o github irá disponibilizar dois tokens. Para a execução da Ada é necessário a exportação do Client ID e do Client Secret, ambos gerados na criação do APP. Exporte ambos no terminal como a seguir. Substitua o CLIENT_ID e o CLIENT_SECRET pelos tokens gerados pelo GitHub na criação do app.

```sh
export GITHUB_OAUTH_CLIENT_ID='CLIENT_ID'
export GITHUB_OAUTH_CLIENT_SECRET='CLIENT_SECRET'
```

##### Exporte a variável de redirecionamento para cadastro de usuários applications

URL definida para realizar o redirecionamento para o telegram assim que é cadastrado no OAuth App do github.

 ```sh
export REDIRECT_URI=http://localhost:5015/user/github/authorize/
```