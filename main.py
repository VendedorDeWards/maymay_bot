import os, random, discord, json
#from dotenv import load_dotenv
#load_dotenv()


numbers=[1,2,3,4,5,6,7,8,9,10]
words=["hi ","hello ","hey ","hola "]
my_list=[]

client = discord.Client()

#puts value in the list
def new_list(l):
    l.append(random.choice(range(1,100)))
    for _ in range(6):
        l.append(random.choice(numbers))
    return l

#starts the game
def start(a):
    if my_list==[]:
        l=new_list(my_list)
        m=random.choice(words)+str(a)+"\n Here are the numbers: "+str(l[1:7])+"\n The goal is: "+str(l[0])
    else:
        m="Please end the previous game before starting a new one."
    return m

#check if the numbers used are in the list
def check_numbers(m,l):
    n=m.replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').replace(')',' ').replace('(',' ').split()
    for i in n:
        if int(i) in l:
            l.remove(int(i))
        else:
            return 0
    return 1

#ends the game
def end_game():
    my_list.clear()

#check the answer given by the player
def calculate(m,l, user):
    if l==[]:
        return "game hasn't started yet"
    #if player used incorrect numbers
    if(check_numbers(m,l[1:7].copy())==0):
        n="The numbers you used aren't correct.\nTry again, using these numbers: "+str(l[1:7])
    #if the numbers used are correct
    else:
        r=eval(m)
        #if answer is the same as the goal
        if r==l[0]:
            n='Congratulation you won!'
            update_score(user)
            end_game()
        else:
            n='Your result is: '+str(r)+'\nThe goal is: '+str(l[0])
    return n

def get_leaderboard():
    with open("./scores.json", "r") as f:
        return f.read()

def get_user_score(user):
    scores = json.loads(get_leaderboard())
    try:
        return scores[user]
    except KeyError:
        return False

def update_score(user):
    with open("./scores.json", "r") as f:
        old_scores = json.loads(f.read())
    with open("./scores.json", "w") as f:
        try:
            old_scores[user] += 1
        except KeyError:
            old_scores[user] = 1
            print(old_scores)
        f.write(json.dumps(old_scores))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    # to start the game
    elif message.content.startswith('$s'):
        m=start(message.author)
        await message.channel.send(m)
    # to give an answer
    elif message.content.startswith('$c '):
        m=message.content.split("$c ",1)[1]
        n=calculate(m, my_list, str(message.author))
        await message.channel.send(str(message.author)+'\n'+n)
    # to check general leaderboard
    elif message.content == "$leaderboard":
        await message.channel.send(get_leaderboard())
    # to check users score
    elif message.content.startswith("$score"):
        user_to_check = message.content.split("$score ", 1)[1]
        await message.channel.send(f"{user_to_check}'s score is: " + str(get_user_score(user_to_check)) if user_to_check else "That user doesn't exist!")
    # to check your score
    elif message.content == "$myscore":
        await message.channel.send("Your score is: " + str(get_user_score(str(message.author))))
    # to end game  
    elif message.content.startswith('$end'):
        end_game()
        await message.channel.send('game ended')

@client.event
async def on_error(event, *args, **kwargs):
    if (event == 'on_message') and (args[0].content.startswith('$c ')) :
        m=args[0].content.split('$c ',1)[1]
        await args[0].channel.send(f'Sorry I could not calculate: {m}\n')

client.run('ODExMDEyMzgxMTMwODgzMTAz.YCsAIw.bSuX5M6V-1Zx47WZ_7SK_I8OZ5E')
