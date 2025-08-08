# RCA SUS Website

Este diretório contém uma versão estática da plataforma de visualização de dados e metodologia do projeto **RCA SUS**. O objetivo do site é apresentar de forma acessível as ideias, dados e métodos empregados na análise de causa raiz de Síndrome Respiratória Aguda Grave (SRAG) no Brasil.

## Conteúdo

- **index.html** – Página inicial com uma descrição geral do projeto, imagem ilustrativa e links para as demais páginas.
- **data.html** – Explorador de dados com gráficos interativos que mostram os estados com maior número de casos e maior incidência em 2019, além de uma série temporal de casos diários.
- **map.html** – Mapa coroplético interativo construído com Leaflet que exibe a incidência de casos por estado e permite interações como destaque ao passar o mouse.
- **methods.html** – Breve descrição da metodologia adotada, incluindo integração de dados, técnicas de inferência causal (redes de gêmeos profundas, grafos causais) e probabilidades de causação.
- **references.html** – Lista de documentos e artigos utilizados como referência para o desenvolvimento do projeto.
- **styles.css** – Folha de estilos utilizada por todas as páginas, definindo cores, espaçamento e layout.
- **data/** – Diretório que armazena os arquivos JSON com dados agregados e o GeoJSON das unidades federativas do Brasil.
- **assets/** – Imagens utilizadas no site, incluindo a arte de capa (hero.png).

## Dependências

O site é completamente estático; os gráficos e mapas são gerados no navegador a partir de bibliotecas de terceiros hospedadas em CDNs. As principais dependências são:

- **[Chart.js](https://www.chartjs.org/)** (versão 4) – Biblioteca de gráficos utilizada para criar os gráficos de barras e linhas na página de dados.
- **[Leaflet](https://leafletjs.com/)** (versão 1.9) – Biblioteca de mapas interativos utilizada na página de mapa.
- **[OpenStreetMap](https://www.openstreetmap.org/)** – Fonte dos tiles para o mapa base.

Estas bibliotecas são carregadas via CDN, portanto é necessária conexão à internet para que o site funcione completamente.

## Uso

1. Clone ou baixe este repositório.
2. Navegue até o diretório `website/`.
3. Abra `index.html` em seu navegador preferido. Não é necessário servidor web, mas se encontrar problemas ao carregar arquivos locais (devido a restrições de CORS), execute um servidor HTTP simples. Por exemplo, com Python:

```bash
python3 -m http.server 8080
```

Em seguida, acesse `http://localhost:8080/website/index.html` no navegador.

## Dados

Os arquivos presentes em `data/` foram gerados a partir dos notebooks de análise (`analises/`) e contêm:

| Arquivo | Descrição |
| --- | --- |
| `top10_total_cases.json` | Lista de estados com maior número absoluto de casos em 2019. |
| `top10_incidence.json` | Lista de estados com maior incidência (casos por 100 mil habitantes) em 2019. |
| `daily_cases.json` | Série temporal de casos diários agregados em 2019. |
| `state_cases_2019.json` | Métricas de casos e incidência por estado usadas no mapa. |
| `brazil_states.geojson` | GeoJSON contendo os limites das unidades federativas brasileiras. |

Estes dados são lidos dinamicamente pelos scripts JavaScript presentes nas páginas. Não é necessário editá-los manualmente.

## Licença

Este website foi desenvolvido exclusivamente para fins acadêmicos e demonstrativos. As bibliotecas externas mantêm suas próprias licenças.