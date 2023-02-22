import { TiDocumentText } from "react-icons/ti";
import "./Header.scss";


const Header = () => {
    return (
        <header id="header">
            <div className="header-content">
                <div className="header-logo">
                    <span className="md">Md</span>
                    <span className="to">2</span>
                    <span className="docx">Docx</span>
                </div>
                <div className="header-docs">
                    <span className="icon"><TiDocumentText /></span>
                    <span className="text">Документация</span>
                </div>
            </div>
        </header>
    )
}

export default Header;