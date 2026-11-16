# Age gaps & hierarchical relationships — reproducibility materials

Code, transcribed published summary statistics, numerical checks, and figures accompanying a methodological review of Date Psychology's [“Age Gaps & Hierarchical Relationships” (2023)](https://datepsychology.com/age-gaps-hierarchical-relationships/), with a limited comparison to the [2024 follow-up](https://datepsychology.com/is-age-gap-disapproval-a-form-of-intrasexual-competition/).

> **Scope:** This is a **reconstruction from published, rounded aggregate statistics**, **not** an independent replication or reanalysis using individual participant data. Alexander's original survey microdata, questionnaire-level data, and original analysis code were not available for the audit. No synthetic participant data are generated or represented as observed data.

## Contents

| File | Purpose |
| --- | --- |
| `reproduce_age_gaps.py` | Runs checks, prints reconstructed statistics, regenerates the five PNG figures. |
| `age_gap_2023_group_stats.csv` | Published sex-specific group sizes, means, and SDs from 2023 for two approval scores. |
| `age_gap_2023_vignette_means.csv` | Four published means comparing age-controlled nominal gap size. |
| `age_gap_2024_age_correlations.csv` | Published age–approval correlations and confidence limits for the 2024 follow-up. |
| `glaser_1986_retrospective.csv` | Reported recalled-at-the-time versus current evaluations of educator–student sexual contact. |
| `student_professor_initiation.csv` | Initiation counts from Bellas & Gossett (plotted), plus Skeen & Nielsen (contextual cross-check). |
| `gignac_2016_correlations.csv` | Correlation-scale effect-size benchmarks misidentified as Cohen’s d in the 2023 article. |
| `other_reported_statistics.csv` | Published ANOVA, Bayes-factor, and relationship-prevalence numbers used for arithmetical checks. |
| `source_manifest.csv` | Sources, data provenance, access scope, and original locations. |
| `reconstruction_results.txt` | Expected reference output from the script. |
| `01_corrected_effect_sizes.png` | Corrected pooled-SD Cohen's d comparisons, without inferential CIs. |
| `02_followup_correlations.png` | 2024 reported Pearson correlations and *author-provided* 95% CIs. |
| `03_same_gap_different_ages.png` | 2023 reported vignette means for matched nominal gap sizes. |
| `04_glaser_recalled_assessments.png` | Glaser & Thorpe (1986) retrospective reported percentages. |
| `05_bellas_initiation.png` | Bellas & Gossett (2001) initiation counts among 20 relationships. |
| `requirements.txt` | Python dependencies. |

## Reproduce

Requires Python 3.10 or later. From the repository directory:

```bash
python -m pip install -r requirements.txt
python reproduce_age_gaps.py
```

This regenerates the five PNG files, prints all arithmetic checks, and writes `reconstruction_results.txt`. Existing files with these names will be overwritten. Run `python reproduce_age_gaps.py --output-dir /some/other/folder` to write outputs elsewhere without overwriting tracked files.

To perform a basic consistency test:

```bash
python reproduce_age_gaps.py --validate-only
```

## What is reconstructed (and what is not)

1. **Sex differences**: Pooled-SD Cohen's d is calculated from the published 2023 *n*, group means and SDs. The resulting values are approximately **0.69** for age-gap approval and **0.47** for hierarchical approval, whereas the text assigns 0.47 and 0.68 respectively. Welch's t calculated from rounded summaries approximately matches the article's t statistics; exact last digits may differ due to rounding. These are *descriptive standardized differences*, not evidence about cause.
2. **Correlation-vs-d benchmark**: Gignac & Szodorai (2016) use **r = .10, .20, .30** as small, typical, and relatively large correlations. Under an equal-group illustration, **r = .30 corresponds to d ≈ .63**, not d = .30. The effect-size reference therefore cannot be applied as quoted.
3. **ANOVA arithmetic**: The reported `F(2,343) = 0.952` implies partial eta-squared of approximately **0.0055**, not the article's **0.0287**, assuming the statistic and degrees of freedom refer to the same conventional ANOVA. We cannot determine which original value is erroneous.
4. **Bayes-factor labeling**: Under standard notation, `BF01 = 0.0228` favors the **alternative** by approximately `1 / 0.0228 = 43.86:1`, not the null. If the intended label were `BF10 = 0.0228`, the author's verbal interpretation would have the stated direction. This is a notation/interpretation conflict, **not** an independently computed Bayes factor.
5. **Prevalence percentages**: The sex-specific percentages correspond to approximately ten men and one woman, or **11 / 346 = 3.18%**, versus the text's **3.4%**. A different denominator (e.g., missing answers) could explain the discrepancy; the package cannot resolve it.
6. **2023 vignette means**: The 5- and 10-year comparisons reproduce the means **as reported**. The figure does not establish that absolute age, rather than other vignette characteristics, *caused* responses. The responses are from repeated ratings, but individual-level covariance is not available: the paper's original unpaired t-tests are **not rerun** here as if independent observations existed.
7. **2024 follow-up**: Pearson r and 95% CI endpoints are **transcribed directly** from Alexander (2024); they are not re-estimated from unknown raw observations. The male count of 452 is **inferred** as 655 total minus 203 women; the original text reports sample sex as about 31% female.
8. **Earlier research**: The Glaser & Thorpe percentages and Bellas & Gossett initiation counts are **transcriptions**, not new analyses. The former reflect retrospective judgments collected at a single time point and have measure-specific denominators. The Bellas counts describe 20 selected relationships; Skeen counts describe 25 interview accounts, **not** representative prevalence estimates.

## Limitations and interpretation

- Small differences in the final decimals of Welch statistics are expected because the original summary measures were rounded.
- This repository does **not** reproduce Alexander's correlations, regressions, model selection, original Bayesian analysis, repeated-measures comparisons, or distributions from participant-level data. Nor does it prove the author's actual program executed the invalid comparison; the apparent pairing problem is based on the reported degrees of freedom and description.
- The five plots deliberately contain no invented standard errors or confidence intervals; error bars are shown only where the 2024 author supplied confidence intervals.
- The figures depict **reported summaries**, not relationship outcomes in a representative population. No causal claims about jealousy, exploitation, partner control, or power imbalances follow from these plots.
- Source articles, their images/screenshots, and copyrighted PDFs are **not redistributed**. See `source_manifest.csv` for URLs and page/section references. Skeen & Nielsen was checked through an accessible transcription rather than a publisher PDF.

## Principal sources

- [Alexander (2023), *Age Gaps & Hierarchical Relationships*](https://datepsychology.com/age-gaps-hierarchical-relationships/).
- [Alexander (2024), *Is Age Gap Disapproval a Form of Intrasexual Competition?*](https://datepsychology.com/is-age-gap-disapproval-a-form-of-intrasexual-competition/).
- [Glaser & Thorpe (1986), *Unethical Intimacy*](https://doi.org/10.1037/0003-066X.41.1.43), *American Psychologist* 41, 43–51.
- [Bellas & Gossett (2001), *Love or the “Lecherous Professor”*](https://doi.org/10.1111/j.1533-8525.2001.tb01779.x), *The Sociological Quarterly* 42, 529–558.
- [Skeen & Nielsen (1983), *Student-Faculty Sexual Relationships*](https://doi.org/10.1007/BF00987082).
- [Gignac & Szodorai (2016), *Effect size guidelines for individual differences researchers*](https://doi.org/10.1016/j.paid.2016.06.069).

The companion Substack critique contains the full substantive argument and additional sources; this repository covers the calculations and figures only.
