# Speedtest Monitoring

Simple app to periodically run internet speed tests
via `speedtest-cli` and store the results in a Sqlite db.

### How to run


Clone repo

```
git clone git@github.com:amas0/speedtest-monitoring.git
```

Build and run docker container:

```
docker build -t speedtest-monitoring .
docker run -d --restart always --name speedtest-monitoring -p 7898:7898 speedtest-monitoring
```

You can check out the Swagger page locally at `http://localhost:7898/docs`. To trigger
a speedtest manually:

```
curl http://localhost:7898/run-test
```

To return all the speed test results:

```
curl http://localhost:7898/get-all-results
```