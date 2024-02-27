import copy
import pprint  # we used this for debugging, so the module is not always used by production code
from calendar import day_abbr
from typing import Callable

import pandas as pd

from .enums import *
from .constants import *
from .data_structures import *



# NOTE: UPDATE THESE ROWS EACH TIME A NEW MONTH'S DATA IS ADDED
months = [
    "202010",
    "202011",
    "202012",
    "202101",
    "202102",
    "202103",
    "202104",
    "202105",
    "202106",
    "202107",
    "202108",
    "202109",
    "202110",
    "202111",
    "202112",
    "202201",
    "202202",
    "202203",
    "202204",
    "202205",
    "202206",
    "202207",
    "202208",
    "202209",
    "202210",
    "202211",
    "202212",
    "202301",
    "202302",
    "202303",
    "202304",
    "202305",
    "202306",
    "202307",
    "202308",
    "202309",
    "202310",
    "202311",
    "202312"
]

month_names = [
    "Oct '20",
    "Nov '20",
    "Dec '20",
    "Jan '21",
    "Feb '21",
    "Mar '21",
    "Apr '21",
    "May '21",
    "Jun '21",
    "Jul '21",
    "Aug '21",
    "Sep '21",
    "Oct '21",
    "Nov '21",
    "Dec '21",
    "Jan '22",
    "Feb '22",
    "Mar '22",
    "Apr '22",
    "May '22",
    "Jun '22",
    "Jul '22",
    "Aug '22",
    "Sep '22",
    "Oct '22",
    "Nov '22",
    "Dec '22",
    "Jan '23",
    "Feb '23",
    "Mar '23",
    "Apr '23",
    "May '23",
    "Jun '23",
    "Jul '23",
    "Aug '23",
    "Sep '23",
    "Oct '23",
    "Nov '23",
    "Dec '23"
]
# the last column index of the achievements (i.e. Trends) sheets (one number per phase)
total_achievement_column = [20, 17, 18]

# achievement_columns = [slice(2, 11), slice(2,6)]
month_lookup = [
    {  # these match column names of the Dashboard spreadsheet's Trends sheet
        "oct": "202010",
        "nov": "202011",
        "dec": "202012",
        "jan": "202101",
        "feb": "202102",
        "mar": "202103",
        "apr": "202104",
        "may": "202105",
        "june": "202106",
        "july": "202107",
        "aug": "202108",
        "sept": "202109",
        "oct.1": "202110",
        "nov.1": "202111",
        "dec.1": "202112",
        "jan.1": "202201",
        "feb.1": "202202",
        "march": "202203",
        "march.1": "202203"
    },
    {
        "oct": "202110",
        "nov": "202111",
        "dec": "202112",
        "jan": "202201",
        "feb": "202202",
        "mar": "202203",
        "apr": "202204",
        "may": "202205",
        "jun": "202206",
        "jul": "202207",
        "aug": "202208",
        "sep": "202209",
        "oct.1": "202210",
        "nov.1": "202211",
        "dec.1": "202212",
        "march": "202303",
    },
    {   # this is not really used anymore since we don't report time series data - included for completeness 
        "oct": "202110",
        "nov": "202111",
        "dec": "202112",
        "jan": "202201",
        "feb": "202202",
        "mar": "202203",
        "apr": "202204",
        "may": "202205",
        "jun": "202206",
        "jul": "202207",
        "aug": "202208",
        "sep": "202209",
        "oct.1": "202210",
        "nov.1": "202211",
        "dec.1": "202212",
        "march": "202303",
        "dec.2": "202312",
    },  
]

number_of_phases = 3
phase_dates = [["202010", "202203"], ["202204", "202303"], ["202304", "202312"]]

# Completed: October 20202 - March 2022
# Current: April 2021 - Current

def in_phase(phase_num, month):
    if phase_num >= 0 and phase_num < len(phase_dates):
        (start_str, end_str) = phase_dates[phase_num]
        if int(start_str) <= int(month) and int(month) <= int(end_str):
            return True
    return False


# target_to_imp_programme_mapping = {
#     "Banking with art, connecting Lives - National Museum Bloemfontein": " Banking with art, connecting Lives - National Museum Bloemfontein",
#     "CSIR - Experiential Training Programme": "CSIR - Experiential Training Programme ",
#     "Community Health Workers": "Community health workers",
#     "Covid-19 Return-To-Play - National Sport Federations": "Covid-19 Return-To-Play - National Sport Federations                                                                                                                                    ",
#     "Digitisation of records - National Library of South Africa": "Digitisation of records - National Library of South Africa ",
#     "Facilities Management": "Facilities Management (PMTE) Employment: ",
#     "In-House Construction projects": "In-House Construction projects ",
#     "Job retention at fee paying schools": "Retain vulnerable teaching posts",
#     "Municipal infrastructure": "Mainstream labour intensive construction methods",
#     "Outreach Team Leaders": "Outreach team leaders",
#     "Oceans and Coast: Source to Sea": "Oceans and Coast: Source to Sea ",
#     "Provincial Roads Maintenance": "Rural roads maintenance",
#     "Real Estate": "Real Estate  (PMTE)",
#     "Services sector development incentives": "Global Business Services Sector",
#     "Subsistence relief fund": "Subsistence producer relief fund",
#     "Retention of social workers": "Social workers",
#     "Vegetables and Fruits": "Vegetables and Fruits ",
#     "WRC - Water Graduate Employment Programme": " WRC - Water Graduate Employment Programme ",
#     "Water and Energy Efficiency": "Water and Energy Efficiency (Green Economy)",
#     "Water and Sanitation Facilities Management": "Water and Sanitation Facilities Management (PMTE)",
#     "Welisizwe Rural Bridges Programme": "Welisizwe Rural Bridges Programme (PMTE) ",
# }

strip_ws = lambda iterable: [pn.strip() for pn in iterable]

# code imported from notebook

