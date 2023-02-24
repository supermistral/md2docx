import Popup from "reactjs-popup";
import "./Modal.scss";


export interface ModalProps {
    children: React.ReactNode;
    open: boolean;
    onClose: () => void;
}


const Modal = ({ children, open, onClose }: ModalProps) => {
    return (
        <Popup open={open} closeOnDocumentClick onClose={onClose}>
            <div className="modal">
                {children}
            </div>
        </Popup>
    )
}

export default Modal;