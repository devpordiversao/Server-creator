# main.py - ServerCreator Bot (VERSÃO COMPLETA COM SISTEMA DE SUGESTÕES AVANÇADO)
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import re
from io import StringIO

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
        self.ticket_cooldowns = {}
        self.suggestion_cooldowns = {}
    
    def load_templates(self):
        """Carrega templates de servidores temáticos EXPANDIDOS"""
        return {
            'rpg': {
                'icon': '🎲',
                'color': discord.Color.dark_purple(),
                'description': 'Servidor temático completo para RPG de mesa',
                'channels': {
                    'texto': [
                        ('📜┃regras-gerais', 'Regras e diretrizes do servidor'),
                        ('📢┃anúncios', 'Anúncios importantes'),
                        ('🎭┃apresentações', 'Apresente seu personagem'),
                        ('🗺️┃lore-mundo', 'História e lore do mundo'),
                        ('📚┃bestiário', 'Criaturas e monstros'),
                        ('🎲┃mesa-principal', 'Mesa de RPG principal'),
                        ('🎲┃mesa-secundária', 'Mesa secundária'),
                        ('🎲┃mesa-aventura', 'Mesa de aventuras'),
                        ('🎲┃mesa-one-shot', 'One-shots e sessões únicas'),
                        ('🎲┃mesa-campanha', 'Campanha principal'),
                        ('💬┃chat-rpg', 'Conversas sobre RPG'),
                        ('🎨┃artes-personagens', 'Artes e tokens'),
                        ('📖┃homebrew', 'Conteúdo caseiro'),
                        ('🎵┃músicas-ambiente', 'Trilhas sonoras'),
                        ('🎬┃streams-sessões', 'Transmissões de jogos'),
                        ('📊┃dados-estatísticas', 'Rolagens e stats'),
                        ('🛒┃comércio-ig', 'Lojas dentro do jogo'),
                        ('🏰┃guildas-facções', 'Grupos e organizações'),
                        ('📜┃missões', 'Board de missões'),
                        ('💀┃cemitério-perso', 'Personagens falecidos'),
                        ('🎪┃eventos-especiais', 'Eventos e festivais'),
                        ('📝┃fichas-personagens', 'Fichas dos players'),
                        ('🤝┃recrutamento-mesas', 'Procurando grupo'),
                        ('🔮┃previsões-oráculo', 'Previsões do destino'),
                    ],
                    'voz': [
                        ('🎙️┃Mesa do Mestre', None),
                        ('🎙️┃Aventura 1', None),
                        ('🎙️┃Aventura 2', None),
                        ('🎙️┃Aventura 3', None),
                        ('🎙️┃Campanha Principal', None),
                        ('🎙️┃One-Shot', 6),
                        ('🎧┃Música Ambiente', None),
                        ('🔒┃Sala Privada 1', 3),
                        ('🔒┃Sala Privada 2', 3),
                        ('🎪┃Eventos Especiais', None),
                    ]
                },
                'roles': [
                    ('👑 Mestre Supremo', discord.Color.gold(), ['administrator'], True),
                    ('🎲 Mestre Narrador', discord.Color.dark_gold(), ['manage_messages', 'mute_members'], True),
                    ('🧙‍♂️ Arquimago', discord.Color.purple(), ['manage_messages'], False),
                    ('⚔️ Paladino', discord.Color.blue(), ['kick_members'], False),
                    ('🏹 Ranger', discord.Color.green(), ['priority_speaker'], False),
                    ('🗡️ Ladino', discord.Color.dark_grey(), [], False),
                    ('🔥 Mago', discord.Color.red(), [], False),
                    ('❄️ Clérigo', discord.Color.teal(), [], False),
                    ('🌿 Druida', discord.Color.dark_green(), [], False),
                    ('⚡ Bárbaro', discord.Color.orange(), [], False),
                    ('🎭 Bardo', discord.Color.magenta(), [], False),
                    ('💀 Necromante', discord.Color.dark_red(), [], False),
                    ('🛡️ Guerreiro', discord.Color.dark_blue(), [], False),
                    ('🔮 Vidente', discord.Color.purple(), [], False),
                    ('🐉 Domador', discord.Color.gold(), [], False),
                    ('📜 Escriba', discord.Color.light_grey(), [], False),
                    ('🎨 Artífice', discord.Color.blurple(), [], False),
                    ('🍺 Alquimista', discord.Color.from_rgb(139, 69, 19), [], False),
                    ('⭐ Aventureiro VIP', discord.Color.from_rgb(255, 215, 0), [], False),
                    ('🎒 Aventureiro', discord.Color.from_rgb(100, 149, 237), [], False),
                    ('👀 Espectador', discord.Color.greyple(), ['view_channel'], False),
                    ('🤖 Bot Sistema', discord.Color.from_rgb(32, 34, 37), ['send_messages'], False),
                ],
                'welcome_message': '🎲 {member} entrou na party! Rolem iniciativa e preparem os dados!',
                'leave_message': '👋 {member} deixou a mesa. Que seus dados rolem nat 20 onde estiver!',
                'welcome_image': 'https://i.imgur.com/rpg_welcome.png',
            },
            
            'loja': {
                'icon': '🛒',
                'color': discord.Color.green(),
                'description': 'Servidor completo para e-commerce e vendas',
                'channels': {
                    'texto': [
                        ('📋┃regras-loja', 'Regras e termos de uso'),
                        ('📢┃novidades', 'Lançamentos e novidades'),
                        ('🛍️┃catálogo-geral', 'Todos os produtos'),
                        ('👕┃roupas', 'Vestuário e moda'),
                        ('👟┃calçados', 'Tênis e sapatos'),
                        ('💻┃eletrônicos', 'Tecnologia e gadgets'),
                        ('🏠┃casa-decoração', 'Utilidades domésticas'),
                        ('🎮┃games', 'Jogos e consoles'),
                        ('📚┃livros', 'Livros e materiais'),
                        ('🎨┃arte-design', 'Produtos artísticos'),
                        ('💰┃promoções', 'Ofertas especiais'),
                        ('🎫┃cupons', 'Códigos de desconto'),
                        ('📦┃rastreamento', 'Status de entregas'),
                        ('🎁┃brindes', 'Produtos gratuitos'),
                        ('⭐┃avaliações', 'Reviews dos clientes'),
                        ('💬┃suporte-chat', 'Atendimento rápido'),
                        ('🎫┃tickets', 'Suporte técnico'),
                        ('🤝┃parcerias', 'Propostas comerciais'),
                        ('📊┃vendas-live', 'Vendas ao vivo'),
                        ('💳┃pagamentos', 'Dúvidas sobre pagamento'),
                        ('🚚┃entregas', 'Informações de envio'),
                        ('🔄┃trocas-devoluções', 'Política de trocas'),
                        ('👥┃afiliados', 'Programa de afiliados'),
                        ('📈┃relatórios', 'Dados e estatísticas'),
                    ],
                    'voz': [
                        ('🎧┃Atendimento 1', None),
                        ('🎧┃Atendimento 2', None),
                        ('🎧┃Suporte VIP', None),
                        ('💼┃Reuniões', 8),
                        ('📊┃Vendas Live', None),
                        ('🎙️┃Podcast Loja', None),
                        ('🔒┃Staff Only', 5),
                        ('🎵┃Espera Musical', None),
                        ('📞┃SAC', 2),
                        ('🤝┃Negociações', 4),
                    ]
                },
                'roles': [
                    ('👑 CEO', discord.Color.gold(), ['administrator'], True),
                    ('💼 Gerente', discord.Color.dark_gold(), ['manage_messages', 'kick_members'], True),
                    ('🛍️ Supervisor', discord.Color.orange(), ['manage_messages'], False),
                    ('💰 Vendedor Ouro', discord.Color.gold(), [], False),
                    ('🥈 Vendedor Prata', discord.Color.light_grey(), [], False),
                    ('🥉 Vendedor Bronze', discord.Color.from_rgb(205, 127, 50), [], False),
                    ('📦 Estoquista', discord.Color.blue(), [], False),
                    ('🎨 Designer', discord.Color.purple(), [], False),
                    ('📱 Social Media', discord.Color.pink(), [], False),
                    ('💻 Dev Site', discord.Color.dark_blue(), [], False),
                    ('🚚 Entregador', discord.Color.green(), [], False),
                    ('🎫 Suporte N1', discord.Color.teal(), [], False),
                    ('🎫 Suporte N2', discord.Color.dark_teal(), [], False),
                    ('⭐ Cliente VIP', discord.Color.from_rgb(255, 215, 0), [], False),
                    ('💎 Cliente Premium', discord.Color.purple(), [], False),
                    ('🛒 Cliente Frequente', discord.Color.blue(), [], False),
                    ('👤 Cliente Novo', discord.Color.green(), [], False),
                    ('👀 Visitante', discord.Color.greyple(), ['view_channel'], False),
                    ('🤖 Bot Loja', discord.Color.from_rgb(32, 34, 37), [], False),
                    ('📢 Anunciante', discord.Color.red(), [], False),
                    ('🎁 Sorteador', discord.Color.magenta(), [], False),
                    ('💳 Financeiro', discord.Color.dark_green(), [], False),
                ],
                'welcome_message': '🛒 Bem-vindo à loja, {member}! Confira nossas ofertas e aproveite!',
                'leave_message': '👋 {member} saiu da loja. Volte sempre para mais ofertas!',
                'welcome_image': 'https://i.imgur.com/shop_welcome.png',
            },
            
            'comunidade': {
                'icon': '🌐',
                'color': discord.Color.blue(),
                'description': 'Servidor completo para comunidades e grupos sociais',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras da comunidade'),
                        ('📢┃anúncios', 'Anúncios oficiais'),
                        ('👋┃boas-vindas', 'Apresente-se aqui!'),
                        ('💬┃chat-geral', 'Conversa livre'),
                        ('🎨┃arte-criações', 'Mostre sua arte'),
                        ('🎵┃música', 'Compartilhe músicas'),
                        ('🎮┃gaming', 'Jogos e players'),
                        ('📺┃anime-mangá', 'Cultura otaku'),
                        ('🎬┃filmes-séries', 'Cinema e TV'),
                        ('📚┃literatura', 'Livros e leituras'),
                        ('🍕┃culinária', 'Comidas e receitas'),
                        ('🏋️┃fitness', 'Saúde e exercícios'),
                        ('💻┃tecnologia', 'Tech e programação'),
                        ('🎓┃estudos', 'Ajuda acadêmica'),
                        ('💼┃trabalho', 'Empregos e carreira'),
                        ('🏆┃eventos', 'Eventos da comunidade'),
                        ('🎉┃sorteios', 'Premiações'),
                        ('🤝┃parcerias', 'Colaborações'),
                        ('💡┃sugestões', 'Ideias para o servidor'),
                        ('😂┃memes', 'Zoeira e humor'),
                        ('🐶┃pets', 'Animais de estimação'),
                        ('🌿┃natureza', 'Fotos da natureza'),
                        ('✈️┃viagens', 'Turismo e lugares'),
                        ('🎭┃roleplay', 'Interpretação de personagens'),
                    ],
                    'voz': [
                        ('🎙️┃Geral 1', None),
                        ('🎙️┃Geral 2', None),
                        ('🎙️┃Geral 3', None),
                        ('🎵┃Música', None),
                        ('🎮┃Gaming Squad', 5),
                        ('🎮┃Gaming Duo', 2),
                        ('📺┃Assistindo Junto', None),
                        ('🔒┃Amigos 1', 3),
                        ('🔒┃Amigos 2', 3),
                        ('🎧┃AFK', None),
                    ]
                },
                'roles': [
                    ('👑 Fundador', discord.Color.gold(), ['administrator'], True),
                    ('🛡️ Admin', discord.Color.red(), ['ban_members', 'manage_messages'], True),
                    ('⚔️ Moderador', discord.Color.orange(), ['kick_members', 'manage_messages'], False),
                    ('🎨 Designer', discord.Color.purple(), [], False),
                    ('🎵 DJ', discord.Color.magenta(), ['priority_speaker'], False),
                    ('🎮 Pro Player', discord.Color.dark_blue(), [], False),
                    ('🎬 Cineasta', discord.Color.dark_red(), [], False),
                    ('📚 Escritor', discord.Color.teal(), [], False),
                    ('🍕 Chef', discord.Color.from_rgb(255, 140, 0), [], False),
                    ('💻 Developer', discord.Color.dark_green(), [], False),
                    ('🏆 Organizador', discord.Color.gold(), [], False),
                    ('🎉 Animador', discord.Color.pink(), [], False),
                    ('📱 Influencer', discord.Color.blue(), [], False),
                    ('🎭 Roleplayer', discord.Color.dark_purple(), [], False),
                    ('📸 Fotógrafo', discord.Color.from_rgb(64, 224, 208), [], False),
                    ('🎓 Mentor', discord.Color.green(), [], False),
                    ('⭐ Membro Antigo', discord.Color.from_rgb(255, 215, 0), [], False),
                    ('💎 Membro VIP', discord.Color.purple(), [], False),
                    ('🎭 Membro Ativo', discord.Color.blurple(), [], False),
                    ('👥 Membro', discord.Color.blue(), [], False),
                    ('🌱 Novato', discord.Color.green(), [], False),
                    ('👀 Visitante', discord.Color.greyple(), ['view_channel'], False),
                ],
                'welcome_message': '🎉 Bem-vindo à comunidade, {member}! Sinta-se em casa!',
                'leave_message': '👋 {member} deixou a comunidade. Sentiremos sua falta!',
                'welcome_image': 'https://i.imgur.com/community_welcome.png',
            },
            
            'jogos': {
                'icon': '🎮',
                'color': discord.Color.dark_red(),
                'description': 'Servidor completo para gamers e e-sports',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras do servidor'),
                        ('📢┃anúncios', 'News e updates'),
                        ('🎯┃buscando-grupo', 'Encontre seu squad'),
                        ('🏆┃ranking', 'Placar de líderes'),
                        ('🎮┃chat-geral', 'Geral gaming'),
                        ('🔫┃fps-games', 'CS:GO, Valorant, CoD'),
                        ('⚔️┃moba', 'LoL, Dota, Smite'),
                        ('🌍┃mmorpg', 'WoW, FF14, BDO'),
                        ('🏗️┃sandbox', 'Minecraft, Terraria'),
                        ('🎲┃indie', 'Jogos independentes'),
                        ('🎌┃gacha', 'Genshin, Honkai, FGO'),
                        ('🏎️┃corrida', 'Forza, Gran Turismo'),
                        ('⚽┃esports', 'FIFA, eFootball'),
                        ('🧩┃puzzle', 'Jogos de lógica'),
                        ('👻┃horror', 'Jogos de terror'),
                        ('🎪┃casual', 'Jogos relaxantes'),
                        ('📺┃streams', 'Promova sua live'),
                        ('🎬┃clips', 'Melhores momentos'),
                        ('🤝┃recrutamento', 'Recrute para seu time'),
                        ('🏆┃torneios', 'Campeonatos'),
                        ('💰┃vendas-troca', 'Mercado de jogos'),
                        ('🛠️┃mods', 'Modificações'),
                        ('💻┃setup', 'Mostre seu setup'),
                        ('📊┃estatísticas', 'Stats e análises'),
                    ],
                    'voz': [
                        ('🎙️┃Lobby', None),
                        ('🎙️┃Squad 1', 4),
                        ('🎙️┃Squad 2', 4),
                        ('🎙️┃Squad 3', 4),
                        ('🎙️┃Ranked 5v5', 5),
                        ('🎙️┃Ranked Duo', 2),
                        ('🎙️┃MMORPG Raid', 8),
                        ('🎵┃Música Game', None),
                        ('🔒┃Clã Privado', 5),
                        ('🎧┃AFK Gaming', None),
                    ]
                },
                'roles': [
                    ('🏆 Dono do Server', discord.Color.gold(), ['administrator'], True),
                    ('🎮 Capitão', discord.Color.dark_gold(), ['manage_messages', 'move_members'], True),
                    ('⭐ Coach', discord.Color.purple(), ['priority_speaker'], False),
                    ('🔫 FPS Pro', discord.Color.red(), [], False),
                    ('⚔️ MOBA King', discord.Color.blue(), [], False),
                    ('🌍 MMO Veteran', discord.Color.green(), [], False),
                    ('🎌 Gacha Whale', discord.Color.pink(), [], False),
                    ('🏎️ Piloto', discord.Color.orange(), [], False),
                    ('⚽ Esports Pro', discord.Color.teal(), [], False),
                    ('🧩 Estrategista', discord.Color.dark_blue(), [], False),
                    ('👻 Survival', discord.Color.dark_grey(), [], False),
                    ('🎪 Casual', discord.Color.light_grey(), [], False),
                    ('📺 Streamer', discord.Color.magenta(), [], False),
                    ('🎬 Criador Conteúdo', discord.Color.from_rgb(255, 0, 255), [], False),
                    ('🏆 Campeão', discord.Color.gold(), [], False),
                    ('🥈 Elite', discord.Color.from_rgb(192, 192, 192), [], False),
                    ('🥉 Competitivo', discord.Color.from_rgb(205, 127, 50), [], False),
                    ('🎯 Tryhard', discord.Color.dark_red(), [], False),
                    ('🎮 Gamer', discord.Color.blue(), [], False),
                    ('🎒 Novato', discord.Color.green(), [], False),
                    ('👀 Viewer', discord.Color.greyple(), ['view_channel'], False),
                    ('🤖 Bot Game', discord.Color.from_rgb(32, 34, 37), [], False),
                ],
                'welcome_message': '🎮 GG! {member} entrou no servidor! Prepara que é hora do clutch!',
                'leave_message': '👋 {member} desconectou. Até a próxima partida!',
                'welcome_image': 'https://i.imgur.com/gaming_welcome.png',
            },
            
            'estudo': {
                'icon': '📚',
                'color': discord.Color.teal(),
                'description': 'Servidor completo para estudos e produtividade',
                'channels': {
                    'texto': [
                        ('📋┃regras', 'Regras de conduta'),
                        ('📅┃calendário', 'Eventos e prazos'),
                        ('📢┃avisos', 'Comunicados importantes'),
                        ('📚┃geral', 'Chat geral de estudos'),
                        ('💻┃programação', 'Códigos e dev'),
                        ('🔢┃matemática', 'Cálculos e fórmulas'),
                        ('🔬┃ciências', 'Física, Química, Bio'),
                        ('🌍┃humanas', 'História, Geo, Socio'),
                        ('🗣️┃idiomas', 'Inglês, Espanhol, etc'),
                        ('🎨┃artes', 'Desenho e criatividade'),
                        ('🎵┃música', 'Teoria e prática'),
                        ('🏥┃medicina', 'Saúde e anatomia'),
                        ('⚖️┃direito', 'Leis e jurisprudência'),
                        ('💼┃administração', 'Negócios e gestão'),
                        ('🔧┃engenharia', 'Projetos e cálculos'),
                        ('📝┃redação', 'Escrita e literatura'),
                        ('🎯┃enem-vestibular', 'Preparação exames'),
                        ('🎓┃faculdade', 'Ensino superior'),
                        ('📖┃concursos', 'Preparação concursos'),
                        ('📝┃resumos', 'Compartilhe anotações'),
                        ('❓┃dúvidas', 'Tire suas dúvidas'),
                        ('🎯┃metas', 'Objetivos diários'),
                        ('🏆┃conquistas', 'Celebre suas vitórias'),
                        ('🤝┃grupos-estudo', 'Forme equipes'),
                    ],
                    'voz': [
                        ('🔇┃Sala Silenciosa', None),
                        ('🗣️┃Discussão', None),
                        ('📖┃Grupo Estudo 1', 5),
                        ('📖┃Grupo Estudo 2', 5),
                        ('📖┃Grupo Estudo 3', 5),
                        ('🎵┃Lo-Fi Focus', None),
                        ('🎙️┃Apresentação', None),
                        ('🔒┃Monitoria', 3),
                        ('📞┃Dúvida Rápida', 2),
                        ('🎧┃Descanso', None),
                    ]
                },
                'roles': [
                    ('👨‍🏫 Diretor', discord.Color.gold(), ['administrator'], True),
                    ('👩‍🏫 Professor', discord.Color.dark_gold(), ['manage_messages', 'mute_members'], True),
                    ('🎓 Monitor', discord.Color.purple(), ['mute_members'], False),
                    ('💻 Dev Sênior', discord.Color.dark_blue(), [], False),
                    ('💻 Dev Júnior', discord.Color.blue(), [], False),
                    ('🔢 Matemático', discord.Color.red(), [], False),
                    ('🔬 Cientista', discord.Color.green(), [], False),
                    ('🌍 Historiador', discord.Color.orange(), [], False),
                    ('🗣️ Poliglota', discord.Color.pink(), [], False),
                    ('🎨 Artista', discord.Color.magenta(), [], False),
                    ('🎵 Músico', discord.Color.teal(), [], False),
                    ('🏥 Médico', discord.Color.from_rgb(255, 0, 0), [], False),
                    ('⚖️ Advogado', discord.Color.dark_grey(), [], False),
                    ('💼 Administrador', discord.Color.dark_green(), [], False),
                    ('🔧 Engenheiro', discord.Color.from_rgb(128, 128, 128), [], False),
                    ('📝 Escritor', discord.Color.from_rgb(139, 69, 19), [], False),
                    ('🎯 Aprovado', discord.Color.gold(), [], False),
                    ('📚 Aluno Destaque', discord.Color.purple(), [], False),
                    ('✏️ Aluno', discord.Color.blue(), [], False),
                    ('🌱 Iniciante', discord.Color.green(), [], False),
                    ('👀 Observador', discord.Color.greyple(), ['view_channel'], False),
                    ('🤖 Bot Educação', discord.Color.from_rgb(32, 34, 37), [], False),
                ],
                'welcome_message': '📚 Bem-vindo aos estudos, {member}! Que o conhecimento esteja com você!',
                'leave_message': '👋 {member} deixou a sala de aula. Bons estudos!',
                'welcome_image': 'https://i.imgur.com/study_welcome.png',
            },
            
            'anime': {
                'icon': '🍥',
                'color': discord.Color.pink(),
                'description': 'Servidor completo para fãs de anime e cultura japonesa',
                'channels': {
                    'texto': [
                        ('📜┃regras', 'Regras do servidor'),
                        ('📢┃anúncios', 'News do mundo otaku'),
                        ('🎌┃apresentações', 'Apresente-se!'),
                        ('💬┃chat-geral', 'Conversa livre'),
                        ('📺┃recomendações', 'Indique animes'),
                        ('📺┃em-exibição', 'Temporada atual'),
                        ('📺┃clássicos', 'Animes antigos'),
                        ('📖┃mangás', 'Discussão de mangás'),
                        ('📖┃light-novels', 'LNs e webnovels'),
                        ('🎨┃fanarts', 'Arte da comunidade'),
                        ('🎨┃cosplay', 'Fotos de cosplay'),
                        ('🎵┃osts', 'Trilhas sonoras'),
                        ('🎵┃openings', 'Aberturas e encerramentos'),
                        ('🎮┃gacha-games', 'Genshin, FGO, etc'),
                        ('🎮┃jogos-anime', 'Games de anime'),
                        ('🎌┃cultura-japonesa', 'Japão e cultura'),
                        ('🗣️┃japonês', 'Aprenda o idioma'),
                        ('🍜┃culinária', 'Comida japonesa'),
                        ('🔥┃batalhas', 'X1 de personagens'),
                        ('⚔️┃versus', 'Debate de animes'),
                        ('💕┃shipping', 'Casais e ships'),
                        ('😂┃memes-otaku', 'Zoeira anime'),
                        ('🎉┃eventos', 'Eventos da comunidade'),
                        ('🎁┃sorteios', 'Prêmios para otakus'),
                    ],
                    'voz': [
                        ('🎙️┃Geral', None),
                        ('🎵┃Karaokê', None),
                        ('📺┃Assistindo Junto', None),
                        ('🎮┃Gacha & Games', None),
                        ('🗣️┃Japonês', None),
                        ('🔒┃Squad Otaku', 4),
                        ('🎌┃Cultura', None),
                        ('🎧┃Música Anime', None),
                        ('🔥┃Debates', 6),
                        ('🎧┃AFK', None),
                    ]
                },
                'roles': [
                    ('👑 Hokage', discord.Color.gold(), ['administrator'], True),
                    ('🥷 Kage', discord.Color.dark_red(), ['manage_messages', 'kick_members'], True),
                    ('🎌 Sensei', discord.Color.orange(), ['manage_messages'], False),
                    ('⚡ Protagonista', discord.Color.gold(), [], False),
                    ('😈 Vilão', discord.Color.dark_purple(), [], False),
                    ('🗡️ Espadachim', discord.Color.from_rgb(192, 192, 192), [], False),
                    ('🔥 Super Sayajin', discord.Color.gold(), [], False),
                    ('❄️ Shinigami', discord.Color.dark_blue(), [], False),
                    ('🍥 Ninja', discord.Color.orange(), [], False),
                    ('⚔️ Caçador', discord.Color.green(), [], False),
                    ('🎭 Ghoul', discord.Color.red(), [], False),
                    ('🎨 Artista', discord.Color.pink(), [], False),
                    ('🎵 Cantor', discord.Color.magenta(), [], False),
                    ('📺 Streamer', discord.Color.purple(), [], False),
                    ('🎮 Gamer Otaku', discord.Color.blue(), [], False),
                    ('🗣️ Polyglota', discord.Color.teal(), [], False),
                    ('🍜 Cozinheiro', discord.Color.from_rgb(255, 140, 0), [], False),
                    ('⭐ Otaku VIP', discord.Color.from_rgb(255, 215, 0), [], False),
                    ('💎 Weeb', discord.Color.purple(), [], False),
                    ('🍥 Otaku', discord.Color.pink(), [], False),
                    ('🌸 Novato', discord.Color.green(), [], False),
                    ('👀 Espectador', discord.Color.greyple(), ['view_channel'], False),
                ],
                'welcome_message': '🍥 Ora ora, {member} chegou! Dattebayo! Prepare-se para a aventura!',
                'leave_message': '👋 {member} foi comer ramen. Sayonara!',
                'welcome_image': 'https://i.imgur.com/anime_welcome.png',
            },
            
            'suporte': {
                'icon': '🎫',
                'color': discord.Color.red(),
                'description': 'Servidor oficial de suporte do ServerCreator Bot',
                'temporary': True,
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
            name='/setupserver para configurar servidores!'
        )
    )
    print(f'{bot.user} está online!')

