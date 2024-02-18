#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Union, Mapping

from dataclasses_json import dataclass_json

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
    multiplicity: int = 1  # Used when merging percentages


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
    viz: str  # enum of "full" and "compact"
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
    metric_type = str = None  # enum of MetricTypeEnum
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
    target_lines: List[int]  # TODO: document what these attributes are used for
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
