<p align="center">
    <img src="https://img.shields.io/badge/microsoft%20azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white"/>
    <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white"/>
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
</p>


# AzStudenv

**AzStudenv** (Azure Student Environement) is primarly designed for Azure Student subscription but can be used with any other Azure subscriptions.

**Attention**, you will be charged creating and using Azure services.

---

Azure Student subscription authorized the usage of 3 public IP addresses per region at the same time. This way **AzStudenv** allows you to create up to 3 linux virtual machines. 

*AzStudenv* allow the creation of 3 images available :

- Debian 11

- Ubuntu 20.04

- Red Hat Linux Entreprise 8



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


## 🔐 Authenticate with Azure CLI

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

You **will need** the `id` key corresponding to your Azure Subscription in order to setup **AzStudenv** `yaml` configuration file.


## 📥 Installation

Clone **AzStudenv** git repositoriy locally.

```shell
$ git clone https://github.com/0xGuillaume/AzStudenv.git
```

Create python virtual environment and install required libraries.

```shell
$ python3 -m venv env

$ source env/bin/activate

$ python3 -m pip install -r requirements.txt
```


## ⚙️  Configuration

### User settings.

In order to configure your personal settings such as :

- Your Azure subscription.
- The Path of your SSH public key.
- The name of the user you will use on your Azure Linux environment.

```bash
azstudenv config \
	--subscription 00000000-0000-0000-0000-000000000000 \
	--ssh-key /path/to/my/sshkey.pub \
	--user foouser
```

### Infrastructure details

Then you have to setup your desire Azure Linux environment with the following options :
	
- Amount of instances you would like to create `[1, 2, 3]`.
- Linux distribution you would like to work on `["debian", "rhel", "ubuntu"]`.
- The name of your POC/project.

```bash
$ azstudenv infra --amount 2 --image debian --poc foopoc
```

## 🚀 Usage

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

## Run from everywhere

If you would like to run **AzStudenv** from anywhere follow steps below :

* Make the `main.py` file executable.
    ```shell
    $ chmod +x AzStudenv/azstudenv/main.py
    ```

* Create a [symbolic link](https://en.wikipedia.org/wiki/Symbolic_link) in `/bin/`.
    ```
    $ sudo ln -s AzStudenv/azstudenv/main.py azstudenv
    ```

* Now you can use **AzStudenv** from anywhere in your terminal.


## 🔬 Linting

Code has been written under the [PEP-8](https://peps.python.org/pep-0008/) and [Google](https://google.github.io/styleguide/pyguide.html) style guides.

[Pylint](https://github.com/PyCQA/pylint) has also been used as static code analyser to help reformat Python code.

```
$ (env) pylint main.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```


## 📦 Dependencies

- [`pylint`](https://pypi.org/project/pylint/) : Static code analyser.
- [`PyYAML`](https://pypi.org/project/PyYAML/) : Yaml parser.
- [`rich`](https://pypi.org/project/rich/) : Pretty text formatting in the terminal.
- [`typer`](https://pypi.org/project/typer/) : Create CLI application.
