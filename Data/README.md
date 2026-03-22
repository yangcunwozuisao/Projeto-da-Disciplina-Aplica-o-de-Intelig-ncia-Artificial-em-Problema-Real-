# Dataset - Projeto IA YouTube

## Descrição Geral
Este dataset foi coletado utilizando a YouTube Data API com o objetivo de analisar comentários de vídeos e identificar padrões de comportamento dos usuários.

Os dados representam informações reais de interação em plataformas digitais e são utilizados para análise exploratória (EDA) e aplicação de técnicas de Inteligência Artificial.

---

## Estrutura dos Arquivos

### videos_clean.csv
Este arquivo contém informações estruturadas dos vídeos coletados no YouTube após o processo de limpeza e padronização dos dados.

#### Campos do dataset

- **videoId**  
  Identificador único do vídeo no YouTube.

- **title**  
  Título do vídeo publicado.

- **description**  
  Descrição do vídeo fornecida pelo criador do conteúdo.

- **channelTitle**  
  Nome do canal responsável pela publicação do vídeo.

- **publishedAt**  
  Data e hora original de publicação do vídeo (formato ISO 8601).

- **duration**  
  Duração do vídeo no formato padrão do YouTube (ISO 8601), por exemplo: PT5M30S.

- **viewCount**  
  Número total de visualizações do vídeo.

- **likeCount**  
  Número total de curtidas do vídeo.

- **commentCount**  
  Número total de comentários do vídeo.

- **duration_sec**  
  Duração do vídeo convertida para segundos (campo tratado para análise quantitativa).

- **published_date**  
  Data de publicação convertida para formato simplificado (YYYY-MM-DD), facilitando análises temporais.

---

### comments.csv

Este arquivo contém os comentários coletados dos vídeos do YouTube, sendo a principal base de dados para análise de sentimentos e extração de padrões.

#### Campos do dataset

- **videoId**  
  Identificador do vídeo ao qual o comentário está associado.

- **commentId**  
  Identificador único do comentário.

- **author**  
  Nome do usuário que publicou o comentário.

- **text**  
  Conteúdo textual do comentário (principal variável para análise de NLP).

- **likeCount**  
  Número de curtidas recebidas pelo comentário.

- **publishedAt**  
  Data e hora de publicação do comentário (formato ISO 8601).

- **isReply**  
  Indica se o comentário é uma resposta a outro comentário (True/False).

- **replyTo**  
  Identificador do comentário original ao qual este comentário responde (caso seja uma resposta).
---

### dataset_nlp.csv
Este dataset contém os dados processados após a aplicação de técnicas de Processamento de Linguagem Natural (NLP), sendo utilizado para análise de sentimentos e extração de padrões.

#### Campos do dataset

- **videoId**  
  Identificador do vídeo associado ao comentário analisado.

- **title**  
  Título do vídeo.

- **channelTitle**  
  Nome do canal do YouTube.

- **publishedAt**  
  Data de publicação do vídeo.

- **duration**  
  Duração do vídeo.

- **viewCount**  
  Número de visualizações do vídeo.

- **commentCount**  
  Número de comentários do vídeo.

- **language**  
  Idioma detectado do comentário (ex: pt, en).

- **keywords**  
  Palavras-chave extraídas automaticamente do texto.

- **sent_label**  
  Classificação do sentimento do comentário (positivo, negativo ou neutro).

- **sent_conf**  
  Grau de confiança do modelo na classificação (ex: 0.95).

- **sent_value**  
  Valor numérico do sentimento (ex: -1 negativo, 0 neutro, +1 positivo).

- **text_short**  
  Versão reduzida ou resumida do comentário original.
  Observação: dataset reduzido para testes iniciais.

---

### dataset_topics.csv
Este dataset contém os dados enriquecidos com análise de tópicos (Topic Modeling), permitindo identificar padrões semânticos nos comentários dos usuários.

#### Campos do dataset

- **videoId**  
  Identificador do vídeo associado ao comentário analisado.

- **title**  
  Título do vídeo.

- **channelTitle**  
  Nome do canal do YouTube.

- **publishedAt**  
  Data de publicação do vídeo.

- **duration**  
  Duração do vídeo.

- **viewCount**  
  Número de visualizações do vídeo.

- **commentCount**  
  Número de comentários do vídeo.

- **language**  
  Idioma detectado do comentário.

- **keywords**  
  Palavras-chave extraídas automaticamente do texto.

- **sent_label**  
  Classificação do sentimento (positivo, negativo ou neutro).

- **sent_conf**  
  Grau de confiança da classificação.

- **sent_value**  
  Valor numérico do sentimento.

- **text_short**  
  Versão resumida do comentário.

- **topic_id**  
  Identificador do tópico atribuído ao comentário.

- **topic_repr**  
  Representação textual do tópico (palavras-chave mais relevantes).
---

### dataset_brands.csv
Este dataset contém informações relacionadas à identificação de marcas e produtos mencionados nos comentários, permitindo análises voltadas ao contexto de negócio e comportamento do consumidor.

#### Campos do dataset

- **videoId**  
  Identificador do vídeo associado ao comentário.

- **title**  
  Título do vídeo.

- **channelTitle**  
  Nome do canal do YouTube.

- **language**  
  Idioma detectado do comentário.

- **viewCount**  
  Número de visualizações do vídeo.

- **brand**  
  Marca identificada no comentário (ex: Apple, Samsung).

- **model_hint**  
  Indicação do modelo do produto mencionado (ex: iPhone 15, Galaxy S23).

- **keywords**  
  Palavras-chave extraídas do comentário.

- **sent_label**  
  Classificação do sentimento (positivo, negativo ou neutro).

- **sent_value**  
  Valor numérico associado ao sentimento.

- **text_short**  
  Versão resumida do comentário original.

---

##  Origem dos Dados
Os dados foram coletados por meio da YouTube Data API (Google Developers, 2025).

---

## Pré-processamento
Os dados passaram pelas seguintes etapas:
- remoção de duplicados
- limpeza de texto
- normalização
- remoção de caracteres especiais

---

## Considerações Éticas
Os dados utilizados são públicos e foram coletados respeitando as políticas da plataforma, sendo utilizados exclusivamente para fins acadêmicos.

---

## Observação Final
Este dataset faz parte do projeto de Inteligência Artificial desenvolvido na Universidade Presbiteriana Mackenzie.
