Passo a Passo: Instalando o Sistema Bibliotecário Felix, o pgAdmin 4 e Configurando o PostgreSQL

    Instalação do Sistema Bibliotecário Felix:
        Primeiro, faça a instalação do Sistema Bibliotecário Felix. Não o execute ainda, pois a senha usada para o sistema de gerenciamento será a mesma que será definida nos passos a seguir.

    Instalação do PostgreSQL:
        Verifique se o PostgreSQL está instalado no seu sistema. Caso não esteja, você pode instalá-lo através do site oficial PostgreSQL Downloads ou usando o gerenciador de pacotes do seu sistema operacional.
        Durante a instalação, anote a senha do usuário padrão postgres, pois será usada na aplicação e no pgAdmin.

    Instalação do pgAdmin 4:
        Acesse o site oficial do pgAdmin 4: pgAdmin 4 Downloads.
        Escolha a versão adequada para Windows e siga as instruções de instalação.
        Após a instalação, inicie o pgAdmin 4.

    Configuração do pgAdmin 4:
        Abra o pgAdmin 4 e, na tela inicial, clique com o botão direito em "Servers" e selecione "Create > Server".
        No campo "Name", insira um nome para o servidor, como Postgres.
        Na aba "Connection", preencha os campos com as configurações padrão:
            Host name/address: localhost
            Port: 5432 (porta padrão do PostgreSQL)
            Username: postgres
            Password: insira a senha que você definiu durante a instalação do PostgreSQL.

    Verificação da Conexão:
        Após configurar o servidor, clique em "Save" para salvar e conectar.
        Se a conexão for bem-sucedida, você verá o servidor listado na aba lateral do pgAdmin 4.

    Configuração da Aplicação:
        Certifique-se de que a sua aplicação está configurada para se conectar ao PostgreSQL usando as mesmas credenciais padrão:
            Host: localhost
            Porta: 5432
            Usuário: postgres
            Senha: a senha configurada durante a instalação.
            Banco de Dados: postgres.

    Execução da Aplicação:
        Com tudo configurado, sua aplicação deve ser capaz de se conectar ao PostgreSQL e operar normalmente utilizando as configurações padrão.

    Pronto!
        Você está pronto para usar o Sistema Bibliotecário Felix. Aproveite todas as funcionalidades que ele oferece para gerenciar sua biblioteca de maneira eficiente e intuitiva!