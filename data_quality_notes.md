# Data-quality notes

These checks run automatically (`python -m src.analyze` writes `results/tables/data_quality_flags.csv`).

## 1. Gel strengths are not standard 3 rpm values
- The biodiesel mud's 10 s gel (105 lb/100 ft2) is above its 10 min gel (82) and above its 300 rpm dial reading (85).
- The diesel mud shows the same pattern: 10 s gel 32 vs 10 min gel 24, and 10 s gel (32) above its 300 rpm dial (30).
- Gel strength normally builds with rest time and is read at 3 rpm, where dial readings are far below the 300 rpm reading.
- The procedure recorded in the source report sets the viscometer to 300 or 600 rpm for the gel test. That is the likely cause, and it
  applies to both muds, so the *comparison between the two* is on a like-for-like basis. The values should not be compared with published
  gel strengths or used for hole-cleaning calculations.

## 2. Zero filtrate for the diesel mud
- "No filtrate or mud cake" is plausible for an oil-continuous mud at low pressure, but the filter-press conditions and the diesel recipe are not recorded.
- The result is reported as "none recorded", not as 0 mL, in the figures.

## 3. Retort sample not identified
- The retort result (oil 5.2, water 2.9, solids 1.9 mL in 10 mL) is not labelled with a mud in the source.
- If it was the biodiesel mud, the oil:water ratio (64.2 : 35.8) is water-richer than the recipe (70.6 : 29.4) and the 70 : 30 ratio listed for 11-14 ppg in the report, and solids are 19 vol %.
  It is kept in `data/raw/retort_sample_unassigned.csv` and is excluded from the figures until the sample is confirmed.

## 4. pH
- Litmus strips respond to the aqueous phase and resolve about 0.5-1 pH unit, so a pH 9 vs 8 difference in oil-continuous muds should not be interpreted.

## 5. Feedstock naming
- The biodiesel was made from palm kernel oil (production section of the source report and the author's confirmation). One heading in the same report, above the mud recipe, says "soya-bean bio-diesel based drilling fluid", and the mud-weight line repeats "soyabean". These are treated as labelling slips in the report; the production procedure itself uses palm kernel oil only.
