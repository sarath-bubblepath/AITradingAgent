from __future__ import annotations

from datetime import date

import typer
from rich.console import Console

from trading_agent.analysis.indicators import calculate_indicators
from trading_agent.config import get_reports_dir
from trading_agent.data.market_data import AlpacaMarketDataProvider, validate_symbol
from trading_agent.ollama_client import chat_with_ollama
from trading_agent.reporting import build_markdown_report, save_report
from trading_agent.schemas import MarketSnapshot

app = typer.Typer(help="Read-only US stock and ETF research snapshot.")
console = Console()


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to Ollama's cloud model"),
) -> None:
    """Send a prompt to the configured Ollama cloud model."""
    try:
        console.print(chat_with_ollama(prompt))
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def analyze(
    ticker: str = typer.Argument(..., help="US stock or ETF ticker, e.g. AAPL or SPY"),
    start: str = typer.Option(..., "--start", help="Start date, YYYY-MM-DD"),
    end: str = typer.Option(..., "--end", help="Inclusive end date, YYYY-MM-DD"),
) -> None:
    """Fetch daily bars, calculate indicators and save a deterministic report."""
    try:
        symbol = validate_symbol(ticker)
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        if end_date < start_date:
            raise typer.BadParameter("--end must be on or after --start.")

        console.print(f"[bold]Fetching daily bars for {symbol}...[/bold]")
        provider = AlpacaMarketDataProvider()
        bars = provider.get_daily_bars(symbol, start_date, end_date)
        indicators = calculate_indicators(bars)

        snapshot = MarketSnapshot(
            ticker=symbol,
            requested_start=start_date.isoformat(),
            requested_end=end_date.isoformat(),
            **indicators,
        )
        report = build_markdown_report(snapshot)
        output_path = save_report(report, symbol, start_date, end_date, get_reports_dir())
        console.print(report)
        console.print(f"\n[green]Saved report:[/green] {output_path.resolve()}")
    except (ValueError, RuntimeError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
