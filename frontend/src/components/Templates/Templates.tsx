import { Box, Button, Collapse, IconButton, List, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { useState } from "react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { SERVER_TEMPLATES } from "../../constants/stubs";
import { TemplateDto } from "../../constants/types";

interface TemplateRowProps {
    row: TemplateDto;
}

const TemplateRow = (props: TemplateRowProps) => {
    const { row } = props;

    const [open, setOpen] = useState(false);

    const handleClick = () => setOpen(!open);

    return (
        <>
            <TableRow sx={{ "& > *": { borderBottom: "unset" } }}>
                <TableCell>
                    <IconButton
                        size="small"
                        onClick={handleClick}
                    >
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    {row.name}
                </TableCell>
                <TableCell align="right">{row.updatedAt}</TableCell>
                <TableCell align="right">{row.createdAt}</TableCell>
                <TableCell align="right">
                    <Button variant="contained">Сохранить</Button>
                </TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={5}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{ maring: 1 }}>
                            <Typography
                                variant="body2"
                                sx={{ margin: 2, whiteSpace: "pre-wrap" }}
                            >
                                <pre>{row.content}</pre>
                            </Typography>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </>
    )
}

const Templates = () => {
    const templates = SERVER_TEMPLATES;

    return (
        <Box>
            <Box>
                <Typography variant="h4" align="center">Хранилище шаблонов</Typography>
            </Box>
            <Box>
                <List
                    sx={{
                        width: "100%",
                        maxWidth: 1200,
                        bgColor: "background.paper",
                        "& > *": { margin: "1em 0" },
                    }}
                >
                </List>
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell />
                                <TableCell>Имя</TableCell>
                                <TableCell align="right">Обновлено</TableCell>
                                <TableCell align="right">Создано</TableCell>
                                <TableCell />
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {
                                templates.map((row) => (
                                    <TemplateRow key={row.id} row={row} />
                                ))
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>
        </Box>
    )
}

export default Templates;
