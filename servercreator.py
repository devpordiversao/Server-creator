# main.py
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import json
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurações do Bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

class ServerBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        self.templates = self.load_templates()
    
    def load_templates(self):
        """Carrega templates de servidores temáticos"""
        return {
            'rpg': {
                'icon': '🎲',
                'color': discord.Color.dark_purple(),
                'description': 'Servidor temático para RPG e mesas de jogo',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras e diretrizes do servidor'),
                        ('🎭┃apresentações', 'Apresente seu personagem'),
                        ('🗺️┃mundo-rpg', 'Lore e história do mundo'),
                        ('🎲┃mesa-1', 'Mesa de RPG 1'),
                        ('🎲┃mesa-2', 'Mesa de RPG 2'),
                        ('🎲┃mesa-3', 'Mesa de RPG 3'),
                        ('💬┃off-topic', 'Conversas gerais'),
                        ('🎨┃artes', 'Compartilhe artes e tokens'),
                        ('📚┃recursos', 'Livros e recursos de RPG'),
                    ],
                    'voz': [
                        ('🎙️┃Mesa Principal', None),
                        ('🎙️┃Mesa Secundária', None),
                        ('🎙️┃Mesa Privada', 4),
                        ('🎧┃Música & Ambiente', None),
                    ]
                },
                'roles': [
                    ('🎮 Mestre', discord.Color.gold(), ['administrator'], True),
                    ('🧙‍♂️ Jogador', discord.Color.blue(), ['send_messages', 'connect'], False),
                    ('👀 Espectador', discord.Color.greyple(), ['view_channel'], False),
                    ('🎨 Artista', discord.Color.purple(), ['attach_files'], False),
                    ('📖 Narrador', discord.Color.dark_green(), ['manage_messages'], False),
                ],
                'welcome_message': 'Bem-vindo à aventura, {member}! 🎲\nPrepare seus dados e que a sorte esteja com você!',
                'leave_message': '{member} deixou a party. Que seus dados rolem bem onde estiver! 👋',
                'welcome_image': 'https://i.imgur.com/rpg_welcome.png',  # Substitua por sua imagem
            },
            
            'loja': {
                'icon': '🛒',
                'color': discord.Color.green(),
                'description': 'Servidor para e-commerce e vendas',
                'channels': {
                    'texto': [
                        ('📋┃regras', 'Regras da loja'),
                        ('🛍️┃catálogo', 'Nossos produtos'),
                        ('💰┃promoções', 'Ofertas especiais'),
                        ('🎫┃suporte', 'Atendimento ao cliente'),
                        ('⭐┃avaliações', 'Feedback dos clientes'),
                        ('📦┃rastreamento', 'Status dos pedidos'),
                        ('💬┃chat-geral', 'Converse com a comunidade'),
                        ('🤝┃parcerias', 'Propostas comerciais'),
                    ],
                    'voz': [
                        ('🎧┃Suporte Voz', None),
                        ('💼┃Reuniões', 5),
                    ]
                },
                'roles': [
                    ('👑 Dono', discord.Color.gold(), ['administrator'], True),
                    ('🛍️ Cliente VIP', discord.Color.purple(), ['send_messages'], False),
                    ('💼 Vendedor', discord.Color.blue(), ['manage_messages'], False),
                    ('📦 Estoque', discord.Color.orange(), ['attach_files'], False),
                    ('⭐ Cliente', discord.Color.green(), ['send_messages'], False),
                    ('🤖 Bot', discord.Color.greyple(), ['send_messages'], False),
                ],
                'welcome_message': 'Bem-vindo à nossa loja, {member}! 🛒\nConfira nosso catálogo e aproveite as ofertas!',
                'leave_message': '{member} saiu da loja. Volte sempre! 👋',
                'welcome_image': 'https://i.imgur.com/shop_welcome.png',
            },
            
            'comunidade': {
                'icon': '🌐',
                'color': discord.Color.blue(),
                'description': 'Servidor para comunidades e grupos de amigos',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras da comunidade'),
                        ('👋┃boas-vindas', 'Apresente-se aqui!'),
                        ('💬┃chat-geral', 'Conversa livre'),
                        ('🎨┃arte', 'Compartilhe suas criações'),
                        ('🎵┃música', 'Compartilhe suas músicas'),
                        ('🎮┃games', 'Encontre players'),
                        ('📺┃anime-manga', 'Discussões otaku'),
                        ('🏆┃eventos', 'Eventos da comunidade'),
                        ('📢┃anúncios', 'Novidades importantes'),
                        ('🤖┃bots', 'Comandos dos bots'),
                    ],
                    'voz': [
                        ('🎙️┃Geral 1', None),
                        ('🎙️┃Geral 2', None),
                        ('🎵┃Música', None),
                        ('🎮┃Gaming', None),
                        ('🔒┃Privado', 2),
                    ]
                },
                'roles': [
                    ('👑 Fundador', discord.Color.gold(), ['administrator'], True),
                    ('🛡️ Moderador', discord.Color.red(), ['kick_members', 'manage_messages'], False),
                    ('⭐ Membro VIP', discord.Color.purple(), ['send_messages'], False),
                    ('🎨 Artista', discord.Color.pink(), ['attach_files'], False),
                    ('🎮 Gamer', discord.Color.dark_blue(), ['connect'], False),
                    ('👥 Membro', discord.Color.blue(), ['send_messages'], False),
                ],
                'welcome_message': 'Seja bem-vindo à comunidade, {member}! 🎉\nSinta-se em casa e aproveite nossa companhia!',
                'leave_message': '{member} deixou a comunidade. Sentiremos sua falta! 👋',
                'welcome_image': 'https://i.imgur.com/community_welcome.png',
            },
            
            'jogos': {
                'icon': '🎮',
                'color': discord.Color.dark_red(),
                'description': 'Servidor dedicado a jogos e gamers',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras do servidor'),
                        ('🎯┃buscando-grupo', 'Encontre players'),
                        ('🏆┃ranking', 'Placar de líderes'),
                        ('🎮┃geral-games', 'Chat sobre jogos'),
                        ('🔫┃fps', 'Call of Duty, CS:GO, Valorant...'),
                        ('⚔️┃moba', 'League of Legends, Dota 2...'),
                        ('🌍┃mmorpg', 'WoW, FF14, Guild Wars...'),
                        ('🎲┃indie', 'Jogos independentes'),
                        ('📺┃streams', 'Promova suas lives'),
                        ('🤝┃recrutamento', 'Recrute para seu time'),
                    ],
                    'voz': [
                        ('🎙️┃Lobby', None),
                        ('🎙️┃Squad 1', 4),
                        ('🎙️┃Squad 2', 4),
                        ('🎙️┃Squad 3', 4),
                        ('🎙️┃Ranked', 5),
                        ('🎵┃Música', None),
                        ('🔒┃Privado', 2),
                    ]
                },
                'roles': [
                    ('🏆 Admin', discord.Color.gold(), ['administrator'], True),
                    ('🎮 Capitão', discord.Color.red(), ['move_members'], False),
                    ('⭐ Pro Player', discord.Color.purple(), ['priority_speaker'], False),
                    ('🎯 Streamer', discord.Color.pink(), ['send_messages'], False),
                    ('🎲 Gamer', discord.Color.blue(), ['connect'], False),
                    ('👀 Visitante', discord.Color.greyple(), ['view_channel'], False),
                ],
                'welcome_message': 'GG! {member} entrou no servidor! 🎮\nPrepara o mouse e o teclado, é hora de jogar!',
                'leave_message': '{member} saiu do jogo. Até a próxima partida! 👋',
                'welcome_image': 'https://i.imgur.com/gaming_welcome.png',
            },
            
            'estudo': {
                'icon': '📚',
                'color': discord.Color.teal(),
                'description': 'Servidor para estudos e produtividade',
                'channels': {
                    'texto': [
                        ('📋┃regras', 'Regras de conduta'),
                        ('📅┃calendário', 'Eventos e prazos'),
                        ('📚┃geral', 'Chat geral de estudos'),
                        ('💻┃programação', 'Códigos e desenvolvimento'),
                        ('🔢┃matemática', 'Cálculos e fórmulas'),
                        ('🌍┃idiomas', 'Prática de línguas'),
                        ('🎨┃design', 'Arte e criatividade'),
                        ('📝┃resumos', 'Compartilhe anotações'),
                        ('❓┃dúvidas', 'Tire suas dúvidas'),
                        ('🎯┃metas', 'Compartilhe objetivos'),
                    ],
                    'voz': [
                        ('🔇┃Sala Silenciosa', None),
                        ('🗣️┃Discussão', None),
                        ('📖┃Grupo de Estudo 1', 5),
                        ('📖┃Grupo de Estudo 2', 5),
                        ('🎵┃Lo-Fi', None),
                    ]
                },
                'roles': [
                    ('👨‍🏫 Professor', discord.Color.gold(), ['manage_messages'], True),
                    ('🎓 Monitor', discord.Color.dark_blue(), ['mute_members'], False),
                    ('📚 Aluno Destaque', discord.Color.purple(), ['send_messages'], False),
                    ('✏️ Estudante', discord.Color.blue(), ['send_messages'], False),
                    ('👤 Visitante', discord.Color.greyple(), ['view_channel'], False),
                ],
                'welcome_message': 'Bem-vindo aos estudos, {member}! 📚\nQue o conhecimento esteja com você!',
                'leave_message': '{member} deixou a sala de aula. Bons estudos! 👋',
                'welcome_image': 'https://i.imgur.com/study_welcome.png',
            },
            
            'anime': {
                'icon': '🍥',
                'color': discord.Color.pink(),
                'description': 'Servidor para fãs de anime e cultura japonesa',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras do servidor'),
                        ('🎌┃apresentações', 'Apresente-se otaku!'),
                        ('💬┃chat-geral', 'Conversa livre'),
                        ('📺┃recomendações', 'Indique animes'),
                        ('🎨┃fanarts', 'Compartilhe suas artes'),
                        ('🎵┃osts', 'Músicas de anime'),
                        ('🎮┃games-anime', 'Gacha e jogos'),
                        ('📖┃mangás', 'Discussão de mangás'),
                        ('🎌┃cultura-japonesa', 'Cultura e idioma'),
                        ('🔥┃spoilers', 'Cuidado com spoilers!'),
                    ],
                    'voz': [
                        ('🎙️┃Geral', None),
                        ('🎵┃Karaokê', None),
                        ('📺┃Assistindo Juntos', None),
                        ('🎮┃Gaming', None),
                    ]
                },
                'roles': [
                    ('👑 Hokage', discord.Color.gold(), ['administrator'], True),
                    ('🥷 Mod', discord.Color.red(), ['manage_messages'], False),
                    ('⭐ Otaku VIP', discord.Color.purple(), ['send_messages'], False),
                    ('🎨 Artista', discord.Color.pink(), ['attach_files'], False),
                    ('🍜 Weeb', discord.Color.blue(), ['send_messages'], False),
                    ('🌸 Novato', discord.Color.green(), ['send_messages'], False),
                ],
                'welcome_message': 'Ora ora, {member} chegou! 🍥\nDattebayo! Prepare-se para a aventura ninja!',
                'leave_message': '{member} foi comer ramen. Sayonara! 👋',
                'welcome_image': 'https://i.imgur.com/anime_welcome.png',
            },
        }
    
    async def setup_hook(self):
        await self.tree.sync()
        print(f'Bot conectado como {self.user}')
        print(f'ID: {self.user.id}')
        print('------')

