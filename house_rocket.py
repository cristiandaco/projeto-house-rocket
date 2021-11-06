import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config( layout= 'wide' )
pd.set_option('display.float_format', lambda x: '%.2f' % x)

st.title( 'Projeto House Rocket' )
st.header( 'Análise de compra e venda de imóveis em Seattle, EUA.' )
st.subheader( 'A House Rocket é uma empresa fictícia que compra e vende imóveis, e o time de negócios '
              'da empresa apresentou os seguintes problemas: ' )
st.subheader( '1) Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?' )
st.subheader( '2) Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço ?' )

@st.cache(  allow_output_mutation = True )
def get_data( path ):
    data = pd.read_csv( path )

    return data

def get_transformation( data ):
    # coluna date para to_datetime()
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # excluir outlier
    data = data[data['bedrooms'] != 33]

    #criar feature price_m2
    data['price_m2'] = data['price'] / (data['sqft_living'] * 0.093)

    # criar feature year
    data['year'] = pd.to_datetime(data['date']).dt.strftime('%Y')

    # criar feature is_waterfront
    data['is_waterfront'] = 'NA'
    data['is_waterfront'] = data['waterfront'].apply(lambda x: 'Waterfront' if x == 1 else
    'No waterfront')

    # criar feature have_basement
    data['have_basement'] = 'NA'
    data['have_basement'] = data['sqft_basement'].apply(lambda x: 'True' if x > 0 else
    'False')

    # criar feature month

    data['month'] = pd.to_datetime( data['date'] ).dt.strftime( '%m' )

    # criar feature season
    data['season'] = 'NA'
    data['season'] = data['month'].apply(lambda x: 'summer/spring' if (x >= '03') & (x <= '9') else
    'fall/winter')

    # feature recomendações de compra
    df = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    df2 = pd.merge(data, df, on='zipcode', how='inner')
    df2.rename(columns={'price_x': 'price', 'price_y': 'median_price'}, inplace=True)

    df2['status'] = 'NA'

    for i in range(len(df2)):
        if (df2.loc[i, 'price'] < df2.loc[i, 'median_price']) & (df2.loc[i, 'condition'] >= 3) & (
                df2.loc[i, 'yr_renovated'] == 0):
            df2.loc[i, 'status'] = 'buy'

        else:
            df2.loc[i, 'status'] = 'no buy'

    # feature recomendações de preço de venda
    df2['sale_price'] = 'NA'

    for i in range(len(df2)):

        if (df2.loc[i, 'season'] == 'summer/spring') & (df2.loc[i, 'status'] == 'buy'):
            df2.loc[i, 'sale_price'] = df2.loc[i, 'price'] * 1.3

        elif (df2.loc[i, 'season'] == 'fall/winter') & (df2.loc[i, 'status'] == 'buy'):
            df2.loc[i, 'sale_price'] = df2.loc[i, 'price'] * 1.1

        else:
            df2.loc[i, 'sale_price'] = 0


    # feature expectativa de lucro
    df2['profit'] = 'NA'

    for i in range(len(df2)):

        if df2.loc[i, 'sale_price'] > 0:
            df2.loc[i, 'profit'] = df2.loc[i, 'sale_price'] - df2.loc[i, 'price']

        else:
            df2.loc[i, 'profit'] = 0

    return data

def get_introduction( data ):

    st.header( 'Resumo dos Dados' )
    atributos = st.sidebar.multiselect( 'Opções de Colunas', data.columns )
    zipcode =  st.sidebar.multiselect( 'Opções de zipcode', data['zipcode'].unique() )

    if ( zipcode != [] ) & ( atributos != [] ):
        data = data.loc[data['zipcode'].isin( zipcode ), atributos]

    elif ( zipcode == [] ) & ( atributos != [] ):
        data = data.loc[:, atributos]

    elif ( zipcode != [] ) & ( atributos == [] ):
        data = data.loc[data['zipcode'].isin( zipcode ), :]

    else:
        data = data.copy()

    st.dataframe( data.head() )

    return None

