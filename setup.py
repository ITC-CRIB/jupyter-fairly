from setuptools import setup, find_packages

setup(
    name="JupyterFAIR",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 'hashlib',
        'requests==2.27.1',
        'python-dotenv==0.19.2',
    ],
    extras_require = {
        'dev': [
            'pytest==7.0.1',
            'jupyterlab==3.0.0',
            'jupyter-packaging==0.11.1',
            'nodejs==0.1.1',
            'beautifulsoup4==4.10.0', # For xml reading and formatting
            'pyoai==2.5.0',           # For OAI-PMH
            'lxml',                   # For OAI-PMH
            'pysqlite3',              # For OAI-PMH
            'oaiharvest',              # For OAI-PMH
            'Sickle'              # For OAI-PMH Alternative provided by zenodo
        ]
    }
)