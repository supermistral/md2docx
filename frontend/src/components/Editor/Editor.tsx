import React, { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import {citePlugin as remarkCite} from "@benrbray/remark-cite";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkFrontmatter from "remark-frontmatter";
import remarkExtendedTable from "remark-extended-table";
import rehypeHighlight from "rehype-highlight";
import rehypeKatex from "rehype-katex";
import { remarkBlockMetadataFilter, remarkFrontmatterFilter } from "../../markdown/filters";
// import Sidebar from "./Sidebar/Sidebar";
import { useLazyGetTaskQuery, useProcessMarkdownMutation } from "../../redux/api/md2docxApi";
import "./Editor.scss";
import { useSelector } from "react-redux";
import { selectEditorQueryState } from "../../redux/selectors/editor";
import { EditorQueryState } from "../../redux/types";
import useAppBarHeight from "../../tools/hooks/layout";

const PROCESS_MARKDOWN_QUERY_INTERVAL = 3000;


const Editor = () => {
    const [text, setText] = useState<string>("");

    const [getTask, { data: taskData, error: taskError }] = useLazyGetTaskQuery();
    const [runProcessMarkdown, { data: processMarkdownData }] = useProcessMarkdownMutation();

    const appBarHeight = useAppBarHeight();

    const editorQueryState = useSelector(selectEditorQueryState);

    useEffect(() => {
        if (editorQueryState === EditorQueryState.ProcessingCompleted) {
            const getQueryInterval = setInterval(() => getTask(), PROCESS_MARKDOWN_QUERY_INTERVAL);
            return () => clearTimeout(getQueryInterval);
        }
    }, [editorQueryState]);

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(e.target.value);
    }

    const handleRunProcessMarkdown = useCallback(() => {
        if (!text) return;

        const formData = new FormData();
        formData.append('code', text)

        if (formData) {
            runProcessMarkdown(formData);
        }
    }, [text]);

    return (
        <div
            className="main-container"
            style={{
                height: `calc(100% - ${appBarHeight}px)`,
            }}
        >
            {/* <Sidebar
                onRunProcessMarkdownClick={handleRunProcessMarkdown}
                task={taskData}
            /> */}
            <div className="editor">
                <div className="editor-input">
                    <textarea className="editor-area" onChange={handleChange} autoFocus />
                </div>
                <div className="editor-preview">
                    <ReactMarkdown
                        children={text}
                        className="editor-area"
                        remarkPlugins={[
                            remarkGfm,
                            // [remarkCite, {}],
                            remarkMath,
                            remarkExtendedTable,
                            remarkFrontmatter,
                            // remarkFrontmatterFilter,
                            // remarkBlockMetadataFilter,
                        ]}
                        rehypePlugins={[
                            [rehypeHighlight, {fragment: true}],
                            rehypeKatex,
                        ]}
                    />
                </div>
            </div>
            {/* {editorQueryState === EditorQueryState.TaskReceived && taskData?.status !== "PENDING" && (
                <ResponseModal task={taskData!} error={taskError} />
            )} */}
        </div>
    )
}

export default Editor;