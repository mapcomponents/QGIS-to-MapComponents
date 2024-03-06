import { useContext, useState } from "react";
import {
  LayerList,
  LayerListItem,
  MlGeoJsonLayer,
  MlWmsLayer,
  Sidebar,
  useMap,
} from "@mapcomponents/react-maplibre";
import { MapComponentizerContext } from "./MapComponentizerContext";
import { getPaintProp, getprojectExtent } from "./utils/MapComponentizerUtils";

const MapComponentizerLayers = () => {
  const context = useContext(MapComponentizerContext) as any;
  const [open, setOpen] = useState(true);
  const mapHook = useMap({
		mapId: undefined,
	});

mapHook.map?.fitBounds(getprojectExtent().bbox)


  return (
    <>
      <Sidebar open={open} setOpen={setOpen} name={context.config?.projectName ?? "MapComponentizer"}>
        <LayerList>
           {context.layers &&
              context.layers.map((layer, idx) => {
                
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
                        options={{ paint: getPaintProp(layer, idx) }} 
                                           
                      />
                    }
                  />
                );
                case "wms":
                   return (
                  <LayerListItem
                    key={layer.name}
                    name={layer.name}
                    configurable={false}
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