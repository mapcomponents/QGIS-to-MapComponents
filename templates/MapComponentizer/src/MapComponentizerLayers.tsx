import { useContext } from "react";
import { LayerList, LayerListItem, MlGeoJsonLayer, Sidebar } from "@mapcomponents/react-maplibre";
import { MapComponentizerContext } from "./MapComponentizerContext";

const MapComponentizerLayers = () => {
  const context = useContext(MapComponentizerContext) as any;

  console.log(context.geojsonLayers)

  return (
    <>
    <Sidebar sx={{zIndex: 1000}}>
      <LayerList>
        {context.geojsonLayers && context.geojsonLayers.map((layer)=>{
            return (
            <LayerListItem 
            key={layer.name}
            name={layer.name}
            configurable={true}
            layerComponent={
            <MlGeoJsonLayer 
            type={layer.type}
            geojson={layer.geojson}            
            /> }
            
            />)
            
        })}

      </LayerList>
      </Sidebar>
    </>
  );
};

export default MapComponentizerLayers;
