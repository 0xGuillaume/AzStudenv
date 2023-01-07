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

There are 3 images available at the moment :

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

You **will need** the `id` key corresponding to your Azure Subscription in order to setup **AzStudenv** `yaml` configuration file.


## Installation

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

Update `azstudenv/config.yaml` file with mandatory keys.

```yaml
azure:
  idrsa: path/to/your/id_rsa.pub
  subscription: your-subscribtion-id
  ...
  vm:
    admin_username: vm_username
```