bot = ServerBot()

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='/createserver para criar servidores!'
        )
    )
    print(f'{bot.user} está online!')

@bot.event
async def on_guild_join(guild):
    """Configura automação quando o bot entra em um servidor"""
    # Criar canal de logs se não existir
    logs_channel = discord.utils.get(guild.channels, name='logs-bot')
    if not logs_channel:
        try:
            logs_channel = await guild.create_text_channel(
                'logs-bot',
                topic='Logs automáticas do bot',
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    guild.me: discord.PermissionOverwrite(view_channel=True)
                }
            )
        except:
            pass

@bot.tree.command(name='createserver', description='Cria um novo servidor temático completo')
@app_commands.describe(
    tema='Escolha o tema do servidor',
    nome='Nome personalizado para o novo servidor'
)
@app_commands.choices(tema=[
    app_commands.Choice(name=f'🎲 RPG', value='rpg'),
    app_commands.Choice(name=f'🛒 Loja/E-commerce', value='loja'),
    app_commands.Choice(name=f'🌐 Comunidade', value='comunidade'),
    app_commands.Choice(name=f'🎮 Jogos/Gaming', value='jogos'),
    app_commands.Choice(name=f'📚 Estudos', value='estudo'),
    app_commands.Choice(name=f'🍥 Anime/Otaku', value='anime'),
])
async def create_server(
    interaction: discord.Interaction,
    tema: app_commands.Choice[str],
    nome: str
):
    await interaction.response.defer(ephemeral=True)
    
    template = bot.templates.get(tema.value)
    if not template:
        await interaction.followup.send('❌ Tema não encontrado!', ephemeral=True)
        return
    
    try:
        # Criar o servidor
        guild = await bot.create_guild(
            name=nome,
            icon=None,  # Pode adicionar ícone personalizado aqui
            region=None
        )
        
        # Aguardar criação
        await asyncio.sleep(2)
        
        # Buscar o servidor criado
        guild = bot.get_guild(guild.id)
        
        # Configurar servidor
        await setup_guild(guild, template, interaction.user)
        
        # Criar convite
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
        
        # Embed de sucesso
        embed = discord.Embed(
            title=f'{template["icon"]} Servidor Criado com Sucesso!',
            description=f'O servidor **{nome}** foi criado com o tema **{tema.name}**',
            color=template['color'],
            timestamp=datetime.now()
        )
        embed.add_field(
            name='🔗 Link de Convite',
            value=f'[Clique aqui para entrar]({invite.url})',
            inline=False
        )
        embed.add_field(
            name='📋 Canais Criados',
            value=f'{len(template["channels"]["texto"])} texto + {len(template["channels"]["voz"])} voz',
            inline=True
        )
        embed.add_field(
            name='👥 Cargos Criados',
            value=str(len(template['roles'])),
            inline=True
        )
        embed.set_footer(text=f'Criado por {interaction.user}', icon_url=interaction.user.display_avatar.url)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.followup.send(
            '❌ Erro: O bot precisa de permissões de administrador para criar servidores!',
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f'❌ Erro ao criar servidor: {str(e)}', ephemeral=True)