# ==================== SISTEMA DE SUGESTÕES AVANÇADO ====================

class SuggestionModal(discord.ui.Modal, title="💡 Enviar Sugestão"):
    nickname = discord.ui.TextInput(
        label="Seu Nick/Apelido",
        placeholder="Como você gostaria de ser chamado?",
        required=True,
        max_length=50
    )
    
    suggestion = discord.ui.TextInput(
        label="Sua Sugestão",
        placeholder="Descreva sua sugestão em detalhes...",
        required=True,
        max_length=1000,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Verificar cooldown
        cooldown_key = f"{interaction.user.id}_{interaction.guild.id}"
        if cooldown_key in bot.suggestion_cooldowns:
            last_suggestion = bot.suggestion_cooldowns[cooldown_key]
            if (datetime.now() - last_suggestion).total_seconds() < 300:  # 5 minutos
                await interaction.response.send_message(
                    "⏳ Você já enviou uma sugestão recentemente! Aguarde 5 minutos.",
                    ephemeral=True
                )
                return
        
        # Buscar canais
        guild = interaction.guild
        suggestions_channel = discord.utils.get(guild.text_channels, name="💡┃sugestões")
        send_suggestion_channel = discord.utils.get(guild.text_channels, name="💌┃enviar-sugestão")
        
        if not suggestions_channel:
            await interaction.response.send_message(
                "❌ Canal de sugestões não encontrado! Contate um administrador.",
                ephemeral=True
            )
            return
        
        # Criar embed da sugestão
        embed = discord.Embed(
            title="💡 Nova Sugestão Recebida",
            description=f"```{self.suggestion.value}```",
            color=discord.Color.blurple(),
            timestamp=datetime.now()
        )
        
        embed.set_author(
            name=self.nickname.value,
            icon_url=interaction.user.display_avatar.url
        )
        
        embed.set_footer(text=f"ID: {interaction.user.id} • Use os botões abaixo para gerenciar")
        
        # Enviar para o canal de sugestões
        suggestion_msg = await suggestions_channel.send(
            content=f"📩 Sugestão de {interaction.user.mention}",
            embed=embed
        )
        
        # Adicionar reações (emojis)
        await suggestion_msg.add_reaction("👍")
        await suggestion_msg.add_reaction("👎")
        await suggestion_msg.add_reaction("🤔")
        
        # Enviar DM para o dono do bot (você)
        try:
            owner = await bot.fetch_user(ADMIN_USER_ID)  # Substitua pelo seu ID
            if owner:
                dm_embed = discord.Embed(
                    title="💡 Nova Sugestão Recebida",
                    description=f"```{self.suggestion.value}```",
                    color=discord.Color.blurple(),
                    timestamp=datetime.now()
                )
                dm_embed.set_author(
                    name=f"{self.nickname.value} ({interaction.user.name})",
                    icon_url=interaction.user.display_avatar.url
                )
                dm_embed.add_field(
                    name="📍 Servidor",
                    value=f"{guild.name} ({guild.id})",
                    inline=True
                )
                dm_embed.add_field(
                    name="👤 Usuário",
                    value=f"{interaction.user.mention} ({interaction.user.id})",
                    inline=True
                )
                dm_embed.add_field(
                    name="🔗 Link",
                    value=f"[Ir para a sugestão]({suggestion_msg.jump_url})",
                    inline=False
                )
                
                # Criar view com botões Aceitar/Recusar
                view = SuggestionDecisionView(
                    suggestion_msg.id,
                    interaction.user.id,
                    self.nickname.value,
                    self.suggestion.value,
                    interaction.user.display_avatar.url
                )
                
                await owner.send(embed=dm_embed, view=view)
        except Exception as e:
            print(f"Erro ao enviar DM: {e}")
        
        # Registrar cooldown
        bot.suggestion_cooldowns[cooldown_key] = datetime.now()
        
        # Confirmar ao usuário
        await interaction.response.send_message(
            "✅ Sua sugestão foi enviada com sucesso! Obrigado por contribuir.",
            ephemeral=True
        )

class SuggestionDecisionView(discord.ui.View):
    def __init__(self, message_id, user_id, nickname, suggestion, avatar_url):
        super().__init__(timeout=None)
        self.message_id = message_id
        self.user_id = user_id
        self.nickname = nickname
        self.suggestion = suggestion
        self.avatar_url = avatar_url
    
    @discord.ui.button(label="✅ Aceitar", style=discord.ButtonStyle.green, custom_id="accept_suggestion")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_decision(interaction, "accepted")
    
    @discord.ui.button(label="❌ Recusar", style=discord.ButtonStyle.red, custom_id="reject_suggestion")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_decision(interaction, "rejected")
    
    async def process_decision(self, interaction: discord.Interaction, decision: str):
        # Buscar canais em todos os servidores onde o bot está
        for guild in bot.guilds:
            if decision == "accepted":
                target_channel = discord.utils.get(guild.text_channels, name="✅┃sugestões-aceitas")
                color = discord.Color.green()
                title = "✅ Sugestão Aceita"
                status = "Aceita"
            else:
                target_channel = discord.utils.get(guild.text_channels, name="❌┃sugestões-recusadas")
                color = discord.Color.red()
                title = "❌ Sugestão Recusada"
                status = "Recusada"
            
            if target_channel:
                embed = discord.Embed(
                    title=title,
                    description=f"```{self.suggestion}```",
                    color=color,
                    timestamp=datetime.now()
                )
                embed.set_author(
                    name=self.nickname,
                    icon_url=self.avatar_url
                )
                embed.set_footer(text=f"Avaliada por {interaction.user.name}")
                
                await target_channel.send(embed=embed)
        
        # Notificar o usuário que sugeriu
        try:
            user = await bot.fetch_user(self.user_id)
            if user:
                dm_embed = discord.Embed(
                    title=f"📢 Sua sugestão foi {status.lower()}!",
                    description=f"```{self.suggestion}```",
                    color=color
                )
                dm_embed.add_field(
                    name="📊 Status",
                    value=f"Sua sugestão foi **{status}** pela equipe.",
                    inline=False
                )
                await user.send(embed=dm_embed)
        except Exception as e:
            print(f"Erro ao notificar usuário: {e}")
        
        # Desabilitar botões
        for child in self.children:
            child.disabled = True
        
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"✅ Sugestão {status.lower()} com sucesso!", ephemeral=True)

class SuggestionButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="💡 Enviar Sugestão",
        style=discord.ButtonStyle.blurple,
        custom_id="send_suggestion_button",
        emoji="💡"
    )
    async def suggestion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SuggestionModal()
        await interaction.response.send_modal(modal)

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
            if (datetime.now() - last_ticket).total_seconds() < 300:
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
        is_staff = any(r.name in ['⚡ Administrador', '🛡️ Moderador', '🎫 Suporte'] for r in interaction.user.roles)
        is_creator = interaction.user.id == self.creator_id
        
        if not (is_staff or is_creator):
            await interaction.response.send_message("❌ Apenas o criador ou staff pode fechar!", ephemeral=True)
            return
        
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
        
        messages = []
        async for msg in interaction.channel.history(limit=200, oldest_first=True):
            if not msg.author.bot:
                messages.append(f"[{msg.created_at.strftime('%H:%M')}] {msg.author.name}: {msg.content}")
        
        transcript = "\n".join(messages[-100:])
        
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
        
        await asyncio.sleep(5)
        await self.channel.delete(reason=f"Ticket fechado por {interaction.user.name}")
    
    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Fechamento cancelado.", embed=None, view=None)

# ==================== COMANDOS ====================

@bot.tree.command(name='dashboard', description='Acesse o site oficial do ServerCreator Bot')
async def dashboard(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🌐 ServerCreator Dashboard',
        description='Acesse nosso site oficial para mais informações!',
        color=discord.Color.blurple(),
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name='🔗 Link do Site',
        value=f'[Clique aqui para acessar]({SITE_URL})',
        inline=False
    )
    
    embed.add_field(
        name='📋 O que você encontra no site:',
        value='• Termos de Serviço\n• Política de Privacidade\n• Informações detalhadas sobre o bot\n• Links de convite e suporte',
        inline=False
    )
    
    embed.set_thumbnail(url='https://i.imgur.com/6fVO3QX.png')
    embed.set_footer(text='ServerCreator Bot • Desenvolvido por Aeth 🜲 ༝ TMZ')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='setupserver', description='Configura o servidor atual com um tema completo')
