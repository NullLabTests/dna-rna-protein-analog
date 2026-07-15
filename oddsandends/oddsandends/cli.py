import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from . import tokenizer, cost, prompt, context, format as fmt, config

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="oddsandends")
def cli():
    pass


@cli.group("tokens")
def tokens():
    """Token counting and estimation."""


@tokens.command("count")
@click.argument("text", required=False)
@click.option("--model", "-m", default=None, help="Model name (default from config)")
@click.option("--file", "-f", "filepath", type=click.Path(exists=True), help="Read from file")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def tokens_count(text, model, filepath, as_json):
    """Count tokens in text or file."""
    if filepath:
        text = Path(filepath).read_text()
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()
    if not text:
        raise click.UsageError("Provide text as argument, --file, or pipe stdin")

    model = model or config.get_default_model()
    result = tokenizer.format_token_count(text, model)

    if as_json:
        click.echo(json.dumps(result, indent=2))
        return

    console.print(f"[bold]Model:[/] {result['model']}")
    if result["exact"] is not None:
        console.print(f"[bold]Exact tokens:[/] {result['exact']}")
    console.print(f"[bold]Estimated tokens:[/] {result['estimated']}")
    console.print(f"[bold]Characters:[/] {result['characters']}")
    console.print(f"[bold]Words:[/] {result['words']}")


@tokens.command("check")
@click.argument("text", required=False)
@click.option("--model", "-m", default=None)
@click.option("--file", "-f", "filepath", type=click.Path(exists=True))
@click.option("--output-tokens", "-o", default=2048, help="Tokens to reserve for output")
def tokens_check(text, model, filepath, output_tokens):
    """Check if text fits in model's context window."""
    if filepath:
        text = Path(filepath).read_text()
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()
    if not text:
        raise click.UsageError("Provide text as argument, --file, or pipe stdin")

    model = model or config.get_default_model()
    token_count = tokenizer.count_tokens(text, model)
    result = context.check_fit(token_count, model, reserve_output=output_tokens)

    if result.get("error"):
        raise click.ClickException(result["error"])

    status = "✓ Fits" if result["fit"] else "✗ Overshoots"
    console.print(f"[bold]Model:[/] {result['model']}")
    console.print(f"[bold]Context window:[/] {result['context_window']}")
    console.print(f"[bold]Your tokens:[/] {result['token_count']}")
    console.print(f"[bold]Reserved for output:[/] {result['reserved_output']}")
    console.print(f"[bold]Available for input:[/] {result['available_for_input']}")
    console.print(f"[bold]{status}[/]" if result["fit"] else f"[bold red]{status} by {result['overshoot_by']} tokens[/]")


@cli.group("cost")
def cost_group():
    """Cost estimation for LLM API calls."""


@cost_group.command("estimate")
@click.option("--input", "input_tokens", type=int, required=True, help="Input token count")
@click.option("--output", "output_tokens", type=int, required=True, help="Output token count")
@click.option("--model", "-m", default=None)
def cost_estimate(input_tokens, output_tokens, model):
    """Estimate API cost for a given token usage."""
    model = model or config.get_default_model()
    result = cost.calculate_cost(input_tokens, output_tokens, model)

    if "error" in result:
        raise click.ClickException(result["error"])

    total = result["total_cost"]
    unit = "¢" if total < 1 else "$"
    display = total * 100 if total < 1 else total

    console.print(f"[bold]Model:[/] {result['model']}")
    console.print(f"[bold]Input tokens:[/] {result['input_tokens']:,}")
    console.print(f"[bold]Output tokens:[/] {result['output_tokens']:,}")
    console.print(f"[bold]Input cost:[/] ${result['input_cost']:.6f}")
    console.print(f"[bold]Output cost:[/] ${result['output_cost']:.6f}")
    console.print(f"[bold]Total:[/] {unit}{display:.4f}" if total < 1 else f"[bold]Total:[/] ${display:.4f}")
    console.print(f"[dim]Pricing: ${result['pricing_per_1m']['input']}/M input, ${result['pricing_per_1m']['output']}/M output[/]")


@cost_group.command("models")
def cost_models():
    """List all supported models with pricing."""
    models = cost.list_models()
    table = Table(title="Supported Models & Pricing")
    table.add_column("Model", style="cyan")
    table.add_column("Input ($/1M)", justify="right")
    table.add_column("Output ($/1M)", justify="right")
    for m in models:
        table.add_row(m["model"], str(m["input_price"]), str(m["output_price"]))
    console.print(table)


@cli.group("prompt")
def prompt_group():
    """Prompt template utilities."""


@prompt_group.command("render")
@click.option("--template", "-t", type=click.Path(exists=True), help="Template file path")
@click.option("--var", "-v", "vars", multiple=True, help="Variables as key=value")
@click.argument("inline_template", required=False)
def prompt_render(template, vars, inline_template):
    """Render a prompt template with variables."""
    if template:
        tmpl = prompt.load_template(template)
    elif inline_template:
        tmpl = inline_template
    elif not sys.stdin.isatty():
        tmpl = sys.stdin.read()
    else:
        raise click.UsageError("Provide a template string, --template file, or pipe stdin")

    kwargs = {}
    for v in vars:
        if "=" not in v:
            raise click.BadParameter(f"Variables must be key=value, got: {v}")
        key, val = v.split("=", 1)
        kwargs[key] = val

    try:
        result = prompt.render(tmpl, **kwargs)
        click.echo(result)
    except KeyError as e:
        raise click.ClickException(str(e))


@prompt_group.command("vars")
@click.argument("template_file", type=click.Path(exists=True))
def prompt_vars(template_file):
    """Extract variable names from a template."""
    tmpl = Path(template_file).read_text()
    variables = prompt.extract_variables(tmpl)
    for v in variables:
        click.echo(v)


@cli.group("config")
def config_group():
    """Manage oddsandends configuration."""


@config_group.command("show")
def config_show():
    """Show current configuration."""
    cfg = config.show()
    console.print(json.dumps(cfg, indent=2))


@config_group.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a config value."""
    cfg = config.set_config(key, value)
    console.print(f"[green]✓[/] Set {key}={value}")


@config_group.command("get")
@click.argument("key")
def config_get(key):
    """Get a config value."""
    val = config.get(key)
    if val is None:
        raise click.ClickException(f"Key not found: {key}")
    click.echo(val)


@cli.group("format")
def format_group():
    """Data format conversion."""


@format_group.command("json")
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option("--yaml", "to_format", flag_value="yaml", help="Convert to YAML")
@click.option("--csv", "to_format", flag_value="csv", help="Convert to CSV")
@click.option("--table", "to_format", flag_value="table", help="Convert to ASCII table")
def format_convert(file, to_format):
    """Convert JSON to other formats."""
    if file:
        data = fmt.from_json(Path(file).read_text())
    elif not sys.stdin.isatty():
        data = fmt.from_json(sys.stdin.read())
    else:
        raise click.UsageError("Provide a file or pipe JSON")

    if to_format == "yaml":
        click.echo(fmt.to_yaml(data))
    elif to_format == "csv":
        if isinstance(data, dict):
            data = [data]
        click.echo(fmt.to_csv(data))
    elif to_format == "table":
        if isinstance(data, dict):
            data = [data]
        console.print(fmt.to_table(data))
    else:
        click.echo(fmt.to_json(data))


@cli.command()
def version():
    """Show version info."""
    console.print(f"oddsandends v{__version__}")


if __name__ == "__main__":
    cli()
