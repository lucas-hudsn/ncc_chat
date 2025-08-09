"""This module provides the main entry point for running the ETL pipeline.
It extracts data from the NCC PDFs, transforms it into parent and child chunks,
and loads it into a vector store for further processing."""

from .main import run_etl_pipeline