@app_commands.describe(tema='Escolha o tema do servidor')
@app_commands.choices(tema=[
    app_commands.Choice(name=f'🎲 RPG', value='rpg'),
    app_commands.Choice(name=f'🛒 Loja/E-commerce', value='loja'),
    app_commands.Choice(name=f'🌐 Comunidade', value='comunidade'),
    app_commands.Choice(name=f'🎮 Jogos/Gaming', value='jogos'),
    app_commands.Choice(name=f'📚 Estudos', value='estudo'),
    app_commands.Choice(name=f'🍥 Anime/Otaku', value='anime'),
])
async def setup_server(interaction: discord.Interaction, tema: app_commands.Choice[str]):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            '❌ Você precisa ser administrador para usar este comando!', 
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    template = bot.templates.get(tema.value)
    if not template:
        await interaction.followup.send('❌ Tema não encontrado!', ephemeral=True)
        return
    
    guild = interaction.guild
    
    try:
        await configure_guild(guild, template, interaction.user)
        
        embed = discord.Embed(
            title=f'{template["icon"]} Servidor Configurado com Sucesso!',
            description=f'O servidor **{guild.name}** foi configurado com o tema **{tema.name}**',
            color=template['color'],
            timestamp=datetime.now()
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
        embed.add_field(
            name='✨ Próximos Passos',
            value='Personalize as permissões e aproveite seu novo servidor!',
            inline=False
        )
        embed.set_footer(text=f'Configurado por {interaction.user}', icon_url=interaction.user.display_avatar.url)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.followup.send(
            '❌ Erro: O bot precisa de permissão de Administrador!',
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f'❌ Erro: {str(e)}', ephemeral=True)

async def configure_guild(guild: discord.Guild, template: dict, admin_user: discord.User):
    """Configura um servidor existente com base no template"""
    
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
            reason='Configuração automática do ServerCreator Bot'
        )
        roles_map[role_name] = role
        await asyncio.sleep(0.5)
    
    # 2. Promover admin ao cargo principal
    member = guild.get_member(admin_user.id)
    if member:
        admin_role = roles_map.get(template['roles'][0][0])
        if admin_role and admin_role not in member.roles:
            await member.add_roles(admin_role, reason='Administrador do servidor')
    
    # 3. Criar categorias
    cat_info = await guild.create_category('📋 INFORMAÇÕES', reason='Configuração automática')
    cat_chat = await guild.create_category('💬 CHATS', reason='Configuração automática')
    cat_extra = await guild.create_category('🎯 ESPECIALIZADOS', reason='Configuração automática')
    cat_voz = await guild.create_category('🔊 CANAIS DE VOZ', reason='Configuração automática')
    await asyncio.sleep(1)
    
    # 4. Criar canais de texto
    welcome_channel = None
    rules_channel = None
    
    texto_channels = template['channels']['texto']
    info_channels = texto_channels[:3]
    chat_channels = texto_channels[3:13]
    extra_channels = texto_channels[13:]
    
    for channel_name, topic in info_channels:
        channel = await guild.create_text_channel(
            name=channel_name,
            category=cat_info,
            topic=topic,
            reason='Configuração automática'
        )
        if 'boas-vindas' in channel_name or 'bem-vindo' in channel_name:
            welcome_channel = channel
        elif 'regras' in channel_name:
            rules_channel = channel
        await asyncio.sleep(0.5)
    
    for channel_name, topic in chat_channels:
        await guild.create_text_channel(
            name=channel_name,
            category=cat_chat,
            topic=topic,
            reason='Configuração automática'
        )
        await asyncio.sleep(0.5)
    
    for channel_name, topic in extra_channels:
        await guild.create_text_channel(
            name=channel_name,
            category=cat_extra,
            topic=topic,
            reason='Configuração automática'
        )
        await asyncio.sleep(0.5)
    
    # 5. Criar canais de voz
    for channel_name, user_limit in template['channels']['voz']:
        await guild.create_voice_channel(
            name=channel_name,
            category=cat_voz,
            user_limit=user_limit,
            reason='Configuração automática'
        )
        await asyncio.sleep(0.5)
    
    # 6. Configurar mensagens de boas-vindas
    if welcome_channel:
        embed = discord.Embed(
            title=f'{template["icon"]} Bem-vindo ao {guild.name}!',
            description=template['description'],
            color=template['color']
        )
        if template.get('welcome_image'):
            embed.set_image(url=template['welcome_image'])
        embed.set_footer(text='Configuração automática do ServerCreator Bot')
        
        await welcome_channel.send(embed=embed)
    
    # 7. Configurar regras
    if rules_channel:
        rules_embed = discord.Embed(
            title='📜 Regras do Servidor',
            description='Leia atentamente as regras para manter a harmonia!',
            color=template['color']
        )
        rules = [
            ('1. Respeito', 'Respeite todos os membros independente de opinião, raça, gênero ou crença.'),
            ('2. Conteúdo Apropriado', 'Proibido conteúdo NSFW, gore ou qualquer material ofensivo.'),
            ('3. Spam', 'Não faça spam ou flood nos canais.'),
            ('4. Divulgação', 'Divulgação apenas nos canais permitidos.'),
            ('5. Regras Específicas', 'Siga as diretrizes de cada canal e tema.'),
        ]
        for title, desc in rules:
            rules_embed.add_field(name=title, value=desc, inline=False)
        
        await rules_channel.send(embed=rules_embed)

