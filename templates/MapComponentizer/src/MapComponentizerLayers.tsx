import { useContext, useState } from "react";
import {
  LayerList,
  LayerListItem,
  MlGeoJsonLayer,
  MlWmsLayer,
  Sidebar,
} from "@mapcomponents/react-maplibre";
import { MapComponentizerContext } from "./MapComponentizerContext";

const MapComponentizerLayers = () => {
  const context = useContext(MapComponentizerContext) as any;
  const [open, setOpen] = useState(true);

  return (
    <>
      <Sidebar open={open} setOpen={setOpen} name={"MapComponentizer"}>
        <LayerList>
           {context.layers &&
              context.layers.map((layer) => {
                switch(layer.type){
                  case "geojson":
                      return (
                  <LayerListItem
                    key={layer.name}
                    name={layer.name}
                    configurable={true}
                    layerComponent={
                      <MlGeoJsonLayer
                        type={layer.geomType}
                        geojson={layer.geojson}                        
                      />
                    }
                  />
                );
                case "wms":
                   return (
                  <LayerListItem
                    key={layer.name}
                    name={layer.name}
                    configurable={true}
                    layerComponent={
                      <MlWmsLayer                      
                      url={layer.url} 
                      urlParameters={layer.urlParameters}                 

                       />
                    }
                  />
                );
                }                  
               
              })}
        </LayerList>
      </Sidebar>
    </>
  );
};

export default MapComponentizerLayers;