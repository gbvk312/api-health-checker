# api-health-checker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

A professional developer tool to quickly monitor the health of multiple API endpoints from a single configuration file.

## Why this is valuable
Many projects have multiple dependencies, microservices, or public APIs they rely on. Ensuring all of these are up and responding properly usually requires heavy monitoring tools like Prometheus. `api-health-checker` is a lightweight, dependency-free alternative to assert endpoint uptime and expected response codes directly from your CLI or CI pipeline.

## Features
- Check multiple API endpoints concurrently (or sequentially).
- Validate HTTP response status codes.
- Validate maximum response wait times.
- Zero external dependencies (uses built-in `json` and `urllib`).

## Installation
Clone the repository:
```bash
git clone https://github.com/gbvk312/api-health-checker.git
cd api-health-checker
```

## Usage

1. Create a JSON configuration detailing your endpoints (an example `endpoints.json` is provided).
2. Run the checker:

```bash
python3 health_checker.py --config endpoints.json
```

Example output:
```text
🔍 Starting API Health Check...
--------------------------------------------------
✅ [200] https://api.github.com/zen (85ms)
✅ [200] https://jsonplaceholder.typicode.com/todos/1 (120ms)
❌ [404] https://httpstat.us/404 -- Expected [200], got 404
--------------------------------------------------
🚨 Health check failed: 1/3 endpoints down.
```

## Development & Testing

Run tests easily using `unittest`:
```bash
python3 -m unittest test_health_checker.py
```

## Roadmap
- [ ] Add YAML configuration support.
- [ ] Add custom header injection for authenticated endpoints.

## License
MIT License