# ==================== COMANDO SUPORTE CORRIGIDO ====================

@bot.tree.command(name='setupsuporte', description='[TEMPORÁRIO] Configura o servidor atual como servidor de suporte oficial')
async def setup_suporte(interaction: discord.Interaction):
    """Configura o servidor ATUAL como servidor de suporte (não cria novo)"""
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            '❌ Apenas administradores podem usar este comando!', 
            ephemeral=True
        )
        return
    
    # Verificar se é o servidor correto (opcional - pode remover)
    await interaction.response.defer(ephemeral=True)
    
    # Aviso temporário
    warning_embed = discord.Embed(
        title="⚠️ Comando Temporário",
        description="Este comando configura o servidor ATUAL como servidor de suporte oficial.\n\n**Atenção:** Todos os canais e cargos existentes serão mantidos, mas o bot vai adicionar os canais e cargos do tema de suporte.",
        color=discord.Color.orange()
    )
    warning_embed.add_field(
        name="📋 O que será criado:",
        value="• 24 canais de texto\n• 10 canais de voz\n• 22 cargos\n• Sistema de tickets com dropdown\n• Canais de Termos, Privacidade, Site e FAQ\n• Sistema de Sugestões Avançado",
        inline=False
    )
    warning_embed.add_field(
        name="⏰ Remoção",
        value="Este comando será desativado em breve!",
        inline=False
    )
    
    # Criar view de confirmação
    class ConfirmSetupView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
        
        @discord.ui.button(label="✅ Confirmar Configuração", style=discord.ButtonStyle.green)
        async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
            await button_interaction.response.defer(ephemeral=True)
            
            guild = button_interaction.guild
            template = bot.templates['suporte']
            
            try:
                # Configurar servidor de suporte
                await configure_support_guild(guild, template, button_interaction.user)
                
                success_embed = discord.Embed(
                    title="🎫 Servidor de Suporte Configurado!",
                    description=f"O servidor **{guild.name}** agora está configurado como servidor de suporte oficial!",
                    color=discord.Color.green()
                )
                success_embed.add_field(
                    name="✅ Criado com sucesso:",
                    value="• Canais de Termos, Privacidade, Site e FAQ\n• Sistema de Tickets com dropdown\n• 22 cargos de suporte\n• Canais de voz e texto organizados\n• Sistema de Sugestões com botão e modal\n• Canais de Sugestões Aceitas/Recusadas",
                    inline=False
                )
                success_embed.add_field(
                    name="🎫 Sistema de Tickets",
                    value="O canal 🎫┃criar-ticket já está funcionando com dropdown!",
                    inline=False
                )
                success_embed.add_field(
                    name="💡 Sistema de Sugestões",
                    value="O canal 💌┃enviar-sugestão está pronto com botão azul!\nAs sugestões vão para 💡┃sugestões com reações.",
                    inline=False
                )
                success_embed.set_footer(text="ServerCreator Suporte • Aeth 🜲 ༝ TMZ")
                
                await button_interaction.followup.send(embed=success_embed, ephemeral=True)
                
                # Desabilitar botões
                for child in self.children:
                    child.disabled = True
                await interaction.edit_original_response(view=self)
                
            except Exception as e:
                await button_interaction.followup.send(f"❌ Erro: {str(e)}", ephemeral=True)
        
        @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red)
        async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
            await button_interaction.response.send_message("❌ Configuração cancelada.", ephemeral=True)
            for child in self.children:
                child.disabled = True
            await interaction.edit_original_response(view=self)
    
    view = ConfirmSetupView()
    await interaction.followup.send(embed=warning_embed, view=view, ephemeral=True)

