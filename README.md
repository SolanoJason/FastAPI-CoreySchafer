## Production storage

Set `ENVIRONMENT=production` and provide the four `GCS_*` variables shown in
`.env.example`. Use a dedicated Google service account with access limited to
the configured bucket. The private key can be supplied as one environment
variable with `\n` sequences; the application converts them to newlines.

For deployments on Google Cloud, prefer workload identity or a mounted secret
over committing a service-account key to the image or repository.
