# Biodiesel-based vs diesel-based drilling mud: laboratory comparison

[![reproduce-and-test](https://github.com/amyonuha-source/drilling-fluid-research-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/amyonuha-source/drilling-fluid-research-portfolio/actions)

Data and reproducible analysis for a biodiesel-based synthetic drilling mud and a conventional diesel-based mud, tested side by side in the
Petroleum Engineering laboratory at the Federal University of Technology, Owerri (SIWES placement, September 2023).

**What I did:** I produced biodiesel from palm kernel oil (300 mL of oil reacted with a methanol and sodium hydroxide solution at 65 °C for one hour, then
the biodiesel was separated from the glycerin), used it as the base oil of a synthetic mud, and tested it against a diesel-based mud for mud weight, pH, rheology,
gel strength and filtration.

![Rheology profile](results/figures/fig1_rheology_profile.png)

## Question and answer

**Question:** can a biodiesel-based mud match a diesel-based mud on the standard properties?

**Answer from these data:** it is comparable on mud weight (11.15 vs 11.3 ppg) but, in this single batch, it did **not** match on filtration or on flow-curve shape.

| Property | Biodiesel mud | Diesel mud | Reading |
|---|---|---|---|
| Mud weight | 11.15 ppg | 11.3 ppg | Similar |
| Plastic viscosity (calculated) | 75 cP | 17 cP | Biodiesel mud is far more viscous |
| Yield point (calculated) | 10 lb/100 ft² | 13 lb/100 ft² | Slightly lower for biodiesel |
| YP / PV | 0.13 | 0.76 | Biodiesel mud is viscosity-dominated, which generally means poorer cuttings suspension at a given viscosity |
| Flow index n (two-point) | 0.91 | 0.65 | Biodiesel mud is close to Newtonian; diesel mud is more shear-thinning |
| Filtrate / cake | 10.8 mL / 8/32 in | none recorded | Conditions not recorded (see below) |
| pH (litmus) | 9 | 8 | Not interpretable for oil-continuous muds |
| Gel strength 10 s / 10 min | 105 / 82 | 32 / 24 | **Not standard values, see below** |

"Higher rheology" is not an advantage by itself: the biodiesel mud's higher dial readings come from plastic viscosity, not yield point.

![Gel strength and filtration](results/figures/fig2_gel_and_filtration.png)

## Data-quality flags (please read)

- **Gel strengths.** In both muds the 10 s gel exceeds the 10 min gel, and both exceed the 300 rpm dial reading. The recorded procedure sets the viscometer to 300 or 600 rpm for gels instead of the standard 3 rpm. Treat the gel numbers as comparable *between these two muds* only.
- **Filtration.** The filter-press pressure, duration and temperature were not recorded and the diesel mud recipe is not documented. Oil-continuous muds normally yield little or no filtrate at low pressure, so "none" mostly reflects fluid type. The informative result is that the biodiesel mud produced 10.8 mL and an 8/32 in cake. A well-emulsified oil-continuous mud would be expected to give much less, so emulsion quality is the first thing to check.
- **Retort.** A retort result is in the source report (oil 5.2, water 2.9, solids 1.9 mL per 10 mL) but is not labelled with a mud. If it was the biodiesel mud, the water fraction (35.8 %) is higher than the recipe (29.4 %) and solids are 19 vol %. It is stored in `data/raw/retort_sample_unassigned.csv` and excluded from the figures.

Full details: [`docs/data_quality_notes.md`](docs/data_quality_notes.md).

## Biodiesel mud recipe

210.2 mL biodiesel, 87.6 mL water (design oil:water 70.6 : 29.4), 8.7 mL primary emulsifier, 4 g lime, 1 g cellulose fluid-loss additive,
6 g bentonite, 10 g calcium chloride, 186.3 g barite. Order and mixing times are in `data/raw/biodiesel_mud_recipe_sep2023.csv`.
The diesel mud recipe was not recorded.

## Run it

```bash
git clone https://github.com/amyonuha-source/drilling-fluid-research-portfolio.git
cd drilling-fluid-research-portfolio
pip install -r requirements.txt
python -m src.analyze      # derived properties + data-quality flags -> results/tables/
python -m src.figures      # figures -> results/figures/
pip install -r requirements-dev.txt && python -m pytest -q
```

## Repository layout

```text
data/raw/          mud comparison table, biodiesel recipe, unassigned retort result
data/metadata/     data_dictionary.csv
src/               config.py · data.py · analyze.py · figures.py
tests/             derivation tests (also run in CI)
results/tables/    derived properties, data-quality flags, oil/water summary
results/figures/   fig1 rheology, fig2 gel and filtration
docs/              methodology.md · data_quality_notes.md
```

## Limitations

- One batch of each mud, one test per property: no replicates, no uncertainty estimate, no significance testing.
- The diesel mud recipe and the filtration test conditions are not recorded, so the filtration contrast is not a controlled comparison.
- Flow index and consistency index are two-point values from 300 and 600 rpm readings only; there is no full flow-curve data in this repository.
- No HPHT filtration, electrical stability, aging or temperature data for this pair of muds.
- Measured at a single laboratory, with a hand-operated viscometer reading maximum dial deflection (as described in the source report).


## Cite

See [`CITATION.cff`](CITATION.cff). Code is MIT-licensed (see `LICENSE`).

**Author:** Chiamaka Onuh, Federal University of Technology, Owerri.
