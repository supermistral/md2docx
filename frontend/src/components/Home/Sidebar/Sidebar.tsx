import { GrCirclePlay } from "react-icons/gr";
import "./Sidebar.scss";


const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="sidebar-content">
                <button className="sidebar-button">
                    <span className="icon"><GrCirclePlay /></span>
                </button>
            </div>
        </div>
    )
}

export default Sidebar;