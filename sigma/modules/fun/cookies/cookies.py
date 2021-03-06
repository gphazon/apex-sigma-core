# Apex Sigma: The Database Giant Discord Bot.
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


async def cookies(cmd: SigmaCommand, message: discord.Message, args: list):
    target = message.author if not message.mentions else message.mentions[0]
    cookie_file = await cmd.db[cmd.db.db_nam].Cookies.find_one({'UserID': target.id}) or {}
    cookie_count = cookie_file.get('Cookies') or 0
    cookie_total = cookie_file.get('Total') or 0
    ender = 'cookie' if cookie_count == 1 else 'cookies'
    title = f'🍪 {target.display_name} got {cookie_count} {ender} this month '
    title += f'and has {cookie_total} in total.'
    response = discord.Embed(color=0xd99e82, title=title)
    await message.channel.send(embed=response)
