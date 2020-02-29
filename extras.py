"""
extras
~~~~~~~~~~~~~~~~~~~~~

An extension to provide extra utilities for fire
"""

from discord.asset import Asset
from discord.utils import parse_time, snowflake_time, _get_as_snowflake
from discord.object import Object
from discord.mixins import Hashable
from discord.enums import ChannelType
from discord.partial_emoji import PartialEmoji
from discord.ext import commands


class PartialPreviewGuild:
    """Represents a "partial" preview guild.
    This model will be given when the user is not part of the
    guild the preview resolves to.
    .. container:: operations
        .. describe:: x == y
            Checks if two partial guilds are the same.
        .. describe:: x != y
            Checks if two partial guilds are not the same.
        .. describe:: hash(x)
            Return the partial guild's hash.
        .. describe:: str(x)
            Returns the partial guild's name.
    Attributes
    -----------
    name: :class:`str`
        The partial guild's name.
    id: :class:`int`
        The partial guild's ID.
    features: List[:class:`str`]
        A list of features the guild has. See :attr:`Guild.features` for more information.
    approximate_member_count: Optional[:class:`int`]
        The approximate number of members in the guild.
    approximate_presence_count: Optional[:class:`int`]
        The approximate number of members currently active in the guild.
        This includes idle, dnd, online, and invisible members. Offline members are excluded.
    icon: Optional[:class:`str`]
        The partial guild's icon.
    banner: Optional[:class:`str`]
        The partial guild's banner.
    splash: Optional[:class:`str`]
        The partial guild's invite splash.
    discovery_splash: Optional[:class:`str`]
        The partial guild's discovery splash.
    description: Optional[:class:`str`]
        The partial guild's description.
    emojis: Tuple[:class:`PartialEmoji`, ...]
        All emojis that the guild owns.
    """

    __slots__ = ('_state', 'features', 'icon', 'approximate_presence_count', 'approximate_member_count', 'banner', 'id', 'name', 'splash',
                 'discovery_splash', 'description', 'emojis')

    def __init__(self, state, data):
        self._state = state
        self.id = int(data['id'])
        self.name = data['name']
        self.features = data.get('features', [])
        self.icon = data.get('icon')
        self.approximate_presence_count = data.get('approximate_presence_count')
        self.approximate_member_count = data.get('approximate_member_count')
        self.banner = data.get('banner')
        self.splash = data.get('splash')
        self.discovery_splash = data.get('discovery_splash')
        self.description = data.get('description')
        self.emojis = tuple(map(lambda d: PartialEmoji.from_dict(d), data.get('emojis', [])))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{0.__class__.__name__} id={0.id} name={0.name!r} features={0.features} ' \
               'description={0.description!r}>'.format(self)

    @property
    def created_at(self):
        """:class:`datetime.datetime`: Returns the guild's creation time in UTC."""
        return snowflake_time(self.id)

    @property
    def icon_url(self):
        """:class:`Asset`: Returns the guild's icon asset."""
        return self.icon_url_as()

    def icon_url_as(self, *, format='webp', static_format='webp', size=1024):
        """The same operation as :meth:`Guild.icon_url_as`."""
        return Asset._from_guild_icon(self._state, self, format=format, static_format=static_format, size=size)

    @property
    def banner_url(self):
        """:class:`Asset`: Returns the guild's banner asset."""
        return self.banner_url_as()

    def banner_url_as(self, *, format='webp', size=2048):
        """The same operation as :meth:`Guild.banner_url_as`."""
        return Asset._from_guild_image(self._state, self.id, self.banner, 'banners', format=format, size=size)

    @property
    def splash_url(self):
        """:class:`Asset`: Returns the guild's invite splash asset."""
        return self.splash_url_as()

    def splash_url_as(self, *, format='webp', size=2048):
        """The same operation as :meth:`Guild.splash_url_as`."""
        return Asset._from_guild_image(self._state, self.id, self.splash, 'splashes', format=format, size=size)

    @property
    def discovery_splash_url(self):
        """:class:`Asset`: Returns the guild's discovery splash asset."""
        return self.discovery_splash_url_as()

    def discovery_splash_url_as(self, *, format='webp', size=2048):
        return Asset._from_guild_image(self._state, self.id, self.discovery_splash, 'discovery-splashes', format=format, size=size)

    def is_icon_animated(self):
        """:class:`bool`: Returns True if the guild has an animated icon."""
        return bool(self.icon and self.icon.startswith('a_'))

class MissingOverride(Exception):
    def __str__(self):
        return f'You are missing the required override for this command'

def has_override(**kwargs):
    def predicate(ctx):
        build = ctx.bot.overrides.get(kwargs.get('build', ''), {})
        if 'active' in build and ctx.author.id in build['active']:
            return True
        raise MissingOverride()
    return commands.check(predicate)
