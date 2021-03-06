﻿# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied
from sigma.core.mechanics.permissions import scp_cache
from sigma.modules.moderation.permissions.nodes.permission_data import get_all_perms


async def enablemodule(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if not message.author.permissions_in(message.channel).manage_guild:
            response = permission_denied('Manage Server')
        else:
            mdl_name = args[0].lower()
            if mdl_name in cmd.bot.modules.categories:
                perms = await get_all_perms(cmd.db, message)
                disabled_modules = perms['DisabledModules']
                if mdl_name in disabled_modules:
                    disabled_modules.remove(mdl_name)
                    perms.update({'DisabledModules': disabled_modules})
                    await cmd.db[cmd.db.db_nam].Permissions.update_one(
                        {'ServerID': message.guild.id}, {'$set': perms})
                    scp_cache.del_cache(message.guild.id)
                    response = discord.Embed(color=0x77B255, title=f'✅ `{mdl_name.upper()}` enabled.')
                else:
                    response = discord.Embed(color=0xFFCC4D, title='⚠ Module not disabled.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Module not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
