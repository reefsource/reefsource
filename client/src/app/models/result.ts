export interface Result {
  id: number,
  created: Date,
  modified: Date,
  lng: number,
  lat: number,
  score: number,
  upload: string
}

export interface PaginatedResult<T> {
  next: string,
  prev: string,
  count: number,
  results: T[]
}
