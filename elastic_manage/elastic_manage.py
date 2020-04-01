#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
import pprint
import click
import json
import pkg_resources

from sre_tools import sreElastic


@click.group()
def cli():
    """CLI for Elasticsearch"""


@cli.command(name="indices")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--node", type=str, required=False, default=None, help="List only indices from specific data node")
def show_elasticsearch_indices(cluster: str, node: str):
    """Show elasticsearch indices with additional information"""

    elastic = sreElastic(host=cluster)
    elastic.list_indices(only_this_node=node)


@cli.command(name="wait")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
def wait_for_elasticsearch_index(cluster: str, index: str):
    """Wait until index relocating"""

    elastic = sreElastic(host=cluster)
    elastic.wait_index_relocation(index=index)


@cli.command(name="fix-shards")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
def fix__elasticsearch_index_allocation(cluster: str, index: str):
    """Fix index allocation to the current data nodes."""

    elastic = sreElastic(host=cluster)
    elastic.index_fix(index=index)


@cli.command(name="reset-allocation")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
def reset_elasticsearch_index_allocation(cluster: str, index: str):
    """Reset index allocation (remove allocation settings)."""

    elastic = sreElastic(host=cluster)
    elastic.index_reset(index=index)


@cli.command(name="info")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
def show_elasticsearch_index_info(cluster: str, index: str):
    """Show index allocation and routing settings."""

    elastic = sreElastic(host=cluster)
    pp = pprint.PrettyPrinter(indent=2, width=120)

    print("\nLocation:")
    pp.pprint(elastic.get_index_location(index))
    print("\nRouting:")
    pp.pprint(elastic.get_index_routing(index))
    print("\n")


cli.command(name="shards-per-node")


@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
@click.option("--number", type=int, required=True, help="Number of shards per node")
def setup_index_shards_per_node(cluster: str, index: str, number: int):
    """Set number of shards per one node setting."""

    elastic = sreElastic(host=cluster)
    elastic.set_number_shards_per_node(index=index, number=number)


@cli.command(name="delete-index")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name")
def delete_elasticsearch_index(cluster: str, index: str):
    """Delete index."""

    elastic = sreElastic(host=cluster)
    elastic.delete_index(index=index)


@cli.command(name="add-replica")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name.")
@click.option("--force", is_flag=True, help="Do without confirmation.")
def add_one_replica_to_elasticsearch_index(cluster: str, index: str, force: bool = False):
    """Delete index."""

    elastic = sreElastic(host=cluster)
    elastic.incr_replica_amount(index=index, without_confirmation=force)


@cli.command(name="remove-replica")
@click.option("--cluster", type=str, required=True, help="Elasticsearch cluster address")
@click.option("--index", type=str, required=True, help="Elasticsearch index name.")
@click.option("--force", is_flag=True, help="Do without confirmation.")
def add_one_replica_to_elasticsearch_index(cluster: str, index: str, force: bool = False):
    """Delete index."""

    elastic = sreElastic(host=cluster)
    elastic.decr_replica_amount(index=index, without_confirmation=force)


@cli.command(name="version")
def default():
    """Show version and exit."""
    version = pkg_resources.require("elastic-manage")[0].version
    print(f"v{version}\n\n")


if __name__ == "__main__":
    cli()