def load_sheets(phase1_excel, phase2_excel, phase3_excel):
    """Reads in the phase1, phase2 and phase3 Excel files and extracts:
    * opportunity_targets_df - complete Targets sheet
    * opportunity_achievements_df - complete Trends sheet
    * implementation_status_df - Implementation Status
    * description_df - Department Descriptions
    * phase1_departments - department names that are in phase 1
    * phase2_departments - department names that are in phase 2
    * phase3_departments - department names that are in phase 3
    * targets_df - just the per department Targets
    * trends_df - the per department Trends
    * provincial_df - provincial breakdowns
    * cities_df - cities breakdown
    * universities_df - universities breakdown
    * demographic_df - demographic breakdown by gender, youth, etc
    """
    # Opportunity Targets: the "Targets" tab
    opportunity_targets_df = [
        pd.read_excel(phase1_excel, sheet_name="Targets", header=None).fillna(0)
    ]

    row_nums = opportunity_targets_df[0].index[opportunity_targets_df[0].iloc[:, 1] == 'Graduate programmes (Property Management Trading Entity)']
    assert len(row_nums) == 1, f"Error: 'Graduate programmes (Property Management Trading Entity)' is not uniquely identified in Phase 1 Targets: {len(row_nums)}"
    dpwi_target_row = row_nums[0]

    row_nums = opportunity_targets_df[0].index[opportunity_targets_df[0].iloc[:, 1] == 'Subsistence producer relief fund']
    assert len(row_nums) == 1, f"Error 'Subsistence producer relief fund' is not uniquely identifed in Phase 1 Targets {len(row_nums)}"
    sprf_phase1_row = row_nums[0]

    opportunity_targets_df.append(
        pd.read_excel(phase2_excel, sheet_name="Targets", header=None).fillna(0)
    )

    row_nums = opportunity_targets_df[1].index[opportunity_targets_df[1].iloc[:, 1] == 'Subsistence Producer Relief Fund']
    assert len(row_nums) == 1, f"Error 'Subsistence Producer Relief Fund' is not uniquely identifed in Phase 2 Targets {len(row_nums)}"
    sprf_phase2_row = row_nums[0]

    opportunity_targets_df.append(
        pd.read_excel(phase3_excel, sheet_name="Targets", header=None).fillna(0)
    )

    # Opportunity Achievements: the "Trends" tab
    opportunity_achievements_df = []
    for sheet in (phase1_excel, phase2_excel, phase3_excel):
        opportunity_achievements_df.append(
            pd.read_excel(sheet, sheet_name="Trends", header=None).fillna(0)
        )

    # Implementation Status: the "Implementation status" tab
    implementation_status_df = []
    for sheet in (phase1_excel, phase2_excel, phase3_excel):
        implementation_status_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Implementation status",
                skiprows=2,
                usecols=range(4),
                names=["department", "programme", "status", "detail"],
            )
        )

    for i in range(len(implementation_status_df)):
        implementation_status_df[i].department = implementation_status_df[
            i
        ].department.ffill()
        implementation_status_df[i].detail = implementation_status_df[i].detail.fillna(
            ""
        )

    # description_df: the "Department Descriptions" tab
    # TODO: figure out why we use phase3_excel for this - is it a superset of phase 1's department? In any case, the departments in phase 3 match those in phase 2
    description_df = pd.read_excel(
        phase3_excel,
        sheet_name="Department Descriptions",
        names=["key", "lead", "paragraph", "Data captured until"],
        usecols=range(4),
        index_col=0,
    ).dropna()

    # department budgets taken from the "Department Description" tab
    department_budget_targets = []
    total_budgets = []
    
    for (sheet, budget_col) in ((phase1_excel, 7), (phase2_excel, 4), (phase3_excel, 4)):
        budget_targets = pd.read_excel(
            sheet,
            sheet_name="Department Descriptions",
            usecols=[0,budget_col],
            skiprows=1,
            nrows=19,
            names=["abbrev", "budget"],
            index_col=0
        ).fillna(0) * 1000

        total_budgets.append(budget_targets.budget.loc["Total"])
        department_budget_targets.append(budget_targets.drop('Total').to_dict()['budget'])

    # total_budgets.append(budget_targets.budget.loc["Total"])
    # department_budget_targets.append(budget_targets)

    # opportunity_type_df = pd.concat(
    #     [opportunity_targets_df.iloc[2:56, 1], opportunity_targets_df.iloc[2:56, 4]], axis=1
    # ).set_index(1)

    # Find the list of departments for the different phases
    phase1_departments = set(
        pd.read_excel(phase1_excel, sheet_name="Targets", skiprows=1)
        .loc[:, "Department"]
        .dropna()
        .iloc[:-1]
    )

    phase2_departments = set(
        pd.read_excel(phase2_excel, sheet_name="Targets", skiprows=1)
        .loc[:, "Department"]
        .dropna()
        .iloc[:-1]
    )

    phase3_departments = set(
        pd.read_excel(phase3_excel, sheet_name="Targets", skiprows=1)
        .loc[:, "Department"]
        .dropna()
        .iloc[:-1]
    )

    # targets df: the "Targets" tab (again)
    # TODO: figure out why both targets_df and opportunity_targets_df are needed
    targets_df = []
    phase_num = 1
    for (sheet, sections) in ((phase1_excel, ["CRE", "LIV", "RET"]), (phase2_excel, ["CRE", "LIV"]), (phase3_excel, ["CRE", "LIV"])):
        targets_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Targets",
                skiprows=1,
                usecols=list(range(6)),
                names = [
                    "department",
                    "programme",
                    "target",
                    "unk",
                    "section",
                    "display_name",
                ]).drop("unk", axis=1)
        )
        assert targets_df[-1].section[0] in sections, f"Error: unexpected section name in Phase{phase_num} Targets"
        phase_num += 1

    for i in range(len(targets_df)):
        targets_df[i].department = targets_df[i].department.ffill()
        targets_df[i].section = targets_df[i].section.ffill()

    # trends_df: the longitudinal data in the "Trends" tab
    trends_df = []
    phase_index = 0
    for (sheet, skiprows) in ((phase1_excel, 5), (phase2_excel, 4), (phase3_excel, 4)):
        trends_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Trends",
                skiprows=skiprows,
                usecols=list(range(total_achievement_column[phase_index] + 1)),
            )
        )
        phase_index += 1

    for i in range(len(trends_df)):
        trends_df[i].columns = [c.lower() for c in trends_df[i].columns]
        trends_df[i].department = trends_df[i].department.ffill()
        trends_df[i] = trends_df[i].fillna(0)
        # if i == 1:
        #     # TODO: document why we drop the october column from phase2 trends
        #     # NOTE: 24 August 2023 - this has become unnecessary because of the new phase2 format
        #     trends_df[i] = trends_df[i].drop("oct", axis=1)

    # provincial_df: the provincial breakdowns in the "Provincial (beneficiaries)" tab
    provincial_df = []
    for sheet in (phase1_excel, phase2_excel, phase3_excel):
        provincial_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Provincial (beneficiaries)",
                skiprows=4,
                usecols=list(range(12)),
            )
        )

    for i in range(len(provincial_df)):
        provincial_df[i].columns = [
            c.lower().replace(" ", "_").replace("-", "_")
            for c in provincial_df[i].columns
        ]
        provincial_df[i].department = provincial_df[i].department.ffill()
        provincial_df[i] = provincial_df[i].fillna(0)

    # cities and universities dimensions have been deprecated - August 2023
    cities_df = [None] * number_of_phases
    universities_df = [None] * number_of_phases
    # cities_df = [
    #     None,
    #     pd.read_excel(
    #         phase2_excel,
    #         sheet_name="Cities (beneficiaries)",
    #         skiprows=4,
    #         usecols=list(range(12)),  # adjust if number of cities changes
    #     ),
    # ]
    # for i in range(len(cities_df)):
    #     if cities_df[i] is None:
    #         continue
    #     cities_df[i].columns = [
    #         c.lower().replace(" ", "_") for c in cities_df[i].columns
    #     ]
    #     cities_df[i].department = cities_df[i].department.fillna(method="pad")
    #     cities_df[i] = cities_df[i].fillna(0)

    # universities_df = [
    #     None,
    #     pd.read_excel(
    #         phase2_excel,
    #         sheet_name="Universities (beneficiaries)",
    #         skiprows=4,
    #         usecols=list(range(26)),  # adjust if number of universities changes - this is number of unis + 2
    #     ),
    # ]
    # for i in range(len(universities_df)):
    #     if universities_df[i] is None:
    #         continue
    #     universities_df[i].columns = [
    #         c.lower().replace(" ", "_").replace("-", "_")
    #         for c in universities_df[i].columns
    #     ]
    #     universities_df[i].department = universities_df[i].department.fillna(
    #         method="pad"
    #     )
    #     universities_df[i] = universities_df[i].fillna(0)

    # demographic_df: the demographic breakdowns in the "Demographic data" tab
    demographic_df = []
    for (sheet, skiprows, usecols) in ((phase1_excel, 8, 9), (phase2_excel, 9, 11), (phase3_excel, 9, 11)):    
        demographic_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Demographic data",
                skiprows=skiprows,
                usecols=list(range(usecols)),
            )
        )

    for i in range(len(demographic_df)):
        demographic_df[i].columns = [
            c.lower().replace(" ", "_").replace("%", "perc").replace("no.", "no")
            for c in demographic_df[i].columns
        ]
        demographic_df[i].department = demographic_df[i].department.ffill()
        demographic_df[i] = demographic_df[i].fillna(0)

    # achievement_totals_df: the totals in the "Demographic data" tab
    achievement_totals_df = []
    for sheet in (phase1_excel, phase2_excel, phase3_excel):
        achievement_totals_df.append(
            pd.read_excel(
                sheet,
                sheet_name="Demographic data",
                skiprows=2,
                usecols=range(2),
                nrows=3,
                names=["section", "total"],
                index_col=0,
            )
        )

    return (
        opportunity_targets_df,
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
        total_budgets
    )


