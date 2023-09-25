#!/usr/bin/env python3
import logging
import secrets

import ops
from charms.traefik_k8s.v2.ingress import IngressPerAppRequirer


ZINC_PORT = 4080


class ZincCharm(ops.CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.zinc_pebble_ready, self._on_zinc_pebble_ready)
        self.framework.observe(self.on.get_admin_password_action, self._on_get_admin_password)

        self._ingress = IngressPerAppRequirer(
            self,
            host=f"{self.app.name}.{self.model.name}.svc.cluster.local",
            port=ZINC_PORT,
            strip_prefix=True,
        )

    def _on_zinc_pebble_ready(self, event: ops.PebbleReadyEvent):
        """Define and start a workload using the Pebble API."""
        if not self._generated_password():
            event.defer()
        container = self.unit.get_container("zinc")
        container.add_layer("zinc", self._pebble_layer, combine=True)
        container.replan()

        self.unit.open_port(protocol="tcp", port=ZINC_PORT)

        self.unit.status = ops.ActiveStatus()

    @property
    def _pebble_layer(self):
        """Return a Pebble layer for managing Zinc."""
        return {
            "services": {
                "zinc": {
                    "override": "replace",
                    "summary": "zinc",
                    # go-runner achieves the equivalent of:`bash -c '/bin/zinc | tee PATH'`, but
                    # without including bash etc. in the image.
                    "command": "/bin/go-runner --log-file=/var/lib/zincsearch/zinc.log --also-stdout=true --redirect-stderr=true /bin/zincsearch",
                    "startup": "enabled",
                    "environment": {
                        "ZINC_DATA_PATH": "/var/lib/zincsearch",
                        "ZINC_FIRST_ADMIN_USER": "admin",
                        "ZINC_FIRST_ADMIN_PASSWORD": self._generated_password(),
                    },
                },
            },
        }

    def _on_get_admin_password(self, event: ops.ActionEvent) -> None:
        """Return the initial generated password for the admin user as an action response."""
        event.set_results({"admin-password": self._generated_password()})

    def _generated_password(self) -> str:
        """Report the generated admin password; generate one if it doesn't exist."""
        # If the peer relation is not ready, just return an empty string
        relation = self.model.get_relation("zinc-peers")
        if not relation:
            return ""

        # If the secret already exists, grab its content and return it
        secret_id = relation.data[self.app].get("initial-admin-password")
        if secret_id:
            secret = self.model.get_secret(id=secret_id)
            return secret.peek_content()["password"]

        if self.unit.is_leader():
            content = {"password": secrets.token_urlsafe(24)}
            secret = self.app.add_secret(content)
            # Store the secret id in the peer relation for other units if required
            relation.data[self.app]["initial-admin-password"] = secret.id
            return content["password"]
        else:
            return ""


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    ops.main(ZincCharm)
