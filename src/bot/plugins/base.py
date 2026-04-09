import logging

from mmpy_bot import Message, Plugin, listen_to

from bot.config import Settings


logger = logging.getLogger(__name__)


class BasePlugin(Plugin):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.app_settings = settings

    def on_start(self) -> None:
        channel_id = self.app_settings.channel_id
        if not channel_id:
            logger.info("Startup channel is not configured, skipping startup message")
            return

        logger.info("Sending startup message to channel %s", channel_id)
        self.driver.create_post(
            channel_id=channel_id,
            message="Bot has started.",
        )

    @listen_to("^ping$", needs_mention=True)
    async def ping(self, message: Message) -> None:
        self.driver.reply_to(message, "pong")

    @listen_to("^echo\\s+(.+)$", needs_mention=True)
    async def echo(self, message: Message, text: str) -> None:
        self.driver.reply_to(message, text)
