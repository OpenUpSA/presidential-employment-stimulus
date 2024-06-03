#!/usr/bin/env python3

import argparse
import json
import sys

from pprint import PrettyPrinter

sys.path.append("../python-src")
from presidential_employment import *


def add_or_replace(departments, department):
    # if a department with sheet_name exists in the list, replace it with the new department, else append to list
    for i, el in enumerate(departments):
        if el.sheet_name == department.sheet_name:
            departments[i] = department
            break
    else:
        departments.append(department)
    return departments


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase1_excel', default="notebooks/Copy of Completed Dashboard March 2022 Peter's version KP2 with budgets.xlsx")
    parser.add_argument('--phase2_excel', default='notebooks/Copy of Spreadsheet 2 - To March 2023 2.xlsx')
    parser.add_argument('--phase3_excel', default="notebooks/Worksheet April 2023 - March 2024.xlsx")
    parser.add_argument('--output_dir', default='data')
    parser.add_argument('--output_filename', default='all_data.json')
    args = parser.parse_args()

    pp = PrettyPrinter(indent=2)
    
    # dump the metric titles 
    json.dump(metric_titles, open(args.output_dir + "/metric_titles.json", "w"), indent=2)

    (opportunity_targets_df,
    opportunity_achievements_df,
    implementation_status_df,
    description_df,
    phase1_departments,
    phase2_departments,
    phase3_departments,
    targets_df,
    trends_df,
    provincial_df,
    cities_df,
    universities_df,
    demographic_df,
    achievement_totals_df,
    dpwi_target_row,
    sprf_phase1_row,
    sprf_phase2_row,
    department_budget_targets,
    total_budgets) = load_sheets(args.phase1_excel, args.phase2_excel, args.phase3_excel)

    department_names = list(set(phase1_departments).union(phase2_departments).union(phase3_departments))

    leads = description_df.lead.to_dict()
    paragraphs = description_df.paragraph.to_dict()

    ## Compute per department data structures
    (all_data_departments, sprf_targets, dpwi_target) = compute_all_data_departments(phase1_departments, phase2_departments, phase3_departments,
                                                    implementation_status_df, demographic_df, description_df,
                                                    targets_df, trends_df, department_names, provincial_df,
                                                    cities_df, universities_df, leads, paragraphs,
                                                    department_budget_targets, opportunity_targets_df,
                                                    dpwi_target_row, [sprf_phase1_row, sprf_phase2_row])

    sprf_target = sum(sprf_targets)  # for the merged data, we just need the total target of phases 1 and 2
    # number_of_phases is defined in presidential_employment/__init__.py
    merged_departments, merged_budget_targets, merged_total_budgets = merge_phases(all_data_departments, sprf_target, dpwi_target, 
                                      number_of_phases-1,
                                      department_budget_targets, total_budgets)

    # updates number of phases to match those in merged_departments
    number_of_phases = 0
    for department in merged_departments:
        for phase in department.phases:
            if (phase.phase_num + 1) > number_of_phases:
                number_of_phases = phase.phase_num + 1 

    ## Compute breakdown of all programmes by demographic dimensions   
    (total_male, 
    total_female, 
    total_unknown_gender,
    total_beneficiaries,
    total_youth, 
    total_unknown_youth, 
    total_provincial, 
    total_unknown_province) = compute_breakdowns(merged_departments)

    ## Overview picture
    (programmes_by_type,
    programmes_by_type_summarised,
    achievements_by_type_by_month,
    provincial_breakdown) = compute_programmes_by_type(merged_departments)

    # ### Check that total add up to totals listed in the spreadsheet
    # # check targets for phase 1 - job opportunities
    # assert (
    #     programmes_by_type[SectionEnum.job_opportunities.name][0]["Total"]["value_target"]
    #     == opportunity_targets_df[0].iloc[6, 7]
    # ), f'{SectionEnum.job_opportunities.name} total mismatch: {programmes_by_type[SectionEnum.job_opportunities.name][0]["Total"]["value_target"]} vs {opportunity_targets_df[0].iloc[6, 7]}'

    # # check targets for phase 2 - job opportunities
    # assert (
    #     programmes_by_type[SectionEnum.job_opportunities.name][1]["Total"]["value_target"]
    #     == opportunity_targets_df[1].iloc[5, 7]
    # ), f'{SectionEnum.job_opportunities.name} total mismatch: {programmes_by_type[SectionEnum.job_opportunities.name][1]["Total"]["value_target"]} vs {opportunity_targets_df[1].iloc[5, 7]}'


    # # check achievements for phase 1 - job opportunities
    # assert (
    #     programmes_by_type[SectionEnum.job_opportunities.name][0]["Total"]["value"] == achievement_totals_df[0].loc["Jobs created","total"]
    # ), f'Phase 1: {SectionEnum.job_opportunities.name} total mismatch computed {programmes_by_type[SectionEnum.job_opportunities.name][0]["Total"]["value"]} vs sheet {achievement_totals_df[0].loc["Jobs created"]}'

    # # check achiements for phase 2 - job opportunities
    # assert (
    #     programmes_by_type[SectionEnum.job_opportunities.name][1]["Total"]["value"] == achievement_totals_df[1].loc["Jobs created","total"]
    # ), f'Phase 2: {SectionEnum.job_opportunities.name} total mismatch {programmes_by_type[SectionEnum.job_opportunities.name][1]["Total"]["value"]} vs {achievement_totals_df[1].loc["Jobs created"]}'

    # # check targets for phase 1 - livelihoods support
    # assert (
    #     programmes_by_type[SectionEnum.livelihoods.name][0]["Total"]["value_target"]
    #     == opportunity_targets_df[0].iloc[7, 7]
    # ), f'{SectionEnum.livelihoods.name} total mismatch: phase 1 target {programmes_by_type[SectionEnum.livelihoods.name][0]["Total"]["value_target"]} vs {opportunity_targets_df[0].iloc[7, 7]}'

    # # check targets for phase 2 - livelihoods support
    # assert (
    #     programmes_by_type[SectionEnum.livelihoods.name][1]["Total"]["value_target"]
    #     == opportunity_targets_df[1].iloc[6, 7]
    # ), f'{SectionEnum.livelihoods.name} total mismatch: phase 2 target {programmes_by_type[SectionEnum.livelihoods.name][1]["Total"]["value_target"]} vs {opportunity_targets_df[1].iloc[6, 7]}'


    # # check achievements for phase 1 - livelihoods support
    # assert (
    #     programmes_by_type[SectionEnum.livelihoods.name][0]["Total"]["value"] == achievement_totals_df[0].loc["Livelihoods supported","total"]
    # ), f'{SectionEnum.job_opportunities.name} total mismatch - phase 1 {programmes_by_type[SectionEnum.livelihoods.name][0]["Total"]["value"]} vs {achievement_totals_df[0].loc["Livelihoods supported"]}'

    # # check achievements for phase 2 - livelihoods support
    # assert (
    #     programmes_by_type[SectionEnum.livelihoods.name][1]["Total"]["value"] == achievement_totals_df[1].loc["Livelihoods supported","total"]
    # ), f'{SectionEnum.job_opportunities.name} total mismatch - phase 2 {programmes_by_type[SectionEnum.livelihoods.name][1]["Total"]["value"]} vs {achievement_totals_df[1].loc["Livelihoods supported"]}'

    # # check targets for phase 1 - jobs retained
    # assert (
    #     programmes_by_type[SectionEnum.jobs_retain.name][0]["Total"]["value_target"]
    #     == opportunity_targets_df[0].iloc[8, 7]
    # ), f'{SectionEnum.jobs_retain.name} total mismatch: {programmes_by_type[SectionEnum.jobs_retain.name][0]["Total"]["value_target"]} vs {opportunity_targets_df[0].iloc[8, 7]}'

    # # check achivements for phase 2 - jobs retained
    # assert (
    #     programmes_by_type[SectionEnum.jobs_retain.name][0]["Total"]["value"] == achievement_totals_df[0].loc["Jobs retained","total"]
    # ), f'{SectionEnum.job_opportunities.name} total mismatch {programmes_by_type[SectionEnum.jobs_retain.name][0]["Total"]["value"]} vs {achievement_totals_df[0].loc["Jobs retained"]}'

    ## Compute breakdowns used in overview and metrics used in overview
    (breakdown_metrics, current_targets, current_achievements) = compute_overview_breakdown(programmes_by_type_summarised,
                                                                                            achievements_by_type_by_month,
                                                                                            provincial_breakdown, number_of_phases)

    overview_metrics = compute_overview_metrics(total_female, total_beneficiaries, total_unknown_gender,
                                programmes_by_type,
                                total_youth, total_unknown_youth,
                                merged_budget_targets, merged_total_budgets,
                                number_of_phases)

    ## Assemble overview and put together final combined data
    overview = compute_overview(description_df, leads, paragraphs, overview_metrics,
                                current_targets, current_achievements, breakdown_metrics)
    all_data = Everything(
        overview=overview,
        departments=all_data_departments
    )

    # Save final data

    # to work around the fact that data from pandas sometimes appears as numpy types, this uses a
    # version of dataclasses-json core.py (https://github.com/pvanheus/dataclasses-json/blob/master/dataclasses_json/core.py)
    # see this PR: https://github.com/lidatong/dataclasses-json/pull/352
    output_filename = args.output_dir + "/" + args.output_filename
    # all_data.departments.sort(key=operator.attrgetter("sheet_name"))
    open(output_filename, "w").write(all_data.to_json(indent=2))
    # print(all_data.to_json(indent=2))
    phase_dates_file = args.output_dir + "/" + "phase_dates.json"
    open(phase_dates_file, "w").write(json.dumps(phase_dates, indent=2))
    print("DONE")    