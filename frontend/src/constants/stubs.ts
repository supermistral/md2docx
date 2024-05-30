import { TemplateDto, UserTemplateDto, OperationDto } from "./types";

export const SERVER_TEMPLATES: Array<TemplateDto> = [
    {
        id: "1",
        name: "Test template 1",
        content: "list:\n  fontsize: 12\n  lvl:\n    1:\n      fontsize: 14\n    2:\n      fontsize: 12\n.class2:\n  left-indent: 1.25\n  right-indent: 0.25",
        createdAt: "2024-04-22 12:00:00",
        updatedAt: "2024-04-22 12:00:00",
    },
    {
        id: "2",
        name: "Test template 2",
        content: "some code",
        createdAt: "2024-04-21 12:00:00",
        updatedAt: "2024-04-21 12:00:00",
    },
    {
        id: "3",
        name: "Test template 3",
        content: "some code",
        createdAt: "2024-04-20 12:00:00",
        updatedAt: "2024-04-20 12:00:00",
    },
]

export const USER_TEMPLATES: Array<UserTemplateDto> = [
    {
        id: "1",
        name: "Saved test template 1",
        content: "Some code",
    },
    {
        id: "2",
        name: "Saved test template 2",
        content: "Some code",
    },
    {
        id: "3",
        name: "Saved test template 3",
        content: "Some code",
    },
]

export const OPERATIONS: Array<OperationDto> = [
    {
        id: "1",
        status: "pending",
        createdAt: "2024-04-22 21:32:42",
        updatedAt: "2024-04-22 21:34:52",
        error: null,
        response: null,
    },
    {
        id: "2",
        status: "success",
        createdAt: "2024-04-21 12:00:00",
        updatedAt: "2024-04-21 12:01:00",
        error: null,
        response: {"docx_file": "aaaaaaa/aaaaaaaaa"},
    },
    {
        id: "3",
        status: "success",
        createdAt: "2024-04-20 12:00:00",
        updatedAt: "2024-04-20 12:00:00",
        error: null,
        response: {"docx_file": "aaaaaaa/aaaaaaaaa"},
    },
]
