# lab-demo-app

A small FastAPI service used to trial the Lab Deploy platform. Releases are performed only by the
`deploy-gcp.yml` workflow, dispatched by the Lab Deploy controller from a reviewed plan. The workflows pin the
platform repository `brianboti/lab-deploy` at commit `a394806f6e631837e05375225e82b0cb00d7f10f`.

- `platform.yaml` is the reviewed deployment specification.
- `/health` is the readiness endpoint probed by Cloud Run and by the release.
