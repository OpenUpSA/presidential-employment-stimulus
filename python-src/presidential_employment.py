from cmath import phase
from enum import Enum
from dataclasses import dataclass
from pprint import PrettyPrinter
from typing import Counter, List, Union, Mapping

from dataclasses_json import dataclass_json
import pandas as pd

SectionEnum = Enum(
    "Section", "targets overview budget_allocated job_opportunities jobs_retain livelihoods in_process"
)

MetricTypeEnum = Enum("MetricType", "currency count")

ProvinceEnum = Enum("Province", "EC FS GP KZN LP MP NC NW WC")

ImplementationStatusEnum = Enum('ImplementationStatus', 'OnTrack MinorChallenges CriticalChallenges')

VizTypeEnum = Enum('VizType', 'bar line two_value percentile count full compact')

LookupTypeEnum = Enum('LookupType', 'department province time age gender vets disabled')

GenderEnum = Enum("Gender", "Male Female")

provinces = [
    "Eastern Cape",
    "Free State",
    "Gauteng",
    "KwaZulu-Natal",
    "Limpopo",
    "Mpumalanga",
    "North West",
    "Northern Cape",
    "Western Cape",
]
province_abbreviations = ["EC", "FS", "GP", "KZN", "LP", "NW", "NC", "WC", "MP"]

province_to_abbrev = {
    "Free State": "FS",
    "Gauteng": "GP",
    "KwaZulu-Natal": "KZN",
    "Limpopo": "LP",
    "Mpumalanga": "MP",
    "North West": "NW",
    "Northern Cape": "NC",
    "Western Cape": "WC",
    "Eastern Cape": "EC",
}

province_header_to_abbrev = {
    "free_state": "FS",
    "gauteng": "GP",
    "kwazulu_natal": "KZN",
    "limpopo": "LP",
    "mpumalanga": "MP",
    "north_west": "NW",
    "northern_cape": "NC",
    "western_cape": "WC",
    "eastern_cape": "EC",
}

department_name_to_abbreviation = {
 'Basic Education': 'DBE',
 'Social Development': 'DSD',
 'Agriculture, Land Reform and Rural Development': 'DALRRD',
 'Forestry, Fisheries and Environment': 'DFFE',
 'Transport': 'DoT',
 'Sports, Arts and Culture': 'DSAC',
 'Cooperative Governance': 'DCOGTA',
 'Trade, Industry and Competition': 'DTIC',
 'Health': 'DoH',
 'Science and Innovation': 'DSI',
 'Public Works and Infrastructure': 'DPWI',
 'National Treasury': 'NT',
 'Higher Education': 'DHET',
 'Tourism': 'Tourism',
 'Employment and Labour': 'DEL',
 'Communications and Digital Technologies': 'DCDT',
 'Women, Youth and Persons with Disabilities': 'DWYPD',
}

department_budget_targets = [{
    'Basic Education': 7_000_000 * 1000,
    'Social Development': 7_000_000 * 1000,
    'Agriculture, Land Reform and Rural Development': 1_000_000_000,
    'Forestry, Fisheries and Environment': 1_983_000 * 1000,
    'Transport': 630_000_000,
    'Sports, Arts and Culture': 665_000_000,
    'Cooperative Governance': 50_000_000,
    'Trade, Industry and Competition': 120_000 * 1000,
    'Health': 180_000_000,
    'Science and Innovation': 45_000_000,
    'Public Works and Infrastructure': 159_000_000
}, {
    'Basic Education': 6_000_000 * 1000, # CRE
    'National Treasury': 841_000 * 1000, # CRE
    'Trade, Industry and Competition': 800_000 * 1000, # CRE
    'Health': 365_000 * 1000, # CRE
    'Forestry, Fisheries and Environment': 318_000 * 1000, # CRE
    'Higher Education': (100_000 * 1000) + (90_000) * 1000, # CRE
    'Sports, Arts and Culture': 15_000 * 1000, # CRE
    'Cooperative Governance': 284_000 * 1000, # CRE 
    'Science and Innovation': 67_000 * 1000, # CRE
    'Tourism': 108_000 * 1000, # CRE
    'Employment and Labour': (20_000 * 1000) + (238_000 * 1000), # CRE and CAT
    'Communications and Digital Technologies': 200_000 * 1000, # CAT
    'Women, Youth and Persons with Disabilities': 30_000 * 1000, # CRE
    'Social Development': 178_000 * 1000, # LIV
    'Agriculture, Land Reform and Rural Development': 750_000 * 1000, # LIV
}
]

section_titles = {
    SectionEnum.targets.name: "Programme targets for this department",
    SectionEnum.job_opportunities.name: "Jobs created",
    SectionEnum.jobs_retain.name: "Jobs retained",
    SectionEnum.livelihoods.name: "Livelihoods supported",
    SectionEnum.targets.name + "_overview": "Programme achievements",
    SectionEnum.job_opportunities.name + "_overview": "Job opportunities",
    SectionEnum.jobs_retain.name + "_overview": "Jobs retained",
    SectionEnum.livelihoods.name + "_overview": "Livelihoods supported",
    SectionEnum.in_process.name: "Opportunities in process"
}

