import { Link } from "@mui/material";
import React from "react";
import { Link as RouterDomLink, LinkProps } from "react-router-dom";
import { AnyProps } from "../../constants/types";

export interface RouteLinkProps extends AnyProps {}


const RouteLink = (props: RouteLinkProps) => (
    <Link
        component={RouterDomLink as React.ElementType<LinkProps>}
        underline="none"
        variant="body2"
        color="inherit"
        sx={{
            width: "100%",
        }}
        {...props}
    />
)

export default RouteLink;
