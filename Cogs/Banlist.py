from discord.ext.commands import Cog
from discord.app_commands import command
from discord import Guild, User, Member, Interaction, errors, Embed

from xbox.webapi.api.provider.profile.models import ProfileResponse
from xbox.webapi.api.provider.people.models import PeopleResponse

from Utils.embed_functions import create_embed, set_embed_attr
from Utils.command_decorators import app_command_requires_role_of_perm_tiers


from Utils.database_helpers import *

from Utils import DatabaseConnectionFail, XboxApiWrapperError

from Views import VerifyView

from typing import Literal, Dict, Tuple

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MyBot # Only imported for type hints



class BanlistLogger:
    @staticmethod
    async def _log_banlist_check(guild: Guild, banlist_log_id: int, user: User, args, failed: bool = False):
        banlist_log = guild.get_channel(banlist_log_id)


        embed = create_embed(
            description = f'**Staff Member:** {user.mention}\n**Used Command:** `user-check` for:\n{args}'
        )

        if failed:
            embed.description += '\n\n❌ However, an error occurred!'
        
        await banlist_log.send(embed = embed)

    @staticmethod
    async def _log_banlist_case(guild: Guild, banlist_log_id: int, user: User, case: int, failed: bool = False):
        banlist_log = guild.get_channel(banlist_log_id)

        embed = create_embed(
            description = f'**Staff Member:** {user.mention}\n**Used Command:** `banlist-case` for case {case}'
        )

        if failed:
            embed.description += '\n\n❌ However, an error occurred!'
        
        await banlist_log.send(embed = embed)
    
    @staticmethod
    async def _log_banlist_add(guild: Guild, banlist_log_id: int, user: User, args, failed: bool = False):
        banlist_log = guild.get_channel(banlist_log_id)

        embed = create_embed(
            description = f'**Staff Member:** {user.mention}\n**Used Command:** `banlist-add` for:\n{args}'
        )

        if failed:
            embed.description += '\n\n❌ However, an error occurred!'

        await banlist_log.send(embed = embed)
    
    @staticmethod
    async def _log_banlist_delete(guild: Guild, banlist_log_id: int, user: User, case: int, failed: bool = False):
        banlist_log = guild.get_channel(banlist_log_id)

        embed = create_embed(
            description = f'**Staff Member:** {user.mention}\n**Used Command:** `banlist-delete` for case {case}'
        )

        if failed:
            embed.description += '\n\n❌ However, an error occurred!'

        await banlist_log.send(embed = embed)
    
    @staticmethod
    async def _log_banlist_lookup(guild: Guild, banlist_log_id: int, user: User, xbox: str, failed: bool = False):
        banlist_log = guild.get_channel(banlist_log_id)

        embed = create_embed(
            description = f'**Staff Member:** {user.mention}\n**Used Command:** `/lookup` for the xbox account: {xbox}'
        )

        if failed:
            embed.description += '\n\n❌ However, an error occurred!'

        await banlist_log.send(embed = embed)