def make_dim(
    lookup_type: str,
    viz_type: str,
    df: pd.DataFrame,
    col_start: int,
    col_end: int,
    key_lookup: Callable[[str], str],
    department_name: str,
    programme_name: str,
    section: str,
) -> Dimension:
    """Make a Dimension from a dataframe where the dataframe has programmes as rows and dimension as columns.

    lookup_type: Lookup type (reference to lookups.json) to lookup abbreviation to full name
    viz_type: Visualisation type (line, bar, etc)
    df: pandas dataframe to be processed
    col_start: starting column of the data
    col_end: ending column of the data
    key_lookup: function to look up Metric key from column names
    department_name: department name
    programme_name: programme name within department
    section: section abbreviation (CRE, LIV, RET)
    returns a Dimension
    """
    row = df.loc[(df.department == department_name) & (df.programme == programme_name)]
    values = []
    if (
        len(
            df.loc[
                (df.department == department_name) & (df.programme == programme_name)
            ]
        )
        == 0
    ):
        data_missing = True
    else:
        nonzero = False
        for key in list(row)[col_start:col_end]:
            value = int(row.loc[:, key].iloc[0])
            if value > 0:
                nonzero = True
            values.append(MetricValue(key=key_lookup(key), value=value))
        if not nonzero:
            data_missing = True
            values = []
        else:
            data_missing = False

    dim = Dimension(
        name=metric_titles[section_abbrev_to_name[section]][
            MetricTypeEnum.count.name + "_" + lookup_type
        ],
        lookup=lookup_type,
        viz=viz_type,
        values=values,
        data_missing=data_missing,
    )
    return dim


