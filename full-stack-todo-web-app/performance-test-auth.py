#!/usr/bin/env python3
"""
Performance testing script for authentication middleware.

This script tests the performance overhead of the JWT authentication
middleware to ensure it meets the sub-100ms requirement.
"""

import time
import requests
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor
import argparse
from typing import List, Tuple
import json
from jose import jwt
from datetime import datetime, timedelta
import os

# Set the secret key for JWT generation
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-key-here-make-it-long-and-random")
ALGORITHM = "HS256"


def create_test_token(user_id: str) -> str:
    """Create a test JWT token for performance testing."""
    payload = {
        "sub": user_id,
        "email": f"user{user_id}@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def make_authenticated_request(base_url: str, user_id: str, token: str) -> Tuple[float, int]:
    """
    Make a single authenticated request and measure response time.

    Args:
        base_url: Base URL of the API
        user_id: User ID to include in the path
        token: JWT token for authentication

    Returns:
        Tuple of (response_time_in_seconds, status_code)
    """
    start_time = time.time()

    try:
        response = requests.get(
            f"{base_url}/api/{user_id}/tasks",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            },
            timeout=30  # 30 second timeout
        )
        response_time = time.time() - start_time
        return response_time, response.status_code
    except requests.exceptions.RequestException as e:
        response_time = time.time() - start_time
        print(f"Request failed: {e}")
        return response_time, 0  # 0 indicates error


def run_performance_test(
    base_url: str,
    num_requests: int,
    concurrency: int,
    user_count: int
) -> dict:
    """
    Run performance test with specified parameters.

    Args:
        base_url: Base URL of the API
        num_requests: Total number of requests to make
        concurrency: Number of concurrent requests
        user_count: Number of different users to simulate

    Returns:
        Dictionary with performance metrics
    """
    print(f"Starting performance test...")
    print(f"- Base URL: {base_url}")
    print(f"- Total requests: {num_requests}")
    print(f"- Concurrency: {concurrency}")
    print(f"- User count: {user_count}")

    # Create test tokens for different users
    tokens = []
    for i in range(user_count):
        user_id = str(i + 1)
        token = create_test_token(user_id)
        tokens.append((user_id, token))

    # Prepare request parameters
    request_params = []
    for i in range(num_requests):
        user_id, token = tokens[i % len(tokens)]  # Round-robin through users
        request_params.append((base_url, user_id, token))

    # Track results
    results = []

    def process_request(params):
        response_time, status_code = make_authenticated_request(*params)
        return response_time, status_code

    # Execute requests concurrently
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(process_request, params) for params in request_params]

        for i, future in enumerate(futures):
            response_time, status_code = future.result()
            results.append(response_time)

            # Progress update
            if (i + 1) % max(1, num_requests // 10) == 0:
                print(f"Progress: {i + 1}/{num_requests} requests completed")

    total_time = time.time() - start_time

    # Calculate metrics
    response_times_ms = [rt * 1000 for rt in results]
    successful_requests = sum(1 for rt, sc in zip(results, [200] * len(results)) if sc == 200)

    metrics = {
        "total_requests": num_requests,
        "successful_requests": successful_requests,
        "failed_requests": num_requests - successful_requests,
        "success_rate": successful_requests / num_requests * 100,
        "total_time_seconds": total_time,
        "requests_per_second": num_requests / total_time,
        "response_times_ms": response_times_ms,
        "avg_response_time_ms": statistics.mean(response_times_ms),
        "median_response_time_ms": statistics.median(response_times_ms),
        "min_response_time_ms": min(response_times_ms),
        "max_response_time_ms": max(response_times_ms),
        "p95_response_time_ms": sorted(response_times_ms)[int(len(response_times_ms) * 0.95)],
        "p99_response_time_ms": sorted(response_times_ms)[int(len(response_times_ms) * 0.99)],
    }

    return metrics


def print_results(metrics: dict):
    """Print performance test results in a formatted way."""
    print("\n" + "="*60)
    print("PERFORMANCE TEST RESULTS")
    print("="*60)

    print(f"Total Requests:           {metrics['total_requests']}")
    print(f"Successful Requests:      {metrics['successful_requests']}")
    print(f"Failed Requests:          {metrics['failed_requests']}")
    print(f"Success Rate:             {metrics['success_rate']:.2f}%")
    print(f"Total Time (seconds):     {metrics['total_time_seconds']:.2f}")
    print(f"Requests Per Second:      {metrics['requests_per_second']:.2f}")
    print()
    print("RESPONSE TIME METRICS:")
    print(f"Average Response Time:    {metrics['avg_response_time_ms']:.2f} ms")
    print(f"Median Response Time:     {metrics['median_response_time_ms']:.2f} ms")
    print(f"Min Response Time:        {metrics['min_response_time_ms']:.2f} ms")
    print(f"Max Response Time:        {metrics['max_response_time_ms']:.2f} ms")
    print(f"P95 Response Time:        {metrics['p95_response_time_ms']:.2f} ms")
    print(f"P99 Response Time:        {metrics['p99_response_time_ms']:.2f} ms")
    print()

    # Check if performance goals are met
    avg_meets_requirement = metrics['avg_response_time_ms'] < 100
    p95_meets_requirement = metrics['p95_response_time_ms'] < 100

    print("REQUIREMENT CHECK:")
    print(f"Average < 100ms:          {'✓ PASS' if avg_meets_requirement else '✗ FAIL'}")
    print(f"P95 < 100ms:              {'✓ PASS' if p95_meets_requirement else '✗ FAIL'}")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description="Performance test for authentication middleware")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Total number of requests to make (default: 100)"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Number of concurrent requests (default: 10)"
    )
    parser.add_argument(
        "--users",
        type=int,
        default=5,
        help="Number of different users to simulate (default: 5)"
    )

    args = parser.parse_args()

    # Run the performance test
    metrics = run_performance_test(
        base_url=args.url,
        num_requests=args.requests,
        concurrency=args.concurrency,
        user_count=args.users
    )

    # Print results
    print_results(metrics)


if __name__ == "__main__":
    main()