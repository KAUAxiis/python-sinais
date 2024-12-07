import time
import random
import telebot
from telebot import types
from datetime import datetime, timedelta
import threading  # Importa threading para execução assíncrona

# Configurações principais
api_key = '7779565596:AAHdQS_ZRcSOb8an-ghQHoyrNnF2evIEibU'
chat_id = '-1002395060138'
admin_id = 5186608966  # Apenas esse usuário pode executar comandos

# Links e informações da Arke999
link_principal = "https://criptongood.com/home/login"
nome_plataforma = "Criptonᵍᵒᵒᵈ"

# Mensagens promocionais com banners
mensagens_promocionais = [
    f'''🌟 <b>VENHA PARA A {nome_plataforma.upper()}!</b> 🌟
    💰 <i>As melhores oportunidades de ganho estão esperando por você!</i>
    👉 <a href="{link_principal}">Clique aqui para jogar agora!</a> 👈''',
    
    f'''🎉 <b>SEJA PARTE DA {nome_plataforma.upper()}!</b> 🎉
    🤑 <i>Receba bônus e prêmios ao registrar-se!</i>
    👉 <a href="{link_principal}">Aproveite agora mesmo!</a> 👈''', 

    f'''💎 <b>OPORTUNIDADE ÚNICA NA {nome_plataforma.upper()}!</b> 💎
    🎁 <i>Ganhos e vantagens exclusivas para novos jogadores!</i>
    👉 <a href="{link_principal}">Venha jogar com a gente!</a> 👈'''
]

# Lista de jogos com os respectivos nomes e fotos
games = {
    "Fortune Tiger": "Fortune_Tiger.jpg",
    "Fortune Rabbit": "Fortune_Rabbit.jpg",
    "Fortune Ox": "Fortune_Ox.jpg",
    "Fortune Mouse": "Fortune_Mouse.jpg",
    "Cash Mania": "Cash_Mania.jpg"
}

# Variável global para armazenar dados do último sinal
ultimo_sinal = {}
auto_registro = True  # Status de mensagens automáticas

# Inicializa o bot com a chave de API fornecida
bot = telebot.TeleBot(api_key)

# Função para enviar um sinal
def enviar_sinal():
    global ultimo_sinal

    # Exclui o jogo atual da lista de jogos disponíveis para garantir diversidade
    jogos_disponiveis = [game for game in games.items() if game[0] != ultimo_sinal.get('game_name')]

    if len(jogos_disponiveis) == 0:
        jogos_disponiveis = list(games.items())  # Reinicia quando todos os jogos já foram enviados

    game_name, game_image = random.choice(jogos_disponiveis)
    ultimo_sinal['game_name'] = game_name
    ultimo_sinal['game_image'] = game_image
    
    rodadas_normal = random.randint(3, 12)
    rodadas_turbo = random.randint(3, 12)
    valido_ate = random.randint(2, 4)
    ultimo_sinal['valido_ate'] = valido_ate

    # Calcular o horário de expiração
    hora_atual = datetime.now()
    expira_ate = hora_atual + timedelta(minutes=valido_ate)
    
    # Ajustar para não ultrapassar 59 minutos e 59 segundos
    if expira_ate.minute >= 60:
        expira_ate = expira_ate.replace(hour=expira_ate.hour + 1, minute=0, second=0)

    expira_ate_formatada = expira_ate.strftime("%H:%M:%S")  # Formato de hora:minuto:segundo

    mensagem_sinal = f'''
🎰 <b>SINAL ENCONTRADO!</b> 🎰

🎮 <b>{game_name}</b> 🎮

🔄 <b>Repita no Máximo:</b> 2 vezes
⏳ <b>Rodadas Normal:</b> {rodadas_normal}x
⚡ <b>Rodadas Turbo:</b> {rodadas_turbo}x
⏱️ <b>Válido até:</b> {valido_ate} minutos (até as {expira_ate_formatada})

💥 <i>Aproveite esta oportunidade de ganhar!</i> 💥

© {nome_plataforma}
'''

    # Criação dos botões de link
    markup = types.InlineKeyboardMarkup()
    botao_jogar = types.InlineKeyboardButton("🎮 Jogue agora", url=link_principal)
    botao_cadastro = types.InlineKeyboardButton("🎁 Cadastre-se e ganhe bônus", url=link_principal)
    markup.add(botao_jogar, botao_cadastro)

    # Enviar a mensagem com a imagem do jogo e os botões
    with open(game_image, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, caption=mensagem_sinal, parse_mode='HTML', reply_markup=markup)
    print(f"[INFO] Mensagem de sinal enviada para o jogo '{game_name}'")

    ultimo_sinal['rodadas_normal'] = rodadas_normal
    ultimo_sinal['rodadas_turbo'] = rodadas_turbo

    # Envia o resultado após o tempo de validade
    time.sleep(valido_ate * 60)
    enviar_resultado()
    time.sleep(15)
    enviar_sinal()

