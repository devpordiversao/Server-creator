# main.py - CORRIGIDO: Bot configura servidor existente (não cria)
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
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

@bot.tree.command(name='setupserver', description='Configura o servidor atual com um tema completo')
@app_commands.describe(
    tema='Escolha o tema do servidor'
)
@app_commands.choices(tema=[
    app_commands.Choice(name=f'🎲 RPG', value='rpg'),
    app_commands.Choice(name=f'🛒 Loja/E-commerce', value='loja'),
    app_commands.Choice(name=f'🌐 Comunidade', value='comunidade'),
    app_commands.Choice(name=f'🎮 Jogos/Gaming', value='jogos'),
    app_commands.Choice(name=f'📚 Estudos', value='estudo'),
    app_commands.Choice(name=f'🍥 Anime/Otaku', value='anime'),
])
async def setup_server(
    interaction: discord.Interaction,
    tema: app_commands.Choice[str]
):
    # Verificar permissões
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
        # Configurar servidor existente
        await configure_guild(guild, template, interaction.user)
        
        # Embed de sucesso
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
        # Verificar se cargo já existe
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
    cat_info = await guild.create_category(
        '📋 INFORMAÇÕES',
        reason='Configuração automática'
    )
    cat_chat = await guild.create_category(
        '💬 CHATS',
        reason='Configuração automática'
    )
    cat_extra = await guild.create_category(
        '🎯 ESPECIALIZADOS',
        reason='Configuração automática'
    )
    cat_voz = await guild.create_category(
        '🔊 CANAIS DE VOZ',
        reason='Configuração automática'
    )
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

@bot.event
async def on_member_join(member):
    """Sistema automático de boas-vindas"""
    guild = member.guild
    
    # Procurar canal de boas-vindas
    welcome_channel = None
    for channel in guild.text_channels:
        if 'bem-vindo' in channel.name or 'boas-vindas' in channel.name:
            welcome_channel = channel
            break
    
    if not welcome_channel:
        return
    
    # Detectar tema pelo cargo principal
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
        
        # Enviar DM
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
    
    # Procurar canal
    channel = None
    for ch in guild.text_channels:
        if 'bem-vindo' in ch.name or 'boas-vindas' in ch.name or 'logs' in ch.name:
            channel = ch
            break
    
    if not channel:
        return
    
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

@bot.tree.command(name='temas', description='Lista todos os temas disponíveis')
async def list_themes(interaction: discord.Interaction):
    embed = discord.Embed(
        title='🎨 Temas Disponíveis',
        description='Escolha um tema ao usar `/setupserver`',
        color=discord.Color.blue()
    )
    
    for key, template in bot.templates.items():
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
        # Deletar canais
        for channel in guild.channels:
            try:
                await channel.delete(reason='Limpeza do servidor')
                await asyncio.sleep(0.5)
            except:
                pass
        
        # Deletar cargos (exceto @everyone e cargos do bot)
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
@app_commands.describe(
    imagem='Imagem do emoji (PNG/JPG)',
    nome='Nome do emoji'
)
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
        name='⚙️ Utilitários',
        value='`/addemoji (imagem) (nome)` - Adiciona emoji\n`/ajuda` - Este menu',
        inline=False
    )
    
    embed.add_field(
        name='📝 Como Usar',
        value='1. Crie um servidor manualmente no Discord\n2. Adicione este bot ao servidor\n3. Use `/setupserver` e escolha o tema\n4. Pronto!',
        inline=False
    )
    
    embed.set_footer(text='Desenvolvido com 💜')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print("❌ ERRO: Token não encontrado! Verifique seu arquivo .env")
    else:
        bot.run(TOKEN)
