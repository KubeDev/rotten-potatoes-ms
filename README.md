# Rotten Potatoes com Microserviços

A aplicação foi construída em ***Python*** que realiza o cadastro de *reviews* para filmes cadastrados através de acesso por uma página web.

## Estrutura do projeto

Essa aplicação utiliza dois microserviços que são utilizados para acessar e atualizar os dados que serão utilizados na aplicação, são eles:

 - [Microserviço de review](https://github.com/nossadiretiva/review) - onde são armazenados os dados de review dos filmes apresentados pela aplicação
 - [Microserviço de filmes](https://github.com/nossadiretiva/movie) - onde estão cadastrados os filmes exibidos no site da aplicação

A imagem abaixo mostra como está organizada a estrutura do projeto da aplicação e seus microserviços:
![Diagrama micro serviço de reviews](https://github.com/nossadiretiva/imagens/blob/master/diagrama_aplicacao.png?raw=true)

## Configuração
São necessárias duas configurações para fazer a aplicação Rotten Potatoes ser executada, que são:

**MOVIE_SERVICE_URI** => URL de acesso ao serviço de listagem de filmes
**REVIEW_SERVICE_URI** => URL de acesso ao serviço de listagem de *reviews*

Exemplo:

    MOVIE_SERVICE_URI: http://[nome_container_microserviço_filmes]:8181
    REVIEW_SERVICE_URI: http://[nome_container_microserviço_reviews]:8282

> No caso da configuração do microserviço de *reviews* ficaria com a URL `http://[nome_container_microserviço_reviews]`, pois esse microserviço, que é executado em ***Dotnet Core***, fica exposto na porta 80

## Criando a imagem para executar o container

Foi criado dentro do projeto um arquivo  `Dockerfile`  contendo o passo-a-passo (receita de bolo) de criação da imagem  _Docker_  que posteriormente será utilizada para execução da aplicação em um container.

    FROM python:3.10.1-slim
    
    RUN pip install --upgrade pip
    
    WORKDIR /app
    
    COPY ./requirements.txt ./requirements.txt
    RUN pip3 install -r requirements.txt
    RUN pip install gunicorn
    
    COPY . .
    
    EXPOSE 5000
    
    ENV FLASK_APP=./app.py
    ENV FLASK_ENV=development
    
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

## Ignorando arquivos desnecessários na criação da imagem

No diretório da aplicação podem existir arquivos indesejados e/ou desnecessários que seriam copiados com o comando  `COPY`  e que poderiam ser ignorados durante o processo de criação da imagem  _Docker_.

Para isso foi criado no mesmo diretório onde se encontram os arquivos do projeto o arquivo  `.dockerignore`  que possui uma lista (com o mesmo padrão do arquivo  `.gitignore`) com os diretórios/arquivos que serão ignorados no momento da execução da cópia dos arquivos para dentro da imagem.

## Executando ambiente da aplicação

Como o ambiente é formado por uma [aplicação web principal](https://github.com/nossadiretiva/rotten-potatoes-ms), um [micro serviço de *review*](https://github.com/nossadiretiva/review) e um [micro serviço de filme](https://github.com/nossadiretiva/movie), a configuração deste ambiente ficou a cargo do *Docker Compose*, que se encontra no diretório da aplicação principal.

Segue abaixo o arquivo que configura o ambiente para execução pelo *Docker Compose*:

    version: '3.8'
    
    services:
      app:
        build:
          context: src
          dockerfile: Dockerfile
        container_name: movie-app
        image: nossadiretiva/movie-app:v1
        ports:
          - 5000:5000
        networks:
          - movie_network
        depends_on:
          - movie-service
          - review-service
        environment:
          MOVIE_SERVICE_URI: http://movie-service:8181
          REVIEW_SERVICE_URI: http://review-service
    
      movie-service:
        build:
          context: ../movie/src
          dockerfile: Dockerfile
        container_name: movie-service
        image: nossadiretiva/movie-service:v1
        ports:
          - 8181:8181
        networks:
          - movie_network
        depends_on:
          - mongodb
        environment:
          MONGODB_URI: mongodb://mongouser:mongopwd@mongodb-movie:27017/admin
    
      review-service:
        build:
          context: ../review/src
          dockerfile: Dockerfile
        container_name: review-service
        image: nossadiretiva/review-service:v1
        ports:
          - 8282:80
        networks:
          - movie_network
        depends_on:
          - postgresdb
        environment:
          ConnectionStrings__MyConnection: Host=postgresdb-movie;Database=review;Username=pguser;Password=Pg@123;
    
      mongodb:
        container_name: mongodb-movie
        image: mongo:5.0.5
        ports: 
          - 27017:27017
        networks:
          - movie_network
        volumes:
          - mongodb_movie_vol:/data/db
        environment:
          MONGO_INITDB_ROOT_USERNAME: mongouser
          MONGO_INITDB_ROOT_PASSWORD: mongopwd
    
      postgresdb:
        container_name: postgresdb-movie
        image: postgres:14.1-alpine
        ports: 
          - 5432:5432
        networks:
          - movie_network
        volumes:
          - postgresdb_movie_vol:/var/lib/postgresql/data
        environment:
          POSTGRES_USER: pguser
          POSTGRES_PASSWORD: Pg@123
          POSTGRES_DB: review
    
    volumes:
      mongodb_movie_vol:
      postgresdb_movie_vol:
    
    networks:
      movie_network:
        driver: bridge
