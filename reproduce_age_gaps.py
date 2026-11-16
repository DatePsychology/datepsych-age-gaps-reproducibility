#!/usr/bin/env python3
"""Recreate figures and arithmetic checks from *published summary numbers only*.

No raw survey participant data or original models are claimed or simulated.
Run with: python reproduce_age_gaps.py [--output-dir PATH] [--validate-only]
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent
BLUE = '#28647e'
SLATE = '#7698a7'
RUST = '#b57e49'
SAND = '#d6aa7f'


def load_csv(name):
    with (ROOT / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def nice_number(value, digits=2):
    return f'{value:.{digits}f}'


def reconstruct():
    rows = load_csv('age_gap_2023_group_stats.csv')
    tests = {}
    for outcome in ('Age-gap approval', 'Hierarchical approval'):
        m = next(r for r in rows if r['outcome'] == outcome and r['group'] == 'Men')
        w = next(r for r in rows if r['outcome'] == outcome and r['group'] == 'Women')
        n1,n2 = int(m['n']),int(w['n'])
        mu1,mu2 = float(m['mean']),float(w['mean'])
        s1,s2 = float(m['sd']),float(w['sd'])
        pooled = math.sqrt(((n1 - 1)*s1*s1 + (n2 - 1)*s2*s2)/(n1 + n2 - 2))
        d = (mu1 - mu2) / pooled
        se2 = s1*s1/n1 + s2*s2/n2
        t = (mu1 - mu2) / math.sqrt(se2)
        df = se2*se2 / ((s1*s1/n1)**2/(n1 - 1) + (s2*s2/n2)**2/(n2 - 1))
        p = 2 * stats.t.sf(abs(t),df)
        tests[outcome] = dict(d=d,t=t,df=df,p=p,article_d=float(m['article_reported_d']),
                              difference=mu1-mu2,n_male=n1,n_female=n2)
    assert 0.67 < tests['Age-gap approval']['d'] < 0.70
    assert 0.45 < tests['Hierarchical approval']['d'] < 0.49

    guidelines = load_csv('gignac_2016_correlations.csv')
    others = load_csv('other_reported_statistics.csv')
    get = lambda name: next(r for r in others if r['item'] == name)
    Frow = get('Political ANOVA F')
    F = float(Frow['reported_value'])
    df1,df2 = int(Frow['df1']),int(Frow['df2'])
    eta = F*df1 / (F*df1 + df2)
    bf = float(get('Bayes factor labeled BF01')['reported_value'])
    total_male = int(next(r for r in rows if r['group']=='Men')['n'])
    total_female = int(next(r for r in rows if r['group']=='Women')['n'])
    male_events = round(total_male * float(get('Men reported professor relationship, percent')['reported_value']) / 100)
    female_events = round(total_female * float(get('Women reported professor relationship, percent')['reported_value']) / 100)
    implied_rate = (male_events + female_events)/(total_male + total_female)*100

    vign = load_csv('age_gap_2023_vignette_means.csv')
    correlations = load_csv('age_gap_2024_age_correlations.csv')
    glaser = load_csv('glaser_1986_retrospective.csv')
    initiation = load_csv('student_professor_initiation.csv')
    by_study = {}
    for row in initiation:
        by_study.setdefault(row['study'],{})[row['category']] = int(row['count'])
    assert sum(by_study['Bellas & Gossett (2001)'].values()) == 20
    assert sum(by_study['Skeen & Nielsen (1983)'].values()) == 25
    assert len(vign) == 4 and len(correlations)==2 and len(glaser)==3
    for x in correlations:
        assert float(x['ci_lower']) <= float(x['r']) <= float(x['ci_upper'])
    assert male_events == 10 and female_events == 1

    results = [
        'Age-gap relationships — reconstruction from published aggregate statistics',
        '=======================================================================',
        'Source: Alexander (2023) and (2024) unless otherwise noted.',
        'These are not recomputations from the original participant-level data.',
        '',
        '2023 sex differences (men minus women; pooled-SD Cohen d):',
    ]
    for name in ('Age-gap approval','Hierarchical approval'):
        q = tests[name]
        results.append(f"  {name}: d = {q['d']:.5f}; reported text d = {q['article_d']:.2f}; "
                       f"Welch t ~= {q['t']:.3f}; df ~= {q['df']:.2f}; p ~= {q['p']:.7g} "
                       '(approximate because published means and SDs are rounded)')
    results += [
        '',
        'Gignac & Szodorai (2016) r benchmarks (not Cohen d):',
    ]
    for row in guidelines:
        r = float(row['reported_r'])
        d_equal_groups = 2*r/math.sqrt(1-r*r)
        results.append(f"  {row['benchmark']}: r={r:.2f}; conversion to d (equal-size two-group approximation)={d_equal_groups:.3f}.")
    results += [
        '  These benchmark correlations are not d; conversion is illustrative, not a claim of equivalent study designs.',
        '',
        'Arithmetic of political ANOVA:',
        f'  F({df1},{df2}) = {F} => partial eta^2 = {eta:.6f} (article reports 0.0287).',
        '',
        'Bayes factor, standard notation:',
        f'  If BF01 = {bf}, BF10 = 1 / BF01 = {1/bf:.4f}, i.e. favors alternative.',
        '  If author meant BF10 = 0.0228, interpretation favoring null would instead have that direction.',
        '  This is a label/interpretation discrepancy, not an independently estimated Bayes factor.',
        '',
        'Reported professor-relationship prevalence:',
        f'  Reconstructed integers from sex-specific rates: {male_events} men + {female_events} woman = '
        f'{male_events+female_events} / {total_male+total_female} = {implied_rate:.4f}%.',
        '  Article overall estimate = 3.4%; missing outcome responses/different denominator not known.',
        '',
        '2024 age–approval correlations (published CIs; transcribed, NOT recomputed):',
    ]
    for c in correlations:
        results.append(f"  {c['group']}: n={c['n']} ({c['n_status']}), r={float(c['r']):+.2f}, "
                       f"95% CI [{float(c['ci_lower']):+.2f}, {float(c['ci_upper']):+.2f}]")
    results.extend(['', 'Matched nominal-gap vignette means (source-reported):'])
    for gap in (5,10):
        matches=sorted((v for v in vign if int(v['nominal_gap_years'])==gap),key=lambda v:int(v['woman_age']))
        results.append(f"  {gap}-year gap: {matches[0]['woman_age']}/{matches[0]['man_age']} -> {matches[0]['mean_approval']}; "
                       f"{matches[1]['woman_age']}/{matches[1]['man_age']} -> {matches[1]['mean_approval']}; "
                       f"difference={float(matches[1]['mean_approval'])-float(matches[0]['mean_approval']):+.2f} points.")
    results.extend(['','Student-professor initiation counts (transcribed):'])
    for study,cats in by_study.items():
        results.append(f"  {study}: professor alone={cats['Professor alone']}, "
                       f"student alone={cats['Student alone']}, mutually initiated={cats['Mutually initiated']}")
    results.extend([
        '',
        'Analysis limitations:',
        '  No raw microdata; no unobserved standard errors, within-person correlations, or CIs invented.',
        '  No original regression, Bayesian ANOVA, or vignette paired t-test reanalysis is claimed.',
        '  All Glaser 1986 values are retrospective perceptions recalled in one survey.',
        '  Figures use source-reported age-gap vignette means and historical counts.',
    ])
    return tests, vign, correlations, glaser, by_study, '\n'.join(results) + '\n'


def run_figures(output_dir, tests, vign, correlations, glaser, by_study):
    # Matplotlib imported only when generating figures (not for --validate-only).
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator

    plt.rcParams.update({
        'font.family':'DejaVu Sans',
        'font.size':11,
        'savefig.facecolor':'white',
        'axes.labelcolor':'#333333',
        'text.color':'#202124',
        'axes.edgecolor':'#777777',
        'axes.spines.top':False,
        'axes.spines.right':False,
        'axes.grid':False,
    })

    def start(height):
        fig,ax = plt.subplots(figsize=(10.2125,height/160),dpi=160)
        fig.patch.set_facecolor('white')
        ax.set_axisbelow(True)
        ax.grid(axis='x',alpha=.10, linewidth=.7)
        return fig,ax

    def save(fig,name):
        fig.savefig(output_dir / name, dpi=160, facecolor='white', bbox_inches=None)
        plt.close(fig)

    # Figure 01: direct recalculated d, not adjusted coefficients.
    fig,ax=start(590)
    outcomes=['Age-gap approval','Hierarchical approval']
    ds=[tests[x]['d'] for x in outcomes]
    y=np.arange(2)
    bars=ax.barh(y,ds,color=[BLUE,SLATE],height=.52)
    ax.set_yticks(y,outcomes)
    ax.invert_yaxis()
    ax.set_xlim(0,.83)
    ax.set_xlabel("Cohen's d (men minus women, pooled SD)")
    for b,v in zip(bars,ds):ax.text(v+.012,b.get_y()+b.get_height()/2,f'{v:.2f}',va='center',fontsize=12,weight='bold')
    fig.subplots_adjust(left=.22,right=.97,top=.94,bottom=.23)
    save(fig,'01_corrected_effect_sizes.png')

    # Figure 02: intervals provided in original article, not calculated from n.
    fig,ax=start(608)
    corr={r['group']:r for r in correlations}
    for label,ypos,color in [('Men',1,BLUE),('Women',0,RUST)]:
        c=corr[label];r=float(c['r']); lo=float(c['ci_lower']); hi=float(c['ci_upper']);n=int(c['n'])
        ax.errorbar([r],[ypos],xerr=[[r-lo],[hi-r]],fmt='o',markersize=8,
                    color=color,ecolor=color,capsize=0,elinewidth=3)
        ax.text(hi+.018,ypos,f'r={r:.2f}  [{lo:.2f}, {hi:.2f}]',va='center',fontsize=10)
    ax.axvline(0,linestyle=':',linewidth=1.2,color='#888888')
    ax.set_ylim(-.7,1.7);ax.set_yticks([1,0],['Men (n ≈ 452)','Women (n = 203)'])
    ax.set_xlim(-.2,.58)
    ax.set_xlabel('Correlation: participant age × age-gap approval (95% CI)')
    fig.subplots_adjust(left=.22,right=.97,top=.93,bottom=.22)
    save(fig,'02_followup_correlations.png')

    # Figure 03: four source-reported means grouped by nominal gap size.
    fig,ax=start(778)
    rows=sorted(vign,key=lambda r:(int(r['nominal_gap_years']),int(r['woman_age'])))
    labels=[f"{r['nominal_gap_years']} years: woman {r['woman_age']}, man {r['man_age']}" for r in rows]
    vals=[float(r['mean_approval']) for r in rows]
    yp=np.arange(len(rows))
    bars=ax.barh(yp, vals, color=[BLUE,SLATE,RUST,SAND],height=.58)
    ax.set_yticks(yp,labels); ax.invert_yaxis()
    ax.set_xlim(0,7.35);ax.set_xlabel('Mean approval rating (1–7)')
    for b,v in zip(bars,vals):ax.text(v+.06,b.get_y()+b.get_height()/2,f'{v:g}',va='center',fontweight='bold')
    fig.subplots_adjust(left=.28,right=.97,top=.95,bottom=.17)
    save(fig,'03_same_gap_different_ages.png')

    # Figure 04: retrospective recalled vs contemporaneous current assessment.
    fig,ax=start(760)
    labels=['Not at all\ncoerced','Ethical\nproblems','Great hindrance\nto work']
    x=np.arange(len(glaser));width=.33
    old=[float(r['at_the_time_pct']) for r in glaser]
    now=[float(r['at_survey_pct']) for r in glaser]
    b1=ax.bar(x-width/2,old,width,label='Recalled view at the time',color=BLUE)
    b2=ax.bar(x+width/2,now,width,label='View at survey',color=RUST)
    ax.set_xticks(x,labels);ax.set_ylim(0,90)
    ax.set_ylabel('Share of applicable respondents (%)')
    ax.grid(axis='y',alpha=.14)
    ax.legend(frameon=False,loc='upper right',fontsize=10,ncol=2)
    for bars in (b1,b2):
        for b in bars:
            v=b.get_height()
            ax.text(b.get_x()+b.get_width()/2,v+1.7,f'{v:g}%',ha='center',fontsize=10)
    fig.subplots_adjust(left=.15,right=.98,top=.92,bottom=.24)
    save(fig,'04_glaser_recalled_assessments.png')

    # Figure 05: relationship-level initiation counts from 20 selected relationships.
    fig,ax=start(551)
    cats=by_study['Bellas & Gossett (2001)']
    labels=['Professor alone','Student alone','Mutually initiated']
    vals=[cats[x] for x in labels]
    bars=ax.barh(np.arange(3),vals,color=[SLATE,BLUE,RUST],height=.53)
    ax.set_yticks(np.arange(3),labels);ax.invert_yaxis()
    ax.set_xlim(0,10);ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.set_xlabel('Relationships (20 distinct relationships)')
    for b,v in zip(bars,vals): ax.text(v+.13,b.get_y()+b.get_height()/2,str(v),va='center',weight='bold')
    fig.subplots_adjust(left=.22,right=.97,top=.94,bottom=.25)
    save(fig,'05_bellas_initiation.png')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,default=ROOT,
                   help='Where to save figures and reconstruction_results.txt (default: repository root)')
    p.add_argument('--validate-only',action='store_true',
                   help='Verify input consistency and print calculations, do not write files')
    args=p.parse_args()
    tests,vign,corr,glaser,init,results=reconstruct()
    print(results)
    if not args.validate_only:
        args.output_dir.mkdir(parents=True,exist_ok=True)
        run_figures(args.output_dir,tests,vign,corr,glaser,init)
        (args.output_dir/'reconstruction_results.txt').write_text(results,encoding='utf-8')
        print('Wrote five figures and reconstruction_results.txt to',args.output_dir)

if __name__=='__main__':main()
