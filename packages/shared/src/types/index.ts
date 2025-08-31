export interface User {
  id: string
  email: string
  name?: string
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  error?: string
}