# Projeto_Analises_Acoes
 
A aplicação permite selecionar empresas brasileiras cadastradas na Ibovespa, avaliar o histórico dos preços, resultados econômicos e gerar 5 cenários de previsibilidade com base na simulação de Monte Carlo.

Na página 01, é possível ter um resumo do histórico dos preços, acompanhar um gráfico de linha com a evolução diária em relação a média e mediana.

É possível analisar um histograma que mostra o % de vezes que uma ação ficou naquele range de valor (Exemplo: Ação da EmpresaYZ ficou 35% do tempo entre R$15 - R$ 20), aliado ao boxplot para identificação de outliers.

A web app exibe as taxas de retornos logaritmos mensal e anual que mostra o quanto aquela ação se valorizou/desvalorizou naquele período medido, seguido pela exibição da correlação entre IPCA, Selic e preço de fechamento e volume da ação filtrada.

Na segunda página, é possível analisar as receitas, custos e despesas e o lucro/prejuízo líquidos anuais, seu % de crescimento/redução Y&Y.

Na terceira página, a aplicação gera 5 cenários com base na simulação de Monte Carlo, no back-end, um segundo modelo é gerado com 45 dias de delay para que seja possível avaliar as previsões com os valores reais e identificar o modelo com menor mean absolute error e assim definir o melhor cenário de previsibilidade para o futuro e também projetar a taxa de retorno daquela ação selecionada.
