# GamerBoxd

Este projeto consiste em um site, similar ao aplicativo Letterboxd, que tem como objetivo possibilitar que seus usuários acessem uma biblioteca de jogos e criem reviews em seu perfil para eles.

Integrantes:  

Túlio Martins de Lima - 2212968  
João Marcello Amaral Lima - 2010580

## Como instalar

Este projeto é composto por duas aplicações em containers Docker:

Backend: Django REST Framework (SQLite)

Frontend: Aplicação estática servida com Nginx

As imagens já estão publicadas no Docker Hub e podem ser usadas sem necessidade do código fonte.

Antes de começar, você precisa ter instalado:

Docker Desktop / Docker Engine
Download: https://www.docker.com/products/docker-desktop/

Para verificar se está instalado corretamente:

```console
docker --version
```

### Rodar o backend

Baixe a imagem do Docker Hub:  
https://hub.docker.com/r/tulio240/progweb-frontend  
```console
docker pull tulio240/progweb-backend:latest
```

```console
docker run -d -p 8000:8000 --name progweb-backend tulio240/progweb-backend:latest  
```  

O backend estará disponível em:  

http://localhost:8000  
 

### Rodar o frontend

Baixe a imagem:    
https://hub.docker.com/r/tulio240/progweb-frontend

```console
docker pull tulio240/progweb-frontend:latest
```

Execute:  

```console
docker run -d -p 5500:80 --name progweb-frontend tulio240/progweb-frontend:latest
```

A aplicação estará disponível no navegador em:

http://localhost:5500

### Ordem de inicialização

🔄 Ordem de inicialização  

O backend precisa estar ativo antes do frontend para que as requisições funcionem corretamente:  

1️⃣ Inicie o backend  
2️⃣ Inicie o frontend  

Se qualquer um cair, você pode reiniciá-lo:  
```console
docker restart progweb-backend  
docker restart progweb-frontend  
```

## Intruções de uso

### Acesso

Para acessar o `GamerBoxd`, será necessário possuir uma conta. Para criar uma conta, basta clicar no botão de `Cadastro` indicado no final do card de login ou acessar /register.html.  

Em cadastro é preciso preencher __nome de usuário__, __email__ e __senha__. No final do processo o usuário será encaminhado para a página de `Login`.

No login basta completar com o __nome de usuário__ e a __senha__ correspondente à conta recém criada.

### Navegação

No topo da página principal, após o login, é possível acessar uma barra de navegação, que pode levar o usuário para duas páginas principais com os botões `Home` e `Perfil` ou acionar o logout pelo botão `Sair`.  

### Home

Em `Home` o usuário pode visualizar uma lista de jogos disponíveis no site. Ao clicar em um jogo, o usuário será direcionada para a página deste jogo.  

Na página de cada jogo, é possível visualizar as reviews criadas para ele, exibidas em formato de card com o nome do usuário, a nota e a descrição.  Além disso, o usuário poderá criar sua própria review para o jogo, clicando no botão disponivel acima da área de reviews.  

Em cada card de review, se o usuário clicar no nome do autor do card, será direcionado para a página de `Perfil` do usuário correspondente.

### Perfil 

Na página de `Perfil` de um usuário, se ele estiver logado terá acesso a duas coisas:

1 - __Edição de perfil__: A partir do botão no card principal, o usuário será encaminhado para a página de edição, na qual poderá enviar uma nova foto de perfil e/ou modificar sua bio. Ao clicar em "salvar alterações", o perfil será atualizado com as novas informações.  

2 - __Suas reviews__: As reviews criadas pelo usuário aparecem em uma coluna logo abaixo do card principal. Ao passar o mouse sobre uma review, dois ícones serão mostrados sobre o card: o primeiro ✏️ é referente à edição das reviews, clicando nele o usuário será encaminhado para uma página onde poderá editar a nota ou o comentário da review; o segundo ❌ é referente à deleção de reviews, clicando nele a review será excluída permanentemente.

## Relato - o que foi prometido x o que foi implementado

__Prometido__  

Conteúdo:  
Faremos, como no primeiro trabalho, um site de review de jogos, similar ao letterboxd, onde usuários podem criar uma conta e acessar sua biblioteca, nas quais adicionam reviews de jogos.  

As principais diferenças serão um incremento nos perfis, no qual usuários agora podem personalizar a própria página e visualizar os perfis de outros usuários e o uso de uma API para cadastro dos jogos no sistema.  

Usuários podem:  
- Criar uma nova conta no site  
- Acessar suas contas já criadas, utilizando email e senha.  
- Personalizar suas páginas de perfil.  
- Visitar perfis de outros usuários.  
- Visualizar suas reviews criadas na página de biblioteca.  
- Criar novas reviews  
- Editar reviews já criadas por ele  
- Deletar reviews já criadas por ele  
- Visualizar os jogos em uma página de jogos  
- Acessar a página individual de um jogo já cadastrado e visualizar as reviews atribuídas a ele (se houver).  

__Feito__  

Implementamos todas as funcionalidades prometidas.

## Link frontend

https://hub.docker.com/r/tulio240/progweb-frontend
https://github.com/ProgWeb-Trabalho2/frontend