from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random
import re

app = Flask(__name__)

groupName = 'Group Name'
whatsappGroupLink = 'https://chat.whatsapp.com/<link>'
friendsNames = ["Salomón","Ladslao","Nicomedes","Julia","Guilermo","Isaías","Joel","Pablo","Lucano"]
pickedFriends = []
phoneNumberList = {}

def pickFriend(friendName):
    global friendsNames, pickedFriends
    availableFriends = list(set(friendsNames) - set(pickedFriends))
    random.shuffle(availableFriends)
    randFriend = ""
    maxIterations = len(availableFriends)
    index = 0
    while index < maxIterations:
        randFriend = availableFriends[index]
        if friendName != randFriend:
            pickedFriends.append(availableFriends[index])
            break
        index += 1

    return randFriend


@app.route('/bot', methods=['POST'])
def bot():
    newMessage = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()

    phoneNumber = request.values.get('WaId')

    if phoneNumber in phoneNumberList:
        msg.body('Opsss, parece que você já está participando do *{groupName}* 😅.\n\nPara proteger a integridade do sorteio, é permitido apenas um sorteio por número de celular.\n\nCaso tenha esquecido quem você sorteou ou esteja com dúvidas, comunique para todos no grupo em: *{whatsappGroupLink}*.')
        return str(resp)

    responded = False
    if newMessage.lower() in ['quero', 'participar', 'quero participar', 'olá', 'ola', 'oi', 'começar', 'sorteio', 'amigo', 'amigo oculto', 'amigo secreto']:
        msg.body('Olá, seja bem vindo ao *{groupName}*.\n\nCaso você ainda não esteja participando do nosso grupo do Whatsapp, por favor acesse o link: *{whatsappGroupLink}* e peça para o administrador adicionar o seu nome na lista de participantes 😊.\n\nPara ingressar no sorteio, primeiro nos responda: qual seu PRIMEIRO nome?')
        responded = True
    if not responded:
        participante = newMessage
        if len(participante.split(' ')) > 1:
            responded = False
            msg.body('Por favor, repita seu nome sem espaços, somente o PRIMEIRO nome. Exemplo: João')
            return str(resp)
        elif not participante in friendsNames:
            msg.body('Seu nome parece não estar na lista de interessados, por favor comunique no nosso grupo do Whatsapp o ocorrido.')
        else:
            amigo = pickFriend(participante)
            if amigo == "":
                msg.body("Todos os nomes já foram sorteados. Obrigado pela participação.")
            else:
                msg.body(
                    f'Seu AMIGO SECRETO é: *{amigo}* 🥳\n\nPense com carinho na escolha do presente 🎁🤩\n\nLembre-se de não compartilhar essa informação com ninguém! 🤫🙊\n\nRecomendamos que delete essa conversa para ninguém descobrir 🤭👀')
                phoneNumberList[phoneNumber] = {'name': participante}
                print(phoneNumberList)
    return str(resp)


if __name__ == '__main__':
    app.run(port=4000)
