import React, { useCallback, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { remarkBlockMetadataFilter, remarkFrontmatterFilter } from "../../markdown/filters";
import Sidebar from "./Sidebar/Sidebar";
import { useLazyGetTaskQuery, useProcessMarkdownMutation } from "../../redux/api/md2docxApi";
import "./Home.scss";
import ResponseModal from "./ResponseModal/ReponseModal";
import { useSelector } from "react-redux";
import { selectEditorQueryState } from "../../redux/selectors/editor";
import { EditorQueryState } from "../../redux/types";


const PROCESS_MARKDOWN_QUERY_INTERVAL = 3000;


const Home = () => {
    const [text, setText] = useState<string>("");

    const [getTask, { data: taskData, error: taskError }] = useLazyGetTaskQuery();
    const [runProcessMarkdown, { data: processMarkdownData }] = useProcessMarkdownMutation();

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
        <div className="main-container">
            <Sidebar
                onRunProcessMarkdownClick={handleRunProcessMarkdown}
                task={taskData}
            />
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
                            remarkFrontmatterFilter,
                            remarkBlockMetadataFilter,
                        ]}
                    />
                </div>
            </div>
            {editorQueryState === EditorQueryState.TaskReceived && taskData?.status !== "PENDING" && (
                <ResponseModal task={taskData!} error={taskError} />
            )}
        </div>
    )
}

export default Home;