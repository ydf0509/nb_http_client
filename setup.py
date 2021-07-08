# coding=utf-8
from pathlib import Path
from setuptools import setup, find_packages

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

# filepath = ((Path(__file__).parent / Path('README.md')).absolute()).as_posix()
filepath = 'README.md'
print(filepath)

setup(
    name='nb_http_client',  #
    version="0.8",
    description=('nb_http_client'),
    keywords=("this most fast http clent,500% fast than requets,also fast than aiohttp and urllib,powered by  universal_object_pool",),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description_content_type="text/markdown",
    long_description=open(filepath, 'r', encoding='utf8').read(),
    # data_files=[filepath],
    author='bfzs',
    author_email='ydf0509@sohu.com',
    maintainer='ydf',
    maintainer_email='ydf0509@sohu.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'universal_object_pool',
        'decorator_libs'
    ]
)
"""
打包上传
python setup.py sdist upload -r pypi


python setup.py sdist & twine upload dist/nb_http_client-0.8.tar.gz
twine upload dist/*


python -m pip install nb_http_client --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步
"""
