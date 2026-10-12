# JMeter API Performance Tests

Small hands-on performance testing project using Apache JMeter against a local FastAPI application.

The project demonstrates HTTP request testing, CSV parameterization, assertions, configurable load generation, non-GUI execution, JTL/HTML reporting, and basic HTTP(S) request recording.

## Project Structure

```text
jmeter-api-performance-tests/
├── app/
│   ├── __init__.py
│   └── main.py
├── test-data/
│   └── items.csv
├── test-plans/
│   ├── api-smoke-test.jmx
│   ├── api-performance-test.jmx
│   └── api-recorder-demo.jmx
├── .gitignore
├── requirements.txt
└── README.md
```

## Test Application

The included FastAPI application provides:

- `GET /health` - basic health check
- `GET /items/{item_id}` - returns test item data
- `GET /slow?delay_ms=100` - introduces a controlled asynchronous delay for performance testing

The `/slow` endpoint uses `asyncio.sleep()` to simulate predictable I/O-style waiting without deliberately consuming CPU.

## JMeter Test Plans

### API Smoke Test

`test-plans/api-smoke-test.jmx`

Demonstrates:

- CSV Data Set Config
- request parameterization
- HTTP response-code assertion
- JSON JMESPath response assertion
- reusable HTTP Request Defaults

Test data is loaded from:

```text
test-data/items.csv
```

The test validates three item responses against their expected names.

### API Performance Test

`test-plans/api-performance-test.jmx`

Runs concurrent requests against the controlled `/slow` endpoint.

The workload can be configured through JMeter properties:

```text
threads
rampup
loops
```

Default values:

```text
threads = 10
rampup = 1
loops = 20
```

Example CLI run:

```bash
jmeter -n \
  -t test-plans/api-performance-test.jmx \
  -Jthreads=10 \
  -Jrampup=1 \
  -Jloops=20 \
  -l results.jtl
```

On Windows, use `jmeter.bat` instead of `jmeter` if JMeter is not available directly through `PATH`.

An HTML dashboard can also be generated:

```bash
jmeter -n \
  -t test-plans/api-performance-test.jmx \
  -Jthreads=10 \
  -Jrampup=1 \
  -Jloops=20 \
  -l results.jtl \
  -e \
  -o report
```

This creates:

```text
results.jtl        # raw test results
report/index.html  # main HTML dashboard
```

The paths are relative to the directory where the command is executed. The report output directory should be empty or not yet exist before generation.

### HTTP(S) Recorder Demo

`test-plans/api-recorder-demo.jmx`

Demonstrates basic use of JMeter's HTTP(S) Test Script Recorder.

A request to the local `/slow` endpoint was routed through JMeter's proxy on port `8888`, producing a reusable HTTP Request sampler and captured HTTP headers.

The recorder is intended for creating test-script requests from observed HTTP traffic; performance measurements are collected when the recorded sampler is subsequently executed.

## Example Performance Comparison

A simple local comparison was performed against:

```text
GET /slow?delay_ms=100
```

| Workload | Samples | Average | Median | Throughput |
|---|---:|---:|---:|---:|
| 1 concurrent user | 20 | ~109 ms | ~105 ms | ~9 req/s |
| 10 concurrent users | 200 | ~104 ms | ~103 ms | ~70 req/s |

The response time remained close to the controlled 100 ms delay while throughput increased substantially as requests were handled concurrently.

These results are illustrative rather than a production benchmark. JMeter and the FastAPI application were running on the same physical machine, so operating-system, networking, JVM, Python, and load-generator resource usage can all affect the measurements.

Raw `.jtl` files and generated HTML reports are intentionally excluded from version control.

## Setup

Create and activate a Python virtual environment, then install the application dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the local API:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Verify it:

```bash
curl http://127.0.0.1:8001/health
```

Apache JMeter 5.6.3 was used while developing the test plans.

## Performance Testing Concepts Practiced

- concurrent virtual users
- thread ramp-up
- request loops
- response time and latency
- throughput
- percentile-based analysis
- warm-up and connection reuse effects
- load-generator resource limitations
- non-GUI test execution
- HTTP request recording