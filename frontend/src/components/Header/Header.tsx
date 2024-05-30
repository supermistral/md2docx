import { AppBar, Box, Button, IconButton, MenuItem, Toolbar, Typography, Stack } from "@mui/material";
import LoginIcon from '@mui/icons-material/Login';
import { useLocation } from "react-router-dom";
import EditorNavbar from "../Editor/EditorNavbar";
import { DRAWER_WIDTH } from "../../constants/layout";
import { PAGES, PAGE_TO_ROUTE } from "../../constants/routes"
import "./Header.scss";
import RouteLink from "../common/RouteLink";

export interface HeaderProps {
    handleSidebarToggle: () => void;
}

const Header = (props: HeaderProps) => {
    const { handleSidebarToggle } = props;

    const location = useLocation();
    const isEditorEnabled = location.pathname === PAGE_TO_ROUTE[PAGES.Editor];

    return (
        <AppBar
            position="fixed"
            sx={{
                width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
                ml: { sm: `${DRAWER_WIDTH}px` },
                background: "#d0e2ff",
                color: "black",
            }}
        >
            <Toolbar sx={{ witdh: "100%" }}>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    edge="start"
                    onClick={handleSidebarToggle}
                    sx={{ mr: 2, display: { sm: "none" } }}
                >
                    <MenuItem />
                </IconButton>
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        width: "100%"
                    }}
                >
                    <Box sx={{ display: "flex" }}>
                        <Box>
                            <Typography
                                variant="h5"
                                noWrap
                                component="div"
                                sx={{ fontWeight: "800" }}
                            >
                                Md2Docx
                            </Typography>
                        </Box>
                        {
                            isEditorEnabled &&
                            <EditorNavbar />
                        }
                    </Box>
                    <Box>
                        <RouteLink to={PAGE_TO_ROUTE[PAGES.AuthLogin]}>
                            <Button variant="contained" endIcon={<LoginIcon />}>
                                Войти
                            </Button>
                        </RouteLink>
                    </Box>
                </Box>
            </Toolbar>
        </AppBar>
    )
}

export default Header;