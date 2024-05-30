import { Box, Tab, Tabs, List, ListItem, Button } from "@mui/material";
import React, { useEffect, useState } from "react";
import { isAuthorized } from "../../tools/helpers/auth";
import { SERVER_TEMPLATES, USER_TEMPLATES } from "../../constants/stubs";
import { UserTemplateDto } from "../../constants/types";


const EditorRegistryTemplateTab = () => {
}


const EditorUserTemplateTab = () => {
}


export interface EditorTemplateSelectorProps {
}


const EditorTemplateSelector = (props: EditorTemplateSelectorProps) => {
    const [value, setValue] = useState("registry");
    const [templates, setTemplates] = useState<Array<UserTemplateDto>>(SERVER_TEMPLATES);
    const authorized = isAuthorized();

    useEffect(() => {
        if (value === "registry") {
            setTemplates(SERVER_TEMPLATES);
        } else {
            setTemplates(USER_TEMPLATES);
        }
    }, [value])

    const handleChange = (event: React.SyntheticEvent, newValue: string) => {
        setValue(newValue);
    }

    return (
        <Box
            sx={{
                position: 'absolute' as 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                maxWidth: 800,
                bgcolor: 'background.paper',
                border: '2px solid #000',
                boxShadow: 24,
                pt: 2,
                px: 4,
                pb: 3,
            }}
        >
            <Tabs
                value={value}
                onChange={handleChange}
                textColor="primary"
                indicatorColor="primary"
            >
                <Tab value="registry" label="Хранилище" />
                <Tab value="user" label="Сохраненные" disabled={!authorized} />
            </Tabs>
            <Box sx={{ marginTop: "1em" }}>
                <List>
                    {
                        templates.map((template) => (
                            <ListItem key={template.id}>
                                <Button
                                    variant="outlined"
                                    fullWidth
                                    sx={{ textTransform: "none" }}
                                >
                                    {template.name}
                                </Button>
                            </ListItem>
                        ))
                    }
                </List>
            </Box>
        </Box>
    )
}

export default EditorTemplateSelector;
