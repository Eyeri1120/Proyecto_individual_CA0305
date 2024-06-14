# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:27:20 2024

@author: Eyeri Méndez
"""

import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from dash import dcc, html, Output, Input

class GenerarGraficos:
    
    # Constructor
    def __init__(self, app):
        
        """
        Constructor de la clase GenerarGraficos. Inicializa una nueva instancia
        de esta clase.

        Parameters:
        -----------
        app: dash.Dash
             Instancia de la aplicación Dash que se va a personalizar
             
        Returns:
        --------
        None
        """
        
        self.__app = app
        
        if self.__app.layout is None:
        
            self.__app.layout = html.Div([
                
                html.H1('Aplicación Dash'),
                
                html.A('Ver HTML', href='/html', target = '_blank'),
                
                html.Div(id = 'contenido_graficos')
                
                ])
        
        # Lista de colores para los gráficos
        self.__colores = [{'label': 'Azul', 'value': 'blue'}, 
                          {'label': 'Rojo', 'value': 'red'}, 
                          {'label': 'Amarillo', 'value': 'yellow'}, 
                          {'label': 'Verde', 'value': 'green'}, 
                          {'label': 'Naranja', 'value': 'orange'}, 
                          {'label': 'Morado', 'value': 'purple'}]
        
        # Lista de temas para los gráficos
        self.__temas = [{'label': 'Plotly', 'value': 'plotly'}, 
                        {'label': 'Plotly Blanco', 'value': 'plotly_white'}, 
                        {'label': 'Plotly Oscuro', 'value': 'plotly_dark'}, 
                        {'label': 'ggplot2', 'value': 'ggplot2'}, 
                        {'label': 'Seaborn', 'value': 'seaborn'}, 
                        {'label': 'Blanco Simple', 'value': 'simple_white'}, 
                        {'label': 'Presentación', 'value': 'presentation'}, 
                        {'label': 'X Grid Apagado', 'value': 'xgridoff'}, 
                        {'label': 'Y Grid Apagado', 'value': 'ygridoff'}, 
                        {'label': 'Grid Encendido', 'value': 'gridon'}]
        
        # Lista de metodos para imputar los valores nulos
        self.__metodos = [{'label': 'Promedio', 'value': 'mean'}, 
                          {'label': 'Mediana', 'value': 'median'}, 
                          {'label': 'Máximo', 'value': 'max'}, 
                          {'label': 'Mínimo', 'value': 'min'}]
        
    # Get app
    @property
    def app(self):
        
        """
        Obtiene la instancia actual de la aplicación.
        
        Parameters:
        -----------
        None

        Returns:
        --------
            object: Instancia de la aplicación almacenada en el atributo 
            privado '__app'.
        """
        
        return self.__app
    
    # Set app
    @app.setter
    def app(self, nueva_app):
        
        """
        Establece una nueva instancia de la aplicación y configura su layout si 
        aún no está definido (si la aplicación está vacía).

        Parameters:
        -----------
        nueva_app : dash.Dash
                    Nueva instancia de la aplicación Dash a ser establecida.
                    
        Returns:
        --------
        None
        """
        
        self.__app = nueva_app
        
        if self.__app.layout is None:
        
            self.__app.layout = html.Div([
                
                html.H1('Aplicación Dash'),
                
                html.A('Ver HTML', href='/html', target = '_blank'),
                
                html.Div(id = 'contenido_graficos')
                
                ])

    # str
    def __str__(self):
        
        '''
        Devuelve una representación legible en forma de cadena de la
        instancia de la clase
               
        Returns
        -------
            str: Texto que describe los atributos de la instancia.
        '''
        
        return 'App actual: Aplicación Dash'
    
    # Crear un gráfico de barras
    def barras(self, df, variable_x, variable_y = False, 
               nombres_categorias = False, nombres_ejes = False):
        
        """
        Método que crea un gráfico de barras agrupadas interactivo en la app 
        actual usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str, opcional
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y. Si no se proporciona, se contará la 
                    frecuencia de los valores de 'variable_x'. Por defecto es False.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para las categorías de la variable_x. 
                            Si no se proporciona, se utilizarán los nombres de las 
                            categorías originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
                      
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de barras
        al layout de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_x])
        
        categorias = list(df[variable_x].unique())
    
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([
                        
                        html.Label('Color:'),
                        dcc.Dropdown(options = self.__colores, value = 'blue', 
                                     id = 'color_barras')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_barras')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_barras', 
                                  placeholder = 'Ingrese el título del gráfico', 
                                  style = {'width': '100%'})], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Label('Frecuencia:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Frecuencia'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_barras')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),

                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'grafico_barras')
            ])
        )
    
        @self.__app.callback(
    
            Output('grafico_barras', 'figure'),
            Input('color_barras', 'value'),
            Input('tema_barras', 'value'),
            Input('titulo_barras', 'value'),
            Input('checklist_barras', 'value')
    
        )
        def grafico_barras(color, tema, titulo, frecuencia):
    
            if not nombres_categorias:
                
                nombres = categorias
                
            else:
                
                nombres = dict(zip(categorias, nombres_categorias))
    
            if not nombres_ejes:
                
                nombre_x = variable_x
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'count'
                
                else:
                    
                    nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'Frecuencia'
                    
                else:
                
                    nombre_y = nombres_ejes[1]
                
            if frecuencia or not variable_y:
                
                fig = px.bar(df.replace({variable_x: nombres}),
                             x = variable_x)
                
            else:
    
                fig = px.bar(df.replace({variable_x: nombres}),
                             x = variable_x, y = variable_y)
    
            fig.update_layout(
    
                xaxis_title = nombre_x,
                yaxis_title = nombre_y,
                title = titulo if titulo else 'Gráfico de barras',
                template = tema
    
            )
    
            fig.update_traces(marker = dict(color = color))
    
            return fig

    # Crear un gráfico de barras agrupadas
    def barras_agrupadas(self, df, variable_x, variable_y = False, variable_agrupar = False, 
                         nombres_categorias = False, nombres_ejes = False, 
                         nombres_leyendas = False):
        
        """
        Método que crea un gráfico de barras agrupadas interactivo en la app 
        actual usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str, opcional
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y. Si no se proporciona, se contará la 
                    frecuencia de los valores de 'variable_x'. Por defecto es False.
                    
        variable_agrupar: str
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar las barras.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para reemplazar los valores únicos 
                            de 'variable_x' en el gráfico. Si no se proporciona, 
                            se utilizarán los valores únicos originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de barras agrupadas
        al layout de la aplicación Dash.
        """
       
        df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_x].unique())
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_barras_agrupadas')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_barras_agrupadas', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([
                
                        html.Label('Frecuencia'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Frecuencia'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_barras_agrupadas')], 
                         
                         style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
                
                dcc.Graph(id = 'grafico_barras_agrupadas')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('grafico_barras_agrupadas', 'figure'),
            Input('tema_barras_agrupadas', 'value'),
            Input('titulo_barras_agrupadas', 'value'),
            Input('checklist_barras_agrupadas', 'value')
            
        )
        def grafico_barras_agrupadas(tema, titulo, frecuencia):
            
            if not nombres_categorias:
                
                nombres = categorias
                
            else:
                
                nombres = dict(zip(categorias, nombres_categorias))
                
            if not nombres_ejes:
                
                nombre_x = variable_x
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'count'
                
                else:
                    
                    nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'Frecuencia'
                
                else:
                    
                    nombre_y = nombres_ejes[1]
                
            if frecuencia or not variable_y:
                
                fig = px.bar(df.replace({variable_x: nombres}), 
                             x = variable_x, color = variable_agrupar,
                             title = titulo if titulo else 'Gráfico de barras agrupadas',
                             barmode = 'group')
                
            else:
                
                fig = px.bar(df.replace({variable_x: nombres}), 
                             x = variable_x, y = variable_y, color = variable_agrupar,
                             title = titulo if titulo else 'Gráfico de barras agrupadas',
                             barmode = 'group')
            
            if nombres_leyendas:
                
                titulo_leyenda = nombres_leyendas[0]
                
                categorias_leyendas = df[variable_agrupar].unique()
                
                labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
            
                fig.for_each_trace(lambda t: t.update
                               (name = labels_leyendas[t.name]))
                
            else:
                
                titulo_leyenda = variable_agrupar
            
            fig.update_layout(
                
                xaxis_title = nombre_x,
                yaxis_title = nombre_y,
                legend_title_text = titulo_leyenda,
                template = tema
                
            )
            
            return fig
        
    # Crear un gráfico de barras apiladas
    def barras_apiladas(self, df, variable_x, variable_y = False, variable_agrupar = False,
                        nombres_categorias = False, nombres_ejes = False, 
                        nombres_leyendas = False):
        
        """
        Método que crea un gráfico de barras apiladas interactivo en la app actual 
        usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str, opcional
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y. Si no se proporciona, se contará la 
                    frecuencia de los valores de 'variable_x'. Por defecto es False.
                    
        variable_agrupar: str
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar las barras.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para reemplazar los valores únicos 
                            de 'variable_x' en el gráfico. Si no se proporciona, 
                            se utilizarán los valores únicos originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de barras apiladas
        al layout de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_x].unique())
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_barras_apiladas')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_barras_apiladas', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([
                
                        html.Label('Frecuencia'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Frecuencia'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_barras_apiladas')], 
                         
                         style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
                
                dcc.Graph(id = 'grafico_barras_apiladas')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('grafico_barras_apiladas', 'figure'),
            Input('tema_barras_apiladas', 'value'),
            Input('titulo_barras_apiladas', 'value'),
            Input('checklist_barras_apiladas', 'value'),
            
        )
        def grafico_barras_apiladas(tema, titulo, frecuencia):
            
            if not nombres_categorias:
                
                nombres = categorias
                
            else:
                
                nombres = dict(zip(categorias, nombres_categorias))
                
            if not nombres_ejes:
                
                nombre_x = variable_x
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'count'
                
                else:
                    
                    nombre_y = variable_y
                
                
            else:
                
                nombre_x = nombres_ejes[0]
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'Frecuencia'
                
                else:
                    
                    nombre_y = nombres_ejes[1]
                
            if frecuencia or not variable_y:
                
                fig = px.bar(df.replace({variable_x: nombres}), 
                             x = variable_x, color = variable_agrupar,
                             title = titulo if titulo else 'Gráfico de barras apiladas',
                             barmode = 'stack')
                
            else:

                fig = px.bar(df.replace({variable_x: nombres}), 
                             x = variable_x, y = variable_y, color = variable_agrupar,
                             title = titulo if titulo else 'Gráfico de barras apiladas',
                             barmode = 'stack')
            
            if nombres_leyendas:
                
                titulo_leyenda = nombres_leyendas[0]
                
                categorias_leyendas = df[variable_agrupar].unique()
                
                labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
            
                fig.for_each_trace(lambda t: t.update
                               (name = labels_leyendas[t.name]))
                
            else:
                
                titulo_leyenda = variable_agrupar
            
            fig.update_layout(
                
                xaxis_title = nombre_x,
                yaxis_title = nombre_y,
                legend_title_text = titulo_leyenda,
                template = tema
                
            )
            
            return fig
        
    # Crear un histograma
    def histograma(self, df, variable_x, variable_y = False, variable_agrupar = False,
                   nombres_categorias = False, nombres_ejes = False):
        
        """
        Método que crea un histograma interactivo en la app actual usando el 
        dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str, opcional
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y. Si no se proporciona, se contará la 
                    frecuencia de los valores de 'variable_x'. Por defecto es False.
                    
        variable_agrupar: str
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el histograma según las categorías de dicha columna.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para reemplazar los valores únicos 
                            de 'variable_agrupar' en el gráfico. Si no se proporciona, 
                            se utilizarán los valores únicos originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
                      
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el histograma al layout 
        de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_agrupar].unique())
        
        if not nombres_categorias:
            
            nombres = categorias
            
        else:
            
            nombres = []
            
            for nombre, categoria in zip(nombres_categorias, categorias):
    
                nombres.append({'label': nombre, 'value': categoria})
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([
                        
                        html.Label('Categoría:'),
                        dcc.Dropdown(options = nombres, value = categorias[0], 
                                     id = 'categorias_histograma')],
                        
                        style = {'display': 'inline-block', 'width': '18%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Color:'),
                        dcc.Dropdown(options = self.__colores, value = 'blue', 
                                     id = 'color_histograma')], 
                        
                        style = {'display': 'inline-block', 'width': '18%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_histograma')], 
                        
                        style = {'display': 'inline-block', 'width': '18%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_histograma', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '18%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Label('Frecuencia:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Frecuencia'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_histograma')], 
                        
                        style = {'display': 'inline-block', 'width': '18%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Número de bins:'),
                        dcc.Slider(id = 'numero_bins', min = 5, max = 50, step = 1, 
                                   value = 10, marks = {i: str(i) for i in range(5, 51, 5)})],
                         
                         style = {'display': 'inline-block', 'width': '80%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'histograma')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('histograma', 'figure'),
            Input('categorias_histograma', 'value'),
            Input('color_histograma', 'value'),
            Input('tema_histograma', 'value'),
            Input('titulo_histograma', 'value'),
            Input('checklist_histograma', 'value'),
            Input('numero_bins', 'value')
            
        )
        def grafico_histograma(categoria, color, tema, titulo, frecuencia, bins):
            
            df_filtrado = df[df[variable_agrupar] == categoria]
            
            if frecuencia or not variable_y:
                
                fig = px.histogram(df_filtrado, x = variable_x, nbins = bins,
                                   title = titulo if titulo else 'Histograma')
                
            else:

                fig = px.histogram(df_filtrado, x = variable_x, y = variable_y,
                                   title = titulo if titulo else 'Histograma',
                                   nbins = bins)
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'count'
                    
                else:
                    
                    nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                
                if frecuencia or not variable_y:
                    
                    nombre_y = 'Frecuencia'
                    
                else:
                    
                    
                    nombre_y = nombres_ejes[1]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y,
                              bargap = 0.1, bargroupgap = 0.1,
                              template = tema)

            fig.update_traces(marker = dict(
                
                color = color, line = dict(color = 'black', width = 0.5)
                
                ))
            
            return fig

    # Crear un gráfico de dispersión
    def dispersion(self, df, variable_x, variable_y, variable_agrupar = False,
                   nombres_ejes = False, nombres_leyendas = False, 
                   nombres_cols = False):
        
        """
        Método que crea un gráfico de dispersión interactivo en la app actual 
        usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y.
                    
        variable_agrupar: str, opcional
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el gráfico. Si no se proporciona, no se 
                          categorizarán los datos en diferentes colores. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        nombres_cols: list, opcional
                      Lista con los nombres de las columnas numéricas del dataframe. 
                      Si no se proporciona, se utilizarán los nombres originales 
                      de las columnas numéricas. Por defecto es False.
                      
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de dispersión 
        al layout de la aplicación Dash.
        """
        
        if variable_agrupar:
            
            df = df.dropna(subset = [variable_agrupar])
        
        cols = df.select_dtypes(include = ['int', 'float']).columns.tolist()
        
        if not nombres_cols:
            
            nombres =  cols
            
        else:
            
            nombres = []
            
            for nombre, columna in zip(nombres_cols, cols):
    
                nombres.append({'label': nombre, 'value': columna})
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                        
                    html.Div([
                            
                        html.Label('Tamaño:'),
                        dcc.Dropdown(options = nombres, value = '', 
                                         id = 'tamanno_dispersion')],
                            
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([
                            
                        html.Label('Agrupar por:'),
                        dcc.Dropdown(options = nombres, value = '', 
                                         id = 'cols_dispersion')],
                            
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_dispersion')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_dispersion')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),

                    html.Div([

                        html.Br(),
                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_dispersion', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '25%', 'padding': '0 1%'}),

                    html.Div([
                        
                        html.Br(),
                        html.Label('Regresión Lineal:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Regresión Lineal'}], 
                                      value = [], inline = True, 
                                      id = 'checklist1_dispersion')], 
                        
                        style = {'display': 'inline-block', 'width': '15%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Categorizar:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Categorizar'}], 
                                      value = ['Categorizar'], inline = True, 
                                      id = 'checklist2_dispersion')], 
                        
                        style = {'display': 'inline-block', 'width': '15%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'dispersion')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('dispersion', 'figure'),
            Input('tamanno_dispersion', 'value'),
            Input('cols_dispersion', 'value'),
            Input('tema_dispersion', 'value'),
            Input('imputar_nan_dispersion', 'value'),
            Input('titulo_dispersion', 'value'),
            Input('checklist1_dispersion', 'value'),
            Input('checklist2_dispersion', 'value')
            
        )
        def grafico_dispersion(categoria, columna, tema, metodo, titulo, regresion, categorizar):
            
            copia_df = df.copy()
            
            if metodo:
                
                if not df[variable_x].dtype in ['category', 'object']:
                
                    operaciones = {
                        
                        'mean': [copia_df[variable_x].mean(), 
                                 copia_df[variable_y].mean()],
                        
                        'median': [copia_df[variable_x].median(), 
                                   copia_df[variable_y].median()],
                        
                        'max': [copia_df[variable_x].max(), 
                                 copia_df[variable_y].max()],
                        
                        'min': [copia_df[variable_x].min(), 
                                copia_df[variable_y].min()]
                        
                    }
                    
                    copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo][0])
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo][1])
                    
                else:
                    
                    operaciones = {
                        
                        'mean': copia_df[variable_y].mean(),
                        
                        'median': copia_df[variable_y].median(),
                        
                        'max': copia_df[variable_y].max(),
                        
                        'min': copia_df[variable_y].min()
                        
                    }
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo])

            if categoria:
                
                tamanno = categoria
                
                copia_df = copia_df.dropna(subset = [categoria])
                
            else:
                
                tamanno = None
                
            if regresion:
                
                regression = 'ols'
                
            else:
                
                regression = None
                
            if columna:
                
                if nombres_cols:
                    
                    titulo_columna = next(item['label'] for item in nombres if item['value'] == columna)
                    
                else:
                    
                    titulo_columna = columna
                    
                if not categorizar or not variable_agrupar:
                    
                    fig = px.scatter(copia_df, x = variable_x, y = variable_y, template = tema,
                                     color = px.Constant('All Points'), size = tamanno, 
                                     trendline = regression,
                                     title = titulo if titulo else 'Gráfico de dispersión')
                    
                    fig.update_layout(showlegend = False)
                        
                else:
                    
                    fig = px.scatter(copia_df, x = variable_x, y = variable_y, template = tema,
                                 color = columna, size = tamanno, trendline = regression,
                                 title = titulo if titulo else 'Gráfico de dispersión')
                    
                    fig.update_layout(coloraxis_colorbar = dict(title = titulo_columna))
                
            else:
                
                if not categorizar or not variable_agrupar:
                    
                    fig = px.scatter(copia_df, x = variable_x, y = variable_y, template = tema,
                                     color = px.Constant('All Points'), size = tamanno, 
                                     trendline = regression,
                                     title = titulo if titulo else 'Gráfico de dispersión')
                    
                    fig.update_layout(showlegend = False)
                    
                    
                    
                else:
                
                    fig = px.scatter(copia_df, x = variable_x, y = variable_y, template = tema,
                                 color = variable_agrupar, size = tamanno, trendline = regression,
                                 title = titulo if titulo else 'Gráfico de dispersión')
                    
                    if not nombres_leyendas:
                        
                        titulo_leyenda = variable_agrupar
                        
                    else:
                        
                        titulo_leyenda = nombres_leyendas[0]
        
                    fig.update_layout(legend_title_text = titulo_leyenda)
                    
                    if nombres_leyendas:
                            
                        categorias_leyendas = df[variable_agrupar].unique()
                            
                        labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
                        
                        fig.for_each_trace(lambda t: t.update
                                           (name = labels_leyendas[t.name]))
                
            if not nombres_ejes:
                    
                nombre_x = variable_x
                nombre_y = variable_y
                    
            else:
                    
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]
                
            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y)
            
            return fig

    # Crear un gráfico de líneas
    def lineas(self, df, variable_x, variable_y, variable_agrupar,
               nombres_ejes = False, nombres_leyendas = False):
        
        """
        Método que crea un gráfico de líneas interactivo en la app actual 
        usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y.
                    
        variable_agrupar: str
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el gráfico.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de líneas
        al layout de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_agrupar])
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_lineas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_lineas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_lineas', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Label('Marcadores:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Marcadores'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_lineas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'lineas')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('lineas', 'figure'),
            Input('tema_lineas', 'value'),
            Input('imputar_nan_lineas', 'value'),
            Input('titulo_lineas', 'value'),
            Input('checklist_lineas', 'value')
            
        )
        def grafico_lineas(tema, metodo, titulo, marcadores):
            
            copia_df = df.copy()
            
            if metodo:
                
                if not df[variable_x].dtype in ['category', 'object']:
                
                    operaciones = {
                        
                        'mean': [copia_df[variable_x].mean(), 
                                 copia_df[variable_y].mean()],
                        
                        'median': [copia_df[variable_x].median(), 
                                   copia_df[variable_y].median()],
                        
                        'max': [copia_df[variable_x].max(), 
                                 copia_df[variable_y].max()],
                        
                        'min': [copia_df[variable_x].min(), 
                                copia_df[variable_y].min()]
                        
                    }
                    
                    copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo][0])
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo][1])
                    
                else:
                    
                    operaciones = {
                        
                        'mean': copia_df[variable_y].mean(),
                        
                        'median': copia_df[variable_y].median(),
                        
                        'max': copia_df[variable_y].max(),
                        
                        'min': copia_df[variable_y].min()
                        
                    }
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo])
            
            if marcadores:
                
                marks = True
            
            else:
                
                marks = False
                
            
            
            fig = px.line(copia_df, x = variable_x, y = variable_y, 
                          color = variable_agrupar, markers = marks,
                          title = titulo if titulo else 'Gráfico de líneas')
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]
                
            if not nombres_leyendas:
                
                titulo_leyenda = variable_agrupar
                
            else:
                
                titulo_leyenda = nombres_leyendas[0]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y,
                              legend_title_text = titulo_leyenda,
                              template = tema)
            
            if nombres_leyendas:
                
                categorias_leyendas = df[variable_agrupar].unique()
                
                labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
            
                fig.for_each_trace(lambda t: t.update
                               (name = labels_leyendas[t.name]))
            
            return fig

    # Crear un gráfico de cajas
    def cajas(self, df, variable_x, variable_y, variable_agrupar = False,
              nombres_categorias = False, nombres_ejes = False, 
              nombres_leyendas = False):
        
        """
        Método que crea un gráfico de cajas interactivo en la app actual 
        usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y.
                    
        variable_agrupar: str, opcional
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el gráfico. Si no se proporciona, no se 
                          categorizarán los datos en diferentes colores. Por defecto es False.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para reemplazar los valores únicos 
                            de 'variable_x' en el gráfico. Si no se proporciona, 
                            se utilizarán los valores únicos originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de cajas 
        al layout de la aplicación Dash.
        """
        
        if variable_agrupar:
            
            df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_x].unique())
        
        if not nombres_categorias:
            
            nombres = categorias
            
        else:
            
            nombres = dict(zip(categorias, nombres_categorias))
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_cajas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_cajas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_cajas', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Categorizar:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Categorizar'}], 
                                      value = ['Categorizar'], inline = True, 
                                      id = 'checklist_cajas')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'cajas')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('cajas', 'figure'),
            Input('tema_cajas', 'value'),
            Input('imputar_nan_cajas', 'value'),
            Input('titulo_cajas', 'value'),
            Input('checklist_cajas', 'value')
            
        )
        def grafico_cajas(tema, metodo, titulo, categorizar):
            
            copia_df = df.copy()
            
            if metodo:
                
                if not df[variable_x].dtype in ['category', 'object']:
                
                    operaciones = {
                        
                        'mean': [copia_df[variable_x].mean(), 
                                 copia_df[variable_y].mean()],
                        
                        'median': [copia_df[variable_x].median(), 
                                   copia_df[variable_y].median()],
                        
                        'max': [copia_df[variable_x].max(), 
                                 copia_df[variable_y].max()],
                        
                        'min': [copia_df[variable_x].min(), 
                                copia_df[variable_y].min()]
                        
                    }
                    
                    copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo][0])
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo][1])
                    
                else:
                    
                    operaciones = {
                        
                        'mean': copia_df[variable_y].mean(),
                        
                        'median': copia_df[variable_y].median(),
                        
                        'max': copia_df[variable_y].max(),
                        
                        'min': copia_df[variable_y].min()
                        
                    }
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo])
                    
            if not categorizar or not variable_agrupar:
                
                fig = px.box(copia_df.replace({variable_x: nombres}), x = variable_x, 
                             y = variable_y, template = tema, 
                             title = titulo if titulo else 'Gráfico de cajas')
                
            else:
                
                fig = px.box(copia_df.replace({variable_x: nombres}), x = variable_x, 
                             y = variable_y, color = variable_agrupar, template = tema, 
                             title = titulo if titulo else 'Gráfico de cajas')
                
                if nombres_leyendas:
                    
                    titulo_leyenda = nombres_leyendas[0]
                    
                    categorias_leyendas = df[variable_agrupar].unique()
                    
                    labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
                
                    fig.for_each_trace(lambda t: t.update
                                   (name = labels_leyendas[t.name]))
                    
                else:
                    
                    titulo_leyenda = variable_agrupar

                fig.update_layout(legend_title_text = titulo_leyenda)
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y)
            
            return fig
        
    # Crear un gráfico de violines
    def violines(self, df, variable_x, variable_y, variable_agrupar = False,  
                 nombres_categorias = False, nombres_ejes = False, 
                 nombres_leyendas = False):
        
        """
        Método que crea un gráfico de violines interactivo en la app actual 
        usando el dataframe dado.
       
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y.
                    
        variable_agrupar: str, opcional
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el gráfico. Si no se proporciona, no se 
                          categorizarán los datos en diferentes colores. Por defecto es False.
                    
        nombres_categorias: list, opcional
                            Lista de nombres para reemplazar los valores únicos 
                            de 'variable_x' en el gráfico. Si no se proporciona, 
                            se utilizarán los valores únicos originales. Por defecto es False.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de violines
        al layout de la aplicación Dash.
        """
       
        if variable_agrupar:
        
            df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_x].unique())
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_violines')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_violines')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_violines', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Categorizar:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Categorizar'}], 
                                      value = ['Categorizar'], inline = True, 
                                      id = 'checklist_violines')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'violines')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('violines', 'figure'),
            Input('tema_violines', 'value'),
            Input('imputar_nan_violines', 'value'),
            Input('titulo_violines', 'value'),
            Input('checklist_violines', 'value')
            
        )
        def grafico_violines(tema, metodo, titulo, categorizar):
            
            if not nombres_categorias:
                
                nombres = categorias
                
            else:
                
                nombres = dict(zip(categorias, nombres_categorias))
            
            copia_df = df.copy()
            
            if metodo:
                
                if not df[variable_x].dtype in ['category', 'object']:
                
                    operaciones = {
                        
                        'mean': [copia_df[variable_x].mean(), 
                                 copia_df[variable_y].mean()],
                        
                        'median': [copia_df[variable_x].median(), 
                                   copia_df[variable_y].median()],
                        
                        'max': [copia_df[variable_x].max(), 
                                 copia_df[variable_y].max()],
                        
                        'min': [copia_df[variable_x].min(), 
                                copia_df[variable_y].min()]
                        
                    }
                    
                    copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo][0])
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo][1])
                    
                else:
                    
                    operaciones = {
                        
                        'mean': copia_df[variable_y].mean(),
                        
                        'median': copia_df[variable_y].median(),
                        
                        'max': copia_df[variable_y].max(),
                        
                        'min': copia_df[variable_y].min()
                        
                    }
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo])
            
            if not categorizar or not variable_agrupar:
                
                fig = px.violin(copia_df.replace({variable_x: nombres}), x = variable_x, 
                                y = variable_y, box = True, points = 'all', 
                                title = titulo if titulo else 'Gráfico de violines')
                
            else:
            
                fig = px.violin(copia_df.replace({variable_x: nombres}), x = variable_x, 
                                y = variable_y, color = variable_agrupar, box = True, 
                                points = 'all', title = titulo if titulo else 'Gráfico de violines')
                
                if not nombres_leyendas:
                    
                    titulo_leyenda = variable_agrupar
                    
                else:
                    
                    titulo_leyenda = nombres_leyendas[0]
                    
                    categorias_leyendas = df[variable_agrupar].unique()
                    
                    labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
                
                    fig.for_each_trace(lambda t: t.update
                                   (name = labels_leyendas[t.name]))

                fig.update_layout(legend_title_text = titulo_leyenda, template = tema)
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y)
            
            return fig

    # Crear un gráfico de areas
    def areas(self, df, variable_x, variable_y, variable_agrupar,
              nombres_ejes = False, nombres_leyendas = False):
        
        """
        Método que crea un gráfico de áreas interactivo en la app actual usando 
        el dataframe dado
        
        Parámetros:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se utilizará como 
                    la variable en el eje y.
                    
        variable_agrupar: str
                          Nombre de la columna en el DataFrame que se utilizará 
                          para agrupar el gráfico.
                             
        nombres_ejes: list, opcional
                      Lista con dos elementos que representan los nombres para los ejes x e y. 
                      Si no se proporciona, se utilizarán los nombres de las variables originales. 
                      Por defecto es False.
           
        nombres_leyendas: list, opcional
                          Lista con el nombre de la leyenda y los nombres para las 
                          categorías en la leyenda. El primer elemento será el título 
                          de la leyenda y los siguientes elementos serán los nombres de 
                          las categorías. Si no se proporciona, se utilizará el nombre 
                          de 'variable_agrupar'. Por defecto es False.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de areas
        al layout de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_agrupar])
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_areas')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_areas')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_areas', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'areas')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('areas', 'figure'),
            Input('tema_areas', 'value'),
            Input('imputar_nan_areas', 'value'),
            Input('titulo_areas', 'value')
            
        )
        def grafico_areas(tema, metodo, titulo):
            
            copia_df = df.copy()
            
            if metodo:
                
                if not df[variable_x].dtype in ['category', 'object']:
                
                    operaciones = {
                        
                        'mean': [copia_df[variable_x].mean(), 
                                 copia_df[variable_y].mean()],
                        
                        'median': [copia_df[variable_x].median(), 
                                   copia_df[variable_y].median()],
                        
                        'max': [copia_df[variable_x].max(), 
                                 copia_df[variable_y].max()],
                        
                        'min': [copia_df[variable_x].min(), 
                                copia_df[variable_y].min()]
                        
                    }
                    
                    copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo][0])
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo][1])
                    
                else:
                    
                    operaciones = {
                        
                        'mean': copia_df[variable_y].mean(),
                        
                        'median': copia_df[variable_y].median(),
                        
                        'max': copia_df[variable_y].max(),
                        
                        'min': copia_df[variable_y].min()
                        
                    }
                    
                    copia_df[variable_y] = copia_df[variable_y].fillna(operaciones[metodo])

            fig = px.area(copia_df, x = variable_x, y = variable_y, 
                          color = variable_agrupar, line_group = variable_agrupar,
                          title = titulo if titulo else 'Gráfico de áreas')
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]
                
            if not nombres_leyendas:
                
                titulo_leyenda = variable_agrupar
                
            else:
                
                titulo_leyenda = nombres_leyendas[0]
                
                categorias_leyendas = df[variable_agrupar].unique()
                
                labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas[1:]))
            
                fig.for_each_trace(lambda t: t.update
                               (name = labels_leyendas[t.name]))

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y,
                              legend_title_text = titulo_leyenda,
                              template = tema)
            
            return fig

    # Crear un gráfico de pastel
    def pastel(self, df, variable_x, variable_y, nombres_leyendas = False):
        
        """
        Método que crea un gráfico de pastel interactivo en la app actual usando
        el dataframe dado.
    
        Parameters:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos para el gráfico.
                          
        variable_x: str
                    Nombre de la columna que contiene los valores numéricos a 
                    representar en el gráfico.
                    
        variable_y: str
                    Nombre de la columna que define las categorías o segmentos 
                    en el gráfico.
                    
        nombres_leyendas: list, opcional
                          Lista para mapear nombres personalizados a las leyendas 
                          de las categorías.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de pastel
        al layout de la aplicación Dash.
        """
        
        # Lista de escalas de colores disponibles
        colores = {
            
            'Blues': px.colors.sequential.Blues,
            'Viridis': px.colors.sequential.Viridis,
            'Cividis': px.colors.sequential.Cividis,
            'Magma': px.colors.sequential.Magma,
            'PiYG': px.colors.diverging.PiYG,
            'RdBu': px.colors.diverging.RdBu,
            'Spectral': px.colors.diverging.Spectral,
            'BrBG': px.colors.diverging.BrBG,
            'Plotly': px.colors.qualitative.Plotly,
            'D3': px.colors.qualitative.D3,
            'Set1': px.colors.qualitative.Set1,
            'Pastel1': px.colors.qualitative.Pastel1,
            'IceFire': px.colors.cyclical.IceFire,
            'Edge': px.colors.cyclical.Edge
            
            }
        
        df = df.dropna(subset = [variable_y])
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_pastel')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_pastel')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([
                    
                        html.Label('Color:'),
                        dcc.Dropdown(options = [{'label': key, 'value': key} for key 
                                                in colores.keys()], value = 'Plotly',
                                     id = 'colores_pastel')], 
                        
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_pastel', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '22%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Hueco en el centro:'),
                        dcc.Slider(id = 'hueco_pastel', min = 0, max = 0.5, step = 0.1, 
                                   value = 0, 
                                   marks = {i: str(i) for i in 
                                            [round(v, 1) for v in 
                                             np.arange(0, 0.51, 0.1)]})],
                         
                         style = {'display': 'inline-block', 'width': '35%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'pastel')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('pastel', 'figure'),
            Input('tema_pastel', 'value'),
            Input('imputar_nan_pastel', 'value'),
            Input('titulo_pastel', 'value'),
            Input('hueco_pastel', 'value'),
            Input('colores_pastel', 'value')
            
        )
        def grafico_pastel(tema, metodo, titulo, hueco, color):
            
            copia_df = df.copy()
            
            if nombres_leyendas:
                
                categorias_leyendas = df[variable_y].unique()
                
                labels_leyendas = dict(zip(categorias_leyendas, nombres_leyendas))
            
                copia_df[variable_y] = copia_df[variable_y].map(labels_leyendas)
            
            if metodo:
                
                operaciones = {
                    
                    'mean': copia_df[variable_x].mean(),
                    
                    'median': copia_df[variable_x].median(),
                    
                    'max': copia_df[variable_x].max(),
                    
                    'min': copia_df[variable_x].min()
                    
                }
                
                copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo])
            
            fig = px.pie(copia_df, values = variable_x, names = variable_y,
                         title = titulo if titulo else 'Gráfico de pastel',
                         template = tema, hole = hueco,
                         color_discrete_sequence = colores[color])
            
            fig.update_traces(marker = dict(line = dict(
                color = '#000000', width = 0.5)))
            
            return fig

    # Crear un gráfico de mapa de calor
    def mapa_calor(self, df, variable_x, variable_y, nombres_ejes = False):
        
        """
        Método que crea un gráfico de mapa de calor interactivo en la app actual 
        usando el dataframe dado.
    
        Parameters:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos a ser graficados.
            
        variable_x: str
                    Nombre de la columna del DataFrame que se usará para el eje x.
                    
        variable_y: str
                    Nombre de la columna del DataFrame que se usará para el eje y.
                    
        nombres_ejes: list, opcional
                      Nombres personalizados para los ejes x e y. Si no se proporcionan, 
                      se utilizarán los nombres de las variables originales.
                      
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de mapa de calor
        al layout de la aplicación Dash.
        """
        
        # Lista de escalas de colores disponibles
        colores = [
            
            'Viridis', 'Cividis', 'Plasma', 'Inferno', 'Magma', 'Turbo',
            'Blues', 'Greens', 'Greys', 'Oranges', 'Reds', 'Purples', 
            'YlGnBu', 'YlOrRd', 'Rainbow'
            
        ]

        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_mapa_calor')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_mapa_calor', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Mostrar números:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Mostrar números'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_mapa_calor')], 
                        
                        style = {'display': 'inline-block', 'width': '28%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Colores:'),
                        dcc.Slider(min = 0, max = len(colores) - 1, value = 2, 
                                   marks = {i: colores[i] for i in range(len(colores))}, 
                                   step = None, id = 'colores_heatmap')], 
                     
                        style = {'display': 'inline-block', 'width': '80%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Bins en el eje x:'),
                        dcc.Slider(id = 'bins_x', min = 5, max = 50, step = 1, 
                                   value = 10, marks = {i: str(i) for i in range(5, 51, 5)})], 
                     
                        style = {'display': 'inline-block', 'width': '40%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Bins en el eje y:'),
                        dcc.Slider(id = 'bins_y', min = 5, max = 50, step = 1, 
                                   value = 10, marks = {i: str(i) for i in range(5, 51, 5)})], 
                     
                        style = {'display': 'inline-block', 'width': '40%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'mapa_calor')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('mapa_calor', 'figure'),
            Input('tema_mapa_calor', 'value'),
            Input('titulo_mapa_calor', 'value'),
            Input('checklist_mapa_calor', 'value'),
            Input('colores_heatmap', 'value'),
            Input('bins_x', 'value'),
            Input('bins_y', 'value'),
            
        )
        def grafico_mapa_calor(tema, titulo, numeros, color, bins_x, bins_y):
                
            if numeros:
                
                text = True
                
            else:
                
                text = False

            fig = px.density_heatmap(df, x = variable_x, y = variable_y, 
                                     text_auto = text, nbinsx = bins_x, nbinsy = bins_y, 
                                     color_continuous_scale = colores[color],
                                     title = titulo if titulo else 'Mapa de calor')
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y,
                              template = tema,
                              coloraxis_colorbar = dict(
                                  title = 'Conteo'))
            
            return fig

    # Crear un gráfico de curvas de densidad
    def densidad(self, df, variable_x, variable_agrupar, nombres_leyendas = False):
        
        """
        Método que crea un gráfico de mapa de densidad interactivo en la app actual 
        usando el dataframe dado.
    
        Parameters:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos a ser graficados.
            
        variable_x: str
                    Nombre de la columna del Dataframe cuyas distribuciones de 
                    densidad se quieren visualizar.
                    
        variable_agrupar: str
                          Nombre de la columna del Datframe que contiene las 
                          categorías para agrupar los datos.
                          
        nombres_leyendas: list, opcional
                          Lista de nombres para las leyendas del gráfico. El primer 
                          elemento de la lista será el título de la leyenda, y los 
                          siguientes elementos serán los nombres de las categorías. 
                          Si no se proporciona, se utilizan los valores únicos de 
                          'variable_agrupar'.
                          
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de densidad 
        al layout de la aplicación Dash.
        """
        
        df = df.dropna(subset = [variable_agrupar])
        
        categorias = list(df[variable_agrupar].unique())
        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_densidad')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Imputar valores nulos por:'),
                        dcc.Dropdown(options = self.__metodos, value = '', 
                                     id = 'imputar_nan_densidad')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_densidad', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Curva normal:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Curva normal'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_densidad')], 
                        
                        style = {'display': 'inline-block', 'width': '20%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'densidad')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('densidad', 'figure'),
            Input('tema_densidad', 'value'),
            Input('imputar_nan_densidad', 'value'),
            Input('titulo_densidad', 'value'),
            Input('checklist_densidad', 'value')
            
        )
        def grafico_densidad(tema, metodo, titulo, tipo):
            
            copia_df = df.dropna(subset = [variable_x])
            
            if metodo:
                
                copia_df = df.copy()
                
                operaciones = {
                        
                    'mean': copia_df[variable_x].mean(),
                        
                    'median': copia_df[variable_x].median(),
                        
                    'max': copia_df[variable_x].max(),
                        
                    'min': copia_df[variable_x].min()
                        
                }
                
                copia_df[variable_x] = copia_df[variable_x].fillna(operaciones[metodo])
                
            lista = []

            for i in range(len(categorias)):

                categoria = copia_df[copia_df[variable_agrupar] == categorias[i]][variable_x]

                lista.append(categoria)
                
            if tipo:
                
                curva = 'normal'
                
            else:
                
                curva = 'kde'

            if nombres_leyendas:
                
                fig = ff.create_distplot(lista, nombres_leyendas[1:], show_hist = False, 
                                         show_rug = False, curve_type = curva)
                
                fig.update_layout(legend_title = nombres_leyendas[0], template = tema, 
                                  title = titulo if titulo else 'Gráfico de densidad')
                
            else:
                
                fig = ff.create_distplot(lista, categorias, show_hist = False, 
                                         show_rug = False, curve_type = curva)
                
                fig.update_layout(title = titulo if titulo else 'Gráfico de densidad',
                                  template = tema)
            
            for trace in fig['data']:
                
                trace['fill'] = 'tozeroy'
            
            return fig

    # Crear un gráfico de contorno de densidad
    def contorno_densidad(self, df, variable_x, variable_y, nombres_ejes = False):
        
        """
        Método que crea un gráfico de mapa de contorno de densidad interactivo 
        en la app actual usando el dataframe dado.
    
        Parameters:
        -----------
        df: pandas.DataFrame
            DataFrame que contiene los datos a ser graficados.
            
        variable_x: str
                    Nombre de la columna en el DataFrame que se usará para el eje x.
                    
        variable_y: str
                    Nombre de la columna en el DataFrame que se usará para el eje y.
                    
        nombres_ejes: list, opcional
                      Lista que contiene los nombres para los ejes x e y. Si no se 
                      proporciona, se usarán los nombres de las columnas por defecto.
                      Por defecto es False.
                      
        Returns:
        --------
        None: La función no retorna ningún valor. Agrega el gráfico de contorno de 
        densidad al layout de la aplicación Dash.
        """
        
        # Lista de escalas de colores disponibles
        colores = [
            
            'Viridis', 'Cividis', 'Plasma', 'Inferno', 'Magma', 'Turbo',
            'Blues', 'Greens', 'Greys', 'Oranges', 'Reds', 'Purples', 
            'YlGnBu', 'YlOrRd', 'Rainbow'
            
        ]

        
        self.__app.layout.children.append(
            html.Div([
                html.Div([
                    
                    html.Div([

                        html.Label('Tema:'),
                        dcc.Dropdown(options = self.__temas, value = 'plotly', 
                                     id = 'tema_contorno_densidad')], 
                        
                        style = {'display': 'inline-block', 'width': '30%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Título del gráfico:'),
                        dcc.Input(type = 'text', id = 'titulo_contorno_densidad', 
                                  placeholder = 'Ingrese el título del gráfico',
                                  style = {'width': '100%'})], 
                     
                        style = {'display': 'inline-block', 'width': '30%', 'padding': '0 1%'}),
                    
                    html.Div([

                        html.Label('Mostrar números:'),
                        dcc.Checklist(options = [{'label': '', 'value': 'Mostrar números'}], 
                                      value = [], inline = True, 
                                      id = 'checklist_contorno_densidad')], 
                        
                        style = {'display': 'inline-block', 'width': '30%', 'padding': '0 1%'}),
                    
                    html.Div([
                        
                        html.Br(),
                        html.Label('Colores:'),
                        dcc.Slider(min = 0, max = len(colores) - 1, value = 2, 
                                   marks = {i: colores[i] for i in range(len(colores))}, 
                                   step = None, id = 'colores_contorno_densidad')], 
                     
                        style = {'display': 'inline-block', 'width': '80%', 'padding': '0 1%'}),
                    
                ], style = {'display': 'flex', 'flex-wrap': 'wrap', 'padding': '10px 0'}),
    
                dcc.Graph(id = 'contorno_densidad')
                
            ])
        )
        
        @self.__app.callback(
            
            Output('contorno_densidad', 'figure'),
            Input('tema_contorno_densidad', 'value'),
            Input('titulo_contorno_densidad', 'value'),
            Input('checklist_contorno_densidad', 'value'),
            Input('colores_contorno_densidad', 'value')
            
        )
        def grafico_contorno_densidad(tema, titulo, numeros, color):
                
            if numeros:
                
                text = True
                
            else:
                
                text = False

            fig = px.density_contour(df, x = variable_x, y = variable_y, template = tema,
                                     title = titulo if titulo else 'Contorno de densidad')
            
            if not nombres_ejes:
                
                nombre_x = variable_x
                nombre_y = variable_y
                
            else:
                
                nombre_x = nombres_ejes[0]
                nombre_y = nombres_ejes[1]

            fig.update_layout(xaxis_title = nombre_x,
                              yaxis_title = nombre_y)
            
            fig.update_traces(contours_coloring = "fill", contours_showlabels = text, 
                              colorscale = colores[color])
            
            return fig