metric_titles = {
    SectionEnum.targets.name: {
        MetricTypeEnum.currency.name: "Budget",
        MetricTypeEnum.count.name: "Beneficiaries",
    },
    SectionEnum.job_opportunities.name: {
        MetricTypeEnum.count.name + '_time': "Employed over time",
        MetricTypeEnum.count.name + '_gender': "Opportunities by Gender",
        MetricTypeEnum.count.name + '_province': "Opportunities in post by Province",
        MetricTypeEnum.count.name + '_age': "Opportunities going to 18-35 year olds",
        MetricTypeEnum.count.name + "_disabled": "Opportunities going to disabled persons",
    },
    SectionEnum.jobs_retain.name: {
        MetricTypeEnum.count.name + "_time": "Jobs saved over time",
        MetricTypeEnum.count.name + "_gender": "Jobs saved by gender",
        MetricTypeEnum.count.name + "_province": "Jobs saved by province",
        MetricTypeEnum.count.name + "_age": "Jobs saved going to 18-35 year olds",
    },
    SectionEnum.livelihoods.name: {
        MetricTypeEnum.count.name + "_time": "Livelihoods supported over time",
        MetricTypeEnum.count.name + "_gender": "Livelihoods supported by gender",
        MetricTypeEnum.count.name + "_province": "Livelihoods supported by province",
        MetricTypeEnum.count.name + "_age": "Livelihoods supported going to 18-35 year olds",
        MetricTypeEnum.count.name + '_vets': "Livelhoods supported going to military veterans",
        MetricTypeEnum.count.name + '_disabled': "Livelhoods supported going to disabled persons",
    }
}

section_abbrev_to_name = {
    'CRE': SectionEnum.job_opportunities.name,
    'LIV': SectionEnum.livelihoods.name,
    'RET': SectionEnum.jobs_retain.name
}

@dataclass_json
@dataclass
class ImplementationDetail:
    programme_name: str
    status: str = None  # enum of OnTrack MinorChallenges CriticalChallenges
    detail: str = None    


@dataclass_json
@dataclass
class MetricValue:
    key: str
    value: Union[float, int]
    value_target: Union[float, int] = None


@dataclass_json
@dataclass
class MultiMetricValue:
    key: str
    value: Mapping[int, Union[float, int]]
    value_target: Mapping[int, Union[float, int]] = None


@dataclass
class PhasedMetricValue:
    key: str
    phase: int
    value: Union[float, int]
    value_target: Union[float, int] = None


@dataclass_json
@dataclass
class Dimension:
    name: str
    viz: str  # enum of VizType "bar" "line" "two_value" "percentile" "count"
    lookup: str  # enum of LookupType "department", "province", "gender", "age", "disability", "military_veteran"
    values: List[Union[MetricValue, PhasedMetricValue, MultiMetricValue]]
    data_missing: bool = False

@dataclass_json
@dataclass
class Metric:
    name: str
    metric_type: str  # enum of 'currency', 'count'
    value: int
    dimensions: List[Dimension] = None
    value_target: int = -1
    implementation_detail: ImplementationDetail = None


@dataclass_json
@dataclass
class PhasedMetric:
    name: str
    metric_type: str  # enum of 'currency', 'count'
    value: List[int]
    total_value: int
    # phases: List[MetricValue]
    viz: str # enum of "full" and "compact"
    dimensions: List[Dimension] = None
    value_target: List[int] = None
    total_value_target: int = None
    implementation_detail: ImplementationDetail = None


@dataclass_json
@dataclass
class Section:
    name: str
    section_type: str  # enum of 'targets', 'budget_allocated', 'job_opportunities', 'jobs_retain', 'livelihoods'
    metrics: List[Union[Metric, PhasedMetric]]
    metric_type = str = None # enum of MetricTypeEnum
    value: int = None
    value_target: int = None


# @dataclass_json
# @dataclass
# class OverviewSection:
#     name: str
#     section_type: str  # enum of 'targets', 'budget_allocated', 'job_opportunities', 'jobs_retain', 'livelihoods'
#     metrics: List[PhasedMetric]
#     metric_type = str = None # enum of MetricTypeEnum
#     value: int = None
#     value_target: int = None


@dataclass_json
@dataclass
class Beneficiary:
    name: str
    department_name: str
    blurb: str
    paragraph: str
    picture_url: str
    featured: bool

    
@dataclass_json
@dataclass
class Phase:
    phase_num: int  # the phase number, starting at 0
    month: int  # the month of latest data
    target_lines: List[int]
    achievement_lines: List[int]
    sections: List[Section]
    implementation_details: List[ImplementationDetail]
    beneficiaries: List[Beneficiary]

@dataclass_json
@dataclass
class Department:
    name: str
    phases: List[Phase]
    sheet_name: str
    lead: str
    paragraph: str


@dataclass_json
@dataclass
class PhaseDates:
    start: str
    end: str


@dataclass_json
@dataclass
class Overview:
    month: int
    name: str  # Would normally be "Programme Overview"
    lead: str
    paragraph: str
    phase_dates: List[PhaseDates]
    footer_header: str
    footer_paragraph: str
    sections: List[Section]


@dataclass_json
@dataclass
class Everything:
    overview: Overview
    departments: List[Department]

