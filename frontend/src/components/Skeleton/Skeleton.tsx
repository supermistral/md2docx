import { Box, CssBaseline, Drawer, Toolbar } from "@mui/material";
import { useState } from "react";
import Navbar from "./Navbar";
import Editor from "../Editor/Editor";
import { Route, Routes } from "react-router-dom";
import { DRAWER_WIDTH } from "../../constants/layout";
import Header from "../Header/Header";
import { PAGES, PAGE_TO_ROUTE } from "../../constants/routes";
import Templates from "../Templates/Templates";
import UserTemplates from "../Templates/UserTemplates";
import Operations from "../Operations/Operations";

export interface SkeletonProps {}

const Skeleton = (props:  SkeletonProps) => {
    const [isClosing, setIsClosing] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    const handleSidebarToggle = () => {
        if (!isClosing) {
            setMobileOpen(!mobileOpen);
        }
    }

    const handleSidebarClose = () => {
        setIsClosing(true);
        setMobileOpen(false);
    }

    const handleSidebarTransitionEnd = () => {
        setIsClosing(false);
    }

    return (
        <Box sx={{ display: "flex" }}>
            <CssBaseline />
            <Header
                handleSidebarToggle={handleSidebarToggle}
            />
            <Box
                component="nav"
                sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
            >
                <Drawer
                    variant="temporary"
                    open={mobileOpen}
                    onTransitionEnd={handleSidebarTransitionEnd}
                    onClose={handleSidebarClose}
                    ModalProps={{
                        keepMounted: true,
                    }}
                    sx={{
                        display: { xs: "block", sm: "none" },
                        "& .MuiDrawer-paper": { boxSizing: "border-box", width: DRAWER_WIDTH },
                    }}
                >
                    <Navbar />
                </Drawer>
                <Drawer
                    variant="permanent"
                    sx={{
                        display: { xs: "none", sm: "block" },
                        "& .MuiDrawer-paper": { boxSizing: "border-box", width: DRAWER_WIDTH },
                    }}
                    open
                >
                    <Navbar />
                </Drawer>
            </Box>
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
                    maxWidth: 1200,
                    margin: "0 auto",
                }}
            >
                <Toolbar />
                <Routes>
                    <Route path={PAGE_TO_ROUTE[PAGES.Editor]} element={<Editor />} />
                    <Route path={PAGE_TO_ROUTE[PAGES.Templates]} element={<Templates />} />
                    <Route path={PAGE_TO_ROUTE[PAGES.UserOperations]} element={<Operations />} />
                    <Route path={PAGE_TO_ROUTE[PAGES.UserTemplates]} element={<UserTemplates />} />
                    <Route path={PAGE_TO_ROUTE[PAGES.UserProfile]} />
                    <Route path={PAGE_TO_ROUTE[PAGES.AuthLogin]} />
                    <Route path={PAGE_TO_ROUTE[PAGES.AuthSignup]} />
                </Routes>
            </Box>
        </Box>
    )
}

export default Skeleton;
