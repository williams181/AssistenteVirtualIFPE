from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('assistenteVirtualIFPE')

trainer = ListTrainer(chatbot)

trainer.train(['olá bom dia!','bom dia, tudo bem?','voce poderia me ajudar?','sim, claro, o que o senhor precisa?'
            ,'onde fica a sala da coordenação?','subindo o corregor a esquerda!'
            ,'como faço para levar um livro para casa?','voce precisar preencher um pequeno formulario'
            ,'quanto tempo posso ficar com o livro?','voce pode ficar com o livro por no maximo 15 dias!'])

while True:
    request = input('voce: ')
    response = chatbot.get_response(request)
    print('Bot: ', response)