def get_metrics( data ):
    #dados por zipcode
    df1 = data[['id', 'zipcode']].groupby( 'zipcode' ).count().reset_index()
    df2 = data[['price', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()

    m1 = pd.merge( df1, df2, on='zipcode', how= 'inner' )
    m2 = pd.merge( m1, df3, on='zipcode', how= 'inner' )
    df = pd.merge( m2, df4, on='zipcode', how= 'inner' )

    df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQFT_LIVING', 'PRICE/M2' ]


    #metricas estatíticas
    atributos = data.select_dtypes(include= ['int64', 'float64'])
    media = pd.DataFrame( atributos.apply( np.mean ) )
    mediana = pd.DataFrame( atributos.apply( np.median ) )
    std = pd.DataFrame( atributos.apply( np.std ) )
    max_ = pd.DataFrame( atributos.apply( np.max ) )
    min_ = pd.DataFrame( atributos.apply( np.min ) )

    df1 = pd.concat( [max_, min_, media, mediana, std], axis= 1 ).reset_index()
    df1.columns = ['ATRIBUTOS', 'MAX', 'MIN', 'MEDIA', 'MEDIANA', 'DESVIO PADRÃO']

    c1, c2 = st.columns( (2) )
    c1.header( 'Dados por zipcode' )
    c1.dataframe( df )

    c2.header( 'Métricas Estatíticas' )
    c2.dataframe( df1 )

    return None

def get_map( data ):
    #mapa dos imóveis
    houses = data[['id', 'price', 'lat', 'long']]

    mapa = px.scatter_mapbox(houses, lat='lat', lon='long',
                             size='price', color='price',
                             color_continuous_scale=px.colors.cyclical.IceFire,
                             size_max=15, zoom=9.5)

    mapa.update_layout(mapbox_style='open-street-map')
    mapa.update_layout(height=600, width=1200, margin={'r': 0, 'l': 0, 't': 0, 'b': 0})

    st.header( 'Mapa dos imóveis' )
    st.plotly_chart( mapa )

    return None

def get_plots( data ):

    st.title( 'Gráficos descritivos dos imóveis' )

    # grafico preço do imóvel por ano de construção
    min_yr_built = int( data['yr_built'].min() )
    max_yr_built = int( data['yr_built'].max() )

    st.sidebar.subheader( 'Selecione o ano de construção' )
    f_yr_built = st.sidebar.slider( 'Ano de construção',
                                    min_yr_built,
                                    max_yr_built,
                                    max_yr_built )

    df = data.loc[data['yr_built'] < f_yr_built]
    df = df[['yr_built', 'price']].groupby( 'yr_built' ).mean().reset_index()

    fig1 = px.line( df, 'yr_built', 'price' )

    #preço médio dos imóveis por dia de oferta

    df = data[['month', 'price']].groupby( 'month' ).mean().reset_index()

    fig2 = px.line(df, 'month', 'price')

    c1, c2 = st.columns( 2 )

    c1.header('Preço médio por ano de construção')
    c1.plotly_chart( fig1 )

    c2.header( 'Preço médio por mês de oferta' )
    c2.plotly_chart( fig2 )

    return None


def get_insights( data ):
    #hipotese primeira
    st.title( 'Avaliação de Hipóteses' )

    st.header('1. Imóveis que possuem vista para água, são 30% mais caros, na média.')
    st.subheader('Verdadeiro. Na verdade, imóveis com vista para água são três vezes mais caros, na média, do que imóveis sem vista para água.')

    df = data[['is_waterfront', 'price']].groupby('is_waterfront').mean().reset_index()

    no_waterfront = df[df['is_waterfront'] == 'No waterfront']['price'].mean()
    waterfront = df[df['is_waterfront'] == 'Waterfront']['price'].mean()
    diference = str(round(((100 / no_waterfront) * waterfront) - 100, 2)) + '%'

    df1 = {'no_waterfront': no_waterfront, 'waterfront': waterfront, 'price_diference': diference}
    df1 = pd.DataFrame([df1])
    st.dataframe( df1 )

    #hipotese segunda
    st.header( '2. Imóveis com data de construção inferior a 1955, são 50% mais baratos, na média.' )
    st.subheader( 'R: Falsa. Imóveis com data de construção inferior a 1955, são 1,75% mais baratos.' )

    yr_built_height = data[data['yr_built'] > 1955]['price'].mean()
    yr_built_low = data[data['yr_built'] <= 1955]['price'].mean()

    diference = str(round(((100 / yr_built_height) * yr_built_low) - 100, 2)) + '%'

    df = {'above_1955': yr_built_height, 'below_1955': yr_built_low, 'price_diference': diference}
    df = pd.DataFrame([df])
    st.dataframe( df )

    #hipotese segunda
    st.header( '3. Imóveis sem porão possuem sqft_lot 50% maiores do que imóveis com porão.' )
    st.subheader( 'R: Imóveis sem porão possuem sqft_lot 22,56% maiores do que imóveis que possuem porão. ' )

    false_basement = data[data['have_basement'] == 'False']['sqft_lot'].mean()
    true_basement = data[data['have_basement'] == 'True']['sqft_lot'].mean()
    diference = str(round(((100 / true_basement) * false_basement) - 100, 2)) + '%'

    df = {'without_basement': false_basement, 'with_basement': true_basement, 'sqft_lot_diference': diference}
    df = pd.DataFrame([df])
    st.dataframe( df )

    #hipotese quarta
    st.header( '4. O crescimento do preço dos imóveis YoY ( Year over Year ) é de 10%.' )
    st.subheader( 'R: Falsa. O crescimento do preço médio de venda dos imóveis, YoY, é de apenas 0,52%' )

    df = data[['year', 'price']].groupby('year').mean().reset_index()
    df['year'] = df['year'].astype('int64')

    year_2014 = df[df['year'] == 2014]['price'][0]
    year_2015 = df[df['year'] == 2015]['price'][1]
    diference = str(round(((100 / year_2014) * year_2015) - 100, 2)) + '%'

    df1 = {'year_2014': year_2014, 'year_2015': year_2015, 'price_diference': diference}
    df1 = pd.DataFrame([df1])

    st.dataframe( df1 )

    #hipotese quinta
    st.header( '5. Imóveis reformados com 3 banheiros são, em média, 30% mais caros do que imóveis não reformados com 3 banheiros.' )
    st.subheader( 'R: Verdadeira. Imóveis reformados, com 3 banheiros são, em média, 39,39% mais caros do que imóveis não reformados, com 3 banheiros.' )

    ren_3b = data[(data['bathrooms'] == 3) & (data['yr_renovated'] > 0)]['price'].mean()
    nren_3b = data[(data['bathrooms'] == 3) & (data['yr_renovated'] == 0)]['price'].mean()

    diference = str(round(((100 / nren_3b) * ren_3b) - 100, 2)) + '%'

    df = {'no_revovated': nren_3b, 'yes_renovated': ren_3b, 'price_diference': diference}
    df = pd.DataFrame([df])
    st.dataframe( df )

    return None

def get_recomendation( data ):
    st.title( 'Recomendações de compra e venda' )

    #recomendações de compra
    df = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    df2 = pd.merge(data, df, on='zipcode', how='inner')
    df2.rename(columns={'price_x': 'price', 'price_y': 'median_price'}, inplace=True)

    df2['status'] = 'NA'

    for i in range(len(df2)):
        if (df2.loc[i, 'price'] < df2.loc[i, 'median_price']) & (df2.loc[i, 'condition'] >= 3) & (
                df2.loc[i, 'yr_renovated'] == 0):
            df2.loc[i, 'status'] = 'buy'

        else:
            df2.loc[i, 'status'] = 'no buy'

    #recomendações do preço de venda
    df2['sale_price'] = 'NA'

    for i in range(len(df2)):

        if (df2.loc[i, 'season'] == 'summer/spring') & (df2.loc[i, 'status'] == 'buy'):
            df2.loc[i, 'sale_price'] = df2.loc[i, 'price'] * 1.3

        elif (df2.loc[i, 'season'] == 'fall/winter') & (df2.loc[i, 'status'] == 'buy'):
            df2.loc[i, 'sale_price'] = df2.loc[i, 'price'] * 1.1

        else:
            df2.loc[i, 'sale_price'] = 0

    c1, c2 = st.columns( 2 )

    c1.header('Recomendações de compra')
    c1.dataframe(df2[['id', 'zipcode', 'condition', 'yr_renovated', 'price', 'median_price', 'status']])

    c2.header('Recomendações do preço de venda')
    c2.dataframe( df2.loc[df2['sale_price'] > 0][['id', 'zipcode', 'price', 'median_price', 'status', 'sale_price']] )

    # lucro da house rocket
    st.header( 'Quanto a House Rocket pode lucrar?' )
    st.subheader( 'A House Rocket pode lucrar em média, a depender do zipcode do imóvel, U$ 107.682,02 por imóvel' )

    df2['profit'] = 'NA'

    for i in range( len( df2 ) ):

        if df2.loc[i, 'sale_price'] > 0:
            df2.loc[i, 'profit'] = df2.loc[i, 'sale_price'] - df2.loc[i, 'price']

        else:
            df2.loc[i, 'profit'] = 0

    df2['profit'] = df2['profit'].astype('int64')

    df3 = df2[df2['profit'] > 0]
    df3 = df3[['zipcode', 'profit']].groupby('zipcode').mean().reset_index()

    st.subheader( 'Lucro médio por zipcode' )
    st.dataframe( df3 )

def get_me( data ):

    st.header( 'Cristian Oliveira' )
    st.subheader( 'email: cris.oliveira.95@hotmail.com' )

    return None


if __name__ == "__main__":
    # extração
    path = 'house_rocket.csv'
    data = get_data( path )

    #transformação
    data = get_transformation( data )
    get_introduction(data)
    get_metrics( data )
    get_map( data )
    get_plots( data )
    get_insights( data )
    get_recomendation( data )
    get_me( data )