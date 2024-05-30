export interface AnyProps extends Record<string, any> {}

export interface TemplateDto {
    id: string;
    name: string;
    content: string;
    createdAt: string;
    updatedAt: string;
}

export interface UserTemplateDto {
    id: string;
    name: string;
    content: string;
}

export interface OperationDto {
    id: string;
    status: string;
    response: any | null;
    error: any | null;
    createdAt: string;
    updatedAt: string;
}