implementation_status_to_enum = {
    'On track': ImplementationStatusEnum.OnTrack.name,
    'Minor challenges': ImplementationStatusEnum.MinorChallenges.name,
    'Critical challenges': ImplementationStatusEnum.CriticalChallenges.name
}

# leads = dict(
#     overview="Building a society that works",
#     DTIC="Piloting new models for re-shoring and expanding global business services",
#     DBE="Teachers assistants and other support for schools",
#     DSD="Income support to practitioners and to the implementation of Covid compliance measures",
#     DOH="Primary Health Care is at the frontline of the battle against Covid-19",
#     DALRRD="Expanding support to farmers and protecting food value chains",
#     DSI="Supporting new graduates entering a hostile labour market",
#     DSAC="To get artists, cultural workers and the sporting sector on the road to recovery",
#     DoT="Improving access to services and opportunities for people in rural areas",
#     DPWI="Graduate placements in the professional services",
#     DEFF="Investing in the environment we live in",
#     DCOGTA="Mainstreaming and improving labour-intensity in infrastructure delivery",
# )

# paragraphs = dict(
#     overview="The COVID-19 pandemic has had a devastating economic impact, threatening the jobs and livelihoods of many South Africans – especially the most vulnerable. The pandemic has exacerbated South Africa’s pre-existing crises of poverty and unemployment.The Presidential Employment Stimulus seeks to confront this impact directly, as part of government’s broader economic recovery agenda. Its aim is to use direct public investment to support employment opportunities – starting right now.",
#     DTIC="The Global Business Services Sector has an impressive track record. Established in 2006/7 to provide offshore customer service delivery, the sector has built from a low base to achieve an average year-on-year export revenue growth of at least 20% since 2014.",
#     DBE="A key priority identified in the National Development Plan is the improvement of quality education, skills development, and innovation. One intervention that has seen some experimentation in South Africa, with significant potential to scale nationally, is the use of school assistants to strengthen the learning environment. An important rationale for school assistants is the need to support teachers in the classroom, freeing up time for teaching and providing additional support to learners to improve education outcomes.",
#     DSD="Livelihoods from the provision of Early Childhood Development services were severely disrupted by the pandemic, with providers facing challenges with re-opening. There are costs associated with doing so safely, and some parents can no longer afford to pay fees as a result of job losses.",
#     DOH="As the world responds to the COVID-19 pandemic, the critical role that community health workers play to enhance the resilience of the national health care system has been foregrounded. They have been on the frontline of active case-finding through screening and contact tracing.",
#     DALRRD="The pandemic has illustrated the vulnerability of our food production and distribution systems. Although exempt from the strictest lockdown regulations, the sector faced severe challenges with disruptions to production and marketing experienced by many small-scale farmers. ",
#     DSI="Given a constrained labour market, fewer opportunities will be available to graduates leaving institutions of higher learning in 2021.\n\nThe Department of Science and Innovation will deliver four programmes through its entities designed to minimise this impact, which will together offer 1,900 unemployed graduates an opportunity to earn an income while gaining meaningful work experience.",
#     DSAC="Under lockdown, there has been no loud applause in jazz venues, no curtain calls for the dancers, no tourists in craft markets – and no victory laps for our sports people. No segment of the creative, cultural and sporting sectors have been untouched",
#     DoT="Rural roads play a vital role in connecting rural communities to services such as health and education, as well as providing access to markets and economic opportunities. However, rural roads infrastructure remains poor in many areas of South Africa",
#     DPWI="In addition to structural skills shortages that were experienced prior to the pandemic, the management of facilities and completion of infrastructure projects has been further impacted by restrictions on the movement of people and limitations placed on completing infrastructure projects during the lockdown. As the economy re-opens, additional capacity is required to address the backlog so that service provision can be restored",
#     DEFF="The work undertaken in environmental, forestry and fishery programmes will touch the length and breadth of the country, from coast to coast, including bushveld, grassland, fynbos, wetlands, mountains, water bodies, catchment areas  – and urban areas, too. The work undertaken affects the air we breathe, the water we drink, the energy we use and the food we eat, supporting a wealth of biodiversity resources and ecological systems essential to life on earth and to the future of the planet.",
#     DCOGTA="Prioritising infrastructure maintenance Mainstreaming and improving labour-intensity in infrastructure deliveryCommunity access to water and sanitation is all the more important in the context of the crisisTOTAL BUDGETR50MJOB OPPORTUNITIES25,000 Before the crisis, many municipalities were already facing critical funding shortfalls and challenges in the sustainable delivery of basic services and the maintenance of infrastructure. The pandemic has compounded these problems by cancelling or stalling implementation of all non-critical infrastructure projects",
# )

# NOTE: UPDATE THESE ROWS EACH TIME A NEW MONTH'S DATA IS ADDED
months = ['202010', '202011', '202012', 
          '202101', '202102', '202103', '202104', '202105', '202106', '202107', '202108', '202109', '202110', '202111', '202112',
          '202201', '202202', '202203', '202204']
month_names = ["Oct '20", "Nov '20", "Dec '20", 
               "Jan '21", "Feb '21", "Mar '21", "Apr '21", "May '21", "Jun '21", "Jul '21", "Aug '21", "Sep '21", "Oct '21", "Nov '21", "Dec '21",
               "Jan '22", "Feb '22", "Mar '22", "Apr '22"]
