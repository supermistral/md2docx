import { Box, Button, Chip, CircularProgress, Collapse, IconButton, List, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import { useState } from "react";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import ArrowCircleDownIcon from '@mui/icons-material/ArrowCircleDown';
import { OPERATIONS } from "../../constants/stubs";
import { OperationDto } from "../../constants/types";

const getIconByOperationStatus = (status: string) => {
    if (status === "pending") {
        return <CircularProgress size={20} />
    } else if (status === "success") {
        return <Chip
            sx={{ ".MuiChip-label": { paddingLeft: 0 } }}
            icon={<CheckCircleIcon />}
            color="success"
        />
    }
    return <Chip
        sx={{ ".MuiChip-label": { paddingLeft: 0 } }}
        icon={<ErrorIcon />}
        color="error"
    />
}

interface OperationRowProps {
    row: OperationDto;
}

const OperationRow = (props: OperationRowProps) => {
    const { row } = props;

    const statusIcon = getIconByOperationStatus(row.status);

    return (
        <>
            <TableRow sx={{ "& > *": { borderBottom: "unset" } }}>
                <TableCell align="center">
                    {statusIcon}
                </TableCell>
                <TableCell align="center">
                    <Button size="small" variant="outlined" color="info" sx={{ textTransform: "lowercase"}}>
                        открыть
                    </Button>
                </TableCell>
                <TableCell align="right">{row.updatedAt}</TableCell>
                <TableCell align="right">{row.createdAt}</TableCell>
                <TableCell align="right">{row.error}</TableCell>
                <TableCell align="right">
                    {
                        row.response?.docx_file && (
                            <Button
                                startIcon={<ArrowCircleDownIcon />}
                                variant="contained"
                                sx={{ fontWeight: 500 }}
                            >
                                Docx
                            </Button>
                        )
                    }
                </TableCell>
            </TableRow>
        </>
    )
}

const Operations = () => {
    const operations = OPERATIONS;

    return (
        <Box>
            <Box>
                <Typography variant="h4" align="center">Операции</Typography>
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
                                <TableCell align="center">Статус</TableCell>
                                <TableCell align="center">Исходники</TableCell>
                                <TableCell align="right">Обновлено</TableCell>
                                <TableCell align="right">Создано</TableCell>
                                <TableCell align="right">Ошибка</TableCell>
                                <TableCell />
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {
                                operations.map((row) => (
                                    <OperationRow key={row.id} row={row} />
                                ))
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>
        </Box>
    )
}

export default Operations;
