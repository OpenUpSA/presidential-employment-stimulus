interface AllData {
  lookups: {
    [id: string]: {
      [key: string]: string
    }
  }
  tabs: Tab[]
}

interface Tab {
  sheet_name: string // DTIC
  month: number // 202101
  name: string // Basic Education
  lead: string // Strengthening the learning environment in schools
  paragraph: string
  sections: Array<{
    name: string // Budget allocated to date
    metrics: Array<{
      name: string // Educational and general assistants
      metric_type: 'currency' | 'count'
      value: number
      value_target?: number
      time?: {
        name: string // Spent over time
        values: Array<{
          month: number // 202101
          name?: string // Nov '20
          value: number
        }>
      }
      gender?: {
        name: string // Jobs by gender
        values: Array<{
          gender: 'female' | 'male'
          value: number
        }>
      }
      age?: {
        name: string // Opportunities for 18-35 year olds
        values: Array<{
          age: string // 18-35
          value: number // fraction of 1
        }>
      }
      province?: {
        name: string // Opportunities by province
        values: Array<{
          province: 'EC' | 'FS' | 'GP' | 'KZN' | 'LP' | 'MP' | 'NC' | 'NW' | 'WC'
          value: number
        }>
      }
    }>
  }>
}
