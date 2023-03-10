<p align="center">
    <img src="https://img.shields.io/badge/microsoft%20azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white"/>
    <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white"/>
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
</p>


# AzStudenv

**AzStudenv** (_Azure Studenv Environment_) is a tool that create an **IaaS** Azure Linux environment for tests and development purpose. This tool has mainly been designed for Azure Student subscriptions but works with a standard subscription as well. 

You can setup your environment up to **3 virtual machines** with the **same** image whatever virtual machines amount needed :

- Debian 11

- Ubuntu 20.04

- Red Hat Linux Entreprise 8

📢  **Attention**, you will be charged creating and using Azure services.

---


## Prerequisites

- An Azure (Student or not) Subscription - [Subscribed](https://azure.microsoft.com/en-us/free/). 

- Terraform 1.3.7 or later - [Downloads](https://developer.hashicorp.com/terraform/downloads).
    ```shell
    $ sudo dnf install -y dnf-plugins-core

    $ sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/$release/hashicorp.repo

    $ sudo dnf install -y terraform
    ```

- Python 3 & Python 3 virtual environment - [Downloads](https://www.python.org/downloads/).
    ```shell
    $ sudo dnf install -y python3 python3-venv
    ```

- Azure CLI - [Downloads](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
    ```shell
    $ sudo dnf install -y azure-cli
    ```


## Authenticate with Azure CLI

Once all prerequisites are satisfied you must authenticate to your **Azure Subscription** in order to let Terraform create infrastructure.

```shell
$ az login
```

Once successfully authenticated, your terminal will display your Azure subscription informations.

```shell
You have logged in. Now let us find all the subscriptions to which you have access...

[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "Foo-Tenant-Id",
    "id": "Foo-Subscription-Id",
    "isDefault": true,
    "managedByTenants": [],
    "name": "Foo-Subscription-Name",
    "state": "Enabled",
    "tenantId": "Foo-TenantId",
    "user": {
      "name": "username@domain.com",
      "type": "user"
    }
  }
]
```

You **will need** the `id` key corresponding to your Azure Subscription in order to configure **AzStudenv**.


## Installation

Clone **AzStudenv** git repositoriy locally.

```shell
$ git clone https://github.com/0xGuillaume/AzStudenv.git
```

1. **Use the tool from its directory:**
Create python virtual environment and install required libraries.

```shell
$ python3 -m venv env

$ source env/bin/activate

$ python3 -m pip install -r requirements.txt
```

2. **Use the tool from anywhere:** Make the `azstudenv` file executable and
create a [symbolic link](https://en.wikipedia.org/wiki/Symbolic_link) in `/usr/local/bin/`.
```shell
$ python3 -m pip install -r requirements.txt

$ chmod +x ./AzStudenv/azstudenv/azstudenv

$ cd /bin/usr/local

$ sudo ln -s /path/to/AzStudenv/azstudenv/azstudenv
```

## Configuration

### User settings.

In order to configure your personal settings such as :

1. Your Azure subscription.
1. The Path of your SSH public key.
1. The name of the user you will use on your Azure Linux environment.

```bash
azstudenv config \
	--subscription 00000000-0000-0000-0000-000000000000 \
	--ssh-key /path/to/my/sshkey.pub \
	--user foouser
```

### Infrastructure details

Then you have to setup your desire Azure Linux environment with the following options :
	
1. Amount of instances you would like to create `[1, 2, 3]`.
1. Linux distribution you would like to work on `["debian", "rhel", "ubuntu"]`.
1. The name of your POC/project.

```bash
$ azstudenv infra --amount 2 --image debian --poc foopoc
```

## Usage

### Build (Apply)

Once you have setup your configuration you can build your Azure infrastructure.

```bash
$ azstudenv build
```

### Destroy

When you finished using your Azure infrastructure feel free to run the following command to destroy your infrastructure and avoid unnecessary costs.

```bash
$ azstudenv destroy
```

### Help

At any time feel free to consult the help to get more details on commands behavior.

```bash
$ azstudenv --help
```

## Linting

Code has been written under the [PEP-8](https://peps.python.org/pep-0008/) and [Google](https://google.github.io/styleguide/pyguide.html) style guides.

[Pylint](https://github.com/PyCQA/pylint) has also been used as static code analyser to help reformat Python code.

```
$ (env) pylint main.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```


## Dependencies

- [`PyYAML`](https://pypi.org/project/PyYAML/) : Yaml parser.
- [`rich`](https://pypi.org/project/rich/) : Pretty text formatting in the terminal.
- [`typer`](https://pypi.org/project/typer/) : Create CLI application.
