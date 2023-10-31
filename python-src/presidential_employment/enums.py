#!/usr/bin/env python3
from enum import Enum

SectionEnum = Enum(
    "Section",
    "targets overview budget_allocated job_opportunities jobs_retain livelihoods in_process",
)

MetricTypeEnum = Enum("MetricType", "currency count")

ProvinceEnum = Enum("Province", "EC FS GP KZN LP MP NC NW WC")

ImplementationStatusEnum = Enum(
    "ImplementationStatus", "OnTrack MinorChallenges CriticalChallenges"
)

VizTypeEnum = Enum("VizType", "bar line two_value percentile count full compact")

LookupTypeEnum = Enum(
    "LookupType", "department city province university time age gender vets disabled repeat"
)

GenderEnum = Enum("Gender", "Male Female")

RepeatEnum = Enum("Repeat", "Repeat New")
