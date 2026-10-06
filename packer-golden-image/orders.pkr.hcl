packer {
  required_plugins {
    docker = {
      version = "= 1.1.1"
      source  = "github.com/hashicorp/docker"
    }
    ansible = {
      version = "= 1.1.2"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

variable "base_image" {
  type    = string
  default = "ubuntu:24.04"
}

source "docker" "orders" {
  image  = var.base_image
  commit = true
}

build {
  name    = "orders-golden"
  sources = ["source.docker.orders"]

  provisioner "shell" {
    inline = ["apt-get update", "apt-get install -y python3"]
  }

  provisioner "ansible" {
    playbook_file = "../ansible-roles-jvm/site.yml"
    groups          = ["orders"]
    extra_arguments = [
      "--extra-vars", "ansible_connection=docker ansible_host=${build.ID} jvm_manage_service=false",
    ]
  }

  post-processor "docker-tag" {
    repository = "orders-golden"
    tags       = ["local"]
  }
}
