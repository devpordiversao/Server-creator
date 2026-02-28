# main.py - ServerCreator Bot (ATUALIZADO COM SISTEMA DE SUPORTE)
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import re
import json

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# URL do site
SITE_URL = "https://server-creator-site-production.up.railway.app/index.html"

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
        self.site_keywords = ['site', 'website', 'pagina', 'página', 'dashboard', 'painel', 'html']
        self.ticket_cooldowns = {}  # Sistema de cooldown para tickets
    
    def load_templates(self):
        """Carrega templates de servidores temáticos"""
        return {
            # ... (mantenha todos os temas anteriores: rpg, loja, comunidade, jogos, estudo, anime)
            
            'suporte': {
                'icon': '🎫',
                'color': discord.Color.red(),
                'description': 'Servidor oficial de suporte do ServerCreator Bot',
                'temporary': True,  # Marca como temporário
                'channels': {
                    'texto': [
                        ('📢┃anúncios', 'Anúncios oficiais do bot'),
                        ('🎉┃novidades', 'Novidades e atualizações'),
                        ('📜┃termos-serviço', 'Termos de Serviço do Bot'),
                        ('🔒┃política-privacidade', 'Política de Privacidade'),
                        ('🌐┃site-oficial', 'Link do site oficial'),
                        ('❓┃faq', 'Perguntas Frequentes'),
                        ('🎫┃criar-ticket', 'Abra seu ticket de suporte'),
                        ('💡┃sugestões', 'Sugestões para o bot'),
                        ('🐛┃bugs', 'Reporte bugs encontrados'),
                        ('💬┃geral', 'Chat geral da comunidade'),
                        ('🎨┃showcase', 'Mostre servidores criados'),
                        ('🤝┃parcerias', 'Propostas de parceria'),
                        ('📊┃estatísticas', 'Stats do bot'),
                        ('🔧┃status-bot', 'Status em tempo real'),
                        ('📖┃guias', 'Tutoriais e guias'),
                        ('🎁┃sorteios', 'Eventos e premiações'),
                        ('👋┃boas-vindas', 'Mensagens de boas-vindas'),
                        ('📋┃regras', 'Regras do servidor'),
                        ('🤖┃comandos', 'Lista de comandos do bot'),
                        ('📝┃changelog', 'Histórico de atualizações'),
                        ('💻┃desenvolvimento', 'Avisos de dev'),
                        ('🎯┃metas', 'Metas da comunidade'),
                        ('🏆┃destaques', 'Membros em destaque'),
                        ('📢┃votações', 'Enquetes da comunidade'),
                    ],
                    'voz': [
                        ('🎙️┃Sala Geral', None),
                        ('🎙️┃Suporte Voz', None),
                        ('🔒┃Staff', 5),
                        ('🎵┃Música', None),
                        ('🎙️┃Eventos', None),
                        ('🔒┃Reunião Staff', 10),
                        ('🎙️┃Parcerias', 4),
                        ('🎧┃AFK', None),
                        ('🎙️┃Dev Talk', 6),
                        ('🎮┃Gaming', None),
                    ]
                },
                'roles': [
                    ('👑 Fundador', discord.Color.gold(), ['administrator'], True),
                    ('⚡ Administrador', discord.Color.red(), ['manage_messages', 'kick_members'], True),
                    ('🛡️ Moderador', discord.Color.orange(), ['manage_messages'], True),
                    ('🎫 Suporte', discord.Color.green(), ['manage_messages'], False),
                    ('💻 Developer', discord.Color.purple(), [], False),
                    ('🎨 Designer', discord.Color.pink(), [], False),
                    ('⭐ Parceiro', discord.Color.gold(), [], False),
                    ('🐛 Bug Hunter', discord.Color.dark_red(), [], False),
                    ('💡 Sugestor', discord.Color.blue(), [], False),
                    ('🎉 Nitro Booster', discord.Color.from_rgb(255, 115, 250), [], False),
                    ('👤 Membro', discord.Color.light_grey(), ['send_messages'], False),
                    ('🤖 Bot Oficial', discord.Color.greyple(), ['send_messages'], False),
                    ('📢 Anúncios', discord.Color.teal(), ['send_messages'], False),
                    ('🔧 Manutenção', discord.Color.dark_grey(), [], False),
                    ('🎖️ Veterano', discord.Color.dark_gold(), [], False),
                    ('🌟 Destaque', discord.Color.yellow(), [], False),
                    ('📝 Beta Tester', discord.Color.dark_blue(), [], False),
                    ('🎁 Giveaway Manager', discord.Color.magenta(), [], False),
                    ('📊 Estatístico', discord.Color.dark_green(), [], False),
                    ('🎤 Streamer', discord.Color.purple(), [], False),
                    ('🎮 Gamer', discord.Color.blue(), [], False),
                    ('👀 Visitante', discord.Color.greyple(), ['view_channel'], False),
                ],
                'welcome_message': '🎉 Bem-vindo ao suporte oficial, {member}! Confira o FAQ antes de abrir um ticket!',
                'leave_message': '👋 {member} deixou o servidor. Volte sempre!',
                'welcome_image': 'https://i.imgur.com/support_welcome.png',
            },
        }

    # ... (mantenha o resto do código anterior: setup_hook, on_ready, etc.)

