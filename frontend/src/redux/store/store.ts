import { configureStore } from "@reduxjs/toolkit";
import { md2docxApi } from "../api/md2docxApi";
import editorReducer from "../slices/editorSlice";


const store = configureStore({
    reducer: {
        editor: editorReducer,
        [md2docxApi.reducerPath]: md2docxApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware()
            .concat(md2docxApi.middleware)
});

export type RootState = ReturnType<typeof store.getState>

export default store;