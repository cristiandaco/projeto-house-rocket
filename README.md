# PROJETO HOUSE ROCKET

link da solução em produção: https://house-rocket-analise.herokuapp.com/

![house_rocket_image](https://user-images.githubusercontent.com/81040797/143085318-13af98c3-5e0e-44e2-a8c1-e2f0fcb619fc.jpg)

## Problema de negócio: 
A House Rocket é uma empresa americana, sediada em Seattle, Washington. A empresa trabalha com compra e venda de imóveis, e para efetuar suas aquisições e valores de venda dos imóveis, a empresa se baseia em dados. Seguindo essas premissas, o CEO da House Rocket apresentou as seguintes requisições:
1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?
2. Uma vez a casa comprada, qual o melhor momento para vendê-la e por qual preço ?

## Premissas assumidas:
1. Os preço médio de venda dos imóveis é em Seattle é de U$ 350.000,00.
2. O preço médio de venda dos imóveis possui sazonalidade.
3. A House Rocket trabalha apenas com imóveis em boas condições.

## As 5 principais hipóteses (geração de insights):

1. Imóveis que possuem vista para água, são 30% mais caros, na média.
R: Verdadeira. Na verdade, imóveis com vista para água são três vezes mais caros, na média, do que imóveis sem vista para água.

2. Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.
R: Falsa. Imóveis com data de construção menor do que 1955, são 1,75% mais baratos.

3. Imóveis sem porão possuem sqft_lot 50% maiores do que imóveis com porão.
R: Falsa. Imóveis sem porão possuem sqft_lot 22,56% maiores do que imóveis que possuem porão. 


4. O crescimento do preço dos imóveis YoY ( Year over Year ) é de 10%.
R: Falsa. O crescimento do preço médio de venda dos imóveis, YoY, é de apenas 0,52%

5. Imóveis reformados com 3 banheiros são, em média, 30% mais caros do que imóveis não reformados com 3 banheiros.
R: Verdadeira. Imóveis reformados, com 3 banheiros são, em média, 39,39% mais caros do que imóveis não reformados, com 3 banheiros.

6. Imóveis vendidos no verão são os mais caros.
R: Falsa. Imóveis vendidos na primavera são os mais caros. Sendo 7,08% mais caros do que imóveis vendidos no inverno.

7. Imóveis construídos nos ano de 2000 a 2010 são 20% mais caros do que imóveis construídos nos anos de 1980 a 1990.
R: Falsa. Na verdade, imóveis contruídos nos anos 2000 são 7,06% mais caros do que imóveis dos anos 1980. 

## Planejamento da solução:

O problema será divido em quatro etapas:

1. Criar visualizações para responder cada uma das cinco hipoteses de negócio.
2. Construir uma tabela com recomendações de compra ou não compra de cada imóvel.
3. Construir uma tabela com recomendação de venda com acréscimo de 10% ou 30%.
4. Fornecer as hipóteses e as tabelas no streamlit.

## Resultados financeiros para o negócio. Quanto a empresa esperar lucrar com a solução?

R: Das mais de dez mil recomendações de compra, a expectativa é que a empresa lucre, em média, U$ 152.630,01 por imóvel vendido, o que pode variar, dependendo do localização do imóvel. 

## Conlusão:

O objetivo foi alcançado? Sim? Não? Por que?

O time de negócios tinha os determinados problemas a serem resolvidos: 

1) Quais são os imóveis que a House Rocket deveria comprar e por qual preço ? 

Determiandos parâmetros foram assumidos para definir quais imóveis comprar e por qual preço comprar: 1) seperar os imóveis por localidade (zipcode), obter a mediana do preço dos imóveis por zipcode e comprar apenas imóveis que se encontrem abaixo do preço mediano da respectiva localidade do imóvel. 2) os dados apresentam os imóveis separados em condições que variam de 1 a 5. Uma das premissas assumidas no início da solução foi, que, a House Rocket trabalha somente com imóveis em ótimas condições, visto isso, a recomendação de compra engloba apenas imóveis que estão com condição de 3 a 5. 3) reconhecendo que os imóveis reformados são, em media, 43,37% mais caros que imóveis não reformados, o último parâmetro utilizados na sugestão de compra, inclui apenas imóveis não reformados.

2) Uma vez a casa comprada, qual o melhor momento para vendê-la e por qual preço ?

Uma das premissas assumidas, manifesta que o preço médio de venda dos imóveis é sazonal. Conforme o ano caminha em direção aos meses mais quentes, os imóveis são vendidos por um preço médio maior do que em meses mais frios. Portanto, os imóveis foram separados por estações, e em média, o preço dos imóveis é 5,27% mais alto nas temporadas summer/spring do que nas temporadas fall/winter. Com base nisso, a sugestão é que os imóveis sejam ofertados por um preço 10% acima do preço de compra nas temporadas frias e 30% nas temporadas de calor.



Próximos passos:
O que pode ser melhorado nessa análise?
A área de Machine Learning pode oferecer recusos que apresentam melhor precisão nas recomendações de compra e venda de imóveis. O uso desse meio seria fundamental para resolver com mais exatidão a solução dos problemas aprensetados pelo time de negócio.

