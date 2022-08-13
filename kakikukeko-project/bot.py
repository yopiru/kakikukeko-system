import json
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import discord
import dislash
from discord.ext import commands
from discord import Client,Embed,webhook,WebhookMessage
from dislash import InteractionClient,Button,ActionRow,ButtonStyle,OptionType,Option

#テンプデータ用の辞書定義
discordidtemp = {}
mcidtemp3 = {}
mcidtemp2 = {}
mcidtemp = {}
gbantemp = {}
gbantemp2 = {}
flag = {}
#discord.py,dislash.pyの色々定義
intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix="Kaiueo.",intents=intents)
interclient = InteractionClient(bot)
#↓使うかどうか怪しいww(webhook用の名前)
HOOK_NAME = "かきくけこコミュニティ管理BOT"
#sqlalchemy色々定義
engine = create_engine('sqlite:///mcid_date.db',encoding="utf-8",echo=False)
session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = session.query_property()
class mcid_date(Base):
    __tablename__ = "mcid_date"
    id = Column(Integer,primary_key=True)
    discordid = Column(Integer,unique=True)
    mcid = Column(String,unique=True)
    uuid = Column(String,unique=True)
    be_mcid = Column(String,unique=True)
    
    def __init__(self, id=None,discordid=None,mcid=None,uuid=None,be_mcid=None):
        self.id = id
        self.discordid = discordid
        self.mcid = mcid
        self.uuid = uuid
        self.be_mcid = be_mcid
class gban_system(Base):
    __tablename__ = "gban_system"
    id = Column(Integer,primary_key=True)
    userid = Column(Integer,unique=True)
    cause = Column(String,unique=True)

    def __init__(self, id=None,userid=None,cause=None):
        self.id = id
        self.userid = userid
        self.cause = cause
