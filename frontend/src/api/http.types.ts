export interface ApiSuccess<T> {
  success: true;
  code: string;
  message: string;
  data: T;
  meta?: Record<string, any>;
}

export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    detail?: string;
    action?: string;
  };
}
