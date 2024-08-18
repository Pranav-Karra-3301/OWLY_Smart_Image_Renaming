from setuptools import setup, find_packages

setup(
    name='owly_smart_image_renaming',
    version='0.1.0',
    author='Pranav Karra',
    description='A smart image renaming tool using advanced technologies like OpenAI API, Cloudinary, Base64, etc.',
    packages=find_packages(),
    install_requires=[
        'openai',
        'cloudinary',
        'requests',
        'pytesseract',
        'Pillow',
        'spacy',
        'torch',
        'transformers',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)