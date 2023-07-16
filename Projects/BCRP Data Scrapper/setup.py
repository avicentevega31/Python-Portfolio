from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name = "scrapper_bcrp_data",
        description = "Librería de python que te permite descargar data del Banco Central de Reserva del Perú (BCRP)"
        license = "MIT",
        url = "https://github.com/avicentevega31/Python-Portfolio/tree/master/Projects/BCRP%20Data%20Scrapper",
        version = "0.0.0",
        author = "Adrian Vicente Vega"
        author_email = "a.vicentevega31@gmail.com",
        long_description = open("README.md").read(),
        packages = find_packages(),
        zip_safe = False,
        install_requires = [],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT Lincense",
            "Operating System :: OS Independent",
            "Programming Language :: Python"
        ],
        
    )