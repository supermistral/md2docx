export interface TaskResponse {
    status: string;
    error?: string;
    detail?: any;
};


export const enum EditorQueryState {
    Initial,
    ProcessingLoading,
    ProcessingCompleted,
    TaskReceived,
};