def compute_all_data_departments(
    phase1_departments,
    phase2_departments,
    phase3_departments,
    implementation_status_df,
    demographic_df,
    description_df,
    targets_df,
    trends_df,
    department_names,
    provincial_df,
    cities_df,
    universities_df,
    leads,
    paragraphs,
    department_budget_targets,
    opportunity_targets_df: list[pd.DataFrame],
    dpwi_target_row: int,
    sprf_row: list[int],
):
    """Compute all_data_departments, which summarises programmes for all departments
    (what will become the department tabs)"""
    all_data_departments = []

    # desc_abbrevs = {
    #     "DoH": "DoH",
    #     "Tourism": "Tourism ",
    #     "DPWI": "DPWI ",
    #     "DCOGTA": "COGTA",
    # }  # deal with special cases in description lookup
    departments = {}
    for department_name in department_names:
        phases = []
        for phase_num in range(number_of_phases):
            # TODO: rationalist this so that we don't have to repeat the code for each phase
            if phase_num == 0 and (not department_name in phase1_departments):
                continue
            elif phase_num == 1 and (not department_name in phase2_departments):
                continue
            elif phase_num == 2 and (not department_name in phase3_departments):
                continue
            department_implementation_details = []
            # print("PHASE", phase_num, trends_df[phase_num].loc[trends_df[phase_num].department == department_name].iloc[:, -1])
            target_section = Section(
                name=section_titles[SectionEnum.targets.name],
                section_type=SectionEnum.targets.name,
                metrics=[
                    Metric(
                        name=metric_titles[SectionEnum.targets.name][
                            MetricTypeEnum.currency.name
                        ],
                        metric_type=MetricTypeEnum.currency.name,
                        value_target=department_budget_targets[phase_num][
                            department_name_to_abbreviation[department_name]
                        ],
                        value=-1,
                        dimensions=[],
                    ),
                    Metric(
                        name=metric_titles[SectionEnum.targets.name][
                            MetricTypeEnum.count.name
                        ],
                        metric_type=MetricTypeEnum.count.name,
                        value_target=targets_df[phase_num]
                        .loc[targets_df[phase_num].department == department_name]
                        .target.sum(),  # overall target of beneficiaries
                        value=trends_df[phase_num]
                        .loc[trends_df[phase_num].department == department_name]
                        .iloc[:, -1]
                        .sum(),  # get the achievement by summing the last column in trends
                        dimensions=[],
                    ),
                ],
            )

            sections = [target_section]
            for section in [
                "CRE",
                "LIV",
                "RET",
            ]:  # TODO: support CAT - Catalytic Interventions
                programme_names = list(
                    targets_df[phase_num]
                    .loc[
                        (targets_df[phase_num].section == section)
                        & (targets_df[phase_num].department == department_name)
                    ]
                    .programme
                )
                if (
                    phase_num == 0
                    and section == "CRE"
                    and department_name
                    == "Agriculture, Land Reform and Rural Development"
                ):
                    # this does not have a target so needs to be added manually
                    programme_names += ["Graduate verifiers"]
                metrics = []

                for programme_name in programme_names:
                    # SPECIAL CASE code
                    if (
                        department_name == "Public Works and Infrastructure"
                        and programme_name == "Project Administrators"
                    ):
                        # this programme is mentioned in Targets and has a line in Implementation Status but has no other data
                        continue
                    imp_status_row = implementation_status_df[phase_num].loc[
                        (
                            implementation_status_df[phase_num].department
                            == department_name
                        )
                        & (
                            implementation_status_df[phase_num].programme
                            == programme_name
                        )
                    ]
                    if len(imp_status_row) == 0 or pd.isna(
                        imp_status_row.status.iloc[0]
                    ):
                        imp_detail = None
                        print("Implementation status missing for: ", phase_num, ":", department_name, ":", programme_name)
                    else:
                        imp_detail = ImplementationDetail(
                            programme_name=programme_name,
                            status=implementation_status_to_enum[
                                imp_status_row.status.iloc[0].strip()
                            ],
                            detail=imp_status_row.detail.iloc[0].strip(),
                        )
                    # SPECIAL CASES: These two programmes have sub-programmes that are not in the Targets sheet
                    # and the implementation datail is not listed for the sub-programmes
                    if (
                        department_name == "Public Works and Infrastructure"
                        and programme_name
                        == "Graduate programmes (Property Management Trading Entity)"
                    ) or (
                        department_name
                        == "Agriculture, Land Reform and Rural Development"
                        and phase_num != 2  # in phase 3 this is a normal programme
                        and (programme_name == "Subsistence producer relief fund" or
                        programme_name == 'Subsistence Producer Relief Fund')
                    ):
                        department_implementation_details.append(imp_detail)
                        continue  # these programmes have no detailed metrics
                    else:
                        try:
                            # collect detailed metrics for programme
                            dimensions = []
                            time_dimension_row = trends_df[phase_num].loc[
                                (trends_df[phase_num].department == department_name)
                                & (trends_df[phase_num].programme == programme_name)
                            ]
                            dimensions.append(
                                make_dim(
                                    LookupTypeEnum.province.name,
                                    VizTypeEnum.bar.name,
                                    provincial_df[phase_num],
                                    2,  # skip first two columns
                                    -1,  # skip last column
                                    lambda key: province_header_to_abbrev[key],
                                    department_name,
                                    programme_name,
                                    section,
                                )
                            )
                            if cities_df[phase_num] is not None:
                                cities_dim = make_dim(
                                    LookupTypeEnum.city.name,
                                    VizTypeEnum.bar.name,
                                    cities_df[phase_num],
                                    2,
                                    -1,
                                    lambda key: city_header_to_abbrev[key],
                                    department_name,
                                    programme_name,
                                    section,
                                )
                                dimensions.append(cities_dim)
                            if universities_df[phase_num] is not None:
                                universities_dim = make_dim(
                                    LookupTypeEnum.university.name,
                                    VizTypeEnum.bar.name,
                                    universities_df[phase_num],
                                    2,
                                    -1,
                                    lambda key: university_header_to_abbrev[key],
                                    department_name,
                                    programme_name,
                                    section,
                                )
                                dimensions.append(universities_dim)
                            dimensions.append(
                                make_dim(
                                    LookupTypeEnum.time.name,
                                    VizTypeEnum.line.name,
                                    trends_df[phase_num],
                                    2,
                                    None,
                                    lambda key: month_lookup[phase_num][key],
                                    department_name,
                                    programme_name,
                                    section,
                                )
                            )
                            demographic_row = demographic_df[phase_num].loc[
                                (
                                    demographic_df[phase_num].department
                                    == department_name
                                )
                                & (
                                    demographic_df[phase_num].programme
                                    == programme_name
                                )
                            ]

                            values = []
                            if len(demographic_row) == 0:
                                data_missing = True
                            else:
                                male_perc = demographic_row.loc[:, "perc_male"].iloc[0]
                                female_perc = demographic_row.loc[
                                    :, "perc_female"
                                ].iloc[0]
                                if male_perc + female_perc == 0:
                                    data_missing = True
                                else:
                                    values = [
                                        MetricValue(
                                            key=GenderEnum.Male.name,
                                            value=male_perc,
                                        ),
                                        MetricValue(
                                            key=GenderEnum.Female.name,
                                            value=female_perc,
                                        ),
                                    ]
                                    if male_perc + female_perc != 1.0:
                                        print(
                                            "M/F PERC PROBLEM:",
                                            department_name,
                                            programme_name,
                                            phase_num,
                                            male_perc,
                                            female_perc,
                                            male_perc + female_perc,
                                        )
                                    data_missing = False

                            gender_dim = Dimension(
                                name=metric_titles[section_abbrev_to_name[section]][
                                    MetricTypeEnum.count.name + "_gender"
                                ],
                                lookup=LookupTypeEnum.gender.name,
                                viz=VizTypeEnum.two_value.name,
                                values=values,
                                data_missing=data_missing,
                            )
                            dimensions.append(gender_dim)

                            data_missing=True
                            values=[]
                            if len(demographic_row) != 0 and "perc_repeat" in demographic_row:
                                repeat_perc = demographic_row.loc[:, "perc_repeat"].iloc[0]
                                new_perc = demographic_row.loc[:, "perc_new"].iloc[0]
                                if (repeat_perc + new_perc) != 0:

                                    values = [
                                        MetricValue(
                                            key=RepeatEnum.Repeat.name,
                                            value=repeat_perc,
                                        ),
                                        MetricValue(
                                            key=RepeatEnum.New.name,
                                            value=new_perc
                                        )
                                    ]
                                    data_missing=False

                                    # TODO: figure out when this should be added. Should it be in:
                                    #       1. all of phase 2
                                    #       2. only programmes from DALLRD where this is relevant
                                    # current option is (2)
                                    repeat_dim = Dimension(
                                        name=metric_titles[section_abbrev_to_name[section]][
                                            MetricTypeEnum.count.name + '_repeat'
                                        ],
                                        lookup=LookupTypeEnum.repeat.name,
                                        viz=VizTypeEnum.two_value.name,
                                        values=values,
                                        data_missing=data_missing
                                    )
                                    dimensions.append(repeat_dim)

                            values = []
                            if len(demographic_row) == 0:
                                data_missing = True
                            else:
                                age_perc = demographic_row.loc[:, "perc_youth"].iloc[0]
                                if age_perc == 0:
                                    data_missing = True
                                    values = []
                                else:
                                    values = [
                                        MetricValue(
                                            key="18-35",
                                            value=age_perc,
                                        )
                                    ]
                                    data_missing = False
                            youth_dim = Dimension(
                                name=metric_titles[section_abbrev_to_name[section]][
                                    MetricTypeEnum.count.name + "_age"
                                ],
                                lookup=LookupTypeEnum.age.name,
                                viz=VizTypeEnum.percentile.name,
                                values=values,
                                data_missing=data_missing,
                            )
                            dimensions.append(youth_dim)

                            #                         # TODO: Rationalise this - disabled and military vets share a lot of code
                            #                         if phase_num == 0:
                            #                             disabled = demographic_row.no_disability.iloc[0]
                            #                             if disabled > 0:
                            #                                 disabled_dim = Dimension(
                            #                                     name=metric_titles[section_abbrev_to_name[section]][MetricTypeEnum.count.name + '_disabled'],
                            #                                     lookup=LookupTypeEnum.disabled.name,
                            #                                     viz=VizTypeEnum.count.name,
                            #                                     values=[MetricValue(key='disabled', value=disabled)]
                            #                                 )
                            #                                 dimensions.append(disabled_dim)

                            #                             # military_vets = demographic_row.no_military_veterans.iloc[0]
                            #                             # if military_vets > 0:
                            #                             #     mv_dim = Dimension(
                            #                             #         name=metric_titles[section_abbrev_to_name[section]][MetricTypeEnum.count.name + '_vets'],
                            #                             #         lookup=LookupTypeEnum.vets.name,
                            #                             #         viz=VizTypeEnum.count.name,
                            #                             #         values=[MetricValue(key='vets', value=military_vets)]
                            #                             #     )
                            #                             #     dimensions.append(mv_dim)
                            #                         elif phase_num == 1:
                            #                             perc_disabled = demographic_row.perc_disability.iloc[0]
                            #                             perc_not_disabled = 1 - perc_disabled
                            #                             if perc_disabled > 0:
                            #                                 disabled_dim = Dimension(
                            #                                     name=metric_titles[section_abbrev_to_name[section]][MetricTypeEnum.count.name + '_disabled'],
                            #                                     lookup=LookupTypeEnum.disabled.name,
                            #                                     viz=VizTypeEnum.two_value.name,
                            #                                     values=[MetricValue(key='disabled', value=perc_disabled), MetricValue(key='not disabled', value=perc_not_disabled)]
                            #                                 )
                            #                                 dimensions.append(disabled_dim)

                            total_value = int(time_dimension_row.iloc[:, -1].iloc[0])
                            target_row = (
                                targets_df[phase_num]
                                .fillna(0)
                                .loc[
                                    (
                                        targets_df[phase_num].department
                                        == department_name
                                    )
                                    & (
                                        targets_df[phase_num].programme
                                        == programme_name
                                    )
                                ]
                                .target
                            )
                            if len(target_row) == 0:
                                # e.g. Graduate verifiers programme doesn't have a target
                                target = -1
                            else:
                                target = target_row.iloc[0]
                            programme_metric = Metric(
                                name=programme_name,
                                metric_type=MetricTypeEnum.count.name,
                                value=total_value,
                                value_target=target,
                                dimensions=dimensions,
                                implementation_detail=imp_detail,
                            ) 
                            metrics.append(programme_metric)
                        except IndexError as e:
                            print(
                                "IndexError (likely typo) on",
                                section,
                                department_name,
                                programme_name,
                                str(e),
                            )

                sections.append(
                    Section(
                        name=section_titles[section_abbrev_to_name[section]],
                        section_type=section_abbrev_to_name[section],
                        metrics=metrics,
                    )
                )
            abbrev = department_name_to_abbreviation[department_name]

            month_info = description_df.loc[
                abbrev, "Data captured until"
            ]
            try:
                month = month_info.strftime("%Y%m")
            except AttributeError as e:
                month_parts = month_info.split("-")
                month = month_parts[2] + month_parts[1]
            phase = Phase(
                phase_num=phase_num,
                month=month,
                sections=sections,
                target_lines=[],
                achievement_lines=[],
                implementation_details=department_implementation_details,
                beneficiaries=[],
            )
            phases.append(phase)
        departments[department_name] = Department(
            name=department_name,
            sheet_name=abbrev,
            lead=leads[abbrev],
            paragraph=paragraphs[abbrev],
            phases=phases,
        )

    for name in sorted(departments.keys()):
        all_data_departments.append(departments[name])

    abbrev_to_name = {}
    for dept in all_data_departments:
        abbrev = department_name_to_abbreviation[dept.name]
        abbrev_to_name[abbrev] = dept.name


    sprf_targets = []
    dpwi_target = 0
    for department in all_data_departments:
        # SPECIAL CASE CODE
        if department.name == "Agriculture, Land Reform and Rural Development":
            # DALLRD has a single programme in phases 1 and 2 but it is represented using multiple metrics
            # - the total target has its own special row in the targets sheet
            for phase in department.phases:
                if phase.phase_num == 0 or phase.phase_num == 1:
                    sprf_target = int(opportunity_targets_df[phase.phase_num].iloc[sprf_row[phase.phase_num], 2])
                    sprf_targets.append(sprf_target)
                    section = find_section(phase.sections, SectionEnum.targets.name)
                    section.value_target = sprf_target
        elif department.name == "Public Works and Infrastructure":
            # DPWI has two programmes in phase 1: the "Graduate programmes (Property Management Trading Entity)"
            # and "Project Administrators". The first of these is represented through multiple metrics
            # and the second one did not have a target. So the total target is represented in the targets sheet
            # by the entry for the "Graduate programmes (Property Management Trading Entity)"
            for phase in department.phases:
                if phase.phase_num == 0:
                    section = find_section(phase.sections, SectionEnum.targets.name)
                    dpwi_target = opportunity_targets_df[phase.phase_num].iloc[dpwi_target_row, 2]
                    section.value_target = dpwi_target
                    

    return (all_data_departments, sprf_targets, dpwi_target)


