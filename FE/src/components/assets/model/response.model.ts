export interface BackendAPIResponse<T> {
    code: number;
    status: boolean;
    message: string;
    data?: T;
}