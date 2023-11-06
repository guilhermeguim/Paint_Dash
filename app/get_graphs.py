import pandas as pd
import plotly.graph_objs as go
import datetime as dt
from datetime import datetime, timedelta


def get_graph(df,size):
    
    
    if size == 1:
        df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
        # Extraia a parte da data do datetime
        df['DATE'] = df['DATE_TIME'].dt.date
        
        # Defina a função para atribuir o valor da coluna 'SHIFT' com base nos intervalos de tempo
        # Define the function to assign the 'SHIFT' value based on time intervals
        def get_shift(time):
            if dt.time(6, 0, 0) <= time.time() < dt.time(15, 48, 0):
                return 1
            elif dt.time(15, 48, 0) <= time.time() < dt.time(0, 0, 0):
                return 2
            elif dt.time(0, 0, 0) <= time.time() < dt.time(1, 4, 0):
                return 2
            else:
                return 3

        # Aplique a função à coluna 'DATE_TIME' para criar a coluna 'SHIFT'
        df['SHIFT'] = df['DATE_TIME'].apply(get_shift)

        ##############GRAFICO 1##############
        
        # Agrupe os dados por LOCAL_TYPE e DATE, somando a coluna ACTIVE em cada grupo
        grouped_df = df.groupby(['LOCAL_TYPE', 'DATE'])['ACTIVE'].sum().reset_index()


        # Crie o gráfico de linhas
        fig1 = go.Figure()

        # Adicione cada linha para cada LOCAL_TYPE ao gráfico
        for local_type in grouped_df['LOCAL_TYPE'].unique():
            df_filtered = grouped_df[grouped_df['LOCAL_TYPE'] == local_type]
            fig1.add_trace(go.Scatter(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], mode='lines+markers', name=local_type, marker=dict(size=12,)))


        # Atualize o layout do gráfico
        fig1.update_layout(
                            height=350, 
                            xaxis_title='Date',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 40,
                                'font': {'size': 12}
                                
                            } for date, active_sum in zip(grouped_df['DATE'], grouped_df['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            xaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=12)),
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=12)),

                            # Personalize o estilo da fonte das legendas
                            legend=dict(font=dict(family='Montserrat, sans-serif',
                                        size=18, 
                                        color='#012C5E'),
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="left",
                                        x=0),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=18),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=18),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E', '#41A4FF']
                        )
        
        ##############CARD 1##############
        # Obtenha a data de hoje
        today = dt.datetime.now().date()

        # Filtre os eventos que ocorreram hoje
        events_today = df[df['DATE_TIME'].dt.date == today]

        # Contagem total de eventos hoje
        total_events_today = events_today.shape[0]
        
        
        ##############CARD 2##############
        # Divida os eventos de hoje por turno
        shift1 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(6, 5, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(15, 48, 0))].shape[0]
        shift2 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(15, 48, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(22, 10, 0))].shape[0]
        shift3 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(22, 10, 0)) | (events_today['DATE_TIME'].dt.time < dt.time(6, 5, 0))].shape[0]

        ##############GRAFICO 2##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SIDE'].value_counts()

        # Crie um gráfico de pizza
        fig2 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig2.update_layout(
            height=160,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=18, 
                        color='#012C5E'),
                        orientation="v"),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=26),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=26),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig2.update_traces(textfont_size=16)
        
        ##############GRAFICO 3##############
        # Agrupe os dados por data e turno e calcule as somas por dia e turno
        grouped_data = df.groupby(['DATE', 'SHIFT'])['ACTIVE'].sum().reset_index()

        # Crie um gráfico de barras clusterizado
        fig3 = go.Figure()

        # Adicione as barras para cada turno no gráfico
        for shift in grouped_data['SHIFT'].unique():
            df_filtered = grouped_data[grouped_data['SHIFT'] == shift]
            fig3.add_trace(go.Bar(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], name=f'Shift {shift}'))

        # Atualize o layout do gráfico
        fig3.update_layout(
            height=280,     
            barmode='group',  # Especifique 'group' para criar barras clusterizadas
            
            xaxis_title='Date',
            yaxis_title='Sum of Events',
            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
            
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade
            xaxis=dict(showgrid=False, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),
            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=18, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=18),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=18),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        ##############GRAFICO 4##############
        # Calcule a contagem de eventos em cada turno no DataFrame total
        lt_counts = df['LOCAL_TYPE'].value_counts()

        # Crie um gráfico de pizza
        fig4 = go.Figure(data=[go.Pie(labels=lt_counts.index, values=lt_counts.values)])

        # Atualize o layout do gráfico
        fig4.update_layout(
            height=300,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1,
                        xanchor="left",
                        x=0),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        fig4.update_traces(textfont_size=20)
        
        ##############GRAFICO 5##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig5 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig5.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig5.update_layout(
                            height=250,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 6##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig6 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig6.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig6.update_layout(
                            height=250,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )

        ##############GRAFICO 7##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']
        
        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig7 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig7.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig7.update_layout(
                            height=250,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 8##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig8 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig8.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig8.update_layout(
                            height=250,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )
        
        ##############GRAFICO 9##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SHIFT'].value_counts()

        # Crie um gráfico de pizza
        fig9 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig9.update_layout(
            height=250,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=18, 
                        color='#012C5E'),
                        orientation="v"),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=26),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=26),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig9.update_traces(textfont_size=16)

        return fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
    elif size == 2:
        df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
        # Extraia a parte da data do datetime
        df['DATE'] = df['DATE_TIME'].dt.date
        
        # Defina a função para atribuir o valor da coluna 'SHIFT' com base nos intervalos de tempo
        # Define the function to assign the 'SHIFT' value based on time intervals
        def get_shift(time):
            if dt.time(6, 5, 0) <= time.time() < dt.time(15, 48, 0):
                return 1
            elif dt.time(15, 48, 0) <= time.time() < dt.time(22, 10, 0):
                return 2
            else:
                return 3

        # Aplique a função à coluna 'DATE_TIME' para criar a coluna 'SHIFT'
        df['SHIFT'] = df['DATE_TIME'].apply(get_shift)

        ##############GRAFICO 1##############
        
        # Agrupe os dados por LOCAL_TYPE e DATE, somando a coluna ACTIVE em cada grupo
        grouped_df = df.groupby(['LOCAL_TYPE', 'DATE'])['ACTIVE'].sum().reset_index()


        # Crie o gráfico de linhas
        fig1 = go.Figure()

        # Adicione cada linha para cada LOCAL_TYPE ao gráfico
        for local_type in grouped_df['LOCAL_TYPE'].unique():
            df_filtered = grouped_df[grouped_df['LOCAL_TYPE'] == local_type]
            fig1.add_trace(go.Scatter(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], mode='lines+markers', name=local_type, marker=dict(size=12,)))


        # Atualize o layout do gráfico
        fig1.update_layout(
                            height=210, 
                            xaxis_title='Date',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 40,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(grouped_df['DATE'], grouped_df['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            xaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),

                            # Personalize o estilo da fonte das legendas
                            legend=dict(font=dict(family='Montserrat, sans-serif',
                                        size=12, 
                                        color='#012C5E'),
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="left",
                                        x=0),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E', '#41A4FF']
                        )
        
        ##############CARD 1##############
        # Obtenha a data de hoje
        today = dt.datetime.now().date()

        # Filtre os eventos que ocorreram hoje
        events_today = df[df['DATE_TIME'].dt.date == today]

        # Contagem total de eventos hoje
        total_events_today = events_today.shape[0]
        
        
        ##############CARD 2##############
        # Divida os eventos de hoje por turno
        shift1 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(6, 5, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(15, 48, 0))].shape[0]
        shift2 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(15, 48, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(22, 10, 0))].shape[0]
        shift3 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(22, 10, 0)) | (events_today['DATE_TIME'].dt.time < dt.time(6, 5, 0))].shape[0]

        ##############GRAFICO 2##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SIDE'].value_counts()

        # Crie um gráfico de pizza
        fig2 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig2.update_layout(
            height=120,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="v"),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig2.update_traces(textfont_size=10)
        
        ##############GRAFICO 3##############
        # Agrupe os dados por data e turno e calcule as somas por dia e turno
        grouped_data = df.groupby(['DATE', 'SHIFT'])['ACTIVE'].sum().reset_index()

        # Crie um gráfico de barras clusterizado
        fig3 = go.Figure()

        # Adicione as barras para cada turno no gráfico
        for shift in grouped_data['SHIFT'].unique():
            df_filtered = grouped_data[grouped_data['SHIFT'] == shift]
            fig3.add_trace(go.Bar(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], name=f'Shift {shift}'))

        # Atualize o layout do gráfico
        fig3.update_layout(
            height=180,     
            barmode='group',  # Especifique 'group' para criar barras clusterizadas
            
            xaxis_title='Date',
            yaxis_title='Sum of Events',
            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
            
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade
            xaxis=dict(showgrid=False, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=12)),
            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=12)),

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        ##############GRAFICO 4##############
        # Calcule a contagem de eventos em cada turno no DataFrame total
        lt_counts = df['LOCAL_TYPE'].value_counts()

        # Crie um gráfico de pizza
        fig4 = go.Figure(data=[go.Pie(labels=lt_counts.index, values=lt_counts.values)])

        # Atualize o layout do gráfico
        fig4.update_layout(
            height=170,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=10, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1,
                        xanchor="left",
                        x=0),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        fig4.update_traces(textfont_size=10)
        
        ##############GRAFICO 5##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig5 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig5.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig5.update_layout(
                            height=150,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 20,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),
                            xaxis=dict(tickfont=dict(size=8)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 6##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig6 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig6.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig6.update_layout(
                            height=150,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 20,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),
                            xaxis=dict(tickfont=dict(size=8)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )

        ##############GRAFICO 7##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']
        
        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig7 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig7.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig7.update_layout(
                            height=165,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),
                            xaxis=dict(tickfont=dict(size=8)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 8##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig8 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig8.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig8.update_layout(
                            height=165,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=8)),
                            xaxis=dict(tickfont=dict(size=8)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )
        
        ##############GRAFICO 9##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SHIFT'].value_counts()

        # Crie um gráfico de pizza
        fig9 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig9.update_layout(
            height=160,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=50, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            


            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig9.update_traces(textfont_size=10)

        return fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    elif size == 3:
        df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
        # Extraia a parte da data do datetime
        df['DATE'] = df['DATE_TIME'].dt.date
        
        # Defina a função para atribuir o valor da coluna 'SHIFT' com base nos intervalos de tempo
        # Define the function to assign the 'SHIFT' value based on time intervals
        def get_shift(time):
            if dt.time(6, 5, 0) <= time.time() < dt.time(15, 48, 0):
                return 1
            elif dt.time(15, 48, 0) <= time.time() < dt.time(22, 10, 0):
                return 2
            else:
                return 3

        # Aplique a função à coluna 'DATE_TIME' para criar a coluna 'SHIFT'
        df['SHIFT'] = df['DATE_TIME'].apply(get_shift)

        ##############GRAFICO 1##############
        
        # Agrupe os dados por LOCAL_TYPE e DATE, somando a coluna ACTIVE em cada grupo
        grouped_df = df.groupby(['LOCAL_TYPE', 'DATE'])['ACTIVE'].sum().reset_index()


        # Crie o gráfico de linhas
        fig1 = go.Figure()

        # Adicione cada linha para cada LOCAL_TYPE ao gráfico
        for local_type in grouped_df['LOCAL_TYPE'].unique():
            df_filtered = grouped_df[grouped_df['LOCAL_TYPE'] == local_type]
            fig1.add_trace(go.Scatter(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], mode='lines+markers', name=local_type, marker=dict(size=8,)))


        # Atualize o layout do gráfico
        fig1.update_layout(
                            height=270, 
                            xaxis_title='Date',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(grouped_df['DATE'], grouped_df['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            xaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),

                            # Personalize o estilo da fonte das legendas
                            legend=dict(font=dict(family='Montserrat, sans-serif',
                                        size=12, 
                                        color='#012C5E'),
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="left",
                                        x=0),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E', '#41A4FF']
                        )
        
        ##############CARD 1##############
        # Obtenha a data de hoje
        today = dt.datetime.now().date()

        # Filtre os eventos que ocorreram hoje
        events_today = df[df['DATE_TIME'].dt.date == today]

        # Contagem total de eventos hoje
        total_events_today = events_today.shape[0]
        
        
        ##############CARD 2##############
        # Divida os eventos de hoje por turno
        shift1 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(6, 5, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(15, 48, 0))].shape[0]
        shift2 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(15, 48, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(22, 10, 0))].shape[0]
        shift3 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(22, 10, 0)) | (events_today['DATE_TIME'].dt.time < dt.time(6, 5, 0))].shape[0]

        ##############GRAFICO 2##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SIDE'].value_counts()

        # Crie um gráfico de pizza
        fig2 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig2.update_layout(
            height=160,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="v"),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig2.update_traces(textfont_size=14)
        
        ##############GRAFICO 3##############
        # Agrupe os dados por data e turno e calcule as somas por dia e turno
        grouped_data = df.groupby(['DATE', 'SHIFT'])['ACTIVE'].sum().reset_index()

        # Crie um gráfico de barras clusterizado
        fig3 = go.Figure()

        # Adicione as barras para cada turno no gráfico
        for shift in grouped_data['SHIFT'].unique():
            df_filtered = grouped_data[grouped_data['SHIFT'] == shift]
            fig3.add_trace(go.Bar(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], name=f'Shift {shift}'))

        # Atualize o layout do gráfico
        fig3.update_layout(
            height=240,     
            barmode='group',  # Especifique 'group' para criar barras clusterizadas
            
            xaxis_title='Date',
            yaxis_title='Sum of Events',
            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
            
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade
            xaxis=dict(showgrid=False, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        ##############GRAFICO 4##############
        # Calcule a contagem de eventos em cada turno no DataFrame total
        lt_counts = df['LOCAL_TYPE'].value_counts()

        # Crie um gráfico de pizza
        fig4 = go.Figure(data=[go.Pie(labels=lt_counts.index, values=lt_counts.values)])

        # Atualize o layout do gráfico
        fig4.update_layout(
            height=220,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1,
                        xanchor="left",
                        x=0),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        fig4.update_traces(textfont_size=14)
        
        ##############GRAFICO 5##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig5 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig5.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig5.update_layout(
                            height=160,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 16}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),
                            xaxis=dict(tickfont=dict(size=14)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 6##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig6 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig6.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig6.update_layout(
                            height=160,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 16}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),
                            xaxis=dict(tickfont=dict(size=14)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )

        ##############GRAFICO 7##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']
        
        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig7 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig7.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig7.update_layout(
                            height=200,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 16}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),
                            xaxis=dict(tickfont=dict(size=14)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 8##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig8 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig8.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig8.update_layout(
                            height=200,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 16}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=14)),
                            xaxis=dict(tickfont=dict(size=14)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=14),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )
        
        ##############GRAFICO 9##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SHIFT'].value_counts()

        # Crie um gráfico de pizza
        fig9 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig9.update_layout(
            height=230,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=50, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=14, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            


            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig9.update_traces(textfont_size=14)

        return fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    elif size == 4:
        df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
        # Extraia a parte da data do datetime
        df['DATE'] = df['DATE_TIME'].dt.date
        
        # Defina a função para atribuir o valor da coluna 'SHIFT' com base nos intervalos de tempo
        # Define the function to assign the 'SHIFT' value based on time intervals
        def get_shift(time):
            if dt.time(6, 5, 0) <= time.time() < dt.time(15, 48, 0):
                return 1
            elif dt.time(15, 48, 0) <= time.time() < dt.time(22, 10, 0):
                return 2
            else:
                return 3

        # Aplique a função à coluna 'DATE_TIME' para criar a coluna 'SHIFT'
        df['SHIFT'] = df['DATE_TIME'].apply(get_shift)

        ##############GRAFICO 1##############
        
        # Agrupe os dados por LOCAL_TYPE e DATE, somando a coluna ACTIVE em cada grupo
        grouped_df = df.groupby(['LOCAL_TYPE', 'DATE'])['ACTIVE'].sum().reset_index()


        # Crie o gráfico de linhas
        fig1 = go.Figure()

        # Adicione cada linha para cada LOCAL_TYPE ao gráfico
        for local_type in grouped_df['LOCAL_TYPE'].unique():
            df_filtered = grouped_df[grouped_df['LOCAL_TYPE'] == local_type]
            fig1.add_trace(go.Scatter(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], mode='lines+markers', name=local_type, marker=dict(size=8,)))


        # Atualize o layout do gráfico
        fig1.update_layout(
                            height=160, 
                            xaxis_title='Date',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 30,
                                'font': {'size': 10}
                                
                            } for date, active_sum in zip(grouped_df['DATE'], grouped_df['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            xaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),

                            # Personalize o estilo da fonte das legendas
                            legend=dict(font=dict(family='Montserrat, sans-serif',
                                        size=12, 
                                        color='#012C5E'),
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.05,
                                        xanchor="left",
                                        x=0),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E', '#41A4FF']
                        )
        
        ##############CARD 1##############
        # Obtenha a data de hoje
        today = dt.datetime.now().date()

        # Filtre os eventos que ocorreram hoje
        events_today = df[df['DATE_TIME'].dt.date == today]

        # Contagem total de eventos hoje
        total_events_today = events_today.shape[0]
        
        
        ##############CARD 2##############
        # Divida os eventos de hoje por turno
        shift1 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(6, 5, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(15, 48, 0))].shape[0]
        shift2 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(15, 48, 0)) & (events_today['DATE_TIME'].dt.time < dt.time(22, 10, 0))].shape[0]
        shift3 = events_today[(events_today['DATE_TIME'].dt.time >= dt.time(22, 10, 0)) | (events_today['DATE_TIME'].dt.time < dt.time(6, 5, 0))].shape[0]

        ##############GRAFICO 2##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SIDE'].value_counts()

        # Crie um gráfico de pizza
        fig2 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig2.update_layout(
            height=100,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="v"),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig2.update_traces(textfont_size=10)
        
        ##############GRAFICO 3##############
        # Agrupe os dados por data e turno e calcule as somas por dia e turno
        grouped_data = df.groupby(['DATE', 'SHIFT'])['ACTIVE'].sum().reset_index()

        # Crie um gráfico de barras clusterizado
        fig3 = go.Figure()

        # Adicione as barras para cada turno no gráfico
        for shift in grouped_data['SHIFT'].unique():
            df_filtered = grouped_data[grouped_data['SHIFT'] == shift]
            fig3.add_trace(go.Bar(x=df_filtered['DATE'], y=df_filtered['ACTIVE'], name=f'Shift {shift}'))

        # Atualize o layout do gráfico
        fig3.update_layout(
            height=160,     
            barmode='group',  # Especifique 'group' para criar barras clusterizadas
            
            xaxis_title='Date',
            yaxis_title='Sum of Events',
            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
            
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade
            xaxis=dict(showgrid=False, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            
            # Personalize o estilo do título dos eixos
            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        ##############GRAFICO 4##############
        # Calcule a contagem de eventos em cada turno no DataFrame total
        lt_counts = df['LOCAL_TYPE'].value_counts()

        # Crie um gráfico de pizza
        fig4 = go.Figure(data=[go.Pie(labels=lt_counts.index, values=lt_counts.values)])

        # Atualize o layout do gráfico
        fig4.update_layout(
            height=140,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=0, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            # Personalize o estilo das linhas de grade

            # Personalize o estilo da fonte das legendas
            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1,
                        xanchor="left",
                        x=0),
            

            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        fig4.update_traces(textfont_size=10)
        
        ##############GRAFICO 5##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig5 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig5.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig5.update_layout(
                            height=105,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            xaxis=dict(tickfont=dict(size=10)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 6##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_interior.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig6 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig6.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig6.update_layout(
                            height=105,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            xaxis_tickformat='%Y-%m-%d',  # Formato da data no eixo x
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            xaxis=dict(tickfont=dict(size=10)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )

        ##############GRAFICO 7##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'rh']
        
        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig7 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig7.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig7.update_layout(
                            height=120,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            xaxis=dict(tickfont=dict(size=10)),

                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#012C5E']
                        )

        ##############GRAFICO 8##############
        # Filtrar o DataFrame onde LOCAL_TYPE é igual a 'interior'
        df_interior = df[df['SIDE'] == 'lh']

        # Obter o timestamp atual
        current_time = datetime.now()

        # Calcular o timestamp para as últimas 2:30h
        last_2h_time = current_time - timedelta(hours=2, minutes=00)

        # Filtrar os dados das últimas 2:30h
        df_last_2h = df_interior[df_interior['DATE_TIME'] >= last_2h_time]
        
        # Agrupar os dados por LOCATION e calcular o somatório total por LOCATION
        location_sum = df_last_2h.groupby('LOCATION')['ACTIVE'].sum().reset_index()

        # Ordenar o DataFrame pelo somatório total em ordem decrescente
        location_sum = location_sum.sort_values(by='ACTIVE', ascending=False)

        # Criar um gráfico de barras ordenado
        fig8 = go.Figure()

        # Adicionar as barras para cada LOCATION no gráfico
        fig8.add_trace(go.Bar(x=location_sum['LOCATION'], y=location_sum['ACTIVE']))

        # Atualizar o layout do gráfico

        fig8.update_layout(
                            height=120,
                            xaxis_title='Location',
                            yaxis_title='Sum of Events',
                            
                            # Reduza o tamanho das margens
                            margin=dict(l=0, r=0, t=0, b=0), 

                            # Defina o fundo do gráfico como transparente
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',

                            # Adicione a exibição dos valores no gráfico
                            annotations=[{
                                'x': date,
                                'y': active_sum,
                                'text': str(active_sum),
                                'showarrow': False,
                                'yshift': 15,
                                'font': {'size': 14}
                                
                            } for date, active_sum in zip(location_sum['LOCATION'], location_sum['ACTIVE'])],
                        
                            # Personalize o estilo das linhas de grade
                            yaxis=dict(showgrid=True, gridcolor='#b9b9b9', gridwidth=1, zeroline=False, showline=False, ticks='outside', tickfont=dict(size=10)),
                            xaxis=dict(tickfont=dict(size=10)),
                            
                            # Personalize o estilo do título dos eixos
                            xaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo x
                            yaxis_title_font=dict(size=12),  # Aumente o tamanho e peso do título do eixo y

                            
                            # Mude as cores das linhas do gráfico
                            colorway=['#41A4FF']
                        )
        
        ##############GRAFICO 9##############
        
        # Calcule a contagem de eventos em cada turno no DataFrame total
        shift_counts = df['SHIFT'].value_counts()

        # Crie um gráfico de pizza
        fig9 = go.Figure(data=[go.Pie(labels=shift_counts.index, values=shift_counts.values)])

        # Atualize o layout do gráfico
        fig9.update_layout(
            height=150,
            title='',
            showlegend=True,
            # Reduza o tamanho das margens
            margin=dict(l=0, r=0, t=50, b=0), 

            # Defina o fundo do gráfico como transparente
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',


            legend=dict(font=dict(family='Montserrat, sans-serif',
                        size=12, 
                        color='#012C5E'),
                        orientation="h",
                        yanchor="bottom",
                        y=1.05,
                        xanchor="left",
                        x=0),
            


            
            # Mude as cores das linhas do gráfico
            colorway=['#012C5E', '#41A4FF','#A0D1FF']
        )
        
        fig9.update_traces(textfont_size=10)

        return fig1, total_events_today, shift1, shift2, shift3, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9