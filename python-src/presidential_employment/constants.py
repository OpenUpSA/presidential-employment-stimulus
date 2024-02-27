#!/usr/bin/env python3

from .enums import *

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

cities = [
    "Cape Town",
    "Johannesburg",
    "Durban",
    "Pretoria",
    "Gqerberha",
    "Bloemfontein",
    "East London",
    "Pietermaritzburg",
    "Polokwane",
]

city_header_to_abbrev = {
    "cape_town": "CPT",
    "johannesburg": "JHB",
    "durban": "DBN",
    "pretoria": "PTA",
    "gqerberha": "GB",
    "bloemfontein": "BFN",
    "east_london": "EL",
    "pietermaritzburg": "PMB",
    "polokwane": "POL",
}

universities = [
    "Cape Peninsula University of Technology",
    "Central University of Technology",
    "Durban University of Technology",
    "Mangosuthu  University of Technology",
    "Nelson Mandela University",
    "Rhodes University",
    "Sefako Makgatho Health Science University",
    "Sol Plaaitje University",
    "Stellenbosch University",
    "North West University",
    "Tshwane University of Technology",
    "University of Cape Town",
    "University of Fort Hare",
    "University of Johannesburg",
    "University of KwaZulu Natal",
    "University of Limpopo",
    "University of Mpumalanga",
    "University of Pretoria",
    "University of South Africa",
    "University of the Free State",
    "University of the Western Cape",
    "University of the Witswatersrand",
    "University of Venda",
    "University of Zululand",
    "Walter Sisulu University",
    "Vaal University of Technology"
]

university_header_to_abbrev = {
    'cape_peninsula_university_of_technology': 'CPUT',
    'central_university_of_technology': 'CUT',
    'durban_university_of_technology': 'DUT',
    'mangosuthu__university_of_technology': 'MUT',
    'nelson_mandela_university': 'NMU',
    'north_west_university': 'NWU',
    'rhodes_university': 'RU',
    'sefako_makgatho_health_science_university': 'SMU',
    'sol_plaaitje_university': 'SPU',
    'stellenbosch_university': 'SU',
    'tshwane_university_of_technology': 'TUT',
    'university_of_cape_town': 'UCT',
    'university_of_fort_hare': 'UFH',
    'university_of_johannesburg': 'UJ',
    'university_of_kwazulu_natal': 'UKZN',
    'university_of_limpopo': 'UL',
    'university_of_mpumalanga': 'UM',
    'university_of_pretoria': 'UP',
    'university_of_south_africa': 'UNISA',
    'university_of_the_free_state': 'UFS',
    'university_of_the_western_cape': 'UWC',
    'university_of_the_witswatersrand': 'WITS',
    'university_of_venda': 'UNIVEN',
    'university_of_zululand': 'UZ',
    'vaal_university_of_technology': 'VUT',
    'walter_sisulu_university': 'WSU'
    }

department_name_to_abbreviation = {
    "Basic Education": "DBE",
    "Social Development": "DSD",
    "Agriculture, Land Reform and Rural Development": "DALRRD",
    "Forestry, Fisheries and Environment": "DFFE",
    "Transport": "DoT",
    "Sports, Arts and Culture": "DSAC",
    "Cooperative Governance": "DCOGTA",
    "Trade, Industry and Competition": "DTIC",
    "Health": "DoH",
    "Science and Innovation": "DSI",
    "Public Works and Infrastructure": "DPWI",
    "National Treasury": "NT",
    "Higher Education": "DHET",
    "Tourism": "Tourism",
    "Employment and Labour": "DEL",
    "Communications and Digital Technologies": "DCDT",
    "Women, Youth and Persons with Disabilities": "DWYPD",
}

