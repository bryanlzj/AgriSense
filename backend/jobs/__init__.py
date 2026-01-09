"""
Background Jobs Package

This package contains scheduled background jobs for AgriSense.

Jobs:
- Weather check: Fetches weather and generates alerts
- Pest risk check: Checks pest-weather correlations and generates alerts
"""

from .scheduler import start_scheduler, stop_scheduler

__all__ = ["start_scheduler", "stop_scheduler"]
