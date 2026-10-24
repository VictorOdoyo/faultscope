# Local HTTP interface

GET /api/examples and /api/example?name=... read packaged allowlisted native examples. POST /api/import validates JSON. POST /api/study accepts network, action and options. Requests are bounded at 2 MB, only static allowlisted UI assets are served, and browser cross-origin POST requests are rejected. The adapter binds to loopback and is intended for a trusted local workstation, not a hardened multi-user internet service. RelayForge additionally accepts /api/relay-import with network and a FaultScope study record. No credentials or cloud storage are required.