async def configure_support_guild(guild: discord.Guild, template: dict, admin_user: discord.User):
    """Configura servidor de suporte com conteúdo específico"""
    
    # 1. Criar cargos (se não existirem)
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
    
    # Promover admin ao cargo Fundador
    member = guild.get_member(admin_user.id)
    if member:
        admin_role = roles_map.get('👑 Fundador')
        if admin_role and admin_role not in member.roles:
            await member.add_roles(admin_role, reason='Fundador do servidor de suporte')
    
    # 2. Criar categorias
    cat_info = await guild.create_category('📋 INFORMAÇÕES', reason='Configuração suporte')
    cat_legal = await guild.create_category('⚖️ LEGAL', reason='Configuração suporte')
    cat_suporte = await guild.create_category('🎫 SUPORTE', reason='Configuração suporte')
    cat_comunidade = await guild.create_category('💬 COMUNIDADE', reason='Configuração suporte')
    cat_voz = await guild.create_category('🔊 VOZ', reason='Configuração suporte')
    cat_staff = await guild.create_category('🔒 STAFF ONLY', reason='Configuração suporte')
    cat_sugestoes = await guild.create_category('💡 SUGESTÕES', reason='Configuração suporte')
    
    await asyncio.sleep(1)
    
    # 3. Criar canais com conteúdo específico
    
    # Canal de Termos
    termos_channel = await guild.create_text_channel(
        '📜┃termos-serviço',
        category=cat_legal,
        topic='Termos de Serviço do ServerCreator Bot'
    )
    
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
        ("👥 Posso sugerir novos temas?", "Sim! Use o canal 💌┃enviar-sugestão ou abra um ticket."),
        ("🐛 Encontrei um bug, e agora?", "Abra um ticket em 🎫┃criar-ticket selecionando 'Reportar Bug'."),
        ("🤝 Como faço parceria?", "Abra um ticket do tipo 'Parceria' e descreva sua proposta."),
        ("⚡ O bot está offline?", "Verifique 🔧┃status-bot ou aguarde reinicialização."),
        ("🗑️ Como limpo o servidor?", "Use o comando `/limparserver` (apenas admins)."),
    ]
    
    for pergunta, resposta in faqs:
        faq_embed.add_field(name=pergunta, value=resposta, inline=False)
    
    faq_embed.set_footer(text="Dúvidas? Abra um ticket em 🎫┃criar-ticket")
    await faq_channel.send(embed=faq_embed)
    
    # Canal de Criar Ticket (com dropdown funcional)
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
    
    # Enviar com o dropdown de tickets
    view = TicketView()
    await ticket_channel.send(embed=ticket_embed, view=view)
    
    # NOVOS CANAIS - Sistema de Sugestões Avançado
    
    # Canal Enviar Sugestão (com botão)
    send_suggestion_channel = await guild.create_text_channel(
        '💌┃enviar-sugestão',
        category=cat_sugestoes,
        topic='Clique no botão abaixo para enviar sua sugestão'
    )
    
    # Configurar permissões - apenas visualização e reações
    await send_suggestion_channel.set_permissions(
        guild.default_role,
        send_messages=False,
        add_reactions=True,
        read_messages=True,
        read_message_history=True
    )
    
    suggestion_embed = discord.Embed(
        title="💡 Envie sua Sugestão",
        description="Tem uma ideia para melhorar o bot ou o servidor?\nClique no botão azul abaixo para enviar sua sugestão!",
        color=discord.Color.blurple()
    )
    suggestion_embed.add_field(
        name="📋 Como funciona:",
        value="1. Clique no botão '💡 Enviar Sugestão'\n2. Preencha seu nick e a sugestão\n3. Aguarde a avaliação da equipe\n4. Receba feedback via DM!",
        inline=False
    )
    suggestion_embed.add_field(
        name="⚠️ Regras:",
        value="• Seja respeitoso e construtivo\n• Uma sugestão a cada 5 minutos\n• Sugestões inapropriadas serão ignoradas",
        inline=False
    )
    suggestion_embed.set_thumbnail(url='https://i.imgur.com/6fVO3QX.png')
    suggestion_embed.set_footer(text='ServerCreator Suporte • Sua opinião é importante!')
    
    # Enviar com botão
    suggestion_view = SuggestionButtonView()
    await send_suggestion_channel.send(embed=suggestion_embed, view=suggestion_view)
    
    # Canal Sugestões (onde aparecem as sugestões enviadas)
    suggestions_channel = await guild.create_text_channel(
        '💡┃sugestões',
        category=cat_sugestoes,
        topic='Sugestões enviadas pelos membros'
    )
    
    # Configurar permissões - apenas visualização e reações
    await suggestions_channel.set_permissions(
        guild.default_role,
        send_messages=False,
        add_reactions=True,
        read_messages=True,
        read_message_history=True
    )
    
    # Canal Sugestões Aceitas
    accepted_channel = await guild.create_text_channel(
        '✅┃sugestões-aceitas',
        category=cat_sugestoes,
        topic='Sugestões que foram implementadas ou aprovadas'
    )
    
    await accepted_channel.set_permissions(
        guild.default_role,
        send_messages=False,
        add_reactions=True,
        read_messages=True,
        read_message_history=True
    )
    
    # Canal Sugestões Recusadas
    rejected_channel = await guild.create_text_channel(
        '❌┃sugestões-recusadas',
        category=cat_sugestoes,
        topic='Sugestões que não foram aprovadas'
    )
    
    await rejected_channel.set_permissions(
        guild.default_role,
        send_messages=False,
        add_reactions=True,
        read_messages=True,
        read_message_history=True
    )
    
    # Canal de Votações (com permissão de reação)
    votacoes_channel = await guild.create_text_channel(
        '📢┃votações',
        category=cat_comunidade,
        topic='Participe das votações da comunidade'
    )
    
    await votacoes_channel.set_permissions(
        guild.default_role,
        send_messages=False,
        add_reactions=True,
        read_messages=True,
        read_message_history=True
    )
    
    # Enviar mensagem inicial no canal de votações
    votacoes_embed = discord.Embed(
        title="📢 Canal de Votações",
        description="Aqui serão postadas enquetes e votações importantes para a comunidade!",
        color=discord.Color.gold()
    )
    votacoes_embed.add_field(
        name="🗳️ Como participar:",
        value="Reaja com os emojis disponíveis em cada votação para expressar sua opinião!",
        inline=False
    )
    await votacoes_channel.send(embed=votacoes_embed)
    
    # Outros canais básicos
    outros_canais = [
        ('📢┃anúncios', cat_info, 'Anúncios oficiais'),
        ('🎉┃novidades', cat_info, 'Novidades do bot'),
        ('🐛┃bugs', cat_comunidade, 'Reporte de bugs'),
        ('💬┃geral', cat_comunidade, 'Chat geral'),
        ('🎨┃showcase', cat_comunidade, 'Mostre seus servidores'),
        ('🤝┃parcerias', cat_comunidade, 'Propostas de parceria'),
        ('📊┃estatísticas', cat_info, 'Stats do bot'),
        ('🔧┃status-bot', cat_info, 'Status em tempo real'),
        ('📖┃guias', cat_info, 'Tutoriais e guias'),
        ('🎁┃sorteios', cat_comunidade, 'Eventos e premiações'),
        ('👋┃boas-vindas', cat_info, 'Mensagens de boas-vindas'),
        ('📋┃regras', cat_info, 'Regras do servidor'),
        ('🤖┃comandos', cat_info, 'Lista de comandos do bot'),
        ('📝┃changelog', cat_info, 'Histórico de atualizações'),
        ('💻┃desenvolvimento', cat_staff, 'Avisos de dev'),
        ('🎯┃metas', cat_comunidade, 'Metas da comunidade'),
        ('🏆┃destaques', cat_comunidade, 'Membros em destaque'),
    ]
    
    for nome, categoria, topico in outros_canais:
        ch = await guild.create_text_channel(nome, category=categoria, topic=topico)
        
        # Configurar canais de informações como somente leitura para @everyone
        if any(x in nome for x in ['📢┃anúncios', '📜┃termos', '🔒┃política', '🌐┃site', '❓┃faq', '📋┃regras', '🤖┃comandos', '📝┃changelog', '📊┃estatísticas', '🔧┃status']):
            await ch.set_permissions(
                guild.default_role,
                send_messages=False,
                add_reactions=True,
                read_messages=True,
                read_message_history=True
            )
        
        await asyncio.sleep(0.5)
    
    # Canais de voz
    for channel_name, user_limit in template['channels']['voz']:
        await guild.create_voice_channel(
            name=channel_name,
            category=cat_voz if 'Staff' not in channel_name else cat_staff,
            user_limit=user_limit
        )
        await asyncio.sleep(0.5)