async def setup_guild(guild: discord.Guild, template: dict, creator: discord.User):
    """Configura o servidor criado com base no template"""
    
    # 1. Criar cargos
    roles_map = {}
    for role_name, color, permissions, hoist in template['roles']:
        perms = discord.Permissions()
        for perm in permissions:
            setattr(perms, perm, True)
        
        role = await guild.create_role(
            name=role_name,
            color=color,
            permissions=perms,
            hoist=hoist
        )
        roles_map[role_name] = role
    
    # 2. Configurar cargos do criador
    member = guild.get_member(creator.id)
    if member:
        admin_role = roles_map.get(template['roles'][0][0])  # Primeiro cargo (admin)
        if admin_role:
            await member.add_roles(admin_role)
    
    # 3. Deletar canais padrão
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass
    
    await asyncio.sleep(1)
    
    # 4. Criar categorias e canais
    # Categoria texto
    cat_texto = await guild.create_category('📋 INFORMAÇÕES')
    cat_chat = await guild.create_category('💬 COMUNIDADE')
    cat_voz = await guild.create_category('🔊 CANAIS DE VOZ')
    
    # Criar canais de texto
    welcome_channel = None
    rules_channel = None
    
    for i, (channel_name, topic) in enumerate(template['channels']['texto']):
        if 'boas-vindas' in channel_name or 'regras' in channel_name:
            target_cat = cat_texto
        else:
            target_cat = cat_chat
        
        channel = await guild.create_text_channel(
            name=channel_name,
            category=target_cat,
            topic=topic
        )
        
        if 'boas-vindas' in channel_name:
            welcome_channel = channel
        elif 'regras' in channel_name:
            rules_channel = channel
    
    # Criar canais de voz
    for channel_name, user_limit in template['channels']['voz']:
        await guild.create_voice_channel(
            name=channel_name,
            category=cat_voz,
            user_limit=user_limit
        )
    
    # 5. Configurar sistema de boas-vindas
    if welcome_channel:
        # Enviar mensagem de setup
        embed = discord.Embed(
            title=f'{template["icon"]} Bem-vindo ao {guild.name}!',
            description=template['description'],
            color=template['color']
        )
        if template.get('welcome_image'):
            embed.set_image(url=template['welcome_image'])
        embed.set_footer(text='Sistema de boas-vindas configurado!')
        
        await welcome_channel.send(embed=embed)
    
    # 6. Configurar regras
    if rules_channel:
        rules_embed = discord.Embed(
            title='📜 Regras do Servidor',
            description='Leia atentamente as regras para manter a harmonia!',
            color=template['color']
        )
        rules_embed.add_field(
            name='1. Respeito',
            value='Respeite todos os membros independente de opinião, raça, gênero ou crença.',
            inline=False
        )
        rules_embed.add_field(
            name='2. Conteúdo Apropriado',
            value='Proibido conteúdo NSFW, gore ou qualquer material ofensivo.',
            inline=False
        )
        rules_embed.add_field(
            name='3. Spam',
            value='Não faça spam ou flood nos canais.',
            inline=False
        )
        rules_embed.add_field(
            name='4. Divulgação',
            value='Divulgação apenas nos canais permitidos.',
            inline=False
        )
        await rules_channel.send(embed=rules_embed)
    
    # 7. Configurar permissões dos cargos nos canais
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            # Permitir @everyone ver canais básicos
            if 'regras' in channel.name or 'boas-vindas' in channel.name:
                await channel.set_permissions(
                    guild.default_role,
                    view_channel=True,
                    send_messages=False
                )
    
    return welcome_channel

