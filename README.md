# Operator Day 2023 Demo Charm
This charm is a demonstration for Operator Day 2023.

## Development setup
```shell
# Install/Setup MicroK8s
sudo snap install microk8s --channel=1.28-strict/stable
sudo adduser $(whoami) snap_microk8s
newgrp snap_microk8s
microk8s status --wait-ready
sudo microk8s enable hostpath-storage dns
sudo snap alias microk8s.kubectl kubectl

# Install Charmcraft
lxd init --auto
sudo snap install charmcraft --classic

# Install Juju
sudo snap install juju
mkdir -p ~/.local/share/juju

# Bootstrap MicroK8s
juju bootstrap microk8s micro
juju add-model development
juju model-config logging-config='<root>=INFO; unit=DEBUG'

# Install jhack
sudo apt update
sudo apt install python3-pip python3-venv unzip -y
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# Close & re-open terminal
pipx install git+https://github.com/PietroPasotti/jhack.git

# Clone this repo
git clone https://github.com/operatorinc/zinc-k8s-operator.git
cd zinc-k8s-operator
git checkout 0-init
```

## Follow along
As you watch the demonstration, follow along in your own environment.  Git tags are provided for each step in the demo:
* [`0-init`](https://github.com/operatorinc/zinc-k8s-operator/tree/0-init): Empty charm created with `charmcraft init`
* [`1-base`](https://github.com/operatorinc/zinc-k8s-operator/tree/1-base): Files removed to create minimal charm
* [`2-ops`](https://github.com/operatorinc/zinc-k8s-operator/tree/2-ops): `ops` framework added back
* [`3-container`](https://github.com/operatorinc/zinc-k8s-operator/tree/3-container): Zinc container added
* [`4-action`](https://github.com/operatorinc/zinc-k8s-operator/tree/4-action): Juju action added
* [`5-defer`](https://github.com/operatorinc/zinc-k8s-operator/tree/5-defer): Defer juju event
