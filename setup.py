from setuptools import setup, find_packages

setup(
    name="roteiro-bot",
    version="1.0.0",
    description="Bot do Telegram para controle de rotas",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot==20.7",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
)
