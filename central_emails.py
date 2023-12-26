import streamlit as st
from pathlib import Path

from utilidade import envia_email

pasta_atual = Path(__file__).parent
pasta_template = pasta_atual / 'templates'
pasta_email = pasta_atual / 'Emails'
pasta_config = pasta_atual / 'config'

def inicializacao():
    if not 'pagina_central_email' in st.session_state:
        st.session_state.pagina_central_email= 'home'
    if not 'destinatarios_atual' in st.session_state:
        st.session_state.destinatarios_atual= ''
    if not 'titutlo_atual' in st.session_state:
        st.session_state.titulo_atual= ''
    if not 'corpo_atual' in st.session_state:
        st.session_state.corpo_atual= ''

def mudar_pagina(nome_pagina):
    st.session_state.pagina_central_email = nome_pagina

# =================== HOME ===================== 
def home():
    destinatario_atual = st.session_state.destinatarios_atual
    titulo_atual = st.session_state.titulo_atual
    corpo_atual = st.session_state.corpo_atual

    st.markdown('# CENTRAL DE EMAILS')
    destinatarios = st.text_input('Destinatarios do email: ', value=destinatario_atual)
    titulo = st.text_input('Titulo do email: ', value=titulo_atual)
    corpo = st.text_area('Corpo do email: ', value=corpo_atual, height=400)
    col1, col2, col3 = st.columns(3)
    col1.button('Enviar email', use_container_width=True, on_click = enviar_email, args= (destinatarios, titulo, corpo))
    col3.button('Limpar ', use_container_width=True, on_click=limpar)

    st.session_state.destinatarios_atual = destinatarios
    st.session_state.titulo_atual = titulo
    st.session_state.corpo_atual = corpo

def limpar():
    st.session_state.destinatarios_atual = ''
    st.session_state.titulo_atual = ''
    st.session_state.corpo_atual = ''

def enviar_email(destinatarios, titulo, corpo):
    destinatarios = destinatarios.replace(' ', '').split(',')
    email_usuario = le_usuario()
    chave = chave_usuario()
    if email_usuario == '':
        st.error("Por favor, preencha um e-mail na pagina de configuração.")
    elif chave == '':
        st.error("Por favor, preencha a chavena pagina de configuração.")

    envia_email(email_usuario, destinatarios=destinatarios, titulo=titulo, corpo=corpo, senha_app=chave)

# =================== TEMPLATES =====================    
def templates():
    st.markdown('# Templates')
    
    for arquivo in pasta_template.glob('*.txt'):
            nome_arquivo = arquivo.stem.replace('_', ' ').upper()
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            col1.button(nome_arquivo, key=f'{nome_arquivo}', use_container_width=True, on_click=usar_template, args=(nome_arquivo, ))
            col2.button('EDITAR', key=f'editar_{nome_arquivo}', use_container_width=True, on_click=editar_template, args=(nome_arquivo, ))
            col3.button('REMOVER', key=f'remover_{nome_arquivo}', use_container_width=True, on_click= remover_template, args=(nome_arquivo, ))



    st.divider()
    st.button('Adicionar novo template', on_click=mudar_pagina, args=('add_novo_template',))
def pag_add_template(nome_template='', texto_template=''):
    nome_template = st.text_input('Nome do Template: ', value=nome_template)
    texto_template = st.text_area('Escreva o texto do template: ', value=texto_template, height=600)
    st.button('Salvar', on_click=salvar_template, args=(nome_template, texto_template))
    
def usar_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_template / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.corpo_atual = texto_arquivo
    mudar_pagina('home')

def salvar_template(nome, texto):
    pasta_template.mkdir(exist_ok=True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_template / nome_arquivo, 'w') as f:
        f.write(texto)
    mudar_pagina('templates')

def remover_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (pasta_template / nome_arquivo).unlink()

