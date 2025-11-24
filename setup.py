from setuptools import setup, find_packages

setup(
    name='job_search_module',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pydantic==2.*',  # Specify a compatible Pydantic version
        'google-generativeai',
<<<<<<< HEAD
        # 'google-colab', # Removed: For Colab-specific functionalities, not needed locally
=======
        'google-colab', # For Colab-specific functionalities
>>>>>>> 61ae92d9877ce1c72fc021455de1c71aa6074cbe
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'autopep8',
            'pyngrok',
            'streamlit',
            'pylint' # Added pylint here
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A module for finding and evaluating job leads using AI.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_repo_name', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
