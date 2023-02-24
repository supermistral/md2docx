/*
    API CONSTANTS
*/


export const HOST_URL = process.env.DEBUG == "1"
    ? (process.env.HOST_URL || "localhost:3000")
    : "";


export const API_URL = `${HOST_URL}/api`;