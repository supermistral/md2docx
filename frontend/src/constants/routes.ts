import { Pages } from "@mui/icons-material";

export enum PAGES {
    Editor,
    Templates,
    UserOperations,
    UserTemplates,
    UserProfile,
    AuthLogin,
    AuthSignup,
}

export const ROUTE_TO_PAGE: Record<string, PAGES> = {
    "/": PAGES.Editor,
    "/templates": PAGES.Templates,
    "/user/operations": PAGES.UserOperations,
    "/user/templates": PAGES.UserTemplates,
    "/user/profile": PAGES.UserProfile,
    "/auth/login": PAGES.AuthLogin,
    "/auth/signup": PAGES.AuthSignup,
}

export const PAGE_TO_ROUTE: Record<PAGES, string> = Object.fromEntries(
    Object.entries(ROUTE_TO_PAGE).map(a => a.reverse())
);
