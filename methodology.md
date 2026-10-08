# Methodology

Source: SIWES laboratory report, Department of Petroleum Engineering, Federal University of Technology, Owerri
(September 2023). Items the report does not record are marked *not recorded*.

## Muds

| | Biodiesel-based mud | Diesel-based mud |
|---|---|---|
| Base oil | biodiesel made from palm kernel oil; specific gravity 0.881 at 60/60 F | diesel; specific gravity 0.844 at 60/60 F |
| Recipe | see `data/raw/biodiesel_mud_recipe_sep2023.csv` | *not recorded* |
| Design oil:water | 70.6 : 29.4 by volume (210.2 mL oil, 87.6 mL water) | *not recorded* |

Order of addition for the biodiesel mud: base oil, primary emulsifier (10 min), lime (5 min), cellulose fluid-loss additive (5 min),
water (15 min), bentonite (5 min), barite (10 min), powdered calcium chloride (5 min).

## Biodiesel production (as recorded)

300 mL palm kernel oil heated to 65 C on a hot plate; 1.5 g sodium hydroxide dissolved in 90 mL methanol (sodium methoxide), filtered, and stirred into the hot
oil for 1 hour; the mixture was left to separate in a separating funnel into biodiesel (upper layer) and glycerin (lower layer), and the glycerin was drawn off.
Yield, wash steps and fuel-property tests (other than the specific gravity above) are not recorded in the report.

## Tests as recorded

| Property | Method |
|---|---|
| Mud weight | Mud balance, read to the nearest 0.1 lb/gal per the procedure in the report |
| pH | Litmus (pH) strip placed in the mud |
| Dial readings | Rotational viscometer, maximum dial deflection at 300 rpm and 600 rpm |
| Gel strength | Viscometer set to 300 or 600 rpm, mud agitated, left to rest 10 s (and 10 min), maximum deflection recorded. **This differs from the standard method, which reads gel strength at 3 rpm.** |
| Retort | 10 mL mud chamber, retort kit; oil, water, solids collected. The report does not state which mud was tested. |
| Filtration | "Standard filter press". Pressure, duration and temperature *not recorded* |
| Base-oil density | Hydrometer, specific gravity at 60/60 F |

## Calculations (`src/analyze.py`)

- PV (cP) = theta600 - theta300; YP (lb/100 ft2) = theta300 - PV; apparent viscosity = theta600 / 2.
- Flow index n = 3.32 log10(theta600 / theta300); consistency index K = theta300 / 511^n.
  These are two-point values. They describe the curve between 300 and 600 rpm only.
- Oil percent = oil / (oil + water) from the recipe or retort; retort solids percent = solids / chamber volume.

## What this dataset cannot support

- Any statement of statistical significance (one batch, one test per property).
- A like-for-like performance ranking of biodiesel versus diesel mud (diesel recipe not recorded, filtration conditions not recorded).
- Conclusions about thermal stability, emulsion stability, lubricity or environmental performance (not measured here).
