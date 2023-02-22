import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { remarkBlockMetadataFilter, remarkFrontmatterFilter } from "../../markdown/filters";
import Sidebar from "./Sidebar/Sidebar";
import "./Home.scss";


const Home = () => {
    const [text, setText] = useState<string>("");

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(e.target.value);
    }

    return (
        <div className="main-container">
            <Sidebar />
            <div className="editor">
                <div className="editor-input">
                    <textarea className="editor-area" onChange={handleChange} />
                </div>
                <div className="editor-preview">
                    <ReactMarkdown
                        children={text}
                        className="editor-area"
                        remarkPlugins={[
                            remarkGfm,
                            remarkFrontmatterFilter,
                            remarkBlockMetadataFilter
                        ]}
                    />
                </div>
            </div>
        </div>
    )
}

export default Home;