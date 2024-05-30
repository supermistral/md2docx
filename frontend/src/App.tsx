import { Provider } from "react-redux";
import store from "./redux/store/store";
import "./index.scss";
import Skeleton from "./components/Skeleton/Skeleton";
import { StyledEngineProvider } from "@mui/material";
import { BrowserRouter } from "react-router-dom";

const App = () => {
    return (
        <div id="wrapper">
            <Provider store={store}>
                <BrowserRouter>
                    <StyledEngineProvider injectFirst>
                        <Skeleton />
                    </StyledEngineProvider>
                </BrowserRouter>
            </Provider>
        </div>
    )
}

export default App;