def filter_departments_by_max_phase(all_data_departments: list[Department], phase: int) -> list[Department]:
    """Filter out departments that don't have a phase <= phase"""
    return [department for department in all_data_departments if department.phases[-1].phase_num <= phase]


def find_section(sections: list[Section], section_name: str):
    for section in sections:
        if section.section_type == section_name:
            return section
    else:
        return None


def find_dimension(dimensions: list[Dimension], dimension_lookup: str):
    for dimension in dimensions:
        if dimension.lookup == dimension_lookup:
            return dimension
    else:
        return None


def merge_phases(all_data_departments: list[Department], sprf_target: int, dwpi_target: int, last_phase: int,
                 department_budget_targets: list[dict[str, float]], total_budgets: list[float]) -> list[Department]:
    max_phase_num = last_phase - 1
    # create synthetic metrics that contain all of the programmes in a section, summed across phases
    new_all_data_departments: list[Department] = []
    for department in all_data_departments:
        new_department = Department(name=department.name, sheet_name=department.sheet_name, lead=department.lead, paragraph=department.paragraph, phases=[])
        new_phase = Phase(phase_num= 0, month=department.phases[0].month, sections=[], target_lines=[], achievement_lines=[], implementation_details=[], beneficiaries=[])
        new_department.phases.append(new_phase)
        new_all_data_departments.append(new_department)
        for phase in department.phases:
            if phase.phase_num > max_phase_num:
                phase = copy.deepcopy(phase)
                phase.phase_num = 1
                new_department.phases.append(phase)
            else:
                new_phase.month = phase.month
                # each department has a "targets" Section with budget and opportunities targets
                # and then optionally a section for each of the CRE, LIV, RET sections
                for section in phase.sections:
                    if section.section_type == SectionEnum.targets.name:
                        if (new_section := find_section(new_phase.sections, SectionEnum.targets.name)) is None:
                            new_section = Section(name=section.name, section_type=section.section_type, metrics=[])
                            new_phase.sections.append(new_section)
                        # metrics_by_name: dict[str, Metric] = {}
                        # for metric in section.metrics:
                        #     metrics_by_name[metric.name] = metric
                        new_metrics_by_name: dict[str, Metric] = {}
                        for metric in new_section.metrics:
                            new_metrics_by_name[metric.name] = metric
                        for metric in section.metrics:
                            if metric.name not in new_metrics_by_name:
                                new_metric = copy.copy(metric)  # this does a shallow copy, which is fine because this section doesn't have Dimensions
                                new_metrics_by_name[metric.name] = new_metric
                                new_section.metrics.append(new_metric)
                            else:
                                new_metric = new_metrics_by_name[metric.name]
                                if metric.value != -1:
                                    new_metric.value += metric.value
                                if metric.value_target != -1:
                                    new_metric.value_target += metric.value_target
                    else:
                        new_section = find_section(new_phase.sections, section.section_type)
                        # all other sections have metrics with Dimensions - the aim is to gather these into a single "metric" for the section
                        if (new_section := find_section(new_phase.sections, section.section_type)) is None:
                            new_section = Section(name=section.name, section_type=section.section_type, 
                                                  metrics=[Metric(name="Consolidated", metric_type=MetricTypeEnum.count.name, value=0, dimensions=[])])
                            new_phase.sections.append(new_section)
                        new_metric = new_section.metrics[0]
                        for metric in section.metrics:
                            new_metric.value += metric.value
                            if metric.value_target != -1:
                                new_metric.value_target += metric.value_target
                            # SPECIAL CASE code: The DALLRD and DWPI metrics for phases 1 and 2 don't have target values, so they need to be inserted
                            # this code gets run once per metric but doesn't need to add up a total - there is one target for the consolidated
                            # section total
                            if department.name == "Agriculture, Land Reform and Rural Development" and section.section_type == SectionEnum.livelihoods.name:
                                new_metric.value_target = sprf_target
                            elif department.name == "Public Works and Infrastructure" and section.section_type == SectionEnum.job_opportunities.name:
                                new_metric.value_target = dwpi_target
                            for dimension in metric.dimensions:
                               if dimension.lookup in (LookupTypeEnum.age.name, LookupTypeEnum.province.name, LookupTypeEnum.gender.name):
                                      if (new_dimension := find_dimension(new_metric.dimensions, dimension.lookup)) is None:
                                        new_dimension = Dimension(name=dimension.name, lookup=dimension.lookup, viz=dimension.viz, values=[], data_missing=dimension.data_missing)
                                        new_metric.dimensions.append(new_dimension)
                                      new_values_by_key = {}
                                      for value in new_dimension.values:
                                        new_values_by_key[value.key] = value
                                      for value in dimension.values:
                                        if value.key not in new_values_by_key:
                                             new_value = copy.copy(value)
                                             new_dimension.values.append(new_value)
                                        else:
                                            new_value = new_values_by_key[value.key]
                                            new_value.value += value.value
                                            if new_dimension.lookup in (LookupTypeEnum.age.name, LookupTypeEnum.gender.name):
                                                new_value.multiplicity += 1
        
    # adjust percentage dimensions by dividing by multiplicity
    for department in new_all_data_departments:
        for phase in department.phases:
            if phase.phase_num == 0:
                for section in phase.sections:
                    if section.section_type == SectionEnum.targets.name:
                        continue
                    for metric in section.metrics:
                        for dimension in metric.dimensions:
                            if dimension.lookup in (LookupTypeEnum.age.name, LookupTypeEnum.gender.name):
                                for value in dimension.values:
                                    if value.multiplicity > 0:
                                        value.value /= value.multiplicity
                                        value.multiplicity = 1

    combined_department_budget_targets = {}                                          
    for phase in range(last_phase):
        # combine department budget targets for all phases but the last one
        for department in department_budget_targets[phase]:
            if department in combined_department_budget_targets:
                combined_department_budget_targets[department] += department_budget_targets[phase][department]
            else:
                combined_department_budget_targets[department] = department_budget_targets[phase][department]
    new_department_budget_targets = [combined_department_budget_targets, department_budget_targets[-1]] # the last phase's budget targets are unchanged
    new_total_budgets = [0, total_budgets[-1]   ] # the last phase's total budget is unchanged
    for phase in range(last_phase):
        new_total_budgets[0] += total_budgets[phase]

    return new_all_data_departments, new_department_budget_targets, new_total_budgets


