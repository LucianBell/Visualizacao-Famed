import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

#url
url = "https://docs.google.com/spreadsheets/d/1Y6R653wcsuvHOwTntZ6tr3EjtHksz5hhmg7YgKaatFo/edit?usp=sharing"

# Create a connection object.
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

df = conn.read(
    spreadsheet=url,
    worksheet="Página1"
)

df = df.iloc[2:40]

# Plotting collected TCLEs
fig_tcle = px.pie(data_frame=df['TCLE'], names=df['TCLE'],  title="Quantidade e Estado de TCLEs:")
fig_tcle.update_traces(textinfo='value')

# Plotting Gender data
fig_gender = px.pie(data_frame=df['Sexo'], names=df['Sexo'], title="Distribuição de gênero dos pacientes:")

# Medical speciality data
speciality_counts = df['Especialidade Médica'].value_counts().reset_index()
speciality_counts.columns = ['Especialidade Médica', 'Count']

speciality_counts = speciality_counts.sort_values(by='Count', ascending=False)

fig_medicalspec = px.bar(data_frame=speciality_counts, x="Especialidade Médica", y="Count", title="Especialidades Médicas:")

# Especialidades Médicas - Pie
fig_medicalspecpie = px.pie(data_frame=df['Especialidade Médica'], names=df['Especialidade Médica'])

# Interventions data
interventions_counts = df['Intervenção '].value_counts().reset_index()
interventions_counts.columns = ['Intervenção ', 'Count']

interventions_counts = interventions_counts.sort_values(by='Count', ascending=False)


fig_interventions = px.bar(data_frame=interventions_counts, x="Intervenção ", y="Count", title="Intervenção:")

# Acceptance of intervention - Pie
fig_accint = px.pie(data_frame=df['Intervenção aceita ou não '], names=df['Intervenção aceita ou não '])

# Acceptance of intervention - Chart
acccount_counts = df['Intervenção aceita ou não '].value_counts().reset_index()
acccount_counts.columns = ['Intervenção aceita ou não ', 'Count']

acccount_counts = acccount_counts.sort_values(by='Count', ascending=False)

fig_acccounts = px.bar(data_frame=acccount_counts, x="Intervenção aceita ou não ", y="Count", title="Intervenção aceita ou não:")

# Alteração na posologia
altposologia_counts = df['Houve alteração na posologia?'].value_counts().reset_index()
altposologia_counts.columns = ['Houve alteração na posologia?', 'Count']

altposologia_counts = altposologia_counts.sort_values(by='Count', ascending=False)

fig_altposologiacount = px.bar(data_frame=altposologia_counts, x="Houve alteração na posologia?", y="Count", title="Houve alteração na posologia:")

# Alteração na posologia - Chart
fig_altposologia = px.pie(data_frame=df['Houve alteração na posologia?'], names=df['Houve alteração na posologia?'])

# Medicação - Chart
medicacaocounts = df['Medicação - Teste'].value_counts().reset_index()
medicacaocounts.columns = ['Medicação - Teste', 'Count']

medicacaocounts = medicacaocounts.sort_values(by='Count', ascending=False)

fig_medicacaocounts = px.bar(data_frame=medicacaocounts, x="Medicação - Teste", y="Count", title="Medicações aplicadas:")

# Medicação - Pie
fig_medicacao = px.pie(data_frame=df['Medicação - Teste'], names=df['Medicação - Teste'])

# Dosagem - Chart
dosagemcounts = df['Dosagem - Teste'].value_counts().reset_index()
dosagemcounts.columns = ['Dosagem - Teste', 'Count']

dosagemcounts = dosagemcounts.sort_values(by='Count', ascending=False)

fig_dosagemcounts = px.bar(data_frame=dosagemcounts, x="Dosagem - Teste", y="Count", title="Dosagem das Medicações:")

# Dosagem - Pie
fig_dosagem = px.pie(data_frame=df['Dosagem - Teste'], names=df['Dosagem - Teste'])