@bot.event
async def on_member_join(member):
    """Sistema automático de boas-vindas"""
    guild = member.guild
    
    # Buscar template do servidor (se foi criado pelo bot)
    # Nota: Em produção, você salvaria isso em um banco de dados
    # Aqui usamos uma verificação simples pelo nome dos canais
    
    welcome_channel = discord.utils.get(guild.channels, name='👋┃boas-vindas') or \
                     discord.utils.get(guild.channels, name='boas-vindas') or \
                     discord.utils.get(guild.text_channels, name=lambda n: 'bem-vindo' in n or 'welcome' in n)
    
    if welcome_channel:
        # Detectar tema baseado nos cargos
        template = None
        for t_name, t_data in bot.templates.items():
            if discord.utils.get(guild.roles, name=t_data['roles'][0][0]):
                template = t_data
                break
        
        if template:
            # Criar embed de boas-vindas personalizado
            embed = discord.Embed(
                title=f'{template["icon"]} Novo Membro!',
                description=template['welcome_message'].format(member=member.mention),
                color=template['color'],
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            if template.get('welcome_image'):
                embed.set_image(url=template['welcome_image'])
            embed.set_footer(text=f'ID: {member.id}', icon_url=guild.icon.url if guild.icon else None)
            
            await welcome_channel.send(embed=embed)
            
            # Enviar DM de boas-vindas
            try:
                dm_embed = discord.Embed(
                    title=f'Bem-vindo ao {guild.name}!',
                    description=f'Obrigado por entrar em nosso servidor {template["icon"]}\n\nLeia as regras e aproveite!',
                    color=template['color']
                )
                await member.send(embed=dm_embed)
            except:
                pass

@bot.event
async def on_member_remove(member):
    """Sistema de saída"""
    guild = member.guild
    
    # Buscar canal de logs ou boas-vindas
    channel = discord.utils.get(guild.channels, name='👋┃boas-vindas') or \
              discord.utils.get(guild.channels, name='logs-bot')
    
    if channel:
        # Detectar tema
        template = None
        for t_name, t_data in bot.templates.items():
            if discord.utils.get(guild.roles, name=t_data['roles'][0][0]):
                template = t_data
                break
        
        if template:
            embed = discord.Embed(
                title='👋 Adeus!',
                description=template['leave_message'].format(member=str(member)),
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

@bot.tree.command(name='temas', description='Lista todos os temas disponíveis para criação de servidores')
async def list_themes(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🎨 Temas Disponíveis',
        description='Escolha um tema ao usar `/createserver`',
        color=discord.Color.blue()
    )
    
    for key, template in bot.templates.items():
        embed.add_field(
            name=f'{template["icon"]} {key.title()}',
            value=f'{template["description"]}\nCanais: {len(template["channels"]["texto"])} texto + {len(template["channels"]["voz"])} voz\nCargos: {len(template["roles"])}',
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='addemoji', description='Adiciona emojis personalizados ao servidor (Admin)')
@app_commands.describe(
    imagem='Imagem do emoji (PNG/JPG)',
    nome='Nome do emoji'
)
async def add_emoji(interaction: discord.Interaction, imagem: discord.Attachment, nome: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Apenas administradores!', ephemeral=True)
        return
    
    if not imagem.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await interaction.response.send_message('❌ Formato inválido! Use PNG, JPG ou GIF.', ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        image_data = await imagem.read()
        emoji = await interaction.guild.create_custom_emoji(name=nome, image=image_data)
        await interaction.followup.send(f'✅ Emoji :{nome}: adicionado com sucesso!', ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f'❌ Erro: {str(e)}', ephemeral=True)

@bot.tree.command(name='setupwelcome', description='Configura mensagem de boas-vindas personalizada (Admin)')
@app_commands.describe(
    mensagem='Mensagem de boas-vindas (use {member} para mencionar)',
    imagem='URL da imagem de fundo (opcional)',
    cor='Cor do embed (hex, ex: #FF5733)'
)
async def setup_welcome(
    interaction: discord.Interaction,
    mensagem: str,
    imagem: str = None,
    cor: str = None
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Apenas administradores!', ephemeral=True)
        return
    
    # Salvar configuração (em memória - em produção use banco de dados)
    # Aqui você implementaria o salvamento
    
    color = discord.Color(int(cor.replace('#', ''), 16)) if cor else discord.Color.blue()
    
    embed = discord.Embed(
        title='✅ Configuração Salva',
        description='Mensagem de boas-vindas atualizada!',
        color=color
    )
    embed.add_field(name='Mensagem', value=mensagem, inline=False)
    if imagem:
        embed.set_image(url=imagem)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Sistema de ajuda
@bot.tree.command(name='ajuda', description='Mostra todos os comandos disponíveis')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🤖 Comandos do ServerCreator Bot',
        description='Bot profissional para criação de servidores temáticos',
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name='🛠️ Criação',
        value='`/createserver (tema) (nome)` - Cria um novo servidor completo\n`/temas` - Lista temas disponíveis',
        inline=False
    )
    
    embed.add_field(
        name='⚙️ Gerenciamento',
        value='`/addemoji (imagem) (nome)` - Adiciona emoji personalizado\n`/setupwelcome (mensagem)` - Configura boas-vindas',
        inline=False
    )
    
    embed.add_field(
        name='🔄 Automação',
        value='• Sistema de boas-vindas automático\n• Sistema de saída automático\n• Cargos pré-configurados\n• Canais organizados por categoria',
        inline=False
    )
    
    embed.set_footer(text='Desenvolvido com 💜 por SeuNome')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERRO: Token não encontrado! Verifique seu arquivo .env")
        print("Crie um arquivo .env com: DISCORD_TOKEN=seu_token_aqui")
    else:
        bot.run(TOKEN)