class BanList(Cog):
    def __init__(self, bot: 'MyBot'):
        self.bot = bot
        self.state = bot.state
        self.config = bot.config

    

    async def _get_friends_check_embed_info(self, xbox: str) -> Tuple[str, int, Literal['clean', 'banned', 'error', 'other']]:
        friends_check_status = ''

        try:
            xbox_profile: ProfileResponse = await self.state.xbox_wrapper.get_xbox_profile_by_gamertag(xbox_gamertag = xbox)
        
        except XboxApiWrapperError as e:
            description = e.message
            colour = 0xf8d146
            friends_check_status = 'error'

            return description, colour, friends_check_status
        
        
        xuid = xbox_profile.profile_users[0].id
        
        try:
            xbox_friends: PeopleResponse = await self.state.xbox_wrapper.get_xbox_friends_by_xuid(xuid = xuid)
        
        except XboxApiWrapperError as e:
            description = e.message
            colour = 0xf8d146
            friends_check_status = 'error'

            return description, colour, friends_check_status
        
    
        if not xbox_friends or not xbox_friends.people:
            description = f'⚠️ {xbox} has no xbox friends.'
            colour = 0xff0000
            friends_check_status = 'other'

            return description, colour, friends_check_status
        
                     
        friends_gamertags = [friend.modern_gamertag for friend in xbox_friends.people]

        friend_ban_cases = check_friends_by_xbox_name(friends_gamertags = friends_gamertags)

        if not friend_ban_cases:
            description = f'✅ {xbox} has no banned xbox friends'
            colour = 0x00ff00
            friends_check_status = 'clean'

            return description, colour, friends_check_status


        grouped_banned_friends = {}

        for case in friend_ban_cases:
            xbox_gamertag = case[2]
            case_id = case[4]

            grouped_banned_friends.setdefault(xbox_gamertag, []).append(case_id)
        
        description, colour = self._create_banned_friends_embed_attrs(grouped_banned_friends = grouped_banned_friends, xbox = xbox)
        friends_check_status = 'banned'

        return description, colour, friends_check_status
    
    def _create_banned_user_embed(self, user: User, xbox:str, discord_ban_cases, xbox_ban_cases) -> Tuple[Embed, bool]:
        banned = False

        description = ''
        
        if not discord_ban_cases:
            description += f'✅ {user.mention} is not on the banlist\n'
        
        else:
            banned = True

            description += f'❌ {user.mention} is on the banlist\n'
            
            for ban in discord_ban_cases:
                case_id = ban[4]

                description += f'Case Id: {case_id}\n'

        if not xbox_ban_cases:
            description += f'\n✅ {xbox} is not on the banlist'

        else:
            banned = True

            description += f'\n❌ {xbox} is on the banlist\n'

            for case in xbox_ban_cases:
                case_id = case[4]

                description += f'Case Id: {case_id}\n'

        if banned:
            colour = 0xff0000
        
        else:
            colour = 0x00ff00
        
        check_embed = create_embed(
            title = 'Banlist Check',
            description = f'{description}',
            colour = colour
        )

        return check_embed, banned
    
    def _create_banned_friends_embed_attrs(self, grouped_banned_friends: Dict, xbox: str) -> Tuple[str, int]:
        description = f'{len(grouped_banned_friends)} of {xbox}\'s friends are on the banlist\n'

        for xbox_gamertag, case_ids in grouped_banned_friends.items():
            description += f'❌ {xbox_gamertag} is on the banlist\n'

            for case_id in case_ids:
                description += f'Case Id: {case_id}\n'
        
        colour = 0xff0000

        return description, colour


    @command(name = 'user-check', description = 'Staff Only | Checks a user against the banlist')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def check(self, interaction: Interaction, user: Member = None, xbox: str = None):
        if not user and not xbox:
            await interaction.response.send_message('❌ You need to provide at least one account: xbox or discord')
            return
        
        await interaction.response.defer(ephemeral = True)

        args = f'Discord User: {user.mention}\n' if user else ''
        args += f'Xbox Gamertag: {xbox}' if xbox else ''

        ban_cases: Dict = check_if_banned(discord_id = user.id, xbox_gamertag = xbox)
        discord_ban_cases = ban_cases.get('discord', None)
        xbox_ban_cases = ban_cases.get('xbox', None)

        check_embed, banned = self._create_banned_user_embed(user = user, xbox = xbox, discord_ban_cases = discord_ban_cases, xbox_ban_cases = xbox_ban_cases)
    
        embeds = []
        embeds.append(check_embed)

        if xbox:
            description, colour, friends_check_status = await self._get_friends_check_embed_info(xbox = xbox)

            friends_check_embed = create_embed(
                title = f'Xbox friends Check',
                description = description,
                colour = colour
            )
            embeds.append(friends_check_embed)


        await interaction.followup.send(embeds = embeds)


        staff_verified_role = interaction.guild.get_role(self.config.roles.staff_verified)

        if not banned and friends_check_status == 'clean':
            
            if staff_verified_role not in user.roles:
                await user.add_roles(staff_verified_role)
                    
        elif not banned and friends_check_status != 'banned':
            view = VerifyView()

            await interaction.followup.send(view = view, ephemeral = True)
            await view.wait()

            if view.verified and staff_verified_role not in user.roles:
                await user.add_roles(staff_verified_role)

            elif not view.verified and staff_verified_role in user.roles:
                await user.remove_roles(staff_verified_role)
                
        elif banned and staff_verified_role in user.roles:
            await user.remove_roles(staff_verified_role)

        
        await BanlistLogger._log_banlist_check(
            guild = interaction.guild,
            banlist_log_id = self.config.channels.logs.banlist,
            user = interaction.user,
            args = args
        )
    
    
    @command(name = 'banlist-case', description = 'Staff Only | Shows the information about a specific ban case')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def case(self, interaction: Interaction, case: int):
        failed = False

        try:
            ban_case = get_bans_by_case_number(case)
        
        except DatabaseConnectionFail as e:
            await interaction.response.send_message(e.message, ephemeral = True)
            failed = True
        
        else:
            if not ban_case:
                await interaction.response.send_message(f'❌ There is no ban case with id {case}', ephemeral = True)
                return
            
            discord_name, discord_id, xbox, reason, *_ = ban_case
            embed = create_embed(
                title = f'ban Id {case}',
                description = f'**Discord Name:** {discord_name}\n**Discord Id:** {discord_id}\n**Xbox:** {xbox}\n**Reason:** {reason}',
                colour = 0xff0000
            )

            await interaction.response.send_message(embed = embed, ephemeral = True)

        finally:
            await BanlistLogger._log_banlist_case(
                guild = interaction.guild,
                banlist_log_id = self.config.channels.logs.banlist,
                user = interaction.user,
                case = case,
                failed = failed
            )
    
    
    @command(name = 'banlist-add', description = 'Staff Only | Adds a ban entry to the banlist')
    @app_command_requires_role_of_perm_tiers(['tier_3','tier_4'])
    async def add(self, interaction: Interaction, member: Member = None, xbox: str = None, reason: str = None):
        failed = False

        if not member and not xbox:
            await interaction.response.send_message('❌ You need to provide at least one account: xbox or discord')
            return
        
        args = f'Discord User: {member.mention}\n' if member else ''
        args += f'Xbox Gamertag: {xbox}' if xbox else ''

        member_name = member.name if member else 'Not Recorded'
        member_id = member.id if member else 'Not Recorded'

        xbox_name = xbox if xbox else 'Not Recorded'

        try:
            add_ban(
                member_name = member_name,
                member_id = member_id,
                xbox_name = xbox_name,
                reason = reason
            )

        except DatabaseConnectionFail as e:
            await interaction.response.send_message(e.message, ephemeral = True)
            failed = True
        
        else:
            await interaction.response.send_message(f'✅ Success', ephemeral = True)
        
        finally:
            await BanlistLogger._log_banlist_add(
            guild = interaction.guild,
            banlist_log_id = self.config.channels.logs.banlist,
            user = interaction.user,
            args = args,
            failed = failed
        )
    

    @command(name = 'banlist-delete', description = 'Staff Only | Deletes a ban from the banlist')
    @app_command_requires_role_of_perm_tiers(['tier_3','tier_4'])
    async def delete(self, interaction: Interaction, case: int):
        failed = False
        
        try:
            delete_ban(
                case = case
            )
        
        except DatabaseConnectionFail as e:
            await interaction.response.send_message(e.message, ephemeral = True)
            failed = True
        
        else:
            await interaction.response.send_message(f'✅ Success', ephemeral = True)

        finally:
            await BanlistLogger._log_banlist_delete(
                guild = interaction.guild,
                banlist_log_id = self.config.channels.logs.banlist,
                user = interaction.user,
                case = case,
                failed = failed
            )
    

    @command(name = 'lookup', description = 'Staff Only | Shows deatiled information about a xbox account')
    @app_command_requires_role_of_perm_tiers(['tier_1'])
    async def lookup(self, interaction: Interaction, xbox: str):
        failed = False

        try:
            xbox_profile: ProfileResponse = await self.state.xbox_wrapper.get_xbox_profile_by_gamertag(xbox_gamertag = xbox)
        
        except XboxApiWrapperError as e:
            await interaction.response.send_message(e.message, ephemeral = True)
            failed = True
        
        else:
            xbox_user = xbox_profile.profile_users[0]

            xuid = xbox_user.id
            gamescore = xbox_user.settings[7].value
            profile_picture = xbox_user.settings[8].value
            reputation = xbox_user.settings[11].value
            
            embed = create_embed(
                description = f'Xbox Id: {xuid}\nGameScore: {gamescore}\nReputation: {reputation}'
            )
            embed = set_embed_attr(
                embed = embed,
                author = {
                    'name': xbox,
                    'icon': profile_picture
                }
            )            
    
            await interaction.response.send_message(embed = embed, ephemeral = True)

        finally:
            await BanlistLogger._log_banlist_lookup(
                guild = interaction.guild,
                banlist_log_id = self.config.channels.logs.banlist,
                user = interaction.user,
                xbox = xbox,
                failed = failed
            )
    

    
    async def cog_app_command_error(self, interaction: Interaction, error):
        if isinstance(error, errors.MissingAnyRole):
            await interaction.response.send_message('❌ You are missing a required role to run this command!', ephemeral = True)
        else:
            print(error)



async def setup(bot: 'MyBot'):
    await bot.add_cog(BanList(bot))