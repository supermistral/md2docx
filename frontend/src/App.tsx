import { Provider } from "react-redux";
import Header from "./components/Header/Header";
import Home from "./components/Home/Home";
import store from "./redux/store/store";
import "./index.scss";


const App = () => {
    return (
        <div id="wrapper">
            <Provider store={store}>
                <Header />
                <Home />
            </Provider>
        </div>
    )
}

export default App;