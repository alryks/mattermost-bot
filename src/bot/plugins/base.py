import logging

from mmpy_bot import Message, Plugin, listen_to, listen_webhook, WebHookEvent, ActionEvent

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

    @listen_webhook("ping")
    @listen_webhook("pong")
    async def action_listener(self, event: WebHookEvent):
        logger.info(str(event.body))
        self.driver.create_post(
            event.body["channel_id"], f"Webhook {event.webhook_id} triggered!"
        )

    @listen_to("!button", direct_only=False)
    async def webhook_button(self, message: Message):
        """Creates a button that will trigger a webhook depending on the choice."""
        self.driver.reply_to(
            message,
            "",
            props={
                "attachments": [
                    {
                        "pretext": None,
                        "text": "Take your pick..",
                        "actions": [
                            {
                                "id": "sendPing",
                                "name": "Ping",
                                "integration": {
                                    "url": f"{self.app_settings.webhook_public_url}:{self.app_settings.webhook_public_port}/"
                                    "hooks/ping",
                                    "context": {
                                        "text": "The ping webhook works! :tada:",
                                    },
                                },
                            },
                            {
                                "id": "sendPong",
                                "name": "Pong",
                                "integration": {
                                    "url": f"{self.app_settings.webhook_public_url}:{self.app_settings.webhook_public_port}/"
                                    "hooks/pong",
                                    "context": {
                                        "text": "The pong webhook works! :tada:",
                                    },
                                },
                            },
                        ],
                    }
                ]
            },
        )