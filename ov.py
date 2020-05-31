# Oveln 写的什么都想干的插件
import json
import os
import datetime
import time
from utils.rtext import *

# 常量表
Version = 'v1.0.1'
SavePath = './ov'
WLSavePath = './ov/WhiteList.json'
BotsSavePath = './ov/Bots.json'
PlayersSavePath = './ov/Players.json'
CommandsPath = './ov/Commands.json'
Perfix = '!!ov'
ele = {
    '-1':'minecraft:the_nether',
    '0':'minecraft:overworld',
    '1':'minecraft:the_end'
}
# admin 3
# helper 2
# user 1
MiniPermissionLevel = {
    'wl':2,
    'bot':2,
    'time':1,
    'cls':1,
    'sp':1,
    'goout':2,
    'cmd':3
}

#变量表
ClsBool = True
WhiteList = []
NumberOfPeople = 0
Bots = {

}
Players = {

}
Commands = []

def command_run(message, text, command):
	return RText(message).set_hover_text(text).set_click_event(RAction.run_command, command)
def command_input(message, text, command):
    return RText(message).set_hover_text(text).set_click_event(RAction.suggest_command, command)
def doHelpMessage(s):
    if (s=='ov'):
        return '''
------- MCDR ov '''+Version+''' -----
        '''+command_run('§e§o§nOveln§r','夸赞Oveln','OvelnNB!')+'''做的啥都想干的插件
§c【指令说明】§r
'''+command_run('§e{}§r'.format(Perfix),'执行','{}'.format(Perfix))+'''                查看ov插件说明§r
'''+command_run('§e{} wl§r'.format(Perfix),'执行','{} wl'.format(Perfix))+'''             玩家白名单功能
'''+command_run('§e{} bot§r'.format(Perfix),'执行','{} bot'.format(Perfix))+'''            服务器假人功能
'''+command_run('§e{} cmd§r'.format(Perfix),'执行','{} cmd'.format(Perfix))+'''            服务器命令集
'''+command_run('§e{} time§r'.format(Perfix),'执行','{} time'.format(Perfix))+'''            在线时长统计
'''+command_run('§e{} cls§r'.format(Perfix),'执行','{} cls'.format(Perfix))+'''            清理掉落物
'''+command_input('§e{} goout 玩家名§r'.format(Perfix),'输入','{} goout 玩家名'.format(Perfix))+'''            踢人
'''
    if (s=='wl'):
        return '''
------- MCDR ov '''+Version+''' -----
§c【指令说明】§r
'''+command_input('§e{} wl add 玩家名§r'.format(Perfix),'输入','{} wl add 玩家名'.format(Perfix))+''' 添加玩家白名单 
'''+command_input('§e{} wl del 玩家名§r'.format(Perfix),'输入','{} del 玩家名'.format(Perfix))+''' 删除玩家白名单
'''+command_run('§e{} wl list§r'.format(Perfix),'执行','{} wl list'.format(Perfix))+'''         查看玩家白名单
'''
    if (s=='bot'):
        return '''
------- MCDR ov '''+Version+''' -----
§c【功能说明】§r
假人会在所有玩家§c下线之后§r出现在§c设置好的位置§r
§c【指令说明】§r
'''+command_input('§e{} bot set 假人名 [x,y,z,p]§r'.format(Perfix),'输入','{} bot set 假人名 x,y,z,p'.format(Perfix))+'''     添加假人,-1地狱,0主世界,1末地 
'''+command_input('§e{} bot del 假人名§r'.format(Perfix),'输入','{} bot del 假人名'.format(Perfix))+'''               删除假人
'''+command_input('§e{} bot lay 假人名§r'.format(Perfix),'输入','{} bot lay 假人名'.format(Perfix))+'''               直接放置假人
'''+command_input('§e{} bot unlay 假人名§r'.format(Perfix),'输入','{} bot unlay 假人名'.format(Perfix))+'''             取消放置假人
'''+command_run('§e{} bot list§r'.format(Perfix),'执行','{} bot list'.format(Perfix))+'''                         查看假人名单
'''
    if (s=='cmd'):
        return '''
------- MCDR ov '''+Version+''' -----
§c【指令说明】§r
'''+command_run('§e{} cmd do§r'.format(Perfix),'执行','{} cmd do'.format(Perfix))+'''                           执行命令集命令
'''+command_run('§e{} cmd read§r'.format(Perfix),'执行','{} cmd read'.format(Perfix))+'''                         热读取命令集
'''+command_run('§e{} cmd list§r'.format(Perfix),'执行','{} cmd list'.format(Perfix))+'''                         查看命令集
'''
#判断数字
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        for i in s:
            unicodedata.numeric(i)  # 把一个表示数字的字符串转换为浮点数返回的函数
            #return True
        return True
    except (TypeError, ValueError):
        pass
    return False
#文件操作
def InitDataPrint(data_, path):
    with open(path,'w') as f:
        data = json.dumps(data_)
        f.write(data)
