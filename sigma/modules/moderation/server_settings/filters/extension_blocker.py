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
import arrow
import discord

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.modules.moderation.warning.issuewarning import warning_data


async def extension_blocker(ev: SigmaEvent, msg: discord.Message):
    if msg.attachments:
        att_files = [att.filename.lower() for att in msg.attachments]
        bexts = await ev.db.get_guild_settings(msg.guild.id, 'BlockedExtensions') or []
        delete = False
        reason = None
        for attf in att_files:
            for bext in bexts:
                if attf.endswith(bext):
                    delete = True
                    reason = bext
                    break
            if delete:
                break
        if delete:
            try:
                filter_warn = await ev.db.get_guild_settings(msg.guild.id, 'FilterAutoWarn')
                if filter_warn:
                    warn_data = warning_data(msg.guild.me, msg.author, f'Said "{reason}".')
                    await ev.db[ev.db.db_cfg.database].Warnings.insert_one(warn_data)
                await msg.delete()
                title = f'🔥 Your upload was deleted for containing a "{reason}" file.'
                to_author = discord.Embed(color=0xFFCC4D, title=title)
                try:
                    await msg.author.send(embed=to_author)
                except discord.Forbidden:
                    pass
                author = f'{msg.author.name}#{msg.author.discriminator}'
                title = f'I deleted {author}\'s upload for having a `{reason}`.'
                log_embed = discord.Embed(color=0xFFCC4D, timestamp=arrow.utcnow().datetime)
                log_embed.description = f'Content: {msg.content}'
                log_embed.set_author(name=title, icon_url=user_avatar(msg.author))
                log_embed.set_footer(text=f'Channel: #{msg.channel.name} [{msg.channel.id}]')
                await log_event(ev.bot, msg.guild, ev.db, log_embed, 'LogFilters')
            except discord.ClientException:
                pass