# ==================== SISTEMA DE TICKETS ====================

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.select(
        placeholder="🎫 Selecione o tipo de ticket",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Dúvida Geral",
                description="Tire suas dúvidas sobre o bot",
                emoji="❓",
                value="duvida"
            ),
            discord.SelectOption(
                label="Reportar Bug",
                description="Encontrou algum erro? Reporte aqui",
                emoji="🐛",
                value="bug"
            ),
            discord.SelectOption(
                label="Sugestão",
                description="Tem uma ideia para o bot? Conta pra gente",
                emoji="💡",
                value="sugestao"
            ),
            discord.SelectOption(
                label="Parceria",
                description="Proposta de parceria comercial",
                emoji="🤝",
                value="parceria"
            ),
            discord.SelectOption(
                label="Denúncia",
                description="Denuncie comportamento indevido",
                emoji="🚨",
                value="denuncia"
            ),
            discord.SelectOption(
                label="Outro",
                description="Assuntos diversos",
                emoji="📝",
                value="outro"
            ),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        ticket_type = select.values[0]
        user = interaction.user
        guild = interaction.guild
        
        # Verificar cooldown
        cooldown_key = f"{user.id}_{guild.id}"
        if cooldown_key in bot.ticket_cooldowns:
            last_ticket = bot.ticket_cooldowns[cooldown_key]
            if (datetime.now() - last_ticket).total_seconds() < 300:  # 5 minutos
                await interaction.response.send_message(
                    "⏳ Você já abriu um ticket recentemente! Aguarde 5 minutos.",
                    ephemeral=True
                )
                return
        
        # Criar canal do ticket
        category = discord.utils.get(guild.categories, name="🎫 TICKETS")
        if not category:
            category = await guild.create_category("🎫 TICKETS")
        
        # Nome do canal
        channel_name = f"ticket-{user.name.lower()}-{ticket_type}"
        channel_name = re.sub(r'[^a-z0-9-]', '', channel_name)[:50]
        
        # Verificar se já existe ticket aberto
        existing = discord.utils.get(guild.channels, name=channel_name)
        if existing:
            await interaction.response.send_message(
                f"❌ Você já tem um ticket aberto: {existing.mention}",
                ephemeral=True
            )
            return
        
        # Criar canal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True
            )
        }
        
        # Adicionar permissões para cargos de staff
        staff_role = discord.utils.get(guild.roles, name="⚡ Administrador") or \
                    discord.utils.get(guild.roles, name="🛡️ Moderador") or \
                    discord.utils.get(guild.roles, name="🎫 Suporte")
        
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True
            )
        
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket de {user.name} | Tipo: {ticket_type}"
        )
        
        # Registrar cooldown
        bot.ticket_cooldowns[cooldown_key] = datetime.now()
        
        # Criar embed do ticket
        embed = discord.Embed(
            title=f"🎫 Ticket Aberto - {ticket_type.title()}",
            description=f"Olá {user.mention}! Seu ticket foi criado com sucesso.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        type_descriptions = {
            'duvida': '❓ **Dúvida Geral**\nDescreva sua dúvida sobre o bot. Tentaremos responder o mais rápido possível!',
            'bug': '🐛 **Reportar Bug**\nDescreva o bug encontrado com detalhes. Se possível, envie screenshots!',
            'sugestao': '💡 **Sugestão**\nConta pra gente sua ideia! Queremos melhorar sempre.',
            'parceria': '🤝 **Proposta de Parceria**\nDescreva sua proposta comercial. Retornaremos em breve.',
            'denuncia': '🚨 **Denúncia**\nDescreva o ocorrido com detalhes e provas se houver.',
            'outro': '📝 **Assunto Diversos**\nDescreva como podemos ajudar você.'
        }
        
        embed.add_field(
            name="📋 Tipo do Ticket",
            value=type_descriptions.get(ticket_type, "Ticket geral"),
            inline=False
        )
        
        embed.add_field(
            name="👤 Aberto por",
            value=f"{user.name} ({user.id})",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Horário",
            value=datetime.now().strftime("%d/%m/%Y %H:%M"),
            inline=True
        )
        
        embed.add_field(
            name="🔒 Ações",
            value="Use os botões abaixo para gerenciar o ticket.",
            inline=False
        )
        
        embed.set_footer(text="ServerCreator Suporte • Aeth 🜲 ༝ TMZ")
        
        # Enviar mensagem com botões
        view = TicketManageView(user.id)
        msg = await ticket_channel.send(
            content=f"{user.mention} {staff_role.mention if staff_role else ''}",
            embed=embed,
            view=view
        )
        
        # Confirmar ao usuário
        await interaction.response.send_message(
            f"✅ Ticket criado com sucesso! Acesse em {ticket_channel.mention}",
            ephemeral=True
        )