def DataFromFile(data_, path):
    if not os.path.exists(path):
        InitDataPrint(data_, path)
    with open(path,'r') as f:
        data = json.load(f)
    return data
def DataSaveFile(data_, path):
    with open(path,'w') as f:
        data = json.dumps(data_)
        f.write(data)


def InitLoadFile():
    global WhiteList
    global Bots
    global Players
    global Commands
    if not os.path.exists(SavePath):
        os.makedirs(SavePath)
    WhiteList = DataFromFile(WhiteList,WLSavePath)
    Bots = DataFromFile(Bots,BotsSavePath)
    Players = DataFromFile(Players,PlayersSavePath)
    Commands = DataFromFile(Commands,CommandsPath)
def LayBot(server,Name, arti):
    Bots[Name][4] = arti
    server.execute('player '+Name+' spawn at '+Bots[Name][0]+' '+Bots[Name][1]+' '+Bots[Name][2]+' facing 1 1 in '+ele[Bots[Name][3]])
def KillBot(server,Name):
    Bots[Name][4] = False
    server.execute('player '+Name+' kill')
def LayBots(server):
    for i in Bots.keys() :
        if not Bots[i][4] :
            LayBot(server, i , False)
def UnLayBots(server):
    for i in Bots.keys() :
        if not Bots[i][4] :
            KillBot(server, i)
def CalcTime(Ti):
    ret = datetime.timedelta(days = Ti[0][0] , seconds = Ti[0][1]) 
    if (Ti[1] != ''):
        ret =ret  + (datetime.datetime.now()-datetime.datetime.strptime(Ti[1],'%Y-%m-%d-%H:%M:%S'))
    ret = ret - datetime.timedelta(microseconds=ret.microseconds)
    return '§c'+str(ret)+'§r'
def dowl(server, command,cmd_len):
    if cmd_len==2:
        return doHelpMessage('wl')
    #add
    if command[2]=='add':
        if (cmd_len == 3):
            return '请输入玩家名'
        if (cmd_len > 4):
            return '指令错误'
        try:
            WhiteList.index(command[3])
            return '已有该玩家白名单'
        except:
            WhiteList.append(command[3])
            DataSaveFile(WhiteList,WLSavePath)
            return '添加成功'
    #del    
    if command[2]=='del':
        if (cmd_len == 3):
            return '请输入玩家名'
        if (cmd_len > 4):
            return '指令错误'
        try:
            id = WhiteList.index(command[3])
            WhiteList.pop(id)
            DataSaveFile(WhiteList,WLSavePath)
            return '删除成功'
        except:
            return '没有该玩家白名单'
    #list
    if command[2]=='list' or command[2]=='li':
        return str(WhiteList)

def dobot(server, command,cmd_len):
    if cmd_len==2:
        return doHelpMessage('bot')
    if command[2]=='set':
        if (cmd_len == 3):
            return '请输入假人名字'
        if (cmd_len == 4):
            return '请输入假人坐标'
        if (cmd_len > 5):
            return '指令错误'
        pos = command[4].split(',')
        print(str(pos))
        if len(pos) ==3 and is_number(pos[0]) and is_number(pos[1]) and is_number(pos[2]):
            pos.append('0')
            pos.append(False)
            Bots[command[3]] = pos
            DataSaveFile(Bots,BotsSavePath)
            return '添加成功'
        if len(pos) ==4 and is_number(pos[0]) and is_number(pos[1]) and is_number(pos[2]) and is_number(pos[3]):
            print(pos)
            pos.append(False)
            Bots[command[3]] = pos
            DataSaveFile(Bots,BotsSavePath)
            return '添加成功'
        else:
            return '坐标错误'
    if command[2] == 'del':
        if (cmd_len == 3):
            return '请输入假人名字'
        if (cmd_len>4):
            return '指令错误'
        try:
            if Bots[command[3]][3] :
                KillBot(server,command[3])
            del Bots[command[3]]
            DataSaveFile(Bots,BotsSavePath)
            return '删除成功'
        except:
            return '假人不存在'
    if command[2] == 'lay':
        if (cmd_len == 3):
            return '输入假人名字'
        if (cmd_len > 4):
                return '指令错误'
        if command[3] in Bots.keys():
            LayBot(server,command[3],True)
            DataSaveFile(Bots,BotsSavePath)
            return '放置成功'
        else:
            return '假人不存在'
    if command[2] == 'unlay':
        if (cmd_len == 3):
            return '输入假人名字'
        if (cmd_len > 4):
                return '指令错误'
        if command[3] in Bots.keys():
            KillBot(server,command[3])
            DataSaveFile(Bots,BotsSavePath)
            return '取消放置成功'
        else:
            return '假人不存在'
    if command[2] == 'list':
        return str(Bots)
    if command[2] == 'NumPlayer':
        return str(NumberOfPeople)
    if command[2] == 'reloadNum' :
        server.execute("list")
        return '重新加载人数成功'
        
