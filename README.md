# Stereographer
Aplicativo para geração de estereogramas simples a partir de dados geológicos tabelados.

![image](https://github.com/FrostPredator/stereographer/assets/114439033/574ba051-804a-480f-9e18-73b319ccdbce)

## Inserindo Dados de um Arquivo
Existem duas formas de inserir dados estruturais no Stereographer:
- Manualmente na interface do programa
- A partir de uma tabela em formato .xlsx ou .csv

Caso opte por carregar os dados de uma tabela pré-existente, os componentes das medidas estruturais devem estar organizados em colunas separadas, como no exemplo abaixo:

| Afloramento | Direcao_plano_falha | Mergulho_plano_falha | Pitch_estrias_falha |
| :---------: | :-----------------: | :------------------: | :-----------------: |
|    EX01     |         270         |          30          |         25          |
|    EX02     |         285         |          30          |         20          |
|    EX03     |         275         |          35          |         25          |
|    EX04     |         280         |          35          |         25          |

**Obs:** Para arquivos CSV, você deve utilizar ponto e vírgula (;) como delimitador de campo.

Para importar a tabela com as medidas no Stereographer, clique no botão "Selecionar", na parte superior direita da interface, e escolha o arquivo.

Depois de carregar o arquivo, selecione na interface o tipo e formato de medida estrutural que você deseja representar. As opções disponíveis são:
- Planos: Strike/Dip
- Planos: Dip direction/Dip
- Linhas: Plunge/Trend
- Rakes: Strike/Dip/Pitch

Em seguida, você deve selecionar na interface as colunas da sua tabela que contêm cada componente da medida estrutural. Usando a tabela apresentada anteriormente, e considerando que tenhamos selecionado "Rakes: Strike/Dip/Pitch" para o tipo de medida, o componente "Strike" seria a coluna "Direcao_plano_falha", por exemplo.

![Pasted image 20240624134146](https://github.com/FrostPredator/stereographer/assets/114439033/58abf6d2-5540-4a64-900b-da16ec4f463b)

Note que apenas colunas contendo somente valores numéricos dentro dos intervalos a seguir aparecerão como opções para esses campos:
- Strike, Dip direction e Trend: 0 - 360
- Dip e Plunge: 0 - 90
- Pitch: -180 - 180
## Conferindo os Dados na Interface

Os dados importados aparecerão na tabela da interface do programa. Aqui você pode conferir e editar os valores de cada campo. Utilize os botões à direita da tabela para adicionar e remover linhas.

![Pasted image 20240624134629](https://github.com/FrostPredator/stereographer/assets/114439033/8385313a-7b14-4573-aecc-959ad3357ae6)

**Obs:** Números decimais (ex: 180,50) podem ser utilizados, mas você deve usar ponto (.) como separador decimal caso insira ou edite os dados manualmente na interface do Stereographer.

Note que, caso você possua células em branco ou que não sejam valores numéricos em alguma das linhas, o programa não permitirá que você gere um estereograma. Nesse caso, você deverá corrigir os dados faltantes ou não-numéricos para liberar os próximos passos.
## Estilizando os Elementos do Estereograma
Abaixo da tabela na interface, você encontrará diversas opções que permitem que você customize o que será plotado no estereograma, e como esses elementos serão estilizados. Essas opções incluem:
- Plotar grandes círculos (para planos) e definir a cor do traço desses círculos
- Plotar polos de planos ou linhas e definir a forma e cor do marcador
- Plotar a densidade de polos de planos ou linhas e definir a rampa de cores utilizadas, e mostrar ou não uma barra de escala dessa rampa de cores
- Mostrar a grade da projeção, e definir se ela será de áreas iguais ou ângulos iguais
- Definir um título para o gráfico
## Gerando o Estereograma
Caso não haja nenhum problema com os dados inseridos, o programa liberará a geração do estereograma.

O botão "Gerar novo stereonet" gera um estereograma novo, contendo apenas os dados definidos atualmente na interface do Stereographer, que pode ser salvo pelo usuário através do botão com ícone de disquete.

![Pasted image 20240624140458](https://github.com/FrostPredator/stereographer/assets/114439033/054a021e-309b-4fe3-8913-a02d14d2b814)

Depois de gerar um estereograma inicial, um botão com o símbolo "+" também será liberado na parte inferior direita da interface do programa. Esse botão permite que você adicione novas medidas ao último estereograma que foi gerado.

Essa função é útil caso você tenha múltiplas estruturas em uma área e queira representá-las no mesmo estereograma, com símbolos e cores distintas. No estereograma abaixo, por exemplo, os círculos pretos representam polos de planos de foliação metamórfica, com contornos de densidade em tons de azul, enquanto os losangos vermelhos representam eixos de dobras de crenulação.

![Pasted image 20240624140919](https://github.com/FrostPredator/stereographer/assets/114439033/84bbb740-fc67-4657-a585-eb64cefc75cf)
