"""Command-line interface for AgentMd."""

import click
import uvicorn

from agentmd.config import settings
from agentmd.server import create_app
from agentmd.utils import get_logger

logger = get_logger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AgentMd - unified AI provider container."""
    pass


@cli.command()
@click.option("--host", default=settings.host, help="Server host")
@click.option("--port", default=settings.port, type=int, help="Server port")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def server(host: str, port: int, reload: bool):
    logger.info(f"Starting AgentMd server on {host}:{port}")
    app = create_app()
    uvicorn.run(app, host=host, port=port, reload=reload)


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("tag", type=str)
def create_vector(input_path: str, tag: str):
    click.echo(f"Vector creation for {input_path} with tag {tag} not implemented yet")


@cli.command()
@click.argument("input_text", type=str)
def llama_test(input_text: str):
    click.echo(f"Llama/Ollama testing for '{input_text}' not implemented yet")


def main():
    cli()


if __name__ == "__main__":
    main()
