export interface Result {
  id: number,
  created: Date,
  modified: Date,
  lat: number,
  long: number,
  score: number,
  upload: string
}

export interface PaginatedResult {
  next: string,
  prev: string,
  results: Result[]
}
