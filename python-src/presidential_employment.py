from cmath import phase
from enum import Enum
from dataclasses import dataclass
from typing import Counter, List, Union, Mapping

from dataclasses_json import dataclass_json

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
 'Department of Women, Youth and Persons with Disabilities': 'DWYPD',
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
    'Department of Women, Youth and Persons with Disabilities': 30_000 * 1000, # CRE
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
    metrics: List[Metric]
    metric_type = str = None # enum of MetricTypeEnum
    value: int = None
    value_target: int = None


@dataclass_json
@dataclass
class OverviewSection:
    name: str
    section_type: str  # enum of 'targets', 'budget_allocated', 'job_opportunities', 'jobs_retain', 'livelihoods'
    metrics: List[PhasedMetric]
    metric_type = str = None # enum of MetricTypeEnum
    value: int = None
    value_target: int = None


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