def compute_breakdowns(all_data_departments: list[Department]):
    """Compute breakdowns by the different demographic dimensions"""
    total_male = [0] * number_of_phases
    total_female = [0] * number_of_phases
    total_unknown_gender = [0] * number_of_phases
    total_beneficiaries = [0] * number_of_phases
    total_youth = [0] * number_of_phases
    total_unknown_youth = [0] * number_of_phases
    total_provincial = {}
    for abbreviation in province_abbreviations:
        total_provincial[abbreviation] = [0] * number_of_phases
    total_unknown_province = [0] * number_of_phases

    for department in all_data_departments:

        for phase in department.phases:
            phase_num = phase.phase_num
            department_male = department_female = department_beneficiaries = 0
            for section in phase.sections:
                for metric in section.metrics:
                    if (
                        section.section_type == SectionEnum.targets.name
                        and metric.name == "Beneficiaries"
                    ):
                        total_beneficiaries[phase_num] += metric.value
                        # print("adding", department.sheet_name, phase_num, metric.value, total_beneficiaries)
                        department_beneficiaries = metric.value
                        continue
                    if metric.value == -1:
                        continue
                    total_value = metric.value
                    gender_found = False
                    age_found = False
                    province_found = False
                    for dimension in metric.dimensions:
                        if dimension.data_missing:
                            continue
                        if dimension.lookup == LookupTypeEnum.gender.name:
                            gender_found = True
                            for value in dimension.values:
                                if value.key == "Male":
                                    department_male += total_value * value.value
                                    total_male[phase_num] += total_value * value.value
                                elif value.key == "Female":
                                    department_female += total_value * value.value
                                    total_female[phase_num] += total_value * value.value
                        elif dimension.lookup == LookupTypeEnum.age.name:
                            age_found = True
                            youth_value = dimension.values[0].value
                            total_youth[phase_num] += youth_value * total_value
                        elif dimension.lookup == LookupTypeEnum.province.name:
                            province_found = True
                            for value in dimension.values:
                                total_provincial[value.key][phase_num] += value.value
                    if metric.value <= 0:
                        continue
                    if not gender_found:
                        total_unknown_gender[phase_num] += metric.value
                    if not age_found:
                        total_unknown_youth[phase_num] += metric.value
                    if not province_found:
                        total_unknown_province[phase_num] += metric.value
            # print(department.name, phase_num, total_beneficiaries, total_unknown_gender, round(total_unknown_gender / total_beneficiaries, 2),
            #       total_unknown_youth, round(total_unknown_youth / total_beneficiaries, 2),
            #       total_unknown_province, round(total_unknown_province / total_beneficiaries, 2))
    return (
        total_male,
        total_female,
        total_unknown_gender,
        total_beneficiaries,
        total_youth,
        total_unknown_youth,
        total_provincial,
        total_unknown_province,
    )


