import discord
from django.http import JsonResponse
from rest_framework.decorators import api_view
import threading
import asyncio


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


greetings_responses = {
    'hello': 'Hello! How can I assist you today?',
    'hi': 'Hi there! Hope you are doing well.',
    'how are you': 'I am just a bot, but thank you for asking! How are you?'
}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user_message = message.content.lower()
    
    if user_message in greetings_responses:
        await message.channel.send(greetings_responses[user_message])
    else:
        await message.channel.send("I'm not sure how to respond to that, but I'm learning!")


bot_thread = None
loop = None


def run_bot():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start('Your-Discord-Bot-Token'))

@api_view(['POST'])
def toggle_bot(request):
    global bot_thread, loop

    if request.data.get('status') == 'start' and bot_thread is None:
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
        return JsonResponse({'status': 'Bot started'}, status=200)

    elif request.data.get('status') == 'stop' and bot_thread is not None:
        asyncio.run_coroutine_threadsafe(client.close(), loop)
        loop.stop()
        bot_thread.join()
        bot_thread = None
        return JsonResponse({'status': 'Bot stopped'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)













# import discord
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# import threading

# # Discord bot configuration
# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

# # Predefined responses for common greetings
# greetings_responses = {
#     'hello': 'Hello! How can I assist you today?',
#     'hi': 'Hi there! Hope you are doing well.',
#     'how are you': 'I am just a bot, but thank you for asking! How are you?'
# }

# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     user_message = message.content.lower()
    
#     # Check if the message matches a greeting
#     if user_message in greetings_responses:
#         await message.channel.send(greetings_responses[user_message])
#     else:
#         await message.channel.send("I'm not sure how to respond to that, but I'm learning!")

# # Variable to store bot status
# bot_thread = None

# # Function to run bot
# def run_bot():
#     client.run('Your-Discord-Bot-Token')

# @api_view(['POST'])
# def toggle_bot(request):
#     global bot_thread
#     if request.data.get('status') == 'start' and bot_thread is None:
#         bot_thread = threading.Thread(target=run_bot)
#         bot_thread.start()
#         return JsonResponse({'status': 'Bot started'}, status=200)
#     elif request.data.get('status') == 'stop' and bot_thread is not None:
#         client.close()
#         bot_thread = None
#         return JsonResponse({'status': 'Bot stopped'}, status=200)
#     return JsonResponse({'error': 'Invalid request'}, status=400)
