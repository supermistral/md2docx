import { createSlice } from "@reduxjs/toolkit";
import { EditorQueryState } from "../types";


const editorSlice = createSlice({
    name: "editor",
    initialState: {
        queryState: EditorQueryState.Initial
    },
    reducers: {
        processingStarted: (state) => {
            state.queryState = EditorQueryState.ProcessingLoading;
        },
        processingCompleted: (state) => {
            state.queryState = EditorQueryState.ProcessingCompleted;
        },
        taskReceived: (state) => {
            state.queryState = EditorQueryState.TaskReceived;
        },
        downloadFinished: (state) => {
            state.queryState = EditorQueryState.Initial;
        }
    }
});

export const {
    processingStarted,
    processingCompleted,
    taskReceived,
    downloadFinished,
} = editorSlice.actions;

export default editorSlice.reducer;