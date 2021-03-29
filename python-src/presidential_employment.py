from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

from dataclasses_json import dataclass_json

SectionEnum = Enum(
    "Section", "targets budget_allocated job_opportunities jobs_retain livelihoods"
)

MetricTypeEnum = Enum("MetricType", "currency count")

ProvinceEnum = Enum("Province", "EC FS GP KZN LP MP NC NW WC")

ImplementationStatusEnum = Enum('ImplementationStatus', 'OnTrack MinorChallenges CriticalChallenges')

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
province_abbreviations = ["EC", "FS", "GP", "KZN", "LP", "NW", "NC", "WC"]

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

GenderEnum = Enum("Gender", "Male Female")


@dataclass_json
@dataclass
class TimeValue:
    month: int  # encoding month as in 202101
    name: str  # human readable time period name
    value: int


@dataclass_json
@dataclass
class AgeValue:
    age_category: str  # 18-35 or youth?
    value: int


@dataclass_json
@dataclass
class GenderValue:
    gender: str  # enum: 'female' or 'male'
    value: int


@dataclass_json
@dataclass
class ProvinceValue:
    province: str  # enum: 'EC' | 'FS' | 'GP' | 'KZN' | 'LP' | 'MP' | 'NC' | 'NW' | 'WC'
    value: int


@dataclass_json
@dataclass
class TimeValues:
    name: str
    values: List["TimeValue"]


@dataclass_json
@dataclass
class ProvinceValues:
    name: str
    values: List["ProvinceValue"]


@dataclass_json
@dataclass
class AgeValues:
    name: str
    values: List["AgeValue"]


@dataclass_json
@dataclass
class GenderValues:
    name: str
    values: List["GenderValue"]


@dataclass_json
@dataclass
class Metric:
    name: str
    metric_type: str  # enum of 'currency', 'count'
    value: int
    time: Optional[TimeValues]
    gender: Optional[GenderValues]
    age: Optional[AgeValues]
    province: Optional[ProvinceValues]
    value_target: int = -1

@dataclass_json
@dataclass
class ImplementationDetail:
    programme_name: str
    status: str = None  # enum of OnTrack MinorChallenges CriticalChallenges
        detail: str = None    

@dataclass_json
@dataclass
class Section:
    name: str
    section_type: str  # enum of 'targets', 'budget_allocated', 'job_opportunities', 'jobs_retain', 'livelihoods'
    metrics: List["Metric"]


@dataclass_json
@dataclass
class Department:
    month: int  # the month of latest data
    name: str
    sheet_name: str
    lead: str
    paragraph: str
    target_lines: Optional[List[int]]
    achievement_lines: Optional[List[int]]
    sections: List["Section"]
    implementation_details: Optional[List["ImplementationDetail"]]


@dataclass_json
@dataclass
class DepartmentValue:
    department: str  # TODO: should be enum
    value: int


@dataclass_json
@dataclass
class DepartmentValues:
    name: str
    values: List["DepartmentValue"]


@dataclass_json
@dataclass
class OverviewMetric:
    name: str
    metric_type: str  # enum of 'currency', 'count'
    value: int
    time: Optional[TimeValues]
    #     department: DepartmentValues
    value_target: int = -1


@dataclass_json
@dataclass
class OverviewSection(Section):
    name: str
    section_type: str
    metric_type: str  # summarise all the Metrics in thise section
    value: int
    value_target: int
    metrics: List["Metric"]


@dataclass_json
@dataclass
class Overview:
    month: int
    name: str  # Would normally be "Programme Overview"
    lead: str
    paragraph: str
    sections: List["OverviewSection"]


@dataclass_json
@dataclass
class Everything:
    overview: Overview
    departments: List["Department"]

implementation_status_to_enum = {
    'On track': ImplementationStatusEnum.OnTrack.name,
    'Minor challenges': ImplementationStatusEnum.MinorChallenges.name,
    'Critical challenges': ImplementationStatusEnum.CriticalChallenges.name
}

section_titles = {
    SectionEnum.targets.name: "Programme targets for this department",
    SectionEnum.job_opportunities.name: "Job opportunities",
    SectionEnum.jobs_retain.name: "Jobs retained",
    SectionEnum.livelihoods.name: "Livelihoods",
    SectionEnum.targets.name + "_overview": "Programme targets",
    SectionEnum.job_opportunities.name + "_overview": "Job opportunities",
    SectionEnum.jobs_retain.name + "_overview": "Jobs retained",
    SectionEnum.livelihoods.name + "_overview": "Livelihoods",
}

metric_titles = {
    SectionEnum.targets.name: {
        MetricTypeEnum.currency.name: "Budget",
        MetricTypeEnum.count.name: "Beneficiaries",
    },
    SectionEnum.job_opportunities.name: {
        MetricTypeEnum.count.name + '_time': "Employed over time",
        MetricTypeEnum.count.name + '_gender': "Opportunities by Gender",
        MetricTypeEnum.count.name + '_province': "Opportunities by Province",
        MetricTypeEnum.count.name + '_age': "Opportunities going to 18-35 year olds",
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
    }

}

leads = dict(
    overview="Building a society that works",
    DTIC="Piloting new models for re-shoring and expanding global business services",
    DBE="Teachers assistants and other support for schools",
    DSD="Income support to practitioners and to the implementation of Covid compliance measures",
    DOH="Primary Health Care is at the frontline of the battle against Covid-19",
    DALLRD="Expanding support to farmers and protecting food value chains",
    DSI="Supporting new graduates entering a hostile labour market",
    DSAC="To get artists, cultural workers and the sporting sector on the road to recovery",
    DoT="Improving access to services and opportunities for people in rural areas",
    DPWI="Graduate placements in the professional services",
    DEFF="Investing in the environment we live in",
    DCOGTA="Mainstreaming and improving labour-intensity in infrastructure delivery",
)