@bot.tree.command(name='temas', description='Lista todos os temas disponíveis')
async def list_themes(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🎨 Temas Disponíveis',
        description='Escolha um tema ao usar `/setupserver`',
        color=discord.Color.blue()
    )
    
    for key, template in bot.templates.items():
        if key == 'suporte':
            continue
        embed.add_field(
            name=f'{template["icon"]} {key.title()}',
            value=f'{template["description"]}\nCanais: {len(template["channels"]["texto"])} texto + {len(template["channels"]["voz"])} voz\nCargos: {len(template["roles"])}',
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='limparserver', description='Limpa todos os canais e cargos do servidor (CUIDADO!)')
@app_commands.describe(confirmar='Digite "SIM" para confirmar')
async def clear_server(interaction: discord.Interaction, confirmar: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Apenas administradores!', ephemeral=True)
        return
    
    if confirmar.upper() != 'SIM':
        await interaction.response.send_message(
            '❌ Para confirmar, digite "SIM" no campo confirmar', 
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    
    try:
        for channel in guild.channels:
            try:
                await channel.delete(reason='Limpeza do servidor')
                await asyncio.sleep(0.5)
            except:
                pass
        
        for role in guild.roles:
            if role.name != '@everyone' and not role.managed:
                try:
                    await role.delete(reason='Limpeza do servidor')
                    await asyncio.sleep(0.5)
                except:
                    pass
        
        await interaction.followup.send('✅ Servidor limpo com sucesso!', ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f'❌ Erro: {str(e)}', ephemeral=True)

@bot.tree.command(name='addemoji', description='Adiciona emojis personalizados (Admin)')
@app_commands.describe(imagem='Imagem do emoji (PNG/JPG)', nome='Nome do emoji')
async def add_emoji(interaction: discord.Interaction, imagem: discord.Attachment, nome: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Apenas administradores!', ephemeral=True)
        return
    
    if not imagem.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await interaction.response.send_message('❌ Formato inválido!', ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        image_data = await imagem.read()
        emoji = await interaction.guild.create_custom_emoji(name=nome, image=image_data)
        await interaction.followup.send(f'✅ Emoji :{nome}: adicionado!', ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f'❌ Erro: {str(e)}', ephemeral=True)

@bot.tree.command(name='ajuda', description='Mostra todos os comandos')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🤖 ServerCreator Bot',
        description='Bot profissional para configuração de servidores',
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name='🛠️ Configuração',
        value='`/setupserver (tema)` - Configura o servidor atual\n`/temas` - Lista temas disponíveis\n`/limparserver` - Limpa o servidor (CUIDADO!)',
        inline=False
    )
    
    embed.add_field(
        name='🌐 Site & Informações',
        value='`/dashboard` - Acessa o site oficial\nPalavras-chave: digite "site" em qualquer canal',
        inline=False
    )
    
    embed.add_field(
        name='⚙️ Utilitários',
        value='`/addemoji (imagem) (nome)` - Adiciona emoji\n`/ajuda` - Este menu',
        inline=False
    )
    
    embed.add_field(
        name='📝 Como Usar',
        value='1. Crie um servidor manualmente no Discord\n2. Adicione este bot ao servidor\n3. Use `/setupserver` e escolha o tema\n4. Pronto!',
        inline=False
    )
    
    embed.set_footer(text='Desenvolvido por Aeth 🜲 ༝ TMZ')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ==================== EVENTOS ====================

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if not message.guild:
        return
    
    content_lower = message.content.lower()
    
    for keyword in bot.site_keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, content_lower):
            embed = discord.Embed(
                title='🌐 Você mencionou o site!',
                description='Parece que você está procurando informações sobre o ServerCreator.',
                color=discord.Color.blurple()
            )
            
            embed.add_field(
                name='🔗 Acesse nosso site oficial:',
                value=f'**[Clique aqui]({SITE_URL})**\n\nOu use o comando `/dashboard`',
                inline=False
            )
            
            embed.add_field(
                name='📋 No site você encontra:',
                value='• Termos de Serviço\n• Política de Privacidade\n• Detalhes sobre todos os temas\n• Informações do desenvolvedor',
                inline=False
            )
            
            embed.set_thumbnail(url='https://i.imgur.com/6fVO3QX.png')
            embed.set_footer(text='ServerCreator Bot • Aeth 🜲 ༝ TMZ')
            
            await message.reply(embed=embed, mention_author=False)
            break
    
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    guild = member.guild
    
    welcome_channel = None
    for channel in guild.text_channels:
        if 'bem-vindo' in channel.name or 'boas-vindas' in channel.name:
            welcome_channel = channel
            break
    
    if not welcome_channel:
        return
    
    template = None
    for t_name, t_data in bot.templates.items():
        main_role_name = t_data['roles'][0][0]
        if discord.utils.get(guild.roles, name=main_role_name):
            template = t_data
            break
    
    if template:
        embed = discord.Embed(
            title=f'{template["icon"]} Novo Membro!',
            description=template['welcome_message'].format(member=member.mention),
            color=template['color'],
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        if template.get('welcome_image'):
            embed.set_image(url=template['welcome_image'])
        embed.set_footer(text=f'ID: {member.id}')
        
        await welcome_channel.send(embed=embed)
        
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
    guild = member.guild
    
    channel = None
    for ch in guild.text_channels:
        if 'bem-vindo' in ch.name or 'boas-vindas' in ch.name or 'logs' in ch.name:
            channel = ch
            break
    
    if not channel:
        return
    
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

# ID do dono do bot (substitua pelo seu ID do Discord)
ADMIN_USER_ID = 123456789012345678  # <-- SUBSTITUA PELO SEU ID DO DISCORD

# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERRO: Token não encontrado! Verifique seu arquivo .env")
    else:
        bot.run(TOKEN)
