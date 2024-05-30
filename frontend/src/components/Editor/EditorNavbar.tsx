import { Box, Button, IconButton, Modal, Stack } from "@mui/material";
import PlayCircleFilledIcon from '@mui/icons-material/PlayCircleFilled';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { useState } from "react";
import EditorTemplateSelector from "./EditorTemplateSelector";

export interface EditorNavbarProps {

}

const EditorNavbar = (props: EditorNavbarProps) => {
    const [templateSelectorOpen, setTemplateSelectorOpen] = useState(false);

    const handleTemplateSelectorOpen = () => {
        setTemplateSelectorOpen(true);
    }

    const handleTemplateSelectorClose = () => {
        setTemplateSelectorOpen(false);
    }

    return (
        <Stack
            direction="row"
            spacing={2}
            sx={{ marginLeft: "1em" }}
        >
            <Box sx={{ alignContent: "center" }}>
                <Button
                    variant="contained"
                    color="success"
                    startIcon={<PlayCircleFilledIcon />}
                    sx={{
                        marginRight: "0",
                        "& .MuiButton-startIcon": { marginRight: "0" }
                    }}
                >
                </Button>
            </Box>
            <IconButton
                color="primary"
                tabIndex={-1}
                role={undefined}
                component="label"
            >
                <FileUploadIcon />
                <input
                    type="file"
                    accept="image/*"
                    style={{
                        clip: "rect(0 0 0 0)",
                        clipPath: "inset(50%)",
                        height: 1,
                        overflow: "hidden",
                        position: "absolute",
                        bottom: 0,
                        left: 0,
                        whiteSpace: "nowrap",
                        width: 1,
                    }}
                />
            </IconButton>    
            <Button
                variant="outlined"
                color="primary"
                size="small"
                onClick={handleTemplateSelectorOpen}
                sx={{ fontWeight: "600" }}
            >
                Подключить шаблон
            </Button>
            <Modal
                open={templateSelectorOpen}
                onClose={handleTemplateSelectorClose}
            >
                <EditorTemplateSelector />
            </Modal>
        </Stack>
    )
}

export default EditorNavbar;
