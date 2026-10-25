.PHONY: test lint smoke smoke-v3 manifests pipeline clean-synthetic

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

# End-to-end run on SYNTHETIC data in an isolated workspace (data/*/_synthetic, results/_synthetic)
smoke:
	uv run morva --synthetic synth
	uv run morva --synthetic ingest
	uv run morva --synthetic clean
	uv run morva --synthetic windows
	uv run morva --synthetic fairway
	uv run morva --synthetic baselines --split val
	uv run morva --synthetic gbm --split val
	uv run morva --synthetic gbm --split val --holdout-eval-vessels
	uv run morva --synthetic regime-report --split val
	uv run morva --synthetic baselines --split transfer_val --region bornholm
	uv run morva --synthetic gbm --split transfer_val --region bornholm
	uv run morva --synthetic regime-report --split transfer_val --region bornholm
	uv run morva --synthetic plot-tracks

# V3 end-to-end run on SYNTHETIC data (DMA + Marine Cadastre formats, calendars, 60-minute windows, intervals)
V3 := --data-config configs/v3/data.yaml --exp-config configs/v3/experiment.yaml
smoke-v3:
	uv run morva --synthetic $(V3) synth
	uv run morva --synthetic $(V3) ingest
	uv run morva --synthetic $(V3) clean
	uv run morva --synthetic $(V3) windows
	uv run morva --synthetic $(V3) fairway
	uv run morva --synthetic $(V3) baselines --split val
	uv run morva --synthetic $(V3) baselines --split transfer_val --region salish_sea
	uv run morva --synthetic $(V3) gbm --split val
	uv run morva --synthetic $(V3) gbm --split transfer_val --region salish_sea
	uv run morva --synthetic $(V3) intervals --split val
	uv run morva --synthetic $(V3) intervals --split transfer_val --region salish_sea
	uv run morva --synthetic $(V3) intervals --split transfer_val --region salish_sea --local-calibration
	uv run morva --synthetic $(V3) intervals --split val --sweep

# Provenance record (checksum, size) for every raw file; existing manifests are kept
manifests:
	uv run morva manifest data/raw/*.zip --notes "DMA daily file, study period 2026-09-19..2026-10-15"

# Real data: validation split only. The test split is run once, manually, with --confirm-test.
pipeline: manifests
	uv run morva ingest
	uv run morva clean
	uv run morva windows
	uv run morva baselines --split val
	uv run morva plot-tracks

clean-synthetic:
	rm -rf data/raw/_synthetic data/raw/us/_synthetic data/interim/_synthetic data/processed/_synthetic \
		data/v3/interim/_synthetic data/v3/processed/_synthetic results/_synthetic results/v2/_synthetic \
		results/v3/_synthetic
