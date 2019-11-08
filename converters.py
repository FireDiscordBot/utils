"""
converters
~~~~~~~~~~~~~~~~~~~~~

An extension to provide custom converters that ignore case or include a fallback to the Discord API if not in cache
"""

from discord import utils
from discord.ext.commands.converter import (
	MemberConverter,
	UserConverter,
	RoleConverter,
	TextChannelConverter,
	VoiceChannelConverter,
	CategoryChannelConverter
)
from discord.ext.commands import BadArgument

class Member(MemberConverter):
	"""
	Member Converter
	---------------------

	Converts to a :class:`~discord.Member`.

	All lookups are via the local guild. If in a DM context, then the lookup
	is done by the global cache.

	The lookup strategy is as follows (in order):
	1. Lookup by ID.
	2. Lookup by mention.
	3. Lookup by name#discrim
	4. Lookup by name
	5. Lookup by nickname
	"""
	async def convert(self, ctx, arg):
		if arg == '^':
			if not ctx.guild:
				raise BadArgument('The "this" operator, ^, can only be used in servers.')
			nextmsg = False
			async for m in ctx.channel.history(limit=5):
				if m.id == ctx.message.id:
					nextmsg = True
				elif nextmsg:
					return m.author
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda m: m.name.lower() == arg.lower() or m.display_name.lower() == arg.lower(), ctx.guild.members)
			if match == None:
				raise BadArgument('Member not found. Make sure the user is in this guild.')
			return match

class User(UserConverter):
	"""
	User Converter
	---------------------

	Converts to a :class:`~discord.User`.

	All lookups are via the global user cache.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name#discrim
    4. Lookup by name
    """
	async def convert(self, ctx, arg):
		if arg == '^':
			if not ctx.guild:
				raise BadArgument('The "this" operator, ^, can only be used in servers.')
			nextmsg = False
			async for m in ctx.channel.history(limit=5):
				if m.id == ctx.message.id:
					nextmsg = True
				elif nextmsg:
					return await super().convert(ctx, str(m.author.id))
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda u: u.name.lower() == arg.lower(), ctx.bot.users)
			if match == None:
				raise BadArgument('User not found.')
			return match

class Role(RoleConverter):
	"""
	Role Converter
	---------------------

	Converts to a :class:`~discord.Role`.

	All lookups are via the local guild. If in a DM context, then the lookup
    is done by the global cache.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name
    """
	async def convert(self, ctx, arg):
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda r: r.name.lower() == arg.lower(), ctx.guild.roles)
			if match == None:
				raise BadArgument('Role not found.')
			return match

class TextChannel(TextChannelConverter):
	"""
	Text Channel Converter
	---------------------

	Converts to a :class:`~discord.TextChannel`.

    All lookups are via the local guild. If in a DM context, then the lookup
    is done by the global cache.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name
	"""
	async def convert(self, ctx, arg):
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda c: c.name.lower() == arg.lower(), ctx.guild.text_channels)
			if match == None:
				raise BadArgument('Text channel not found.')
			return match

class VoiceChannel(VoiceChannelConverter):
	"""
	Voice Channel Converter
	---------------------

	Converts to a :class:`~discord.VoiceChannel`.

    All lookups are via the local guild. If in a DM context, then the lookup
    is done by the global cache.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name
	"""
	async def convert(self, ctx, arg):
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda c: c.name.lower() == arg.lower(), ctx.guild.voice_channels)
			if match == None:
				raise BadArgument('Voice channel not found.')
			return match

class Category(CategoryChannelConverter):
	"""
	Category Converter
	---------------------

	Converts to a :class:`~discord.CategoryChannel`.

    All lookups are via the local guild. If in a DM context, then the lookup
    is done by the global cache.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name
	"""
	async def convert(self, ctx, arg):
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda c: c.name.lower() == arg.lower(), ctx.guild.categories)
			if match == None:
				raise BadArgument('Category not found.')
			return match

class UserWithFallback(UserConverter):
	"""
	User Converter
	---------------------

	Converts to a :class:`~discord.User`.

    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name#discrim
    4. Lookup by name
	5. Fallback to Discord API if an ID is provided.
    """
	async def convert(self, ctx, arg):
		if arg == '^':
			if not ctx.guild:
				raise BadArgument('The "this" operator, ^, can only be used in servers.')
			nextmsg = False
			async for m in ctx.channel.history(limit=5):
				if m.id == ctx.message.id:
					nextmsg = True
				elif nextmsg:
					return await super().convert(ctx, str(m.author.id))
		try:
			return await super().convert(ctx, arg)
		except BadArgument as e:
			match = utils.find(lambda u: u.name.lower() == arg.lower(), ctx.bot.users)
			if match == None:
				try:
					uid = int(arg)
				except Exception:
					raise BadArgument('User couldn\'t be found. Try providing an ID')
				if uid:
					try:
						return await ctx.bot.fetch_user(uid)
					except Exception:
						raise BadArgument('Invalid ID provided!')
			return match