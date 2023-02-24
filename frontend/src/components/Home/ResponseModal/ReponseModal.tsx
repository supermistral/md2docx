import { useState } from "react";
import { useDispatch } from "react-redux";
import { API_URL } from "../../../constants/api";
import { downloadFinished } from "../../../redux/slices/editorSlice";
import { TaskResponse } from "../../../redux/types";
import Modal from "../../Modal/Modal";
import "./ResponseModal.scss";


export interface ResponseModalProps {
    task: TaskResponse;
    error?: any;
}


const getErrorHeader = (errorCode?: string) => {
    switch (errorCode) {
        case "MetadataValidationError":
            return "Ошибка в блоке метаданных";
        default:
            return "Ошибка";
    }
}


const isError = (task: TaskResponse) => task.status !== 'SUCCESS';


const ResponseModal = ({ task, error }: ResponseModalProps) => {
    const [open, setOpen] = useState<boolean>(true);
    const dispatch = useDispatch();

    const closeModal = () => {
        setOpen(false);
        dispatch(downloadFinished());
    };

    return (
        <Modal open={open} onClose={closeModal}>
            {isError(task) ? (
                <div className="error">
                    <div className="error-content">
                        <div className="error-header">
                            {getErrorHeader(task.error)}
                        </div>
                        <div className="error-items">
                            {Array.isArray(task.detail) && task.detail.map((error, i) => (
                                <div key={i} className="error-item">
                                    <div className="key">{error.key}</div>
                                    <div className="message">{error.message}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            ) : (
                <div className="document">
                    <div className="document-content">
                        <div className="document-items">
                            <a href={`${API_URL}/md2docx/document/`} className="document-item">
                                <div className="label docx">docx</div>
                                <div className="download">Загрузить</div>
                            </a>
                            <a href="#" className="document-item">
                                <div className="label pdf">pdf</div>
                                <div className="download">Загрузить</div>
                            </a>
                        </div>
                    </div>
                </div>
            )}
        </Modal>
    )
}

export default ResponseModal;