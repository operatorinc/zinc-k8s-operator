#!/usr/bin/env python3
import logging

import ops


class ZincCharm(ops.CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.zinc_pebble_ready, self._on_zinc_pebble_ready)

    def _on_zinc_pebble_ready(self, event: ops.PebbleReadyEvent):
        """Define and start a workload using the Pebble API."""
        container = self.unit.get_container("zinc")
        container.add_layer("zinc", self._pebble_layer, combine=True)
        container.replan()

        self.unit.open_port(protocol="tcp", port=4080)

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
                        "ZINC_FIRST_ADMIN_PASSWORD": "password",
                    },
                },
            },
        }


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    ops.main(ZincCharm)
