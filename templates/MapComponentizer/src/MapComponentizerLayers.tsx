import { useContext, useState } from "react";
import { LayerList, LayerListFolder, LayerListItem, MlGeoJsonLayer, Sidebar } from "@mapcomponents/react-maplibre";
import { MapComponentizerContext } from "./MapComponentizerContext";

const MapComponentizerLayers = () => {

    const context = useContext(MapComponentizerContext) as any;
    const [open, setOpen] = useState(true);

  return (
    <>
    <Sidebar open={open} setOpen={setOpen} name={"MapComponentizer"}>
      <LayerList>
      <LayerListFolder name={"Vector Layers"} visible={true} >
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
</LayerListFolder>
      </LayerList>
      </Sidebar>
    </>
  );
};

export default MapComponentizerLayers;