# the last column index of the achievements (i.e. Trends) sheets (one number per phase)
total_achievement_column = [16,8]

# achievement_columns = [slice(2, 11), slice(2,6)]
month_lookup = [{  # these match column names of the Dashboard spreadsheet's Trends sheet
    'oct': '202010',
    'nov': '202011',
    'dec': '202012',
    'jan': '202101',
    'feb': '202102',
    'mar': '202103',
    'apr': '202104',
    'may': '202105',
    'june': '202106',
    'july': '202107',
    'aug': '202108',
    'sept': '202109',
    'oct.1': '202110',
    'nov.1': '202111',
    'dec.1': '202112'
},
{
    'oct': '202110',
    'nov': '202111',
    'dec': '202112',
    'jan': '202201',
    'feb': '202202',
    'mar': '202203',
    'apr': '202204'
}]

number_of_phases = 2
phase_dates = [
    ['202010', '202112'],
    ['202110', '202204']
]


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

def load_sheets(phase1_excel, phase2_excel):
    """Reads in the phase1 and phase2 Excel files and extracts:
        * opportunity_targets_df - complete Targets sheet
        * opportunity_achievements_df - complete Trends sheet
        * implementation_status_df - Implementation Status
        * description_df - Department Descriptions
        * phase1_departments - department names that are in phase 1
        * phase2_departments - department names that are in phase 2
        * targets_df - just the per department Targets
        * trends_df - the per department Trends
        * provincial_df - provincial breakdowns
        * demographic_df - 
        """
    opportunity_targets_df = [pd.read_excel(
        phase1_excel, sheet_name="Targets", header=None
    ).fillna(0)]

    opportunity_targets_df.append(pd.read_excel(
        phase2_excel, sheet_name="Targets", header=None
    ).fillna(0))

    opportunity_achievements_df = [pd.read_excel(
        phase1_excel, sheet_name="Trends", header=None
    ).fillna(0)]

    opportunity_achievements_df.append(pd.read_excel(
        phase2_excel, sheet_name="Trends", header=None
    ).fillna(0))

    implementation_status_df = [pd.read_excel(
        phase1_excel,
        sheet_name="Implementation status",
        skiprows=2,
        usecols=range(4),
        names=["department", "programme", "status", "detail"],
    )]

    implementation_status_df.append(pd.read_excel(
        phase2_excel,
        sheet_name="Implementation status",
        skiprows=2,
        usecols=range(4),
        names=["department", "programme", "status", "detail"],
    ))

    for i in range(len(implementation_status_df)):
        implementation_status_df[i].department = implementation_status_df[i].department.fillna(method='pad')
        implementation_status_df[i].detail = implementation_status_df[i].detail.fillna('')

    description_df = pd.read_excel(
        phase2_excel,
        sheet_name="Department Descriptions",
        names=['key', 'lead', 'paragraph', 'Data captured until'],
        usecols=range(4),
        index_col=0
    ).dropna()
    
    # opportunity_type_df = pd.concat(
    #     [opportunity_targets_df.iloc[2:56, 1], opportunity_targets_df.iloc[2:56, 4]], axis=1
    # ).set_index(1)

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

    targets_df = [pd.read_excel(
        phase1_excel,
        sheet_name="Targets",
        skiprows=1,
        usecols=list(range(6)),
        names=["department", "programme", "target", "unk", "section", "display_name"],
    ).drop("unk", axis=1)]

    targets_df.append(pd.read_excel(
        phase2_excel,
        sheet_name="Targets",
        skiprows=1,
        usecols=list(range(6)),
        names=["department", "programme", "target", "unk", "section", "display_name"],
    ))

    for i in range(len(targets_df)):
        targets_df[i].department = targets_df[i].department.fillna(method="pad")
        targets_df[i].section = targets_df[i].section.fillna(method="pad")

    trends_df = [pd.read_excel(
        phase1_excel,
        sheet_name="Trends",
        skiprows=5,
        usecols=list(range(total_achievement_column[0]+1)),
    )]

    trends_df.append(pd.read_excel(
        phase2_excel,
        sheet_name="Trends",
        skiprows=4,
        usecols=list(range(total_achievement_column[1]+1)),
    ))

    for i in range(len(trends_df)):
        trends_df[i].columns = [c.lower() for c in trends_df[i].columns]
        trends_df[i].department = trends_df[i].department.fillna(method="pad")
        trends_df[i] = trends_df[i].fillna(0)
        if i == 1:
            # TODO: document why we drop the october column from phase2 trends
            trends_df[i] = trends_df[i].drop('oct', axis=1)

    provincial_df = [pd.read_excel(
        phase1_excel,
        sheet_name="Provincial (beneficiaries)",
        skiprows=4,
        usecols=list(range(12)),
    )]
    provincial_df.append(pd.read_excel(
        phase2_excel,
        sheet_name="Provincial (beneficiaries)",
        skiprows=4,
        usecols=list(range(12)),
    ))

    for i in range(len(provincial_df)):
        provincial_df[i].columns = [
            c.lower().replace(" ", "_").replace("-", "_") for c in provincial_df[i].columns
        ]
        provincial_df[i].department = provincial_df[i].department.fillna(method="pad")
        provincial_df[i] = provincial_df[i].fillna(0)

    demographic_df = [pd.read_excel(
        phase1_excel,
        sheet_name="Demographic data",
        skiprows=8,
        usecols=list(range(9)),
    )]

    demographic_df.append(pd.read_excel(
        phase2_excel,
        sheet_name="Demographic data",
        skiprows=9,
        usecols=list(range(9)),
    ))

    for i in range(len(demographic_df)):
        demographic_df[i].columns = [
            c.lower().replace(" ", "_").replace("%", "perc").replace('no.', 'no') for c in demographic_df[i].columns
        ]
        demographic_df[i].department = demographic_df[i].department.fillna(method="pad")
    # demographic_df = demographic_df.fillna(0)

    achievement_totals_df = [pd.read_excel(phase1_excel, sheet_name='Demographic data', skiprows=2, usecols=range(2), nrows=3, names=['section', 'total'], index_col=0)]
    achievement_totals_df.append(
        pd.read_excel(phase2_excel, sheet_name='Demographic data', skiprows=2, usecols=range(2), nrows=3, names=['section', 'total'], index_col=0)
    )

    return (opportunity_targets_df,
            opportunity_achievements_df,
            implementation_status_df,
            description_df,
            phase1_departments,
            phase2_departments,
            targets_df,
            trends_df,
            provincial_df,
            demographic_df,
            achievement_totals_df)


