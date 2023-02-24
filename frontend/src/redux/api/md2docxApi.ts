import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_URL } from "../../constants/api";
import { processingCompleted, processingStarted, taskReceived } from "../slices/editorSlice";
import { TaskResponse } from "../types";


export const md2docxApi = createApi({
    reducerPath: 'md2docx',
    baseQuery: fetchBaseQuery({ baseUrl: `${API_URL}/md2docx` }),
    tagTypes: ['md2docx'],
    endpoints: (builder) => ({
        processMarkdown: builder.mutation<any, FormData>({
            query: (body) => ({
                url: '/',
                method: 'POST',
                body,
            }),
            async onQueryStarted(body, { dispatch, queryFulfilled }) {
                dispatch(processingStarted());
                try {
                    const { data } = await queryFulfilled;
                    dispatch(processingCompleted());
                } catch (err) {}
            }
        }),
        getTask: builder.query<TaskResponse, void>({
            query: () => '/',
            async onQueryStarted(_, { dispatch, queryFulfilled }) {
                try {
                    const { data } = await queryFulfilled;
                    dispatch(taskReceived());
                } catch (err) {}
            }
        }),
    }),
});


export const {
    useProcessMarkdownMutation,
    useGetTaskQuery,
    useLazyGetTaskQuery,
} = md2docxApi;