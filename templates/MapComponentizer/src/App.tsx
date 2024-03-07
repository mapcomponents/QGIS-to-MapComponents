import "./App.css";
import { MapLibreMap, MlNavigationTools } from "@mapcomponents/react-maplibre";
import MapComponentizerLayers from "./MapComponentizerLayers";

function App() {
  return (
    <>
      <MapLibreMap
        options={{
          style: "https://wms.wheregroup.com/tileserver/style/osm-bright.json",
          zoom: 2,
        }}
        style={{ position: "absolute", top: 0, bottom: 0, left: 0, right: 0 }}
      />
<MlNavigationTools showCenterLocationButton={true} showFollowGpsButton={false}/>
     <MapComponentizerLayers />
     
    </>
  );
}

export default App;