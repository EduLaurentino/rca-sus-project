# Origem dos Dados Utilizados

Este documento descreve a origem exata dos conjuntos de dados utilizados no projeto de inferência causal aplicada à epidemiologia (Síndrome Respiratória Aguda Grave – SRAG).

## Dados de Saúde

### SIVEP‑Gripe – SRAG 2019 e 2020 (SVS/MS)

- **Fonte**: Sistema de Vigilância Epidemiológica da Gripe (SIVEP‑Gripe), coordenado pela Secretaria de Vigilância em Saúde do Ministério da Saúde do Brasil.
- **Descrição**: Base de dados contendo notificações de internações e óbitos por Síndrome Respiratória Aguda Grave (SRAG) no âmbito do Sistema Único de Saúde (SUS).
- **Local de download**: Portal OpenDataSUS. Para 2019 e 2020, os arquivos CSV foram obtidos nos seguintes endereços, respectivamente:
  - 2019: `https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2019/INFLUD19-26-06-2025.csv`
  - 2020: `https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2020/INFLUD20-26-06-2025.csv`
- **Acesso**: Dados públicos e anonimizados, publicados de forma contínua pelo Ministério da Saúde【13†L57-L66】.

### Arquivos agregados

- **aggregated_sivep_2019.csv** e **aggregated_sivep_2020.csv**: planilhas derivadas por meio de agregação do número de casos por Unidade Federativa (UF) e data de início dos sintomas, produzidas a partir dos dados originais do SIVEP‑Gripe. Esses arquivos foram gerados localmente com scripts em Python.

## Dados Demográficos e Socioeconômicos

### Estimativa Populacional 2021 (IBGE)

- **Fonte**: Instituto Brasileiro de Geografia e Estatística (IBGE).
- **Descrição**: Estimativas da população residente por Unidade da Federação em 1º de julho de 2021, publicadas no Diário Oficial da União.
- **Local de download**: Arquivo Excel `estimativa_dou_2021.xls` obtido no site do IBGE através do repositório público de estatísticas (`https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2021/`).
- **Observação**: Utilizado para calcular incidências per capita das notificações de SRAG.

## Dados Geoespaciais

### Malhas Territoriais – Unidades da Federação 2022

- **Fonte**: IBGE – Diretoria de Geociências.
- **Descrição**: Shapefile com os limites geográficos das 27 Unidades da Federação (UF) do Brasil (coordenadas em projeção SIRGAS 2000).
- **Arquivo**: `BR_UF_2022.zip`
- **Local de download**: Diretório público do IBGE (`https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_UF_2022.zip`).
- **Utilização**: Permite análises espaciais e produção de mapas coropléticos para os indicadores de SRAG.

### Malha Territorial do País 2022

- **Fonte**: IBGE – Diretoria de Geociências.
- **Descrição**: Shapefile da área total do Brasil (`BR_Pais_2022.zip`), utilizado como base cartográfica de referência.
- **Local de download**: Diretório público do IBGE no mesmo caminho das malhas de UF (`https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Pais_2022.zip`).

## Documentos de Referência

- **Ph.D in Causal Inference.pdf**: Documento descritivo do projeto de doutorado em inferência causal e epidemiologia.
- **BRACIS2025rca_Springer.pdf**: Artigo sobre técnicas de causalidade relacionado ao projeto.
- **Estimating Categorical Counterfactuals via Deep Twin Networks.pdf**: Artigo descrevendo redes gêmeas profundas para inferência contrafactual【23†L38-L44】.

## Outros Materiais

- **Dicionários de dados e documentação**: As bases do Ministério da Saúde normalmente acompanham dicionários de dados descrevendo campos e códigos. Os dicionários do SIVEP‑Gripe, SINAN e SIM podem ser consultados nos portais OpenDataSUS e TabNet (DATASUS)【13†L100-L108】【18†L123-L131】. Recomenda‑se verificar a documentação oficial para interpretação de variáveis específicas.