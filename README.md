# IoTConnect

IoTConnect is a framework (developed with Django REST framework) for getting IoT devices securely connected to wireless networks. Many IoT devices do not support WPA2-Enterprise, and therefore cannot be connected securely to enterprise networks using the traditional WPA2-Personal mode. Using technology that allows access points to support multiple pre-shared keys, however, each device may be given a unique, personal PSK. This technology is called PPSK, multi-PSK, DPSK or similar, depending on who you ask. We will refer to this technology as Personal Pre-shared Keys (PPSK). This is a prerequisite.

IoTConnect presents a design pattern that, in the best case scenario, allows you to achieve a fully working solution with four overridden methods and a single view class.

The framework was developed by Magnus Bakke and Liang Zhu of the Norwegian University of Science and Technology as part of a research and development project for Uninett AS, Norway's provider of network infrastructure and technology in research and education.

## Getting Started

Please note that there is no package available. Therefore, it is necessary to clone the project. The project includes an example that assumes the usage of Aerohive's HiveManager for PPSK and Dataporten by Uninett as an identity provider for authentication.

### Prerequisites

You must have access to a PPSK-issuing AP controller and access points that support the technology. Most variations of the technology are proprietary. Providers include:

* Aerohive
* Aruba
* Ruckus
* hostapd

hostapd is free and allows you to make a list of (PSK,MAC address) pairs. The downside is that the daemon must be restarted every time this list is updated for the changes to take effect.

Python >3.6 is required. See requirements.txt as well.

### Installing

Clone the project:

```
git clone https://github.com/Audiopolis/IoTConnect.git
```

Install the requirements:

```
pip3 install -r requirements.txt
```

Rename the directories and files referencing Uninett to suit your own environment. We will assume that the directory *uninett_api* is still named *uninett_api*. The following can be customized to your own needs and preferences.

Inside *uninett_api/settings/*, create three files: *_locals.py*, *_secrets.py*, and *_testing.py* (or *_production.py*, for example, whichever fits).

In *_locals.py*, create a variable *FRONTEND_URL*. Its value should be the frontend's URL, including *http://* or *https://*. Add a second variable, *BACKEND_URL*, whose value should be the URL to the backend.

Inside *_secrets.py*, we have placed our OAuth secrets, including secret keys and bearer tokens for HiveManager and Dataporten.

Inside *_testing.py*, we have placed the settings to be used by the testing server.

This must be done for each environment, including development computers. These files are ignored by Git, keeping secrets safe and local settings local. Please note that each environment (development, testing, staging, production, etc.) should have its own application registered with the identity provider, and the OAuth details for each application exists within *_secrets.py* on each environment in our case.

Inspect the code in the *connect* app, which can be renamed, inspect and get familiar with the code of *DataportenRedirectView*, *ConnectView*, *FeideAuthenticator* and *HiveManagerAdapter*. Customize these classes to suit your needs.

Customize the tests within the *connect* app to reflect your own changes.

Also note that the *CustomExceptionMiddleware* middleware is installed in the *base* settings. This should be removed or customized.

## Contributing

Please create a feature branch for your changes and squash multiple commits if possible.

## Notes

Please note the presence of the custom DisableCSRFMiddleware and the disabling of django.middleware.csrf.CsrfViewMiddleware. These changes were made because of an unidentified issue that caused Ajax calls to sometimes fail, likely because of cookie states that are difficult to reproduce. These changes should not be included in a production environment, as it may make users vulnerable to CSRF attacks. We do not believe such an attack will be worth the effort for an attacker, considering the prize is to gain access to the internet.

## Authors

* **Magnus Bakke** - [Audiopolis](https://github.com/Audiopolis)
* **Liang Zhu** - [helliio](https://github.com/helliio)

See also the list of [contributors](https://github.com/Audiopolis/IoTConnect/contributors) who participated in this project.

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.

## Acknowledgments

* Aerohive for lending us two access points and a HiveManager license
* Uninett AS for office space and guidance