def compute_programmes_by_type(all_data_departments: list[Department]):
    """Compute programmes_by_type, which is an overview of programmes by the opportunity type
    """
    # what we need
    # - Total budget
    # - Total beneficiaries
    #   - target
    #   - achieved
    # Total female beneficiaries
    #  - % of total
    # Total youth beneficiaries
    #  - % of total
    # By section
    #   LIV, RET, CRE
    #   - target and achievement
    #   - by department and phase

    # we want a few things here:
    # for Overview we want top level info (and OverviewSection) with a total value per phase per section
    #
    # and then for departments we want a dictionary of department_name to MultiMetricValue (2 values, 1 per phase)
    
    # NOTE: for the purposes of this function we're just computing across the phases in the "merged" all_data_departments
    programmes_by_type = {
        SectionEnum.job_opportunities.name: dict(
            [(i, {}) for i in range(number_of_phases)]
        ),
        SectionEnum.livelihoods.name: dict([(i, {}) for i in range(number_of_phases)]),
        SectionEnum.jobs_retain.name: dict([(i, {}) for i in range(number_of_phases)]),
    }

    achievements_by_type_by_month = {}
    for section_type in [
        e.name
        for e in SectionEnum
        if e.name != "cat_interventions"
        and e.name != "targets"
        and e.name != "budget_allocated"
    ]:
        achievements_by_type_by_month[section_type] = {}
        for month in months:
            achievements_by_type_by_month[section_type][month] = 0

    # this stores the achievement values from the last months of the previous phase
    achievement_cache = {
        SectionEnum.job_opportunities.name: dict(
            [(i, 0) for i in range(number_of_phases - 1)]
        ),
        SectionEnum.livelihoods.name: dict(
            [(i, 0) for i in range(number_of_phases - 1)]
        ),
        SectionEnum.jobs_retain.name: dict(
            [(i, 0) for i in range(number_of_phases - 1)]
        ),
    }

    for department in all_data_departments:
        for phase_num, phase in enumerate(department.phases[:-1]):
            for section in phase.sections:
                for metric in section.metrics:
                    for dimension in metric.dimensions:
                        if (
                            dimension.values
                            and dimension.lookup == LookupTypeEnum.time.name
                        ):
                            # print("saving", section.section_type, dimension.values[-1].value)
                            achievement_cache[section.section_type][
                                phase_num
                            ] += dimension.values[-1].value

    provincial_breakdown = {}
    for section_name in (SectionEnum.job_opportunities.name, SectionEnum.livelihoods.name, SectionEnum.jobs_retain.name):
        provincial_breakdown[section_name] = {}
        for abbrev in province_abbreviations:
            provincial_breakdown[section_name][abbrev] = [0] * number_of_phases
    
    for department in all_data_departments:
        for phase in department.phases:
            # achievements_df = (
            #     opportunity_achievements_df[phase.phase_num].iloc[3:, 1:].set_index(1)
            # )
            section_value = 0
            section_target_value = 0
            for section in phase.sections:
                if section.section_type == SectionEnum.targets.name:
                    # skip over (budget and beneficiary) targets section
                    continue
                total_value = 0
                total_target_value = 0
                for metric in section.metrics:
                    for dimension in metric.dimensions:
                        if dimension.lookup == LookupTypeEnum.province.name:
                            for value in dimension.values:
                                provincial_breakdown[section.section_type][value.key][phase.phase_num] += value.value
                    #             if (
                    #                 department.sheet_name == "DALRRD"
                    #                 and metric.name == "Graduate Employment"
                    #             ):
                    #                 continue
                    # if phase.phase_num == 1 and section.section_type == SectionEnum.job_opportunities.name:
                    #     print(department.sheet_name, metric.value_target, metric.value)
                    # NOTE: this disabled because we now merge the phases - PvH 2024-02-11
                    # if metric.name not in achievements_df.index:
                    #     print(
                    #         "Metric not found in achievements_df",
                    #         department.name,
                    #         metric.name,
                    #     )
                    total_value += metric.value
                    if metric.value_target > 0:
                        total_target_value += metric.value_target
                    for dimension in metric.dimensions:
                        if dimension.lookup == LookupTypeEnum.time.name:
                            for metric_value in dimension.values:
                                month = metric_value.key
                                value = metric_value.value
                                achievements_by_type_by_month[section.section_type][
                                    month
                                ] += value

                # SPECIAL CASE code removed here because we now look up the target values
                # when we compute all_data_departments
                programmes_by_type[section.section_type][phase.phase_num][
                    department.sheet_name
                ] = {
                    "value": total_value,
                    "value_target": total_target_value,
                    "phase": phase.phase_num,
                }
                if (
                    "Total"
                    not in programmes_by_type[section.section_type][phase.phase_num]
                ):
                    programmes_by_type[section.section_type][phase.phase_num][
                        "Total"
                    ] = dict(value=0, value_target=0)
                programmes_by_type[section.section_type][phase.phase_num]["Total"][
                    "value"
                ] += total_value
                programmes_by_type[section.section_type][phase.phase_num]["Total"][
                    "value_target"
                ] += total_target_value
                section_value += total_value
                section_target_value += total_target_value

    for section_type in achievements_by_type_by_month:
        if section_type == "overview" or section_type == "in_process":
            continue
        for month in achievements_by_type_by_month[section_type]:
            for phase_num in range(1, number_of_phases):
                # print(month, phase_num, in_phase(phase_num, month), in_phase(phase_num - 1, month))
                # print("test 2", in_phase(phase_num - 1, month))
                if in_phase(phase_num, month) and not in_phase(phase_num - 1, month):
                    # print("adding cache to:", section_type, month,achievement_cache[section_type][phase_num - 1], "was", achievements_by_type_by_month[section_type][month])
                    achievements_by_type_by_month[section_type][
                        month
                    ] += achievement_cache[section_type][phase_num - 1]

    # we currently have programmes_by_type which is structured
    # programme_type -> phase -> department
    #
    # we need programme_type -> department -> phase
    # with phase_num starting at 1

    programmes_by_type_summarised = {}
    for programme_type in programmes_by_type:
        programmes_by_type_summarised[programme_type] = {}
        for phase_num in programmes_by_type[programme_type]:
            for department in programmes_by_type[programme_type][phase_num]:
                if department not in programmes_by_type_summarised[programme_type]:
                    programmes_by_type_summarised[programme_type][department] = {
                        "value": {},
                        "value_target": {},
                    }
                programmes_by_type_summarised[programme_type][department]["value"][
                    phase_num
                ] = programmes_by_type[programme_type][phase_num][department]["value"]
                programmes_by_type_summarised[programme_type][department][
                    "value_target"
                ][phase_num] = programmes_by_type[programme_type][phase_num][
                    department
                ][
                    "value_target"
                ]

    # pp.pprint(programmes_by_type_summarised)
    # pp = PrettyPrinter(indent=2)
    # pp.pprint(programmes_by_type)
    return (
        programmes_by_type,
        programmes_by_type_summarised,
        achievements_by_type_by_month,
        provincial_breakdown
    )


def sort_dept_metric(element):
    # element is a pair - (department_name, dictionary) where the dictionary contains
    # {'value': {phase_num: amount} ... }
    value = element[1]["value"]
    value_total = 0
    for phase_num in value:
        value_total += value[phase_num]
    return value_total


def compute_overview_breakdown(
    programmes_by_type_summarised, achievements_by_type_by_month, provincial_breakdown: dict[str, dict[str, list[int]]], number_of_phases: int
):
    
    breakdown_metrics = [
        PhasedMetric(
            name=section_titles[section_name],
            metric_type=section_name,
            viz=VizTypeEnum.full.name,
            total_value=sum(
                programmes_by_type_summarised[section_name]["Total"]["value"].values()
            ),
            total_value_target=sum(
                programmes_by_type_summarised[section_name]["Total"][
                    "value_target"
                ].values()
            ),
            value=programmes_by_type_summarised[section_name]["Total"]["value"],
            value_target=programmes_by_type_summarised[section_name]["Total"][
                "value_target"
            ],
            dimensions=[
                Dimension(
                    # by department needs to have a MultiMetricValue
                    name="by department",
                    viz=VizTypeEnum.bar.name,
                    lookup=LookupTypeEnum.department.name,
                    values=[
                        MultiMetricValue(
                            key=department_name,
                            value=outputs["value"],
                            value_target=outputs["value_target"],
                        )
                        for department_name, outputs in sorted(
                            department_info.items(),
                            key=sort_dept_metric,
                            reverse=True,
                        )
                        if sum(outputs["value_target"].values()) > 0
                        and not (
                            department_name.startswith("value")
                            or department_name == "Total"
                        )
                    ],
                ),
                Dimension(
                    # by time needs to have PhasedMetricValues - currently this is broken
                    # because I don't know how to handle overlapping phases
                    name="over time",
                    viz=VizTypeEnum.line.name,
                    lookup=LookupTypeEnum.time.name,
                    values=[
                        MetricValue(key=key, value=value)
                        for key, value in achievements_by_type_by_month[
                            section_name
                        ].items()
                    ],
                ),
                Dimension(
                    name="by province",
                    viz=VizTypeEnum.bar.name,
                    lookup=LookupTypeEnum.province.name,
                    values=[
                        MultiMetricValue(
                            key=province_abbrev,
                            value=provincial_breakdown[section_name][province_abbrev]
                        ) for province_abbrev in sorted(provincial_breakdown[section_name].keys())
                    ]
                )
            ],
        )
        for section_name, department_info in programmes_by_type_summarised.items()
        if not section_name.startswith("value")
    ]
    # add up all the metrics across all the programmes
    current_targets = dict(
        [
            (
                phase_num,
                sum(
                    [
                        metric.value[phase_num] if metric.value[phase_num] > 0 else 0
                        for metric in breakdown_metrics
                    ]
                ),
            )
            for phase_num in range(number_of_phases)
        ]
    )
    current_achievements = dict(
        [
            (
                phase_num,
                sum(
                    [
                        metric.value_target[phase_num]
                        if metric.value_target[phase_num] > 0
                        else 0
                        for metric in breakdown_metrics
                    ]
                ),
            )
            for phase_num in range(number_of_phases)
        ]
    )

    return (breakdown_metrics, current_targets, current_achievements)


