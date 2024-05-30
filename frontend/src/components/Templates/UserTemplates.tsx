import { Box, Button, Collapse, IconButton, List, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { useState } from "react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import EditNoteIcon from '@mui/icons-material/EditNote';
import DeleteIcon from '@mui/icons-material/Delete';
import { USER_TEMPLATES } from "../../constants/stubs";
import { UserTemplateDto } from "../../constants/types";

interface UserTemplateRowProps {
    row: UserTemplateDto;
}

const UserTemplateRow = (props: UserTemplateRowProps) => {
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
                <TableCell align="right" size="small">
                    <Button variant="outlined" startIcon={<EditNoteIcon />}>
                        Изменить
                    </Button>
                </TableCell>
                <TableCell align="center" size="small">
                    <IconButton>
                        <DeleteIcon />
                    </IconButton>
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

const UserTemplates = () => {
    const templates = USER_TEMPLATES;

    return (
        <Box>
            <Box>
                <Typography variant="h4" align="center">Сохраненные шаблоны</Typography>
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
                        <TableBody>
                            {
                                templates.map((row) => (
                                    <UserTemplateRow key={row.id} row={row} />
                                ))
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>
        </Box>
    )
}

export default UserTemplates;