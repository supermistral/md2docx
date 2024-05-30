import { Avatar, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar, Typography } from "@mui/material"
import WysiwygIcon from '@mui/icons-material/Wysiwyg';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import BeenhereIcon from '@mui/icons-material/Beenhere';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import RouteLink from "../common/RouteLink";
import { useLocation, Link } from "react-router-dom";
import { PAGES, PAGE_TO_ROUTE, ROUTE_TO_PAGE } from "../../constants/routes";


const Navbar = () => {
    const location = useLocation()

    const pathname = location.pathname;
    const PageType = ROUTE_TO_PAGE[pathname] ?? null;

    const getActiveRouteItemProps = (page: PAGES) => {
        if (PageType != page) return {};
        return {
            sx: {
                background: "#eee",
                borderRight: "4px solid #888",
            },
        };
    }

    const getListItemIcon = (page: PAGES, el: JSX.Element) => {
        if (PageType != page) return el;
        return <Avatar sx={{ width: "32px", height: "32px" }}>{el}</Avatar>
    }

    return (
        <div>
            <Toolbar />
            <Divider />
            <List>
                <ListItem
                    key={"editor"}
                    disablePadding
                    {...getActiveRouteItemProps(PAGES.Editor)}
                >
                    <RouteLink to={PAGE_TO_ROUTE[PAGES.Editor]}>
                        <ListItemButton>
                            <ListItemIcon>
                                {getListItemIcon(PAGES.Editor, <WysiwygIcon />)}
                            </ListItemIcon>
                            <ListItemText primary={"Редактор"} />
                        </ListItemButton>
                    </RouteLink>
                </ListItem>
                <ListItem
                    key={"templates"}
                    disablePadding
                    {...getActiveRouteItemProps(PAGES.Templates)}
                >

                    <RouteLink to={PAGE_TO_ROUTE[PAGES.Templates]}>
                        <ListItemButton>
                            <ListItemIcon>
                                {getListItemIcon(PAGES.Templates, <FormatListBulletedIcon />)}
                            </ListItemIcon>
                            <ListItemText primary={"Шаблоны"} />
                        </ListItemButton>
                    </RouteLink>
                </ListItem>
            </List>
            <Divider />
            <ListItem key={"user-data"} sx={{ marginTop: "2em" }}>
                <ListItemText
                    primary={<Typography variant="h6">Мои данные</Typography>}
                    sx={{ textAlign: "center" }}
                />
            </ListItem>
            <List>
                <ListItem
                    key={"user-operations"}
                    disablePadding
                    {...getActiveRouteItemProps(PAGES.UserOperations)}
                >
                    <RouteLink to={PAGE_TO_ROUTE[PAGES.UserOperations]}>
                        <ListItemButton>
                            <ListItemIcon>
                                {getListItemIcon(PAGES.UserOperations, <PendingActionsIcon />)}
                            </ListItemIcon>
                            <ListItemText primary={"Операции"} />
                        </ListItemButton>
                    </RouteLink>
                </ListItem>
                <ListItem
                    key={"user-templates"}
                    disablePadding
                    {...getActiveRouteItemProps(PAGES.UserTemplates)}
                >
                    <RouteLink to={PAGE_TO_ROUTE[PAGES.UserTemplates]}>
                        <ListItemButton>
                            <ListItemIcon>
                                {getListItemIcon(PAGES.UserTemplates, <FormatListBulletedIcon />)}
                            </ListItemIcon>
                            <ListItemText primary={"Сохраненные шаблоны"} />
                        </ListItemButton>
                    </RouteLink>
                </ListItem>
                <ListItem
                    key={"user-profile"}
                    disablePadding
                    {...getActiveRouteItemProps(PAGES.UserProfile)}
                >
                     <RouteLink to={PAGE_TO_ROUTE[PAGES.UserProfile]}>
                        <ListItemButton>
                            <ListItemIcon>
                                {getListItemIcon(PAGES.UserProfile, <AccountBoxIcon />)}
                            </ListItemIcon>
                            <ListItemText primary={"Профиль"} />
                        </ListItemButton>
                    </RouteLink>
                </ListItem>
            </List>
        </div>
    )
}

export default Navbar;