def compute_overview_metrics(
    total_female,
    total_beneficiaries,
    total_unknown_gender,
    programmes_by_type,
    total_youth,
    total_unknown_youth,
    department_budget_targets,
    total_budgets,
    number_of_phases: int
):
    # metrics breakdown
    female_by_phases = {}
    phase_total_budgets = []
    for i, phase_num in enumerate(range(number_of_phases)):
        female_by_phases[phase_num] = total_female[phase_num] / (total_beneficiaries[phase_num] - total_unknown_gender[phase_num])
        phase_total_budgets.append(sum(department_budget_targets[i].values()))
        assert total_budgets[i] == phase_total_budgets[i], f"Budget in Phase {phase_num} spreadsheet is not the same as computed budget: {total_budgets[i]} vs {phase_total_budgets[i]}" 
    
    overall_female_perc = sum(female_by_phases.values()) / number_of_phases

    overview_metrics = []

    total_budget = PhasedMetric(
        name="Total budget allocated",
        metric_type=MetricTypeEnum.currency.name,
        viz=VizTypeEnum.full.name,
        total_value=sum(phase_total_budgets),
        value=phase_total_budgets,
        value_target=[None] * number_of_phases,
        dimensions=[],
    )
    overview_metrics.append(total_budget)

    achievements_by_phase_value = dict(
        [(phase_num, 0) for phase_num in range(number_of_phases)]
    )
    achievements_by_phase_value_target = dict(
        [(phase_num, 0) for phase_num in range(number_of_phases)]
    )

    for section_type in programmes_by_type:
        for phase_num in range(number_of_phases):
            # print(section_type, programmes_by_type[section_type][phase_num]['Total'])
            achievements_by_phase_value[phase_num] += programmes_by_type[section_type][
                phase_num
            ]["Total"]["value"]
            achievements_by_phase_value_target[phase_num] += programmes_by_type[
                section_type
            ][phase_num]["Total"]["value_target"]

    achievements = PhasedMetric(
        name="Total opportunities",
        metric_type=MetricTypeEnum.count.name,
        viz=VizTypeEnum.full.name,
        total_value=sum(achievements_by_phase_value.values()),
        value=achievements_by_phase_value,
        total_value_target=sum(achievements_by_phase_value_target.values()),
        value_target=achievements_by_phase_value_target,
        dimensions=[],
    )
    overview_metrics.append(achievements)

    gender_breakdown = PhasedMetric(
        name="Total female beneficiaries",
        metric_type="targets_count",
        viz=VizTypeEnum.compact.name,
        value=female_by_phases,
        total_value=overall_female_perc,
        value_target=-1,
        dimensions=[],
    )
    overview_metrics.append(gender_breakdown)

    youth_by_phases = {}
    for phase_num in range(number_of_phases):
        # SPECIAL CASE CODE: This is here because for the current (2024) data Kate wants
        # the youth percentage to be calculated as a percentage of the total beneficiaries,
        # including the unknowns. This is different from the previous years
        if phase_num == 1:
            total = total_beneficiaries[phase_num]
        else:
            total = (total_beneficiaries[phase_num] - total_unknown_youth[phase_num])
        youth_by_phases[phase_num] = total_youth[phase_num] / total

    overall_youth_perc = sum(youth_by_phases.values()) / number_of_phases
    youth_breakdown = PhasedMetric(
        name="Total youth beneficiaries",
        metric_type="targets_count",
        viz=VizTypeEnum.compact.name,
        value=youth_by_phases,
        total_value=overall_youth_perc,
        value_target=-1,
        dimensions=[],
    )
    overview_metrics.append(youth_breakdown)

    return overview_metrics


def compute_overview(
    description_df,
    leads,
    paragraphs,
    overview_metrics,
    current_targets,
    current_achievements,
    breakdown_metrics,
):

    overview_name = "Overview"
    month_info = description_df.loc[overview_name, "Data captured until"]
    try:
        month = month_info.strftime("%Y%m")
    except AttributeError as e:
        month_parts = month_info.split("-")
        month = month_parts[2] + month_parts[1]
    overview = Overview(
        month=month,
        name="Programme overview",
        lead=leads[overview_name],
        phase_dates=phase_dates,
        paragraph=paragraphs[overview_name],
        footer_header=leads["Disclaimer"],
        footer_paragraph=paragraphs["Disclaimer"],
        sections=[
            Section(
                name="Programme Achievements",
                section_type=SectionEnum.overview.name,
                metrics=overview_metrics,
                value=current_targets,
                value_target=current_achievements,
            ),
            Section(
                name="Performance breakdown",
                section_type=SectionEnum.overview.name,
                metrics=breakdown_metrics,
                value=[-1, -1],
                value_target=[-1, -1],
            ),
        ],
    )

    # overview.sections.insert(
    #     0,
    #     Section(
    #         name=section_titles[SectionEnum.targets.name + "_overview"],
    #         section_type=SectionEnum.targets.name,
    #         metrics=[
    #             Metric(
    #                 name=metric_titles[SectionEnum.targets.name][
    #                     MetricTypeEnum.currency.name
    #                 ],
    #                 metric_type=MetricTypeEnum.currency.name,
    #                 dimensions=[],
    #                 # value=int(opportunity_targets_df.iloc[2, 7] * 1000),
    #                 value=0,
    #                 value_target=(opportunity_targets_df.iloc[2, 6] * 1000),
    #             ),
    #             Metric(
    #                 name=metric_titles[SectionEnum.targets.name][MetricTypeEnum.count.name],
    #                 metric_type=MetricTypeEnum.count.name,
    #                 dimensions=[],
    #                 value=int(
    #                     opportunity_achievements_df.iloc[59, total_achievement_column]
    #                 ),
    #                 value_target=int(opportunity_targets_df.iloc[56, 2]),
    #             ),
    #             Metric(
    #                 name="Opportunities in process",
    #                 metric_type=MetricTypeEnum.count.name,
    #                 dimensions=[],
    #                 value_target=int(opportunity_achievements_df.iloc[2, 1]),
    #                 value=0,
    #             ),
    #         ],
    #         value=None,
    #         value_target=None,
    #     ),
    # )

    # # print(overview.to_json(indent=2))
    return overview