def editar_template(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_template / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.nome_template_editar = nome
    st.session_state.texto_template_editar = texto_arquivo
    mudar_pagina('editar_template')
# =================== LISTA DE EMAILS ===================== 
def lista_emails():
    st.markdown('# Lista de Emails')
    st.divider()
    for arquivo in pasta_email.glob('*.txt'):
        nome_arquivo = arquivo.stem.replace('_', ' ').upper()
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.button(nome_arquivo, key=f'{nome_arquivo}', use_container_width=True, on_click=usa_email, args=(nome_arquivo, ))
        col2.button('EDITAR', key=f'editar_{nome_arquivo}', use_container_width=True, on_click=editar_email, args=(nome_arquivo, ))
        col3.button('REMOVER', key=f'remover_{nome_arquivo}', use_container_width=True, on_click=remover_email, args=(nome_arquivo, ))

    st.divider()

    st.button('Adicionar Emails', on_click=mudar_pagina, args=('Add_novos_emails', ))

def pag_add_emails(nome_lista='', emails='' ):
    nome_lista = st.text_input('Nome da lista: ', value=nome_lista)
    emails = st.text_area('Escreva o Email: ', value=emails, height=600)
    st.button('Salvar', on_click=salvar_lista, args=(nome_lista, emails))
    pass


def usa_email(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_email / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.destinatarios_atual = texto_arquivo
    mudar_pagina('home')

def salvar_lista(nome, texto):
    pasta_email.mkdir(exist_ok=True)
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_email / nome_arquivo, 'w') as f:
        f.write(texto)
    mudar_pagina('lista_emails')

def remover_email(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    (pasta_email / nome_arquivo).unlink()

def editar_email(nome):
    nome_arquivo = nome.replace(' ', '_').lower() + '.txt'
    with open(pasta_email / nome_arquivo) as f:
        texto_arquivo = f.read()
    st.session_state.nome_email_editar = nome
    st.session_state.texto_email_editar = texto_arquivo
    mudar_pagina('editar_email')

# =================== CONFIGURAÇÃO ===================== 
def configuracao():
    st.markdown('# Configuração')
    email = st.text_input('Digite seu email: ')
    st.button('Salvar', key='salvar email', on_click=salvar_email, args=(email, ))
    chave = st.text_input('Digite a chave de  email: ')
    st.button('Salvar', key='salvar chave', on_click=salvar_chave, args=(chave, ))

def salvar_email(email):
    pasta_config.mkdir(exist_ok=True)  
    with open(pasta_config/ 'email_usuario.txt', 'w') as f: 
        f.write(email)

def salvar_chave(chave):
    pasta_config.mkdir(exist_ok=True)  
    with open(pasta_config/ 'chave.txt', 'w') as f:   
        f.write(chave)


def le_usuario():
    pasta_config.mkdir(exist_ok=True) 
    if (pasta_config / 'email_usuario.txt').exists():
        with open(pasta_config/'email_usuario.txt','r') as f:
            return f.read()
    return ''


def chave_usuario():
    pasta_config.mkdir(exist_ok=True) 
    if (pasta_config / 'chave.txt').exists():
        with open(pasta_config/'email_usuario.txt','r') as f:
            return f.read()
    return ''

# =================== MAIN ===================== 
def main():
    inicializacao()

    st.sidebar.button('Central de Emails', use_container_width=True, on_click=mudar_pagina, args=('home',))
    st.sidebar.button('Templates', use_container_width=True, on_click=mudar_pagina, args=('templates',))
    st.sidebar.button('Lista de Emails', use_container_width=True, on_click=mudar_pagina, args=('lista_emails',))
    st.sidebar.button('Configuração', use_container_width=True, on_click=mudar_pagina, args=('configuracao',))


    if st.session_state.pagina_central_email == 'home':
        home()
    elif st.session_state.pagina_central_email == 'templates':
        templates()
    elif st.session_state.pagina_central_email == 'add_novo_template':
        pag_add_template()
    elif st.session_state.pagina_central_email == 'editar_template':
        nome_template_editar =  st.session_state.nome_template_editar 
        texto_template_editar  = st.session_state.texto_template_editar 
        pag_add_template(nome_template_editar,texto_template_editar)
    elif st.session_state.pagina_central_email == 'lista_emails':
        lista_emails()
    elif st.session_state.pagina_central_email == 'Add_novos_emails':
        pag_add_emails()
    elif st.session_state.pagina_central_email == 'editar_email':
        nome_email = st.session_state.nome_email_editar 
        texto_email = st.session_state.texto_email_editar 
        pag_add_emails(nome_email, texto_email)
    elif st.session_state.pagina_central_email == 'configuracao':
        configuracao()
main()