# <div align="center">Synapse</div>

<div align="center"><i>The Graphical Search Engine</i></div>

***

## Table of Contents

- [Synapse](#synapse)
	- [Table of Contents](#table-of-contents)
	- [Introduction](#introduction)
	- [Contribution](#contribution)
	- [License](#license)

## Introduction

Research made easy. Visualize graphically all your resources sorted into topics.

Created for the IBDP Computer Science HL Internal Assessment.

Backend is written in Python Flask (with PostGreSQL) and stored in the `api` folder. Frontend is built with React Next.JS and SCSS and stored in `client`.

Make sure to create a `.env` file in the `app` folder with the following contents (filled out):

```shell
DATABASE_URL = '' # Connection String to Database

GOOGLE_API_KEY = '' # https://developers.google.com/custom-search/v1/introduction
IP_WHO_API_KEY = '' # https://ipwho.org/

# Google Engine ID
GOOGLE_ANY_ENGINE_ID = ''
```

## Contribution

If you want to contribute to this project, please follow the guidelines below:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes and commit them
4. Push the new branch to your fork
5. Submit a pull request

## License

This project is licensed under the MIT license. See our [LICENSE](LICENSE) for more information.