class TicketManageView(discord.ui.View):
    def __init__(self, creator_id):
        super().__init__(timeout=None)
        self.creator_id = creator_id
    
    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Verificar se é staff ou criador
        is_staff = any(r.name in ['⚡ Administrador', '🛡️ Moderador', '🎫 Suporte'] for r in interaction.user.roles)
        is_creator = interaction.user.id == self.creator_id
        
        if not (is_staff or is_creator):
            await interaction.response.send_message("❌ Apenas o criador ou staff pode fechar!", ephemeral=True)
            return
        
        # Confirmar fechamento
        embed = discord.Embed(
            title="🔒 Fechar Ticket?",
            description="Tem certeza que deseja fechar este ticket?",
            color=discord.Color.orange()
        )
        
        view = ConfirmCloseView(self.creator_id, interaction.channel)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="📋 Transcrição", style=discord.ButtonStyle.blurple, custom_id="transcript")
    async def transcript_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Gerando transcrição...", ephemeral=True)
        
        # Coletar mensagens
        messages = []
        async for msg in interaction.channel.history(limit=200, oldest_first=True):
            if not msg.author.bot:
                messages.append(f"[{msg.created_at.strftime('%H:%M')}] {msg.author.name}: {msg.content}")
        
        transcript = "\n".join(messages[-100:])  # Últimas 100 mensagens
        
        # Criar arquivo
        from io import StringIO
        file = discord.File(StringIO(transcript), filename=f"transcript-{interaction.channel.name}.txt")
        
        await interaction.followup.send("📄 Transcrição:", file=file, ephemeral=True)

