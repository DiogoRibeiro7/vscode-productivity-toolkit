<!--
MIT License

Copyright (c) 2025 Diogo Ribeiro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

# Integration: Docker Compose

Combine toolkit tasks with Docker Compose to provide consistent local development stacks.

## Compose Definition

```yaml
version: "3.9"
services:
  api:
    build: ./services/api
    command: npm run dev
    ports:
      - "3000:3000"
    volumes:
      - ./:/workspace
    env_file:
      - .env
  worker:
    build: ./services/worker
    command: python -m pipeline.worker
    volumes:
      - ./:/workspace
    depends_on:
      - api
```

## Related Tasks

| Task | Purpose |
| --- | --- |
| `javascript:docker-compose-up` | Spins up the multi-service stack with log streaming.
| `javascript:docker-compose-stop` | Gracefully stops and removes containers.
| `python:docker-build` | Builds Python images for worker services before deployment.
| `toolkit:observability-snapshot` | Aggregates logs, metrics, and security scans pre-release.

## Workflow

1. Launch the stack with `javascript:docker-compose-up`.
2. Develop against the running services; hot reload is enabled via bind mounts.
3. Execute `javascript:docker-compose-tests` (if configured) to run integration suites inside containers.
4. Tear down resources with `javascript:docker-compose-stop` when finished.

Pairing Compose with curated tasks keeps local environments reproducible and production-like.