def make_dim(dim_type, lookup_type, df, col_start, col_end, key_lookup,
             department_name, programme_name, section):
    row = df.loc[(df.department == department_name) & (df.programme == programme_name)]
    values = []
    if len(df.loc[(df.department == department_name) & (df.programme == programme_name)]) == 0:
        data_missing = True
    else:
        nonzero = False
        for key in list(row)[col_start:col_end]:
            value = int(row.loc[:, key])
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
            MetricTypeEnum.count.name + "_" + dim_type
        ],
        lookup=dim_type,
        viz=lookup_type,
        values=values,
        data_missing=data_missing,
    )
    return dim


def compute_all_data_departments(phase1_departments, phase2_departments, 
                                 implementation_status_df, demographic_df, description_df,
                                 targets_df, trends_df, department_names, provincial_df,
                                 leads, paragraphs):
    """Compute all_data_departments, which summarises programmes for all departments
       (what will become the department tabs)"""
    all_data_departments = []

    desc_abbrevs = {"DoH": "DoH",
                    "Tourism": "Tourism ",
                    "DPWI": "DPWI ",
                    "DCOGTA": "COGTA" }  # deal with special cases in description lookup
    departments = {}
    for department_name in department_names:
        phases = []
        for phase_num in range(number_of_phases):
            if phase_num == 0 and (not department_name in phase1_departments):
                continue
            elif phase_num == 1 and (not department_name in phase2_departments):
                continue
            department_implementation_details = []
            target_section = Section(
                name=section_titles[SectionEnum.targets.name],
                section_type=SectionEnum.targets.name,
                metrics=[
                    Metric(
                        name=metric_titles[SectionEnum.targets.name][
                            MetricTypeEnum.currency.name
                        ],
                        metric_type=MetricTypeEnum.currency.name,
                        value_target=department_budget_targets[phase_num][department_name],
                        value=-1,
                        dimensions=[],
                    ),
                    Metric(
                        name=metric_titles[SectionEnum.targets.name][MetricTypeEnum.count.name],
                        metric_type=MetricTypeEnum.count.name,
                        value_target=targets_df[phase_num].loc[
                            targets_df[phase_num].department == department_name
                        ].target.sum(),  # overall target of beneficiaries
                        value=trends_df[phase_num].loc[trends_df[phase_num].department == department_name]
                        .iloc[:, -1]
                        .sum(),  # get the achievement by summing the last column in trends
                        dimensions=[],
                    ),
                ],
            )
            
            sections = [target_section]
            for section in ["CRE", "LIV", "RET"]:  # TODO: support CAT - Catalytic Interventions
                programme_names = list(
                    targets_df[phase_num].loc[
                        (targets_df[phase_num].section == section)
                        & (targets_df[phase_num].department == department_name)
                    ].programme
                )
                if phase_num == 0 and section == 'CRE' and department_name == 'Agriculture, Land Reform and Rural Development':
                    # this does not have a target so needs to be added manually
                    programme_names += ['Graduate verifiers']
                metrics = []

                for programme_name in programme_names:
                    if department_name == 'Public Works and Infrastructure' and programme_name == 'Project Administrators':
                        # this programme is mentioned in Targets and has a line in Implementation Status but has no other data
                        continue
                    imp_status_row = implementation_status_df[phase_num].loc[
                        (implementation_status_df[phase_num].department == department_name)
                        & (implementation_status_df[phase_num].programme == programme_name)
                    ]
                    if len(imp_status_row) == 0 or pd.isna(imp_status_row.status.iloc[0]):
                        imp_detail = None
                    else:
                        imp_detail = ImplementationDetail(
                            programme_name=programme_name,
                            status=implementation_status_to_enum[imp_status_row.status.iloc[0].strip()],
                            detail=imp_status_row.detail.iloc[0].strip(),
                        )
                    if (
                        department_name == "Public Works and Infrastructure"
                        and programme_name
                        == "Graduate programmes (Property Management Trading Entity)"
                    ) or (
                        department_name == "Agriculture, Land Reform and Rural Development"
                        and programme_name == "Subsistence producer relief fund"
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
                            dimensions.append(make_dim(LookupTypeEnum.province.name,
                                                       VizTypeEnum.bar.name,
                                                       provincial_df[phase_num], 2, -1, lambda key: province_header_to_abbrev[key],
                                                       department_name, programme_name, section))
                            dimensions.append(make_dim(LookupTypeEnum.time.name,
                                                       VizTypeEnum.line.name, trends_df[phase_num], 2, None, lambda key: month_lookup[phase_num][key],
                                                       department_name, programme_name, section))

                            demographic_row = demographic_df[phase_num].loc[
                                (demographic_df[phase_num].department == department_name)
                                & (demographic_df[phase_num].programme == programme_name)
                            ]

                            values = []
                            if len(demographic_row) == 0:
                                data_missing = True
                            else:
                                male_perc = demographic_row.loc[:, "perc_male"].iloc[0]
                                female_perc = demographic_row.loc[:, "perc_female"].iloc[0]
                                if male_perc + female_perc == 0:
                                    data_missing = True
                                else:
                                    values=[
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
                                        print("M/F PERC PROBLEM:", department_name, programme_name, phase_num, male_perc, female_perc, male_perc + female_perc)
                                    data_missing=False

                            gender_dim = Dimension(
                                name=metric_titles[section_abbrev_to_name[section]][
                                    MetricTypeEnum.count.name + "_gender"
                                ],
                                lookup=LookupTypeEnum.gender.name,
                                viz=VizTypeEnum.two_value.name,
                                values=values,
                                data_missing=data_missing
                            )
                            dimensions.append(gender_dim)

                            values = []
                            if len(demographic_row) == 0:
                                data_missing = True
                            else:
                                age_perc = demographic_row.loc[:, "perc_youth"].iloc[0]
                                if age_perc == 0:
                                    data_missing = True
                                    values = []
                                else:
                                    values=[
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
                                data_missing=data_missing
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

                            total_value = int(time_dimension_row.iloc[:,-1].iloc[0])

                            target_row = targets_df[phase_num].fillna(0).loc[
                                    (targets_df[phase_num].department == department_name)
                                    & (targets_df[phase_num].programme == programme_name)
                                ].target
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
                            print("IndexError on", section, department_name, programme_name, str(e))

                sections.append(
                    Section(
                        name=section_titles[section_abbrev_to_name[section]],
                        section_type=section_abbrev_to_name[section],
                        metrics=metrics,
                    )
                )
            abbrev = department_name_to_abbreviation[department_name]
            
            month_info = description_df.loc[
                desc_abbrevs.get(abbrev, abbrev), "Data captured until"
            ]
            try:
                month = month_info.strftime('%Y%m')
            except AttributeError as e:
                month_parts = month_info.split('-')
                month = month_parts[2] + month_parts[1]
            phase = Phase(
                    phase_num=phase_num,
                    month=month,
                    sections=sections,
                    target_lines=[],
                    achievement_lines=[],
                    implementation_details=department_implementation_details,
                    beneficiaries = []
                )
            phases.append(phase)
        departments[department_name] = Department(
            name=department_name,
            sheet_name=abbrev,
            lead=leads[desc_abbrevs.get(abbrev, abbrev)],
            paragraph=paragraphs[desc_abbrevs.get(abbrev, abbrev)],
            phases=phases
        )
        
    for name in sorted(departments.keys()):
        all_data_departments.append(departments[name])
        
    abbrev_to_name = {}
    for dept in all_data_departments:
        abbrev = department_name_to_abbreviation[dept.name]
        abbrev_to_name[abbrev] = dept.name

    return all_data_departments

def compute_breakdowns(all_data_departments):
    """Compute breakdowns by the different demographic dimensions"""
    total_male = [0] * number_of_phases
    total_female = [0] * number_of_phases
    total_unknown_gender = [0] * number_of_phases
    total_beneficiaries = [0] * number_of_phases
    total_youth = [0] * number_of_phases
    total_unknown_youth = [0] * number_of_phases
    total_provincial = {}
    total_unknown_province = [0] * number_of_phases

    for department in all_data_departments:

        for abbreviation in province_abbreviations:
            total_provincial[abbreviation] = [0] * number_of_phases
        for phase in department.phases:
            phase_num = phase.phase_num
            department_male = department_female = department_beneficiaries = 0
            for section in phase.sections:
                for metric in section.metrics:
                    if section.section_type == SectionEnum.targets.name and metric.name == "Beneficiaries":
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
                                if value.key == 'Male':
                                    department_male += total_value * value.value
                                    total_male[phase_num] += total_value * value.value
                                elif value.key == 'Female':
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
    return (total_male, total_female, total_unknown_gender, total_beneficiaries,
            total_youth, total_unknown_youth, total_provincial, total_unknown_province)


def compute_programmes_by_type(all_data_departments, opportunity_achievements_df, opportunity_targets_df):
    """Compute programmes_by_type, which is an overview of programmes by the opportunity type"""
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
    programmes_by_type = {
        SectionEnum.job_opportunities.name: dict([(i, {}) for i in range(number_of_phases)]),
        SectionEnum.livelihoods.name: dict([(i, {}) for i in range(number_of_phases)]),
        SectionEnum.jobs_retain.name: dict([(i, {}) for i in range(number_of_phases)]),
    }

    achievements_by_type_by_month = {}
    for section_type in [
        e.name for e in SectionEnum if e.name != "cat_interventions" and e.name != "targets" and e.name != "budget_allocated"
    ]:
        achievements_by_type_by_month[section_type] = {}
        for month in months:
            achievements_by_type_by_month[section_type][month] = 0

    # this stores the achievement values from the last months of the previous phase
    achievement_cache = {
        SectionEnum.job_opportunities.name: dict([(i, 0) for i in range(number_of_phases-1)]),
        SectionEnum.livelihoods.name: dict([(i, 0) for i in range(number_of_phases-1)]),
        SectionEnum.jobs_retain.name: dict([(i, 0) for i in range(number_of_phases-1)]),
    }

    for department in all_data_departments:
        for phase_num, phase in enumerate(department.phases[:-1]):
            for section in phase.sections:
                for metric in section.metrics:
                    for dimension in metric.dimensions:
                        if dimension.values and dimension.lookup == LookupTypeEnum.time.name:
                            # print("saving", section.section_type, dimension.values[-1].value)
                            achievement_cache[section.section_type][phase_num] += dimension.values[-1].value

    for department in all_data_departments:
        for phase in department.phases:
            achievements_df = opportunity_achievements_df[phase.phase_num].iloc[3:, 1:].set_index(1)
            section_value = 0
            section_target_value = 0
            for section in phase.sections:
                if section.section_type == SectionEnum.targets.name:
                    # skip over (budget and beneficiary) targets section
                    continue
                total_value = 0
                total_target_value = 0
                for metric in section.metrics:
                    #             if (
                    #                 department.sheet_name == "DALRRD"
                    #                 and metric.name == "Graduate Employment"
                    #             ):
                    #                 continue
                    # if phase.phase_num == 1 and section.section_type == SectionEnum.job_opportunities.name:
                    #     print(department.sheet_name, metric.value_target, metric.value)
                    if metric.name not in achievements_df.index:
                        print(
                            "Metric not found in achievements_df", department.name, metric.name
                        )
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
                                
                if (
                    department.name == "Agriculture, Land Reform and Rural Development"
                    and section.section_type == SectionEnum.livelihoods.name
                ):
                    # this programme from DALRRD only has an overall target,
                    # not one target per sub-programme
                    if phase.phase_num == 0:
                        row = 8
                    elif phase.phase_num == 1:
                        row = 7
                    total_target_value = int(opportunity_targets_df[phase.phase_num].iloc[row, 2])
                elif (
                    department.name == "Public Works and Infrastructure"
                    and section.section_type == SectionEnum.job_opportunities.name
                ):
                    # this is a phase 1 programme that just has an overall target
                    total_target_value = int(opportunity_targets_df[phase.phase_num].iloc[47, 2])
                #         print(department.name, section.name, total_value, total_target_value)
                programmes_by_type[section.section_type][phase.phase_num][department.sheet_name] = {
                    "value": total_value,
                    "value_target": total_target_value,
                    "phase": phase.phase_num
                }
                if "Total" not in programmes_by_type[section.section_type][phase.phase_num]:
                    programmes_by_type[section.section_type][phase.phase_num]["Total"] = dict(
                        value=0, value_target=0
                    )
                programmes_by_type[section.section_type][phase.phase_num]["Total"]["value"] += total_value
                programmes_by_type[section.section_type][phase.phase_num]["Total"][
                    "value_target"
                ] += total_target_value
                section_value += total_value
                section_target_value += total_target_value

    for section_type in achievements_by_type_by_month:
        if section_type == 'overview' or section_type == 'in_process':
            continue
        for month in achievements_by_type_by_month[section_type]:
            for phase_num in range(1, number_of_phases):
                # print(month, phase_num, in_phase(phase_num, month), in_phase(phase_num - 1, month))
                # print("test 2", in_phase(phase_num - 1, month))
                if in_phase(phase_num, month) and not in_phase(phase_num - 1, month):
                    # print("adding cache to:", section_type, month,achievement_cache[section_type][phase_num - 1], "was", achievements_by_type_by_month[section_type][month])
                    achievements_by_type_by_month[section_type][month] += achievement_cache[section_type][phase_num - 1]

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
                    programmes_by_type_summarised[programme_type][department] = {'value': {}, 'value_target': {}}
                programmes_by_type_summarised[programme_type][department]["value"][phase_num] = programmes_by_type[programme_type][phase_num][department]["value"]
                programmes_by_type_summarised[programme_type][department]["value_target"][phase_num] = programmes_by_type[programme_type][phase_num][department]["value_target"]

    # pp.pprint(programmes_by_type_summarised)
    pp = PrettyPrinter(indent=2)
    # pp.pprint(programmes_by_type)
    return (programmes_by_type, programmes_by_type_summarised, achievements_by_type_by_month)


def sort_dept_metric(element):
    # element is a pair - (department_name, dictionary) where the dictionary contains
    # {'value': {phase_num: amount} ... }
    value = element[1]['value']
    value_total = 0
    for phase_num in value:
        value_total += value[phase_num]
    return value_total


def compute_overview_breakdown(programmes_by_type_summarised, achievements_by_type_by_month):
    breakdown_metrics = [
                    PhasedMetric(
                        name=section_titles[section_name],
                        metric_type=section_name,
                        viz=VizTypeEnum.full.name,
                        total_value=sum(programmes_by_type_summarised[section_name]["Total"]["value"].values()),
                        total_value_target=sum(programmes_by_type_summarised[section_name]["Total"]["value_target"].values()),
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
                                    if sum(outputs["value_target"].values()) > 0 and not (
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
                        ],
                    )
                    for section_name, department_info in programmes_by_type_summarised.items()
                    if not section_name.startswith("value")
                ]
    # add up all the metrics across all the programmes
    current_targets = dict([
        (phase_num, sum([metric.value[phase_num] if metric.value[phase_num] > 0 else 0 for metric in breakdown_metrics]))
        for phase_num in range(number_of_phases)])
    current_achievements = dict([
        (phase_num, sum([metric.value_target[phase_num] if metric.value_target[phase_num] > 0 else 0 for metric in breakdown_metrics]))
        for phase_num in range(number_of_phases)])
    
    return(breakdown_metrics, current_targets, current_achievements)


def compute_overview_metrics(total_female, total_beneficiaries, total_unknown_gender,
                             opportunity_targets_df, programmes_by_type,
                             total_youth, total_unknown_youth):
    # metrics breakdown

    female_by_phases = dict(
        [(phase_num, total_female[phase_num] / (total_beneficiaries[phase_num] - total_unknown_gender[phase_num])) 
        for phase_num in range(number_of_phases)]
    )
    overall_female_perc = sum(female_by_phases.values()) / 2

    overview_metrics = []

    phase_1_budget = opportunity_targets_df[0].iloc[2,6] * 1000
    phase_2_budget = opportunity_targets_df[1].iloc[2,6] * 1000

    total_budget = PhasedMetric(
        name="Total budget allocated",
        metric_type=MetricTypeEnum.currency.name,
        viz=VizTypeEnum.full.name,
        total_value=phase_1_budget + phase_2_budget,
        value=[phase_1_budget, phase_2_budget],
        value_target=[None] * number_of_phases,
        dimensions=[],
        
    )
    overview_metrics.append(total_budget)

    achievements_by_phase_value = dict([(phase_num, 0) for phase_num in range(number_of_phases)])
    achievements_by_phase_value_target = dict([(phase_num, 0) for phase_num in range(number_of_phases)])

    for section_type in programmes_by_type:
        for phase_num in range(number_of_phases):
            # print(section_type, programmes_by_type[section_type][phase_num]['Total'])
            achievements_by_phase_value[phase_num] += programmes_by_type[section_type][phase_num]['Total']['value']
            achievements_by_phase_value_target[phase_num] += programmes_by_type[section_type][phase_num]['Total']['value_target']

    achievements = PhasedMetric(
        name="Total beneficiaries assisted",
        metric_type=MetricTypeEnum.count.name,
        viz=VizTypeEnum.full.name,
        total_value=sum(achievements_by_phase_value.values()),
        value=[achievements_by_phase_value[0], achievements_by_phase_value[1]],
        total_value_target=sum(achievements_by_phase_value_target.values()),
        value_target=[achievements_by_phase_value_target[0], achievements_by_phase_value_target[1]],
        dimensions=[]
    )
    overview_metrics.append(achievements)

    gender_breakdown = PhasedMetric(
        name="Total female beneficiaries",
        metric_type="targets_count",
        viz=VizTypeEnum.compact.name,
        value=female_by_phases,
        total_value=overall_female_perc,
        value_target=-1,
        dimensions=[]
    )
    overview_metrics.append(gender_breakdown)

    youth_by_phases=value=dict(
        [(phase_num, total_youth[phase_num] / (total_beneficiaries[phase_num] - total_unknown_youth[phase_num]))
        for phase_num in range(number_of_phases)]
    )
    overall_youth_perc = sum(youth_by_phases.values()) / 2
    youth_breakdown = PhasedMetric(
        name="Total youth beneficiaries",
        metric_type="targets_count",
        viz=VizTypeEnum.compact.name,
        value=youth_by_phases,
        total_value=overall_youth_perc,
        value_target=-1,
        dimensions=[]
    )
    overview_metrics.append(youth_breakdown)
    return overview_metrics

def compute_overview(description_df, leads, paragraphs, overview_metrics,
                     current_targets, current_achievements, breakdown_metrics):

    month_info = description_df.loc["overview", "Data captured until"]
    try:
        month = month_info.strftime('%Y%m')
    except AttributeError as e:
        month_parts = month_info.split('-')
        month = month_parts[2] + month_parts[1]
    overview = Overview(
        month=month,
        name="Programme overview",
        lead=leads["overview"],
        phase_dates=phase_dates,
        paragraph=paragraphs["overview"],
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
                value=[-1,-1],
                value_target=[-1,-1]
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