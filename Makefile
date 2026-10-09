.PHONY: test lint smoke pipeline clean-synthetic

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

# End-to-end run on SYNTHETIC data in an isolated workspace (data/*/_synthetic, results/_synthetic)
smoke:
	uv run vesselmind --synthetic synth
	uv run vesselmind --synthetic ingest
	uv run vesselmind --synthetic clean
	uv run vesselmind --synthetic windows
	uv run vesselmind --synthetic baselines --split val
	uv run vesselmind --synthetic plot-tracks

# Real data: validation split only. The test split is run once, manually, with --confirm-test.
pipeline:
	uv run vesselmind ingest
	uv run vesselmind clean
	uv run vesselmind windows
	uv run vesselmind baselines --split val
	uv run vesselmind plot-tracks

clean-synthetic:
	rm -rf data/raw/_synthetic data/interim/_synthetic data/processed/_synthetic results/_synthetic
