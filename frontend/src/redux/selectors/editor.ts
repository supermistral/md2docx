import { RootState } from "../store/store";


export const selectEditorQueryState = (state: RootState) => state.editor.queryState;