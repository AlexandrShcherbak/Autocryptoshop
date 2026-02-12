# - *- coding: utf- 8 - *-
import configparser
import os


def _clean(value: str) -> str:
    return value.strip() if value else ""


def _read_settings() -> configparser.ConfigParser:
    config_path = os.getenv("SETTINGS_FILE", "settings.ini")
    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")
    return parser


def _setting(parser: configparser.ConfigParser, key: str, env_key: str, default: str = "", required: bool = False) -> str:
    value = _clean(os.getenv(env_key))
    if not value and parser.has_option("settings", key):
        value = _clean(parser.get("settings", key, fallback=default))

    if required and not value:
        raise RuntimeError(
            f"Missing required setting '{key}'. Set {env_key} environment variable "
            "or configure it in settings.ini"
        )

    return value or default


read_config = _read_settings()

# TELEGRAM BOT
bot_token = _setting(read_config, "token", "ACS_BOT_TOKEN", required=True)  # Токен бота
path_database = _setting(read_config, "database_path", "ACS_DATABASE_PATH", default="tgbot/data/database.db")  # Путь к БД
bot_version = "23.3"  # Версия бота

# CrystalPay
crystal_Cassa = _setting(read_config, "Crystal_Cassa", "ACS_CRYSTAL_CASSA")  # имя кассы (то что в скобках)
crystal_Token = _setting(read_config, "Crystal_Token", "ACS_CRYSTAL_TOKEN")  # первый токен

# Lolzteam Market
lolz_token = _setting(read_config, "lolz_token", "ACS_LOLZ_TOKEN")  # лолз токен
lolz_id = _setting(read_config, "lolz_id", "ACS_LOLZ_ID")  # лолз id
lolz_nick = _setting(read_config, "lolz_nick", "ACS_LOLZ_NICK")  # лолз ник

# ЮMoney
yoomoney_token = _setting(read_config, "yoomoney_token", "ACS_YOOMONEY_TOKEN")  # юмани токен
yoomoney_number = _setting(read_config, "yoomoney_number", "ACS_YOOMONEY_NUMBER")  # юмани номер

# Lava
lava_secret_key = _setting(read_config, "lava_secret_key", "ACS_LAVA_SECRET_KEY")  # лава секретный ключ
lava_project_id = _setting(read_config, "lava_project_id", "ACS_LAVA_PROJECT_ID")  # лава ID проекта

# Crypto
crypto_wallet_address = _setting(read_config, "crypto_wallet_address", "ACS_CRYPTO_WALLET_ADDRESS")  # адрес USDT BEP-20 кошелька
crypto_private_key = _setting(read_config, "crypto_private_key", "ACS_CRYPTO_PRIVATE_KEY")  # приватный ключ кошелька
bscscan_api_key = _setting(read_config, "bscscan_api_key", "ACS_BSCSCAN_API_KEY")  # API ключ BSCScan
polygonscan_api_key = _setting(read_config, "polygonscan_api_key", "ACS_POLYGONSCAN_API_KEY")  # API ключ Polygonscan
etherscan_api_key = _setting(read_config, "etherscan_api_key", "ACS_ETHERSCAN_API_KEY")  # API ключ Etherscan

# Каналы
channel_id = _setting(read_config, "channel_id", "ACS_CHANNEL_ID")  # айди канала для подписки
channel_url = _setting(read_config, "channel_url", "ACS_CHANNEL_URL")  # ссылка на канал
logs_channel_id = _setting(read_config, "logs_channel_id", "ACS_LOGS_CHANNEL_ID")  # айди канала для логов
# Каналы
channel_id = read_config['settings']['channel_id'].strip().replace(" ", "") # айди канала для подписки
channel_url = read_config['settings']['channel_url'].strip().replace(" ", "") # ссылка на канал

logs_channel_id = read_config['settings']['logs_channel_id'].strip().replace(" ", "") # айди канала для логов
