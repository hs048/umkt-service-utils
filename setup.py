from setuptools import setup

setup(
    name='hendra-048-service',
    version='0.2',
    author='hendra saputra',
    author_email='hs048@umkt.ac.id',
    description='My package description',
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type='text/markdown',
    url='https://github.com/hs048/umkt-service-utils',
    packages=['service_utility'],
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
        'PyJWT==1.7.1'
    ],
)