# Via de administração - Chart
viaadmincounts = df['Via de administração'].value_counts().reset_index()
viaadmincounts.columns = ['Via de administração', 'Count']

viaadmincounts = viaadmincounts.sort_values(by='Count', ascending=False)

fig_viaadmincounts = px.bar(data_frame=viaadmincounts, x="Via de administração", y="Count", title="Via de administração das medicações:")

# Via de administração - Pie
fig_viaadmin = px.pie(data_frame=df['Via de administração'], names=df['Via de administração'])

# End - Pie
fig_end = px.pie(data_frame=df['Desfecho'], names=df['Desfecho'])

# End - bar
end_counts = df['Desfecho'].value_counts().reset_index()
end_counts.columns = ['Desfecho', 'Count']

end_counts = end_counts.sort_values(by='Count', ascending=False)

fig_endcounts = px.bar(data_frame=end_counts, x="Desfecho", y="Count", title="Desfecho:")

# Pyramid
df['Count'] = 1
age_bins = pd.cut(df['Idade'], bins=range(0, 101, 5))
df['AgeGroup'] = age_bins

grouped = df.groupby(['Sexo', 'AgeGroup']).count().reset_index()

# Separate data for males and females
male_data = grouped[grouped['Sexo'] == 'M']
female_data = grouped[grouped['Sexo'] == 'F']

# Prepare the data for plotting
male_data = male_data[['AgeGroup', 'Count']].rename(columns={'Count': 'Male_Count'})
female_data = female_data[['AgeGroup', 'Count']].rename(columns={'Count': 'Female_Count'})

# Merge male and female data
merged_data = pd.merge(male_data, female_data, on='AgeGroup', how='outer').fillna(0)

# Convert counts to negative for males (for plotting purposes)
merged_data['Male_Count'] = -merged_data['Male_Count']

# Plotly Population Pyramid
fig = go.Figure()

fig.add_trace(go.Bar(
    y=merged_data['AgeGroup'].astype(),
    x=merged_data['Male_Count'],
    name='Male',
    orientation='h',
))

fig.add_trace(go.Bar(
    y=merged_data['AgeGroup'].astype(),
    x=merged_data['Female_Count'],
    name='Female',
    orientation='h',
))

fig.update_layout(
    title='Pirâmide Etária da População do Estudo',
    barmode='overlay',
    bargap=0.2,
    xaxis=dict(title='População do Estudo', tickvals=[-500, -250, 0, 250, 500], ticktext=['500', '250', '0', '250', '500'], range=[-max(merged_data['Male_Count'].min(), merged_data['Female_Count'].max()), 
               max(merged_data['Female_Count'].max(), -merged_data['Male_Count'].min())]),
    yaxis=dict(title='Grupos de Idade'),
)

# Print results.
# st.dataframe(df)
logo = Image.open('images\logo.png')

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image=logo)

st.header("Projeto IA Famed - Visualização", divider='green')
st.subheader("_..._")


st.plotly_chart(figure_or_data=fig_tcle)
st.plotly_chart(figure_or_data=fig_gender)

st.plotly_chart(figure_or_data=fig)

st.plotly_chart(figure_or_data=fig_medicalspec)
st.plotly_chart(figure_or_data=fig_medicalspecpie)

st.plotly_chart(figure_or_data=fig_interventions)

st.plotly_chart(figure_or_data=fig_acccounts)
st.plotly_chart(figure_or_data=fig_accint)

st.plotly_chart(figure_or_data=fig_altposologiacount)
st.plotly_chart(figure_or_data=fig_altposologia)

st.plotly_chart(figure_or_data=fig_medicacaocounts)
st.plotly_chart(figure_or_data=fig_medicacao)

st.plotly_chart(figure_or_data=fig_dosagemcounts)
st.plotly_chart(figure_or_data=fig_dosagem)

st.plotly_chart(figure_or_data=fig_viaadmincounts)
st.plotly_chart(figure_or_data=fig_viaadmin)

st.plotly_chart(figure_or_data=fig_endcounts)
st.plotly_chart(figure_or_data=fig_end)
