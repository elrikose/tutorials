# Container Hardening

Keep the size of the container small by using multistage builds

```dockerfile
FROM ubuntu AS base
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN CGO_ENABLED=0 go build app.go

FROM alpine
COPY --from=base /app .
CMD ["/app"]
```

Set version tags where appropriate for things like Alpine

```dockerfile
FROM ubuntu AS base
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN CGO_ENABLED=0 go build app.go

FROM alpine:3.20.1
COPY --from=base /app .
CMD ["/app"]
```

- If at any point you have to build it in the future it would fail. 
- If there is a security failure you'd be notified.

Don't run as root

```dockerfile
...

FROM alpine:3.20.1
RUN addgroup -s app && adduser -s app -G app -h /home/app

COPY --from=base /app /home/appuser/
USER appuser
CMD ["/app"]
```

Make file system read only by `chmod`-ing folders and files

Remove shell access by `RUN rm -r /bin/sh`



