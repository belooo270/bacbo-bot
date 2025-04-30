import telebot
import random
import threading
import time
import os

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
usuarios_auto = set()

# Variável para simular o "resultado real"
def obter_resultado_real():
    return random.choice(['🔵 <b>Player</b>', '🔴 <b>Banker</b>', '🟡 <b>Empate Dourado</b>'])

def prever_bacbo():
    resultados = [
        ('🔵 <b>Player</b>', 49.995),
        ('🔴 <b>Banker</b>', 49.995),
        ('🟡 <b>Empate Dourado</b>', 0.01)
    ]
    escolhas, pesos = zip(*resultados)
    return random.choices(escolhas, weights=pesos)[0]

def enviar_auto_previsao():
    while True:
        previsao = prever_bacbo()
        resultado_real = obter_resultado_real()

        acertou = previsao == resultado_real
        status = '✅ <b>ACERTOU!</b>' if acertou else '❌ <b>ERROU!</b>'

        mensagem = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🎲 <b>Bac Bo - Nova Previsão</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🧠 Previsão: {previsao}\n"
            f"🎯 Resultado Real: {resultado_real}\n"
            f"{status}\n\n"
            "⏳ Próxima previsão em 30s...\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )

        for user_id in list(usuarios_auto):
            try:
                bot.send_message(user_id, mensagem)
            except:
                pass

        time.sleep(30)

@bot.message_handler(commands=['start'])
def start(mensagem):
    usuarios_auto.add(mensagem.chat.id)
    bot.send_message(mensagem.chat.id, "✅ Previsões ativadas!\nVocê receberá sinais do Bac Bo automaticamente a cada 30 segundos.")

threading.Thread(target=enviar_auto_previsao).start()
bot.polling()