Base.metadata.create_all(bind=engine)
#BOT起動の動作
@bot.event
async def on_ready():
    print('BOT起動')
    activity = discord.Activity(name='かきくけこコミュニティ', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
#スラッシュコマンドエラー
@bot.event
async def on_slash_command_error(inter, error):
    if isinstance(error,dislash.slash_commands.errors.MissingPermissions):
        embed1 = discord.Embed(title=('エラー'),description='権限不足です。',color=discord.Color.red())
        await inter.reply(embed=embed1, ephemeral=True)
    elif isinstance(error,dislash.slash_commands.errors.BotMissingPermissions):
        emd = discord.Embed(title=('エラー'),description='botに必要な権限がありません。',color=discord.Color.red())
        await inter.reply(embed=emd, ephemeral=True)
    elif isinstance(error,dislash.slash_commands.errors.BotMissingAnyRole):
        emd5 = discord.Embed(title='エラー',description='botに必要な権限がありません。')
        await inter.reply(embed=emd5, ephemeral=True)
    elif isinstance(error,dislash.slash_commands.errors.BadArgument):
        emd2 = discord.Embed(title=('エラー'),description='引数がエラーをおこしています。',color=discord.Color.red())
        await inter.reply(embed=emd2, ephemeral=True)
    else:
        embed2 = discord.Embed(title=('エラー'), description='不明なエラーが発生しました。',color=discord.Color.red())
        embed2.add_field(name='エラーログ',value=error)
        await inter.reply(embed=embed2, ephemeral=True)
        raise error
#データベースの内容削除
@interclient.slash_command(
    name = "dbedit",
    description = 'データベースの操作します。(よぴるのみ実行可能)',
    options = [Option('discordid',"discordid",OptionType.STRING),Option("mcid","mcid",OptionType.STRING),Option("be_mcid","be_mcid",OptionType.STRING),Option("editmcid","変更後のMCID書く",OptionType.STRING)],
    test_guilds="943859907877306478",
)
async def dbedit(inter,discordid=None,mcid=None,be_mcid=None,editmcid=None):
    if inter.author.id == 400604650233135115:
        if discordid == None and mcid == None and be_mcid == None and editmcid == None:
            await inter.respond(content="なんも指定しないぞ",ephemeral=True)
        else:
            row = ActionRow(Button(style=ButtonStyle.red,label="削除",custom_id="yes"),Button(style=ButtonStyle.green,label="書き換え",custom_id="no"))
            emd5 = discord.Embed(title="どうしますか?",description=f"選択情報 \n **discordid**: {discordid} \n **MCID**: {mcid} \n **editmcid**: {editmcid} \n **be_mcid**: {be_mcid}",color=discord.Color.red())
            msg = await inter.reply(content="",embed=emd5,components=[row], ephemeral=True)
            on_click = msg.create_click_listener(timeout=20)
            mcidtemp[inter.author.id] = mcid
            if not discordid == None:
                discordidtemp[inter.author.id] = discordid
            if not mcid == None:
                mcidtemp2[inter.author.id] = mcid
            if not editmcid == None:
                mcidtemp3[inter.author.id] = editmcid
            @on_click.not_from_user(inter.author,cancel_others=True, reset_timeout=False)
            async def on_wrong_user(inter):
                await inter.reply("あなたが実行した、コマンドではありません。", ephemeral=True)
            @on_click.matching_id("yes")
            async def on_yes(inter):
                if inter.author.id in discordidtemp:
                    await inter.reply("データベースの情報を取得中 <a:road:969468636068732968>", ephemeral=True)
                    discordid = discordidtemp[inter.author.id]
                    date = session.query(mcid_date).all()
                    userid = (int(discordid))
                    for datekun in date:
                        if datekun.discordid == userid:
                            await inter.edit("データベースの情報を削除中 <a:road:969468636068732968>")
                            editmcid = session.query(mcid_date).filter(mcid_date.discordid == userid).first()
                            session.delete(editmcid)
                            session.commit()
                            await inter.edit("削除完了")
                else:
                    await inter.reply("わりー、削除はdiscordのユーザーID限定なんだ")
            @on_click.matching_id("no")
            async def on_no(inter):
                if inter.author.id in mcidtemp2.keys() and inter.author.id in mcidtemp3.keys():
                    date = session.query(mcid_date).all()
                    mcid = mcidtemp2[inter.author.id]
                    editmcid = mcidtemp3[inter.author.id]
                    for datekun in date:
                        if datekun.mcid == mcid:
                            await inter.reply("mojangのAPIに接続中 <a:road:969468636068732968>", ephemeral=True)
                            url = (f"https://api.mojang.com/users/profiles/minecraft/{editmcid}")
                            response = requests.get(url)
                            try:
                                uuid = response.json()["id"]
                            except:
                                emd3 = discord.Embed(title="存在しないMCIDもしくは、mojangのAPIにアクセスできません。",color=discord.Color.red())
                                await inter.edit(content="",embed=emd3)
                                return
                            await inter.edit("データベースの情報を更新中 <a:road:969468636068732968>")
                            editmcid1 = session.query(mcid_date).filter(mcid_date.mcid == datekun.mcid).first()
                            editmcid1.mcid = editmcid
                            editmcid1.uuid = uuid
                            session.commit()
                            mcidtemp2.pop(inter.author.id)
                            await inter.edit("更新完了")
                else:
                    await inter.reply("わりーな、削除するのには、MCIDとeditmcidに名前かいてや", ephemeral=True)
    else:
        await inter.respond("なんだろう、、、よぴるしか実行できないんすよ",ephemeral=True)
#MCID_LISTのデータベースにアクセス
@interclient.slash_command(
    name = "dbcheck_class_mcid_list",
    description = 'データベースの中身の確認します。(よぴるのみ実行可能)',
    options = [Option('discordid',"discordid",OptionType.STRING)],
    test_guilds="943859907877306478",
)
async def dbcheck_class_mcid_list(inter,discordid=None):
    if inter.author.id == 400604650233135115 or inter.author.id == 850621909942140938:
        if discordid == None:
            dates = session.query(mcid_date).all()
            emd = discord.Embed(title="mcid_date",color=discord.Color.purple())
            for datesan in dates:
                emd.add_field(name=f"id:{datesan.id}",value=f" **discordid**: {datesan.discordid} **mcid**: {datesan.mcid} \n **uuid**: {datesan.uuid} **be_mcid**: {datesan.be_mcid}")
            await inter.reply(embed=emd, ephemeral=True)
        else:
            discordid =(int(discordid))
            dates = session.query(mcid_date).all()
            for datekun in dates:
                if datekun.discordid == discordid:
                    emd = discord.Embed(title="discordユーザーID指定",description=f"**id**: {datekun.id} **discordid**: {datekun.discordid} **mcid**: {datekun.mcid} \n **uuid**: {datekun.uuid} **be_mcid**: {datekun.be_mcid}",color=discord.Color.purple())
                    await inter.reply(embed=emd, ephemeral=True)
                    return
            await inter.reply('指定ユーザーIDが見つかりませんでした。',ephemeral=True)
    else:
        await inter.reply(content="よぴるしか実行できません。", ephemeral=True)
#GBANシステムのデータベースにアクセス
@interclient.slash_command(
    name = "dbcheck_class_gban_system",
    description = 'データベースの中身の確認します。(よぴるのみ実行可能)',
    options = [Option('userid',"userid",OptionType.STRING)],
)
async def dbcheck_class_gban_system(inter,userid=None):
    if inter.author.id == 400604650233135115 or inter.author.id == 850621909942140938:
        if userid == None:
            emd = discord.Embed(title=('gban_system'),color=discord.Color.purple())
            dates = session.query(gban_system).all()
            for date in dates:
                emd.add_field(name=f"primary_key {date.id}",value=f"名前: <@{date.userid}> \n ユーザーID: {date.userid} \n 理由: {date.cause}")
            await inter.respond(embed=emd,ephemeral=True)
        else:
            emd = discord.Embed(title=('gban_system(id指定)'),color=discord.Color.purple())
            dates = session.query(gban_system).all()
            for date in dates:
                if userid == date.userid:
                    emd.add_field(name=f"primary_key {date.id}",value=f"名前: <@{date.userid}> \n ユーザーID: {date.userid} \n 理由: {date.cause}")
                    break
            await inter.respond(embed=emd,ephemeral=True)
    else:
        await inter.respond("なんだろう、、、実行するのやめてもらっていいですか?")
#java版マイクラサーバー参加登録用コマンド
@interclient.slash_command(
    name = "java_mcid_add",
    description = 'JAVA版のユーザーのMCIDをサーバーに参加できるように登録します。',
    options = [Option('mcid',"MCIDを書いてください。",OptionType.STRING,required=True)],
    test_guilds="943859907877306478",
)
async def java_mcid_add(inter,mcid=None):
    flag[inter.author.id] = False
    await inter.reply("データベース読み込み中 <a:road:969468636068732968>")
    dates = session.query(mcid_date).all()
    userid = (int(inter.author.id))
    flag1 = False
    for date in dates:
        if date.discordid == userid:
            if date.mcid == None:
                flag1 = True
                break
            else:
                row = ActionRow(Button(style=ButtonStyle.green,label="はい",custom_id="yes"),Button(style=ButtonStyle.red,label="いいえ",custom_id="no"))
                emd5 = discord.Embed(title="あなたは既に登録されています、変更しますか?",description="現在のあなたの登録情報" + "\n" + f"MCID: {date.mcid}" + "\n" + f"UUID: {date.uuid}",color=discord.Color.red())
                msg = await inter.edit(content="",embed=emd5,components=[row])
                on_click = msg.create_click_listener(timeout=20)
                mcidtemp[inter.author.id] = mcid
                @on_click.not_from_user(inter.author,cancel_others=True, reset_timeout=False)
                async def on_wrong_user(inter):
                    await inter.reply("あなたが実行した、コマンドではありません。", ephemeral=True)
                @on_click.matching_id("yes")
                async def on_yes(inter):
                    await msg.edit(content="変更処理を開始しました <a:road:969468636068732968>",embed=None,components=[])
                    mcid = mcidtemp[inter.author.id]
                    mcidlists = open('mcidlist.json','r')
                    mcidlist = json.load(mcidlists)
                    check = json.dumps(mcidlist)
                    userid = (int(inter.author.id))
                    for kakunin in check:
                        if kakunin == mcid:
                            await msg.edit(content="既に別の人が登録していますけど、、、、同じ人が2人以上いるんですか・・・?" ,embed=None)
                            return
                    else:
                        emd2 = discord.Embed(title="mojangのAPIに接続中 <a:road:969468636068732968>",color=discord.Color.blue())
                        await msg.edit(content="",embed=emd2)
                        url = (f"https://api.mojang.com/users/profiles/minecraft/{mcid}")
                        response = requests.get(url)
                        try:
                            uuid = response.json()["id"]
                        except:
                            emd3 = discord.Embed(title="存在しないMCIDもしくは、mojangのAPIにアクセスできません。",color=discord.Color.red())
                            await msg.edit(content="",embed=emd3)
                            return
                        else:
                            mcid = response.json()["name"]
                            emd4 = discord.Embed(title="既に登録済みです！！",description="大文字と小文字を変えて同じ人をもう一人登録しようとしないでください！！",color=discord.Color.red())
                            if mcid in check:
                                await msg.edit(content="",embed=emd4)
                                return
                            emd2 = discord.Embed(title="ファイル更新処理中 <a:road:969468636068732968>",color=discord.Color.blue())
                            await msg.edit(content="",embed=emd2)
                            userid = (int(inter.author.id))
                            try:
                                dates2 = session.query(mcid_date).all()
                                for datekun in dates2:
                                        if datekun.discordid == userid:
                                            deletetemp = {"name":datekun.mcid, "uuid":datekun.uuid}
                                            editmcid = session.query(mcid_date).filter(mcid_date.mcid == datekun.mcid).first()
                                            editmcid.mcid = mcid
                                            editmcid.uuid = uuid
                                            session.commit()
                                            break
                                temp = {"name":mcid,"uuid":uuid}
                                mcidlist.append(temp)
                                mcidlist.remove(deletetemp)
                                with open('mcidlist.json','w') as f:
                                    json.dump(mcidlist,f,ensure_ascii=False, indent=4)
                            except:
                                emd = discord.Embed(title="エラーが発生しました。",description="データベースの保存時にエラーが発生しました。申し訳ございませんが、\n <@400604650233135115> に伝えてください。(伝えないと、後々めんどうなことになるかもしれません。)",color=discord.Color.red())
                                await msg.edit(embed=emd)
                                return
                            emd = discord.Embed(title="ユーザー情報の上書き保存をしました。",description="登録情報" + "\n" + f"MCID: {mcid}" + "\n" + f"UUID: {uuid}",color=discord.Color.purple())
                            await msg.edit(embed=emd)
                            mcidlists.close
                    mcidtemp.pop(inter.author.id)
            @on_click.matching_id("no")
            async def on_no(inter):
                await msg.edit(content="変更せずに終了しました。",embed=None,components=[])
                mcidtemp.pop(inter.author.id)
                return
            @on_click.timeout
            async def on_timeout():
                if inter.author.id in flag.keys():
                    flag.pop(inter.author.id)
                else:
                    await msg.edit(content="変更せずに終了しました。",embed=None,components=[])
                if inter.author.id in mcidtemp.keys():
                    mcidtemp.pop(inter.author.id)
                else:
                    pass
                return
        else:
            pass
    mcidlists = open('mcidlist.json','r')
    mcidlist = json.load(mcidlists)
    check = json.dumps(mcidlist)
    if mcid in check:
        await inter.edit("既に別の人が登録していますけど、、、、同じ人が2人以上いるんですか・・・?")
        return
    else:
        emd2 = discord.Embed(title="mojangのAPIに接続中 <a:road:969468636068732968>",color=discord.Color.blue())
        await inter.edit(content="",embed=emd2)
        url = (f"https://api.mojang.com/users/profiles/minecraft/{mcid}")
        response = requests.get(url)
        try:
            uuid = response.json()["id"]
        except:
            emd3 = discord.Embed(title="存在しないMCIDもしくは、mojangのAPIにアクセスできません。",color=discord.Color.red())
            await inter.edit(content="",embed=emd3)
            return
        else:
            mcid = response.json()["name"]
            emd4 = discord.Embed(title="既に登録済みです！！",description="大文字と小文字を変えて同じ人をもう一人登録しようとしないでください！！",color=discord.Color.red())
            if mcid in check:
                await inter.edit(content="",embed=emd4)
                return
            emd2 = discord.Embed(title="ファイルに保存処理中 <a:road:969468636068732968>",color=discord.Color.blue())
            await inter.edit(content="",embed=emd2)
            temp = {"name":mcid,"uuid":uuid}
            mcidlist.append(temp)
            with open('mcidlist.json','w') as f:
                json.dump(mcidlist,f,ensure_ascii=False, indent=4)
            userid = (int(inter.author.id))
            add = mcid_date(discordid=userid,mcid=mcid,uuid=uuid)
            try:
                if flag1 == True:
                    editmcid2 = session.query(mcid_date).filter(mcid_date.discordid == userid).first()
                    editmcid2.mcid = mcid
                    editmcid2.uuid = uuid
                    session.commit()
                else:
                    session.add(add)
                    session.commit()
            except:
                emd = discord.Embed(title="エラーが発生しました。",description="マイクラの参加リストにあなたは登録されましたが、データベースの保存時にエラーが発生しました。申し訳ございませんが、<@400604650233135115> に伝えてください。(伝えないと、後々めんどうなことになるかもしれません。)",color=discord.Color.red())
                await inter.edit(embed=emd)
                return
            emd = discord.Embed(title="ユーザー登録が完了しました。",description="登録情報" + "\n" + f"MCID: {mcid}" + "\n" + f"UUID: {uuid}",color=discord.Color.purple())
            await inter.edit(embed=emd)
    mcidlists.close
#統合版のマイクラサーバー参加登録用コマンド
@interclient.slash_command(
    name = "be_mcid_add",
    description = '統合版のユーザーのゲーマータグをサーバーに参加できるように登録します。',
    options = [Option('gamertag',"ゲーマータグを書いてください。",OptionType.STRING,required=True)],
    test_guilds="943859907877306478",
)
async def be_mcid_add(inter,gamertag=None):
    await inter.reply("データベース読み込み中 <a:road:969468636068732968>")
    dates = session.query(mcid_date).all()
    userid = (int(inter.author.id))
    flag2 = False
    for date in dates:
        if date.discordid == userid:
            if date.be_mcid == None:
                flag2 = True
                break
            else:
                mcidtemp2[inter.author.id] = date.be_mcid
                row = ActionRow(Button(style=ButtonStyle.green,label="はい",custom_id="yes"),Button(style=ButtonStyle.red,label="いいえ",custom_id="no"))
                emd5 = discord.Embed(title="あなたは既に登録されています、変更しますか?",description="現在のあなたの登録情報" + "\n" + f"ゲーマータグ: {date.be_mcid}",color=discord.Color.red())
                msg = await inter.edit(content="",embed=emd5,components=[row])
                on_click = msg.create_click_listener(timeout=20)
                mcidtemp[inter.author.id] = gamertag
                @on_click.not_from_user(inter.author,cancel_others=True, reset_timeout=False)
                async def on_wrong_user(inter):
                    await inter.reply("あなたが実行した、コマンドではありません。", ephemeral=True)
                @on_click.matching_id("yes")
                async def on_yes(inter):
                    await msg.edit(content="変更処理を開始しました <a:road:969468636068732968>",embed=None,components=[])
                    be_mcidlists = open('be_mcidlist.json','r')
                    be_mcidlist = json.load(be_mcidlists)
                    addgamertag = (str("." + gamertag))
                    check = json.dumps(be_mcidlist)
                    if gamertag in check:
                        await msg.edit("既に別の人が登録していますけど、、、、同じ人が2人以上いるんですか・・・?")
                        return
                    else:
                        emd2 = discord.Embed(title="ファイルに保存処理中 <a:road:969468636068732968>",color=discord.Color.blue())
                        await msg.edit(content="",embed=emd2)
                        temp = {"name":addgamertag}
                        temp2 = {"name":mcidtemp2[inter.author.id]}
                        be_mcidlist.append(temp)
                        be_mcidlist.remove(temp2)
                        with open('be_mcidlist.json','w') as f:
                            json.dump(be_mcidlist,f,ensure_ascii=False, indent=4)
                        userid = (int(inter.author.id))
                        try:
                            editmcid3 = session.query(mcid_date).filter(mcid_date.discordid == userid).first()
                            editmcid3.be_mcid = addgamertag
                            session.commit()
                        except:
                            emd = discord.Embed(title="エラーが発生しました。",description="マイクラの参加リストにあなたは登録されましたが、データベースの保存時にエラーが発生しました。申し訳ございませんが、<@400604650233135115> に伝えてください。(伝えないと、後々めんどうなことになるかもしれません。)",color=discord.Color.red())
                            await msg.edit(embed=emd)
                            return
                        session.close
                        emd = discord.Embed(title="ユーザー情報を上書き保存しました。",description="登録情報" + "\n" + f"ゲーマータグ: {gamertag}",color=discord.Color.purple())
                        await msg.edit(embed=emd)                
                    mcidtemp.pop(inter.author.id)
                    return
            @on_click.matching_id("no")
            async def on_no(inter):
                await msg.edit(content="変更せずに終了しました。",embed=None,components=[])
                mcidtemp.pop(inter.author.id)
                return
            @on_click.timeout
            async def on_timeout():
                if inter.author.id in flag.keys():
                    flag.pop(inter.author.id)
                else:
                    await msg.edit(content="変更せずに終了しました。",embed=None,components=[])
                if inter.author.id in mcidtemp.keys():
                    mcidtemp.pop(inter.author.id)
                else:
                    pass
                return
            if flag2 == True:
                pass
            else:
                session.close
                return
        else:
            pass
    be_mcidlists = open('be_mcidlist.json','r')
    be_mcidlist = json.load(be_mcidlists)
    addgamertag = (str("." + gamertag))
    check = json.dumps(be_mcidlist)
    if gamertag in check:
        await inter.edit("既に別の人が登録していますけど、、、、同じ人が2人以上いるんですか・・・?")
        return
    else:
        emd2 = discord.Embed(title="ファイルに保存処理中 <a:road:969468636068732968>",color=discord.Color.blue())
        await inter.edit(content="",embed=emd2)
        temp = {"name":addgamertag}
        be_mcidlist.append(temp)
        with open('be_mcidlist.json','w') as f:
            json.dump(be_mcidlist,f,ensure_ascii=False, indent=4)
        userid = (int(inter.author.id))
        add = mcid_date(discordid=userid,be_mcid=addgamertag)
        try:
            if flag2 == True:
                editmcid3 = session.query(mcid_date).filter(mcid_date.discordid == userid).first()
                editmcid3.be_mcid = addgamertag
                session.commit()
            else:
                session.add(add)
                session.commit()
        except:
            emd = discord.Embed(title="エラーが発生しました。",description="マイクラの参加リストにあなたは登録されましたが、データベースの保存時にエラーが発生しました。申し訳ございませんが、<@400604650233135115> に伝えてください。(伝えないと、後々めんどうなことになるかもしれません。)",color=discord.Color.red())
            await inter.edit(embed=emd)
            return
        session.close
        emd = discord.Embed(title="ユーザー登録が完了しました。",description="登録情報" + "\n" + f"ゲーマータグ: {gamertag}",color=discord.Color.purple())
        await inter.edit(embed=emd)
#GBANシステム
@interclient.slash_command(
    name = "gban",
    description = 'かきくけこサーバーのグローバルBANシステムに違反者を登録します。(現状はよぴるのみ実行可能)',
    options = [Option('id',"ユーザーIDを書いて下さい。",OptionType.STRING,required=True),Option('cause',"理由を書いて下さい。",OptionType.STRING,required=True)],
)
async def gban(inter,id=None,cause=None):
    if inter.author.id == 400604650233135115:
        emd = discord.Embed(title=('本当に登録しますか?'),description=f'選択情報 \n 名前: <@{id}> \n ユーザーID: {id} \n 理由: {cause}',color=discord.Color.blue())
        row = ActionRow(Button(style=ButtonStyle.green,label="登録",custom_id="add"))
        msg = await inter.reply(embed=emd,ephemeral=True,components=[row])
        on_click = msg.create_click_listener(timeout=10)
        gbantemp[inter.author.id] = id
        gbantemp2[inter.author.id] = cause
        @on_click.matching_id("add")
        async def on_add(inter):
            await inter.reply("データベース読み込み中 <a:road:969468636068732968>",ephemeral=True)
            banid = (int(gbantemp[inter.author.id]))
            cause = gbantemp2[inter.author.id]
            dates = session.query(gban_system).all()
            flag3 = False
            for date in dates:
                if date.userid == banid:
                    await inter.edit("既に登録されています、なので登録できません。")
                    flag3 = True
                    return
                                                                                    
            if flag3 == False:
                await inter.edit("データベースに保存処理中 <a:road:969468636068732968>")
                add = gban_system(userid=banid,cause=cause)
                try:
                    session.add(add)
                    session.commit()
                    await inter.edit("かきくけこグローバルBANシステムに違反者を追加しました。")
                except:
                    await inter.edit("データベースの保存処理中に、エラーが発生しました。")
            else:
                pass
    else:
        await inter.reply("よぴる以外実行できましぇーん＾＾",ephemeral=True)
#サーバー入室時にする処理
@bot.event
async def on_member_join(ctx,member:discord.Member):
    dates = session.query(mcid_date).all()
    for date in dates:
        if date.userid == ctx.author.id:
            await ctx.send("あなたは、かきくけこコミュニティ関連のサーバーでBANされています、当サーバーに参加することはできません。")
            await member.ban(delete_message_days=7, reason="かきくけこコミュニティ関連のサーバーでBANされていたから。")
#サーバー退室時にする処理
@bot.event
async def on_guild_remove(guild):
    dates = session.query(mcid_date).all()
    for date in dates:
        if date.userid == guild.author.id:
            userid = (int(guild.author.id))
            delete = session.query(mcid_date).filter(mcid_date.discordid == userid).first()
            mcidlists = open('mcidlist.json','r')
            mcidlist = json.load(mcidlists)
            deletetemp = {"name":date.mcid, "uuid":date.uuid}
            mcidlist.remove(deletetemp)
            with open('mcidlist.json','w') as f:
                json.dump(mcidlist,f,ensure_ascii=False, indent=4)
            session.delete(delete)
            session.commit()

#discordのAPIに接続
bot.run('')