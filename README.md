# SchemaSpyGUI

> Interface gráfica moderna para execução, gerenciamento e automação do SchemaSpy.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **OBSERVAÇÃO**
Esta refatoração foi desenvolvida utilizando a IDE Antigravity (https://antigravity.google/)
Em algumas partes, com grandes complexidades, utilizei PROMPTs/Agentes/Copilotos aplicados no Google Gemini (https://gemini.google.com/app?hl=pt-BR)

---

# 📖 Sobre o Projeto

O **SchemaSpyGUI** é uma reescrita completa da interface gráfica originalmente utilizada para execução do SchemaSpy, porem utilizando novos conceitos e tecnologia.

O projeto foi desenvolvido com o objetivo de oferecer uma experiência moderna, intuitiva e organizada para geração da documentação de bancos de dados, simplificando o gerenciamento de projetos, conexões e execuções.

A nova arquitetura foi construída utilizando princípios modernos de engenharia de software, proporcionando maior qualidade, escalabilidade e facilidade de manutenção.

> **Importante**
>
> O SchemaSpyGUI **não substitui o SchemaSpy** e agrega valor para quem está estudando arquitetura de dados, emgenharia de software, modelagem. O principal intuito deste projeto é melhoara as minhas habilidades de desenvolvimento em Python e construçlão de PROMPTs/Agentes de IA.
>
> Ele funciona como uma interface gráfica responsável por organizar, configurar e executar o SchemaSpy de forma simplificada.

---

# 🎯 Objetivos

A reescrita possui os seguintes objetivos:

- Modernizar completamente a aplicação
- Melhorar a experiência do usuário
- Eliminar o alto acoplamento da versão anterior
- Facilitar manutenção
- Suportar múltiplos bancos de dados
- Automatizar configurações
- Organizar projetos de documentação
- Simplificar a execução do SchemaSpy
- Possibilitar futuras expansões

---

# ✨ Principais Funcionalidades

- Cadastro de Projetos
- Cadastro de Conexões
- Cadastro de Ambientes
- Execução do SchemaSpy
- Histórico de Execuções
- Armazenamento de parâmetros
- Gerenciamento de drivers JDBC
- Configuração automática das conexões
- Validação de dados
- Geração de documentação HTML
- Exportação e Importação de configurações
- Logs detalhados de execução

---

# 🏗 Arquitetura

O projeto foi desenvolvido seguindo uma arquitetura modular baseada em boas práticas de desenvolvimento.

Principais padrões utilizados:

- Clean Architecture
- SOLID
- Repository Pattern
- Service Layer
- DTO Pattern
- MVVM
- Dependency Injection
- Event Bus
- Factory Pattern

---

# 💻 Tecnologias

- Python 3.11+
- PyQt6
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- Graphviz
- Java Runtime
- SchemaSpy

---

# 📂 Estrutura do Projeto

```text
schemaspygui/
│
├── application/
│   ├── core/
│   ├── database/
│   ├── domain/
│   ├── infrastructure/
│   ├── platform/
│   └── shared/
│
├── config/
├── docs/
├── scripts/
├── tests/
└── resources/
```

---

# 🚀 Benefícios

A nova versão proporciona:

- Código desacoplado
- Alta manutenibilidade
- Organização por camadas
- Maior facilidade para testes
- Interface moderna
- Maior produtividade
- Melhor organização das configurações
- Facilidade para evolução futura

---

# 🔄 Fluxo da Aplicação

```text
Projeto
     │
     ▼
Conexão
     │
     ▼
Validação
     │
     ▼
Execução do SchemaSpy
     │
     ▼
Geração da Documentação
     │
     ▼
Histórico
```

---

# 🛠 Bancos de Dados Suportados

Atualmente a aplicação suporta:

- Oracle
- SQL Server
- PostgreSQL
- MySQL
- MariaDB
- DB2
- SQLite
- H2
- Firebird

Novos bancos poderão ser adicionados sem necessidade de alteração da arquitetura principal.

---

# 📋 Requisitos

- Python 3.11 ou superior
- Java Runtime (JRE/JDK)
- Graphviz
- SchemaSpy
- Driver JDBC correspondente ao banco de dados

---

# 📈 Roadmap

## Versão 1.0

- Interface gráfica
- CRUD de Projetos
- CRUD de Conexões
- Execução do SchemaSpy
- Histórico
- Configurações

## Versão 1.1

- Execução em lote
- Exportação de configurações
- Importação de projetos
- Atualização automática do SchemaSpy

## Versão 2.0

- Agendamento de execuções
- Plugins
- Comparação entre documentações
- Dashboard de execuções
- Relatórios

---

# 🤝 Contribuição

Contribuições são bem-vindas.

Caso encontre algum problema, abra uma Issue.

Caso queira colaborar com o desenvolvimento, envie um Pull Request.

---

# 📚 Projeto Relacionado

Durante a evolução do SchemaSpyGUI surgiu um novo projeto corporativo:

## M2DB Catalog Manager

O **M2DB Catalog Manager (Metadata, Versioning & Database Documentation Platform)** é uma plataforma independente voltada para governança e catalogação de bancos de dados.

Enquanto o **SchemaSpyGUI** permanece focado exclusivamente na execução e gerenciamento do SchemaSpy, o M2DB Catalog Manager amplia esse conceito oferecendo funcionalidades como:

- Catálogo de Metadados
- Versionamento
- Comparação de Estruturas
- Governança de Dados
- Observabilidade
- Multi-SGBD
- Inteligência Artificial
- Análise de Impacto
- Integração com CI/CD

Essa separação garante que cada projeto mantenha objetivos claros e evolua de forma independente.

---

# 📄 Licença

Este projeto é distribuído sob a licença **MIT**.

Consulte o arquivo **LICENSE** para maiores informações.

---

# 👨‍💻 Autor

**Luciano Merighetti Marwell**

Desenvolvido com foco em qualidade, arquitetura de software e governança de dados.