# department_budget_targets = [
#     {
#         "Basic Education": 7_000_000 * 1000,
#         "Social Development": 7_000_000 * 1000,
#         "Agriculture, Land Reform and Rural Development": 1_000_000_000,
#         "Forestry, Fisheries and Environment": 1_983_000 * 1000,
#         "Transport": 630_000_000,
#         "Sports, Arts and Culture": 665_000_000,
#         "Cooperative Governance": 50_000_000,
#         "Trade, Industry and Competition": 120_000 * 1000,
#         "Health": 180_000_000,
#         "Science and Innovation": 45_000_000,
#         "Public Works and Infrastructure": 159_000_000,
#         "Tourism": 1 * 1000, # ??
#         "Women, Youth and Persons with Disabilities": 1 * 1000, # ???
#         "Communications and Digital Technologies": 1 * 1000, # ???
#     },
#     {
#         "Basic Education": 6_000_000 * 1000,  # CRE
#         "National Treasury": 841_000 * 1000,  # CRE
#         "Trade, Industry and Competition": 800_000 * 1000,  # CRE
#         "Health": 365_000 * 1000,  # CRE
#         "Forestry, Fisheries and Environment": 318_000 * 1000,  # CRE
#         "Higher Education": (100_000 * 1000) + (90_000) * 1000,  # CRE
#         "Sports, Arts and Culture": 15_000 * 1000,  # CRE
#         "Cooperative Governance": 284_000 * 1000,  # CRE
#         "Science and Innovation": 67_000 * 1000,  # CRE
#         "Tourism": 108_000 * 1000,  # CRE
#         "Employment and Labour": (20_000 * 1000) + (238_000 * 1000),  # CRE and CAT
#         "Communications and Digital Technologies": 200_000 * 1000,  # CAT
#         "Women, Youth and Persons with Disabilities": 30_000 * 1000,  # CRE
#         "Social Development": 178_000 * 1000,  # LIV
#         "Agriculture, Land Reform and Rural Development": 750_000 * 1000,  # LIV
#     },
# ]

section_titles = {
    SectionEnum.targets.name: "Programme targets for this department",
    SectionEnum.job_opportunities.name: "Job opportunities created",
    SectionEnum.jobs_retain.name: "Jobs retained",
    SectionEnum.livelihoods.name: "Livelihoods supported",
    SectionEnum.targets.name + "_overview": "Programme achievements",
    SectionEnum.job_opportunities.name + "_overview": "Job opportunities",
    SectionEnum.jobs_retain.name + "_overview": "Jobs retained",
    SectionEnum.livelihoods.name + "_overview": "Livelihoods supported",
    SectionEnum.in_process.name: "Opportunities in process",
}

metric_titles = {
    SectionEnum.targets.name: {
        MetricTypeEnum.currency.name: "Budget",
        MetricTypeEnum.count.name: "Beneficiaries",
    },
    SectionEnum.job_opportunities.name: {
        MetricTypeEnum.count.name + "_time": "Employed over time",
        MetricTypeEnum.count.name + "_gender": "Opportunities by Gender",
        MetricTypeEnum.count.name + "_province": "Opportunities in post by Province",
        MetricTypeEnum.count.name + "_city": "Opportunities in post by City",
        MetricTypeEnum.count.name
        + "_university": "Opportunities in post by University",
        MetricTypeEnum.count.name + "_age": "Opportunities going to 18-35 year olds",
        MetricTypeEnum.count.name
        + "_disabled": "Opportunities going to disabled persons",
        MetricTypeEnum.count.name
        + "_repeat": "Opportunities going to repeat TODO",

    },
    SectionEnum.jobs_retain.name: {
        MetricTypeEnum.count.name + "_time": "Jobs saved over time",
        MetricTypeEnum.count.name + "_gender": "Jobs saved by gender",
        MetricTypeEnum.count.name + "_province": "Jobs saved by province",
        MetricTypeEnum.count.name + "_city": "Jobs saved by city",
        MetricTypeEnum.count.name + "_university": "Jobs saved by university",
        MetricTypeEnum.count.name + "_age": "Jobs saved going to 18-35 year olds",
        MetricTypeEnum.count.name
        + "_repeat": "Jobs saved going to repeat TODO",
    },
    SectionEnum.livelihoods.name: {
        MetricTypeEnum.count.name + "_time": "Livelihoods supported over time",
        MetricTypeEnum.count.name + "_gender": "Livelihoods supported by gender",
        MetricTypeEnum.count.name + "_province": "Livelihoods supported by province",
        MetricTypeEnum.count.name + "_city": "Livelihoods supported by city",
        MetricTypeEnum.count.name
        + "_university": "Livelihoods supported by university",
        MetricTypeEnum.count.name
        + "_age": "Livelihoods supported going to 18-35 year olds",
        MetricTypeEnum.count.name
        + "_vets": "Livelhoods supported going to military veterans",
        MetricTypeEnum.count.name
        + "_disabled": "Livelhoods supported going to disabled persons",
        MetricTypeEnum.count.name
        + "_repeat": "Livelhoods supported going to repeat TODO",

    },
}

section_abbrev_to_name = {
    "CRE": SectionEnum.job_opportunities.name,
    "LIV": SectionEnum.livelihoods.name,
    "RET": SectionEnum.jobs_retain.name,
}

implementation_status_to_enum = {
    "On track": ImplementationStatusEnum.OnTrack.name,
    "Minor challenges": ImplementationStatusEnum.MinorChallenges.name,
    "Critical challenges": ImplementationStatusEnum.CriticalChallenges.name,
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