# Função para enviar o resultado de uma partida
def enviar_resultado():
    total_jogadores = random.randint(15, 20)
    total_vencedores = total_jogadores - random.randint(0, 5)

    mensagem_resultado = f'''
🏆 <b>RESULTADOS DA PARTIDA</b> 🏆

🎮 <u>{ultimo_sinal['game_name']}</u> 🎮

👥 <b>Total de pessoas que jogaram:</b> {total_jogadores}
🎉 <b>Total de pessoas que ganharam:</b> {total_vencedores}

🎊 <i>Parabéns aos vencedores!</i> 🎊

© {nome_plataforma}
'''

    # Criação dos botões de link
    markup = types.InlineKeyboardMarkup()
    botao_jogar = types.InlineKeyboardButton("🎮 Jogue agora", url=link_principal)
    botao_cadastro = types.InlineKeyboardButton("🎁 Cadastre-se e ganhe bônus", url=link_principal)
    markup.add(botao_jogar, botao_cadastro)

    # Enviar a mensagem de resultado
    bot.send_message(chat_id=chat_id, text=mensagem_resultado, parse_mode='HTML', reply_markup=markup)
    print(f"[INFO] Mensagem de resultados enviada para o jogo '{ultimo_sinal['game_name']}'")

# Função para enviar uma mensagem promocional
def enviar_mensagem_promocional():
    mensagem_promocional = random.choice(mensagens_promocionais)

    # Imagem promocional
    image_path = "promo_image.jpg"  # Coloque o caminho para sua imagem promocional

    # Enviar a mensagem promocional com a imagem
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, caption=mensagem_promocional, parse_mode='HTML')

    print("[INFO] Mensagem promocional enviada.")

# Função para agendar envio automático de mensagens promocionais a cada 10 minutos
def agendar_mensagem_promocional():
    global auto_registro
    def loop_agendamento():
        while True:
            if auto_registro:
                print("[INFO] Enviando mensagem promocional...")
                time.sleep(600)
                enviar_mensagem_promocional()
    
    # Inicia o agendamento em uma thread separada
    agendamento_thread = threading.Thread(target=loop_agendamento)
    agendamento_thread.daemon = True  # Permite que a thread seja encerrada quando o programa terminar
    agendamento_thread.start()

# Função para notificar o administrador
def notificar_admin():
    data_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_admin = f"🟢 O bot foi iniciado em {data_inicio}.\nID do administrador: {admin_id}."
    bot.send_message(admin_id, mensagem_admin)

# Função de gerenciamento de comandos
@bot.message_handler(commands=['start', 'stop', 'arke', 'autoregistrar', 'limpar'])
def handle_command(message):
    if message.from_user.id != admin_id:
        bot.reply_to(message, "🚫 Comando recusado.")
        print(f"[WARNING] Comando recusado para o usuário com ID: {message.from_user.id}")
        return

    if message.text == '/start':
        bot.reply_to(message, "🔑 Por favor, registre-se! Aguarde...") 
        time.sleep(2)
        bot.reply_to(message, "🚀 Bot iniciado!")
        notificar_admin()
        enviar_sinal()
        
    elif message.text == '/stop':
        bot.reply_to(message, "🛑 O bot foi interrompido.")
        print("[INFO] O bot foi interrompido.")
        exit()

    elif message.text == '/arke':
        bot.reply_to(message, f"🔗 Acesse o site oficial da {nome_plataforma}: {link_principal}")

    elif message.text == '/autoregistrar':
        auto_registro = not auto_registro
        status = "ativado" if auto_registro else "desativado"
        bot.reply_to(message, f"Auto registro {status}.")

    elif message.text == '/limpar':
        ultimo_sinal.clear()
        bot.reply_to(message, "🧹 Todos os dados foram limpos.")

# Agendar o envio de mensagens promocionais
agendar_mensagem_promocional()

# Iniciar o bot
bot.polling(non_stop=True)
