import discord
from discord import app_commands
from discord.ext import commands
import os


# 환경변수 불러오기
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 닉네임 변경 및 역할 부여 슬래시 명령어 (관리자 전용)
@bot.tree.command(
    name="닉네임변경하기",
    description="다른 사용자의 닉네임을 고유번호, 닉네임, 직업 형식으로 설정하고 역할을 부여합니다.",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    사용자id="닉네임을 변경할 대상 사용자",
    고유번호="고유번호",
    닉네임="닉네임",
    직업="직업",
    역할="부여할 역할"
)
async def 닉네임변경하기(
    interaction: discord.Interaction,
    사용자id: discord.Member,
    고유번호: str,
    닉네임: str,
    직업: str,
    역할: discord.Role
):
    new_nick = f"{고유번호}  ·  {닉네임}  ·  {직업}"
    if len(new_nick) > 32:
        new_nick = new_nick[:32]

    print(f"[디버그] 대상: {사용자id.display_name}, 새 닉네임: {new_nick}")

    # 닉네임 변경 시도
    try:
        await 사용자id.edit(nick=new_nick)
        nick_changed = True
        print("[디버그] 닉네임 변경 성공")
    except discord.Forbidden:
        nick_changed = False
        print("[디버그] 닉네임 변경 권한 없음")
    except Exception as e:
        await interaction.response.send_message(
            f"❌ 닉네임 변경 중 오류 발생: {e}", ephemeral=True
        )
        return

    # 역할 부여 시도
    try:
        await 사용자id.add_roles(역할)
        role_added = True
        print("[디버그] 역할 부여 성공")
    except discord.Forbidden:
        role_added = False
        print("[디버그] 역할 부여 권한 없음")
    except Exception as e:
        await interaction.response.send_message(
            f"❌ 역할 부여 중 오류 발생: {e}", ephemeral=True
        )
        return

    # 응답
    response_message = ""
    if nick_changed:
        response_message += f"✅ 닉네임이 `{new_nick}` 으로 변경되었습니다.\n"
    else:
        response_message += "❌ 닉네임 변경 권한이 없습니다.\n"

    if role_added:
        response_message += f"✅ 역할 `{역할.name}` 이(가) 부여되었습니다."
    else:
        response_message += f"❌ 역할 `{역할.name}` 을(를) 부여할 권한이 없습니다."

    try:
        await interaction.response.send_message(response_message, ephemeral=True)
    except discord.InteractionResponded:
        await interaction.followup.send(response_message, ephemeral=True)

@bot.tree.command(
    name="임직원목록",
    description="요식팩토리 임직원 목록을 출력해요.",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.checks.has_permissions(administrator=True)  # 관리자만 가능
async def announcement(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 요식팩토리 임직원 목록",
        description="회장\n\njason43031\n\n장충동왕국밥\n\nsung3408(사장)\njaden_houn(상무)\nleehw2021(점장)\nHwabon_stn(매니저)\nJUKDO_MARKET(부매니저)\nChoisoungbin(부매니저)\nhaha11556654433221(과장)\n7477wonce(대리)\nwehw4747(사원)\nkr8242(인턴)\nsibaslfaasdfasdfasdljasdhl(인턴)\nwol1410(인턴)\nkuhbmn(인턴)\neuudididirh8(인턴)\nDuck_Gae2(인턴)\nha_sugu2(인턴)\nRNRtyzm6565(인턴)\nrtuiiooqou7000(인턴)\novertrue93(인턴)\nRoblox_cerater9012(인턴)\nton_ys0905(인턴)\n\n인백스테이크 하우스\n\nAnnouncements1234(사장)\nkjs64007077(부장)\nggtgg6tg(부장)\ndkekwknd(인턴)\nlottegiant_2(인턴)\nleessamg2(인턴)\nbbabang12(인턴)\njunhaa_yee(인턴)\nimgirl_iloveme(인턴)\nhoug_KOREA(인턴)\n\n연화스시\n\n1209lkh(사장)\nwwwwunun(사원)\nJinSeubae(사원)\nwjddusgh3756(사원)\ndldhksdud(사원)\n\n비서실\n\nyumin821(비서실장)\nechoda100(수석비서관)\ntjdjhdidjddj(수행비서관)\nyandkig(총무비서관)\n\n신사업부\n\ncomet(개발팀장)\nanchenbin34(과장)\nweapon0100(대리)\nbunawl(주임)\nkamkor13243(사원)\n\n경비대\n\nAWDAADADAWDE(경비대장)\n0_0siwoo(경비반장)\npsj1026(경비반장)\njoj123ei2(사원)\nchicken_kimchi192(사원)\nwjddnjs0323(인턴)",
        color=discord.Color.blue()
    )
    embed.set_footer(text="요식팩토리 비서실")
    await interaction.response.send_message(embed=embed)


# 봇 준비 시 슬래시 명령어 동기화
@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print("✅ 슬래시 명령어 동기화 완료")


bot.run(os.getenv("TOKEN"))
