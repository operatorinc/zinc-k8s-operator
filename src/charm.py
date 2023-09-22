#!/usr/bin/env python3
import logging

import ops


class ZincK8SOperatorCharm(ops.CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self._on_start)

    def _on_start(self, event: ops.StartEvent):
        logger.warning("Hello, Kubecon!")


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    ops.main(ZincK8SOperatorCharm)
