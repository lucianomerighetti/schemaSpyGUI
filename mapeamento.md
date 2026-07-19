# Mapeamento De/Para: Importação de Conexões (DBeaver & Oracle SQL Developer)

Este documento estabelece o mapeamento detalhado dos campos encontrados nos arquivos de conexões JSON exportados pelo **DBeaver** e **Oracle SQL Developer** para as tabelas de banco de dados locais `tb_projeto` e `tb_conexao` do SchemaSpy GUI.

---

## 1. Origem: DBeaver (`dbeaver_*.json`)

O arquivo do DBeaver (geralmente exportado do arquivo `data-sources.json` ou recursos similares) possui um nó raiz com a chave `"connections"`, contendo um dicionário de objetos indexados pelo ID único da conexão. Os dados da conexão ficam divididos entre o nível raiz do objeto e o sub-nó `"configuration"`.

### Mapeamento para `tb_projeto`

| Campo Destino (`tb_projeto`) | Tipo do Campo | Caminho/Chaves Originais no JSON do DBeaver | Descrição / Observação |
| :--- | :--- | :--- | :--- |
| **nm_projeto** | TEXT (Unique) | `name` | O nome da conexão no DBeaver. |
| **tp_database** | TEXT | `provider` / `driver` | O provedor do banco de dados (ex: `sqlite`, `sqlserver`, `postgresql`, `mysql`, `oracle`). |
| **nm_host** | TEXT | `configuration.host` | Endereço do host/servidor do banco de dados. |
| **nm_schema** | TEXT | `configuration.database` | No SQLite ou SQL Server, representa o banco padrão; mapeado conforme contexto. |
| **nu_porta** | INTEGER | `configuration.port` | Porta numérica do serviço de banco. |
| **nm_database** | TEXT | `configuration.database` | Nome da base de dados física / arquivo. |

### Mapeamento para `tb_conexao`

| Campo Destino (`tb_conexao`) | Tipo do Campo | Caminho/Chaves Originais no JSON do DBeaver | Descrição / Observação |
| :--- | :--- | :--- | :--- |
| **nm_conexao** | TEXT | `name` | O nome da conexão (mesmo do projeto). |
| **tp_database** | TEXT | `provider` / `driver` | Provedor do banco mapeado para as chaves compatíveis. |
| **nm_host** | TEXT | `configuration.host` | Servidor/IP. |
| **nm_schema** | TEXT | `configuration.database` | Nome do banco ou pasta de arquivo. |
| **nu_porta** | INTEGER | `configuration.port` | Porta do serviço. |
| **nm_database** | TEXT | `configuration.database` | Nome da base de dados física. |
| **nm_usuario** | TEXT | `configuration.user` / `configuration.userName` | Usuário de autenticação do banco (pode vir vazio dependendo das regras locais de segurança). |
| **tx_password** | TEXT | `configuration.password` | Senha da conexão (frequentemente omitida por motivos de segurança). |
| **ds_caminho** | TEXT | `configuration.database` | Se for SQLite, armazena o caminho absoluto do arquivo. |
| **ds_jdbc_driver** | TEXT | `driver` | Nome do driver JDBC (ex: `sqlite_jdbc`, `postgres-jdbc`). |
| **ds_jdbc_url** | TEXT | `configuration.url` | A URL JDBC completa exportada ou autogerada a partir do template do banco. |

---

## 2. Origem: Oracle SQL Developer (`oracle_*.json`)

O arquivo exportado pelo Oracle SQL Developer possui um nó raiz `"connections"` contendo uma lista de objetos. Cada objeto contém dados em formato plano e chaves técnicas detalhadas contidas sob o sub-dicionário `"info"`.

### Mapeamento para `tb_projeto`

| Campo Destino (`tb_projeto`) | Tipo do Campo | Caminho/Chaves Originais no JSON do SQL Developer | Descrição / Observação |
| :--- | :--- | :--- | :--- |
| **nm_projeto** | TEXT (Unique) | `info.ConnName` / `name` | O nome da conexão/projeto. |
| **tp_database** | TEXT | `info.RaptorConnectionType` / `info.driver` / `type` | Tipo de banco (normalizado para `Oracle` de forma heurística). |
| **nm_host** | TEXT | `info.hostname` | Nome ou IP do servidor de banco de dados. |
| **nm_schema** | TEXT | `info.serviceName` | Nome do serviço de banco Oracle / Schema principal. |
| **nu_porta** | INTEGER | `info.port` | Porta de conexão (padrão: `1521`). |
| **nm_database** | TEXT | `info.serviceName` / `info.sid` | Nome do Serviço ou SID de banco de dados. |

### Mapeamento para `tb_conexao`

| Campo Destino (`tb_conexao`) | Tipo do Campo | Caminho/Chaves Originais no JSON do SQL Developer | Descrição / Observação |
| :--- | :--- | :--- | :--- |
| **nm_conexao** | TEXT | `info.ConnName` / `name` | O nome da conexão. |
| **tp_database** | TEXT | `info.RaptorConnectionType` / `info.driver` | Tipo de banco normalizado. |
| **nm_host** | TEXT | `info.hostname` | Servidor/IP. |
| **nm_schema** | TEXT | `info.serviceName` / `info.sid` / `info.database` | Mapeado para o service name ou SID. |
| **nu_porta** | INTEGER | `info.port` | Porta do banco Oracle. |
| **nm_database** | TEXT | `info.serviceName` / `info.sid` / `info.database` | Nome do Serviço ou SID de banco de dados. |
| **nm_usuario** | TEXT | `info.user` | Usuário do banco de dados (esquema Oracle). |
| **tx_password** | TEXT | `info.user` / `info.password` | Senha (salva no de/para ou vazia se não gravada). |
| **ds_caminho** | TEXT | `info.database` / `""` | Vazio para conexões Oracle padrão (não baseado em arquivo). |
| **ds_jdbc_driver** | TEXT | `info.driver` | Classe do Driver JDBC (ex: `oracle.jdbc.OracleDriver`). |
| **ds_jdbc_url** | TEXT | `info.customUrl` | A string JDBC de conexão completa (ex: `jdbc:oracle:thin:@//host:port/service`). |
