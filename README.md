# blocks-inventory

Release inventory for the SELISE `<Blocks/>` platform. This repository is the ledger of published
container image tags: for every service it records which image versions exist per component (API
and worker) and per environment (production, staging, enterprise), together with the GitHub
Actions workflows that build, scan, and roll those images out.

## Overview

The repository holds no application code. It is a manifest and CI repository:

- One directory per service (for example `blocks-idp-net/`, `blocks-localization-net/`), each with
  an `api/` and a `worker/` subdirectory.
- Inside those, one text file per environment (`prod.txt`, `stg.txt`, `enterprise.txt`) listing the
  published image tags in chronological order, one `repository/image:tag` per line.
- `.github/workflows/`: the shared unit test, SAST, SCA, and DAST pipelines plus the build, push,
  and GitOps deployment workflows.
- `.github/config/values-config.json` and `.github/actions/setvars/`: shared configuration and the
  variable-setup composite action used by those workflows.

## Repository structure

```
blocks-inventory/
├── blocks-<service>-net/
│   ├── api/
│   │   ├── prod.txt          # published API image tags, one per line
│   │   ├── stg.txt
│   │   └── enterprise.txt
│   └── worker/
│       └── ...               # same layout for the worker image
├── .github/
│   ├── actions/setvars/      # composite action shared by the workflows
│   ├── config/               # shared workflow configuration
│   └── workflows/            # unit test, SAST, SCA, DAST, build, push, deployment
├── LICENSE
└── README.md
```

## Getting started

There is nothing to build or run. To read the current state of a service, open the relevant file:

```bash
tail -5 blocks-idp-net/api/prod.txt      # the most recent production API images
```

## How entries are added

Tags are appended by the release workflows, not by hand. A new line appears when a build is
promoted to that environment, so the last line of a file is the current version. Avoid editing or
reordering existing lines: the history of the file is the release history.

## Configuration

The workflows read their settings from `.github/config/values-config.json` and from repository and
organization level Actions variables and secrets. No credentials are stored in this repository, and
none should be added: registry and deployment credentials belong in GitHub secrets.

## Contributing and security

- Contribution conventions and workflow: [CONTRIBUTING.md](CONTRIBUTING.md)
- Reporting a vulnerability: [SECURITY.md](SECURITY.md)
- Community standards: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

See [LICENSE](LICENSE).
