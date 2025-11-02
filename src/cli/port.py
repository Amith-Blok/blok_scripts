import typer
from rich import print
from typing import List, Optional
from src.pipeline.sea_freight_db_pipeline import sea_freight_db_pipeline

app = typer.Typer()


@app.command()
def sea_freight(
    run_list: Optional[List[str]] = typer.Argument(
        None,
        help="List of regions to process (e.g., EU NA OC ME FE CN AF SA IS CA). If not provided, runs all regions.",
    ),
    dont_run_list: Optional[List[str]] = typer.Option(
        None, "--exclude", "-e", help="List of regions to exclude from processing"
    ),
):
    # Default list of all regions
    all_regions = ["EU", "NA", "OC", "ME", "FE", "CN", "AF", "SA", "IS", "CA"]

    # If run_list is not provided, use all regions
    if run_list is None:
        run_list = all_regions

    # Filter out regions in dont_run_list
    if dont_run_list:
        run_list = [region for region in run_list if region not in dont_run_list]

    print(f"[bold green]Processing regions:[/bold green] {', '.join(run_list)}")
    sea_freight_db_pipeline(run_list=run_list)


if __name__ == "__main__":
    app()
