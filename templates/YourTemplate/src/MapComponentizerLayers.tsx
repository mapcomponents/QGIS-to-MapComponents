import { useContext, useState, useEffect } from "react";
import {
  LayerList,
  LayerListItem,
  MlGeoJsonLayer,
  MlMeasureTool,
  MlWmsLayer,
  Sidebar,
  useMap,
} from "@mapcomponents/react-maplibre";
import { MapComponentizerContext } from "./MapComponentizerContext";
import {
  getLabels,
  getPaintProp,
  getprojectExtent,
} from "./utils/MapComponentizerUtils";
import MapComponentizerToolBar from "./utils/MapComponentizerToolBar";
import LayersIcon from "@mui/icons-material/Layers";
import StraightenIcon from "@mui/icons-material/Straighten";
import MlFeatureInfo from "./MlFeatureInfo";
import InfoIcon from '@mui/icons-material/Info';

const MapComponentizerLayers = () => {
  const context = useContext(MapComponentizerContext) as any;
  const [open, setOpen] = useState(true);
  const [showMeasureTool, setShowMeasureTool] = useState(false);
  const [featureInfoLayers, setFeatureInfoLayers] = useState<string[]>([]);
  const mapHook = useMap({
    mapId: undefined,
  });
  mapHook.map?.fitBounds(getprojectExtent(context.layers).bbox);

  const tools = [
    { icon: <LayersIcon />, action: () => setOpen(!open) },
    {
      icon: <StraightenIcon />,
      action: () => setShowMeasureTool(!showMeasureTool),
    },
  ];
  
  useEffect(()=>{
    context?.config?.order && setFeatureInfoLayers(context.config.order)
      }, [context.config])

  return (
    <>
      <MapComponentizerToolBar tools={tools} />
      <Sidebar
        open={open}
        setOpen={setOpen}
        name={context.config?.projectName ?? "MapComponentizer"}
      >
        <LayerList>
          {context.layers &&
            context.layers.map((layer, idx) => {
              switch (layer.type) {
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
                          layerId={layer.name}
                          options={{ paint: getPaintProp(layer, idx) }}
                          labelProp={"_"}
                          labelOptions={getLabels(layer)}
                        />
                      }
                      buttons={
                        <InfoIcon 
                        sx={{color: (theme)=> featureInfoLayers.indexOf(layer.name) !== -1
                                ? theme.palette.primary.main
                                : "lightgray"                              
                        }}
                          onClick={() => {
                            setFeatureInfoLayers((current) => {
                              const currentTmp = [...current];

                              if (current.indexOf(layer.name) !== -1) {
                                currentTmp.splice(
                                  currentTmp.indexOf(layer.name),
                                  1
                                );
                              }else{
                                currentTmp.push(layer.name)
                              }
                              return currentTmp;
                            });
                          }}
                        >
                          i
                        </InfoIcon>
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
                          urlParameters={{
                            layers: "",
                            ...layer.urlParameters,
                          }}
                        />
                      }
                    />
                  );
              }
            })}
        </LayerList>

        {showMeasureTool && <MlMeasureTool />}
        <MlFeatureInfo layers={featureInfoLayers} />
      </Sidebar>
    </>
  );
};

export default MapComponentizerLayers;