def takeSecond(elem):
    return elem[1]

def dotime(server , command , cmd_len):
    if cmd_len == 2 :
        ret = '------------§c玩家在线时间§r------------\n'
        times = []
        for i in Players.keys():
            times.append([i,CalcTime(Players[i])])
        times.sort(reverse = True,key=takeSecond)
        for i in times:
            ret = ret+'§e'+i[0]+'§r'+(' '*(65-len(i[0])*2-len(i[1])*2))+i[1]+'\n'
        return ret
    if command[2] in Players.keys():
        return '§e'+command[2]+'§r'+' '+CalcTime(Players[command[2]])
    if command[2] == 'time':
        return str(Players)

def docls(server , command , cmd_len):
    global ClsBool
    ClsBool = True
    for sec in range(0,30):
        if sec==0 or sec==10 or sec>=20 :
            server.say(command_run('还有§c{}§r秒清除掉落物'.format(30-sec),'点击终止清除','{} sp'.format(Perfix)))
        for i in range(1,10):
            time.sleep(0.1)
            if not ClsBool:
                server.say('中止清除掉落物')
                return
    server.execute('kill @e[type=item]')
def dogoout(server , command , cmd_len):
    if cmd_len==3:
        server.execute('ban '+command[2])
        server.execute('pardon '+command[2])
        return '滚蛋了！'
    else:
        return '你输入的啥？？？'
def docmd(server , command , cmd_len):
    global Commands
    if cmd_len==2 :
        return doHelpMessage('cmd')
    if cmd_len==3 and command[2]=='do':
        for cmd in Commands:
            server.execute(cmd)
        return '执行了'+str(len(Commands))+'个命令'
    if cmd_len==3 and command[2]=='read':
        Commands = DataFromFile(Commands,CommandsPath)
        return '读取成功'
    if cmd_len==3 and command[2]=='list':
        return str(Commands)
def on_player_left(server, player):
    #检测是否是假人，如果是就重生
    if not player in Players.keys():
       if Bots[player][4]:
           LayBot(server,player,Bots[player][4])
    else:
        #人数统计
        global NumberOfPeople
        NumberOfPeople = NumberOfPeople - 1
        if NumberOfPeople == 0 :
            LayBots(server)
        #在线时长更新
        now = Players[player]
        times = datetime.timedelta(days=now[0][0] , seconds=now[0][1]) + (datetime.datetime.now()-datetime.datetime.strptime(now[1],'%Y-%m-%d-%H:%M:%S'))
        Players[player] = [[times.days,times.seconds],'']
        DataSaveFile(Players,PlayersSavePath)

def on_player_joined(server , player):
    #whitelist check
    try:
        WhiteList.index(player)
    except:
        server.execute('ban '+player)
        server.execute('pardon '+player)
    
    if not (player in Bots.keys()):
        #人数统计
        global NumberOfPeople,Players
        NumberOfPeople = NumberOfPeople + 1
        if NumberOfPeople == 1 :
            UnLayBots(server)
        #在线时长更新
        if not player in Players:
            Players[player] = [[0,0],datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')]# Players[]=[总时长(s),上线时间]
            DataSaveFile(Players,PlayersSavePath)
        else:
            Players[player][1] = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            DataSaveFile(Players,PlayersSavePath)
def on_load(server, old_module):
    server.add_help_message('!!ov', 'ov插件帮助')
    InitLoadFile()
    #Query Number of player
    server.execute('list')
def on_info(server, info):
    command = info.content.split()
    if (info.player == None):
        if command[0] == 'There':
            global NumberOfPeople
            NumberOfPeople = int(command[2])
            return
    if len(command) == 0 or command[0] !=Perfix :
        return
    cmd_len = len(command)
    
    # MCDR permission check
    global MiniPermissionLevel
    if cmd_len >= 2 and command[1] in MiniPermissionLevel.keys():
        if server.get_permission_level(info) < MiniPermissionLevel[command[1]]:
            server.reply(info , '§c权限不足！§r')
            return
    
    #!!ov
    if cmd_len == 1:
        server.reply(info , doHelpMessage('ov'))
    #wl
    if cmd_len >= 2 and command[1] == 'wl':
        server.reply(info , dowl(server , command , cmd_len))
    #bot
    if cmd_len>=2 and command[1] == 'bot':
        server.reply(info , dobot(server,command,cmd_len))
    #time
    if cmd_len>=2 and command[1] == 'time':
        server.reply(info , dotime(server,command,cmd_len))
    #cls
    if cmd_len>=2 and command[1] == 'cls':
        server.reply(info , docls(server,command,cmd_len))
    #sp
    if cmd_len>=2 and command[1] == 'sp':
        global ClsBool
        ClsBool = False
    #goout
    if cmd_len>=2 and command[1] == 'goout':
        server.reply(info , dogoout(server,command,cmd_len))
    if cmd_len>=2 and command[1] == 'cmd':
        server.reply(info , docmd(server,command,cmd_len))