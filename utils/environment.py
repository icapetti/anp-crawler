from os import environ, getenv

from dotenv import load_dotenv

def code_location() -> str:
    """
        Get the location of this script based on the value of
        the environment variable SCRAPYENV_ENVIRONMENT.
        Its value can either be "development" or "production".
    """

    user = environ.get("USER") if environ.get("USER") else environ.get("USERNAME")
    load_dotenv(f'/home/{user}/.env')
    env = getenv("SCRAPYVAR_ENVIRONMENT")

    return env if env else "development"