paragraphs = dict(
    overview="The COVID-19 pandemic has had a devastating economic impact, threatening the jobs and livelihoods of many South Africans – especially the most vulnerable. The pandemic has exacerbated South Africa’s pre-existing crises of poverty and unemployment.The Presidential Employment Stimulus seeks to confront this impact directly, as part of government’s broader economic recovery agenda. Its aim is to use direct public investment to support employment opportunities – starting right now.",
    DTIC="The Global Business Services Sector has an impressive track record. Established in 2006/7 to provide offshore customer service delivery, the sector has built from a low base to achieve an average year-on-year export revenue growth of at least 20% since 2014.",
    DBE="A key priority identified in the National Development Plan is the improvement of quality education, skills development, and innovation. One intervention that has seen some experimentation in South Africa, with significant potential to scale nationally, is the use of school assistants to strengthen the learning environment. An important rationale for school assistants is the need to support teachers in the classroom, freeing up time for teaching and providing additional support to learners to improve education outcomes.",
    DSD="Livelihoods from the provision of Early Childhood Development services were severely disrupted by the pandemic, with providers facing challenges with re-opening. There are costs associated with doing so safely, and some parents can no longer afford to pay fees as a result of job losses.",
    DOH="As the world responds to the COVID-19 pandemic, the critical role that community health workers play to enhance the resilience of the national health care system has been foregrounded. They have been on the frontline of active case-finding through screening and contact tracing.",
    DALLRD="The pandemic has illustrated the vulnerability of our food production and distribution systems. Although exempt from the strictest lockdown regulations, the sector faced severe challenges with disruptions to production and marketing experienced by many small-scale farmers. ",
    DSI="Given a constrained labour market, fewer opportunities will be available to graduates leaving institutions of higher learning in 2021.\n\nThe Department of Science and Innovation will deliver four programmes through its entities designed to minimise this impact, which will together offer 1,900 unemployed graduates an opportunity to earn an income while gaining meaningful work experience.",
    DSAC="Under lockdown, there has been no loud applause in jazz venues, no curtain calls for the dancers, no tourists in craft markets – and no victory laps for our sports people. No segment of the creative, cultural and sporting sectors have been untouched",
    DoT="Rural roads play a vital role in connecting rural communities to services such as health and education, as well as providing access to markets and economic opportunities. However, rural roads infrastructure remains poor in many areas of South Africa",
    DPWI="In addition to structural skills shortages that were experienced prior to the pandemic, the management of facilities and completion of infrastructure projects has been further impacted by restrictions on the movement of people and limitations placed on completing infrastructure projects during the lockdown. As the economy re-opens, additional capacity is required to address the backlog so that service provision can be restored",
    DEFF="The work undertaken in environmental, forestry and fishery programmes will touch the length and breadth of the country, from coast to coast, including bushveld, grassland, fynbos, wetlands, mountains, water bodies, catchment areas  – and urban areas, too. The work undertaken affects the air we breathe, the water we drink, the energy we use and the food we eat, supporting a wealth of biodiversity resources and ecological systems essential to life on earth and to the future of the planet.",
    DCOGTA="Prioritising infrastructure maintenance Mainstreaming and improving labour-intensity in infrastructure deliveryCommunity access to water and sanitation is all the more important in the context of the crisisTOTAL BUDGETR50MJOB OPPORTUNITIES25,000 Before the crisis, many municipalities were already facing critical funding shortfalls and challenges in the sustainable delivery of basic services and the maintenance of infrastructure. The pandemic has compounded these problems by cancelling or stalling implementation of all non-critical infrastructure projects",
)

months = [202010, 202011, 202012, 202101]
month_names = ["Oct '20", "Nov '20", "Dec '20", "Jan '21"]

target_to_imp_programme_mapping = {
    "Banking with art, connecting Lives - National Museum Bloemfontein": " Banking with art, connecting Lives - National Museum Bloemfontein",
    "CSIR - Experiential Training Programme": "CSIR - Experiential Training Programme ",
    "Community Health Workers": "Community health workers",
    "Covid-19 Return-To-Play - National Sport Federations": "Covid-19 Return-To-Play - National Sport Federations                                                                                                                                    ",
    "Digitisation of records - National Library of South Africa": "Digitisation of records - National Library of South Africa ",
    "Facilities Management": "Facilities Management (PMTE) Employment: ",
    "In-House Construction projects": "In-House Construction projects ",
    "Job retention at fee paying schools": "Retain vulnerable teaching posts",
    "Municipal infrastructure": "Mainstream labour intensive construction methods",
    "Outreach Team Leaders": "Outreach team leaders",
    "Oceans and Coast: Source to Sea": "Oceans and Coast: Source to Sea ",
    "Provincial Roads Maintenance": "Rural roads maintenance",
    "Real Estate": "Real Estate  (PMTE)",
    "Services sector development incentives": "Global Business Services Sector",
    "Subsistence relief fund": "Subsistence producer relief fund",
    "Retention of social workers": "Social workers",
    "Vegetables and Fruits": "Vegetables and Fruits ",
    "WRC - Water Graduate Employment Programme": " WRC - Water Graduate Employment Programme ",
    "Water and Energy Efficiency": "Water and Energy Efficiency (Green Economy)",
    "Water and Sanitation Facilities Management": "Water and Sanitation Facilities Management (PMTE)",
    "Welisizwe Rural Bridges Programme": "Welisizwe Rural Bridges Programme (PMTE) ",
}
