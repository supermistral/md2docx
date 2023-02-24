import { useMemo } from "react";
import { GrCirclePlay } from "react-icons/gr";
import { FiLoader } from "react-icons/fi";
import { useSelector } from "react-redux";
import { EditorQueryState, TaskResponse } from "../../../redux/types";
import "./Sidebar.scss";
import { selectEditorQueryState } from "../../../redux/selectors/editor";


export interface SidebarProps {
    onRunProcessMarkdownClick: () => void;
    task?: TaskResponse;
}


const Sidebar = ({ onRunProcessMarkdownClick, task }: SidebarProps) => {
    const editorQueryState = useSelector(selectEditorQueryState);

    const isLoading = useMemo(() => (
        (editorQueryState === EditorQueryState.ProcessingLoading ||
            editorQueryState === EditorQueryState.ProcessingCompleted) &&
        (!task || task.status === "PENDING")
    ), [editorQueryState, task]);

    const taskStatusClass = useMemo(() => {
        if (editorQueryState === EditorQueryState.ProcessingLoading) return "loading";
        else if (
            editorQueryState === EditorQueryState.ProcessingCompleted && 
            (!task || task.status === "PENDING")
        ) return "pending";
        return "";
    }, [editorQueryState, task]);

    const taskStatusText = useMemo(() => (
        taskStatusClass === "loading" ? "Загрузка" : "В обработке"
    ), [taskStatusClass]);

    return (
        <div className="sidebar">
            <div className="sidebar-content">
                <div className={`sidebar-button run-button ${taskStatusClass}`}>
                    <button onClick={onRunProcessMarkdownClick} disabled={!!taskStatusClass}>
                        <span className="icon">
                            <GrCirclePlay />
                        </span>
                    </button>
                    {isLoading && (
                        <div className="button-label">
                            <div className="text">
                                {taskStatusText}
                            </div>
                            <div className="loader">
                                <span className="icon icon-loader"><FiLoader /></span>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Sidebar;