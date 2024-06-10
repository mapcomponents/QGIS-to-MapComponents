import React from "react";
import ReactDOM from "react-dom/client";
import { MapComponentsProvider } from "@mapcomponents/react-maplibre";
import App from "./App";
import "./index.css";
import { MapComponentizerContextProvider } from "./MapComponentizerContext";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <MapComponentizerContextProvider>
      <MapComponentsProvider>
        <App />
      </MapComponentsProvider>
    </MapComponentizerContextProvider>
  </React.StrictMode>
);