class ConfirmCloseView(discord.ui.View):
    def __init__(self, creator_id, channel):
        super().__init__(timeout=60)
        self.creator_id = creator_id
        self.channel = channel
    
    @discord.ui.button(label="✅ Sim, fechar", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Ticket Fechado",
            description=f"Fechado por {interaction.user.mention}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Aguardar 5 segundos e deletar
        await asyncio.sleep(5)
        await self.channel.delete(reason=f"Ticket fechado por {interaction.user.name}")
    
    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Fechamento cancelado.", embed=None, view=None)

# ==================== COMANDO DE SUPORTE ====================

@bot.tree.command(name='criarsuporte', description='[TEMPORÁRIO] Cria servidor de suporte completo')
@app_commands.describe(
    nome='Nome do servidor de suporte'
)
async def criar_suporte(
    interaction: discord.Interaction,
    nome: str = "ServerCreator Suporte"
):
    """Comando temporário para criar servidor de suporte"""
    await interaction.response.defer(ephemeral=True)
    
    # Aviso que é temporário
    warning_embed = discord.Embed(
        title="⚠️ Comando Temporário",
        description="Este comando será removido em breve. Use apenas para criar o servidor oficial de suporte!",
        color=discord.Color.orange()
    )
    await interaction.followup.send(embed=warning_embed, ephemeral=True)
    
    try:
        # Criar servidor (funciona porque o bot está criando, não usuário comum)
        guild = await bot.create_guild(name=name)
        await asyncio.sleep(3)
        guild = bot.get_guild(guild.id)
        
        if not guild:
            await interaction.followup.send("❌ Erro ao criar servidor!", ephemeral=True)
            return
        
        # Configurar com template de suporte
        template = bot.templates['suporte']
        await configure_support_guild(guild, template, interaction.user)
        
        # Criar convite
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
        
        # Embed de sucesso
        embed = discord.Embed(
            title="🎫 Servidor de Suporte Criado!",
            description=f"**{nome}** está pronto!",
            color=discord.Color.green()
        )
        embed.add_field(name="🔗 Convite", value=f"[Entrar no servidor]({invite.url})", inline=False)
        embed.add_field(name="⚠️ Aviso", value="Este comando será removido em 24 horas. Guarde o convite!", inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Agendar remoção do comando (simulação)
        asyncio.create_task(remove_support_command_later())
        
    except Exception as e:
        await interaction.followup.send(f"❌ Erro: {str(e)}", ephemeral=True)

async def remove_support_command_later():
    """Simula remoção do comando após 24h"""
    await asyncio.sleep(86400)  # 24 horas
    print("⚠️ Comando /criarsuporte deve ser removido manualmente agora!")

async def configure_support_guild(guild: discord.Guild, template: dict, admin_user: discord.User):
    """Configura servidor de suporte com conteúdo específico"""
    
    # 1. Criar cargos
    roles_map = {}
    for role_name, color, permissions, hoist in template['roles']:
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if existing_role:
            roles_map[role_name] = existing_role
            continue
            
        perms = discord.Permissions()
        for perm in permissions:
            setattr(perms, perm, True)
        
        role = await guild.create_role(
            name=role_name,
            color=color,
            permissions=perms,
            hoist=hoist,
            reason='Configuração do servidor de suporte'
        )
        roles_map[role_name] = role
        await asyncio.sleep(0.5)
    
    # Promover admin
    member = guild.get_member(admin_user.id)
    if member:
        admin_role = roles_map.get('👑 Fundador')
        if admin_role:
            await member.add_roles(admin_role)
    
    # 2. Deletar canais padrão
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.5)
        except:
            pass
    
    await asyncio.sleep(2)
    
    # 3. Criar categorias
    cat_info = await guild.create_category('📋 INFORMAÇÕES')
    cat_legal = await guild.create_category('⚖️ LEGAL')
    cat_suporte = await guild.create_category('🎫 SUPORTE')
    cat_comunidade = await guild.create_category('💬 COMUNIDADE')
    cat_voz = await guild.create_category('🔊 VOZ')
    cat_staff = await guild.create_category('🔒 STAFF ONLY')
    
    await asyncio.sleep(1)
    
    # 4. Criar canais com conteúdo específico
    
    # Canal de Termos
    termos_channel = await guild.create_text_channel(
        '📜┃termos-serviço',
        category=cat_legal,
        topic='Termos de Serviço do ServerCreator Bot'
    )
    
    # Enviar Termos de Serviço
    termos_embed = discord.Embed(
        title="📜 Termos de Serviço",
        description="Leia atentamente os termos antes de usar o bot.",
        color=discord.Color.blue(),
        url=f"{SITE_URL}/termos.html"
    )
    termos_embed.add_field(
        name="🔗 Link Completo",
        value=f"[Clique aqui para ler os termos completos]({SITE_URL}/termos.html)",
        inline=False
    )
    termos_embed.add_field(
        name="⚠️ Resumo",
        value="• O bot requer permissão de Administrador\n• Não nos responsabilizamos por perda de dados\n• Uso comercial proibido sem autorização\n• Respeite as diretrizes do Discord",
        inline=False
    )
    await termos_channel.send(embed=termos_embed)
    
    # Canal de Privacidade
    priv_channel = await guild.create_text_channel(
        '🔒┃política-privacidade',
        category=cat_legal,
        topic='Política de Privacidade do ServerCreator Bot'
    )
    
    priv_embed = discord.Embed(
        title="🔒 Política de Privacidade",
        description="Como tratamos seus dados.",
        color=discord.Color.green(),
        url=f"{SITE_URL}/privacidade.html"
    )
    priv_embed.add_field(
        name="🔗 Link Completo",
        value=f"[Clique aqui para ler a política completa]({SITE_URL}/privacidade.html)",
        inline=False
    )
    priv_embed.add_field(
        name="🛡️ Nosso Compromisso",
        value="• Não vendemos seus dados\n• Dados temporários apagados em 24h\n• Sem armazenamento de mensagens\n• Segurança em primeiro lugar",
        inline=False
    )
    await priv_channel.send(embed=priv_embed)
    
    # Canal do Site
    site_channel = await guild.create_text_channel(
        '🌐┃site-oficial',
        category=cat_info,
        topic='Link do site oficial do ServerCreator'
    )
    
    site_embed = discord.Embed(
        title="🌐 Site Oficial",
        description="Acesse nosso site para mais informações!",
        color=discord.Color.blurple()
    )
    site_embed.add_field(
        name="🔗 Link",
        value=f"**[{SITE_URL}]({SITE_URL})**",
        inline=False
    )
    site_embed.add_field(
        name="📋 Conteúdo do Site",
        value="• Termos de Serviço\n• Política de Privacidade\n• Informações detalhadas\n• Links de convite",
        inline=False
    )
    site_embed.set_thumbnail(url='https://i.imgur.com/6fVO3QX.png')
    await site_channel.send(embed=site_embed)
    
    # Canal FAQ
    faq_channel = await guild.create_text_channel(
        '❓┃faq',
        category=cat_suporte,
        topic='Perguntas Frequentes'
    )
    
    faq_embed = discord.Embed(
        title="❓ Perguntas Frequentes (FAQ)",
        description="Tire suas dúvidas aqui!",
        color=discord.Color.gold()
    )
    
    faqs = [
        ("🤔 O que é o ServerCreator?", "Bot que configura servidores Discord completos em segundos com temas automatizados."),
        ("💰 O bot é gratuito?", "Sim! 100% gratuito para todos os usuários."),
        ("🔒 É seguro dar permissão de Admin?", "Sim, o bot precisa criar canais e cargos. Nunca abusamos das permissões."),
        ("🎨 Quantos temas existem?", "6 temas: RPG, Loja, Comunidade, Jogos, Estudos e Anime."),
        ("📊 Quantos canais são criados?", "24+ canais de texto e 10 canais de voz por tema."),
        ("👥 Posso sugerir novos temas?", "Sim! Use o canal 💡┃sugestões ou abra um ticket."),
        ("🐛 Encontrei um bug, e agora?", "Abra um ticket em 🎫┃criar-ticket selecionando 'Reportar Bug'."),
        ("🤝 Como faço parceria?", "Abra um ticket do tipo 'Parceria' e descreva sua proposta."),
        ("⚡ O bot está offline?", "Verifique 🔧┃status-bot ou aguarde reinicialização."),
        ("🗑️ Como limpo o servidor?", "Use o comando `/limparserver` (apenas admins)."),
    ]
    
    for pergunta, resposta in faqs:
        faq_embed.add_field(name=pergunta, value=resposta, inline=False)
    
    faq_embed.set_footer(text="Dúvidas? Abra um ticket em 🎫┃criar-ticket")
    await faq_channel.send(embed=faq_embed)
    
    # Canal de Criar Ticket (com dropdown)
    ticket_channel = await guild.create_text_channel(
        '🎫┃criar-ticket',
        category=cat_suporte,
        topic='Abra seu ticket de suporte aqui'
    )
    
    ticket_embed = discord.Embed(
        title="🎫 Central de Suporte",
        description="Precisa de ajuda? Selecione uma opção abaixo!",
        color=discord.Color.red()
    )
    ticket_embed.add_field(
        name="📋 Tipos de Ticket",
        value="• ❓ Dúvida Geral\n• 🐛 Reportar Bug\n• 💡 Sugestão\n• 🤝 Parceria\n• 🚨 Denúncia\n• 📝 Outro",
        inline=False
    )
    ticket_embed.add_field(
        name="⏰ Horário de Atendimento",
        value="Nossa equipe responde o mais rápido possível. Seja paciente!",
        inline=False
    )
    ticket_embed.add_field(
        name="⚠️ Importante",
        value="• Um ticket por vez\n• Descreva bem seu problema\n• Seja educado\n• Aguarde 5 minutos entre tickets",
        inline=False
    )
    ticket_embed.set_thumbnail(url='https://i.imgur.com/6fVO3QX.png')
    ticket_embed.set_footer(text='ServerCreator Suporte • Selecione uma opção abaixo')
    
    # Enviar mensagem com dropdown
    view = TicketView()
    await ticket_channel.send(embed=ticket_embed, view=view)
    
    # Outros canais básicos
    outros_canais = [
        ('📢┃anúncios', cat_info, 'Anúncios oficiais'),
        ('🎉┃novidades', cat_info, 'Novidades do bot'),
        ('💡┃sugestões', cat_comunidade, 'Sugestões da comunidade'),
        ('🐛┃bugs', cat_comunidade, 'Reporte de bugs'),
        ('💬┃geral', cat_comunidade, 'Chat geral'),
        ('🎨┃showcase', cat_comunidade, 'Mostre seus servidores'),
        ('🤝┃parcerias', cat_comunidade, 'Propostas de parceria'),
    ]
    
    for nome, categoria, topico in outros_canais:
        await guild.create_text_channel(nome, category=categoria, topic=topico)
        await asyncio.sleep(0.5)
    
    # Canais de voz
    for channel_name, user_limit in template['channels']['voz']:
        await guild.create_voice_channel(
            name=channel_name,
            category=cat_voz if 'Staff' not in channel_name else cat_staff,
            user_limit=user_limit
        )
        await asyncio.sleep(0.5)
    
    # Boas-vindas
    welcome_channel = await guild.create_text_channel(
        '👋┃boas-vindas',
        category=cat_info,
        topic='Mensagens de boas-vindas'
    )
    
    welcome_embed = discord.Embed(
        title="🎉 Bem-vindo ao ServerCreator Suporte!",
        description="Servidor oficial de suporte do bot.",
        color=discord.Color.green()
    )
    welcome_embed.add_field(
        name="📋 Primeiros Passos",
        value="1️⃣ Leia as regras em 📋┃regras\n2️⃣ Confira o FAQ em ❓┃faq\n3️⃣ Visite o site em 🌐┃site-oficial\n4️⃣ Abra um ticket se precisar de ajuda!",
        inline=False
    )
    welcome_embed.add_field(
        name="🎫 Precisa de Ajuda?",
        value="Vá em 🎫┃criar-ticket e selecione o tipo de atendimento.",
        inline=False
    )
    await welcome_channel.send(embed=welcome_embed)

# ... (mantenha o resto do código: on_message, dashboard, setupserver, etc.)

# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERRO: Token não encontrado! Verifique seu arquivo .env")
    else:
        bot.run(TOKEN)
