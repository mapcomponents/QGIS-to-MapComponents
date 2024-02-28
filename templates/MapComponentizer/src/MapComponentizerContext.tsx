import React, { Dispatch, SetStateAction, useEffect, useState } from "react";

const MapComponentizerContext = React.createContext({});
const MapComponentizerProvider = MapComponentizerContext.Provider;

const MapComponentizerContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [geojsonLayers, setGeojsonLayers] = useState<any[]>([]);
  const [geojsonIndex, setGeojsonIndex] = useState<string[]>([]);
  const [wmsLayers, setWmsLayers] = useState<any[]>([]);
  const [wmsIndex, setWmsIndex] = useState<string[]>([]);
  console.log(wmsIndex)
  console.log(wmsLayers);

  const fetchIndexes = async (
    setter: Dispatch<SetStateAction<string[]>>,
    type: string
  ) => {
    const indexResponse = await fetch(`../exported/${type}/index.json`);
    const index = await indexResponse.json();
    setter(index);
  };

  const fetchLayerFiles = async (
    setter: Dispatch<SetStateAction<any[]>>,
    index: string[],
    layerType: string
  ) => {
    const filesPromises = index.map(async (layer) => {
      const fileResponse = await fetch(`../exported/${layerType}/${layer}`);
      const fileData = await fileResponse.json();
      return fileData;
    });

    try {
      const fetchedLayers = await Promise.all(filesPromises);
      setter(fetchedLayers);
    } catch (error) {
      console.error("Error fetching" + layerType + " files:", error);
    }
  };

  //fetch config objects for every layer
  useEffect(() => {
    geojsonIndex.length > 0 && fetchLayerFiles(setGeojsonLayers, geojsonIndex, "geojson");
  }, [geojsonIndex]);

  useEffect(() => {
    wmsIndex.length > 0 && fetchLayerFiles(setWmsLayers, wmsIndex, "wms");
  }, [wmsIndex]);

  //get layer lists for each layer type
  useEffect(() => {
    // Call the fetchData function when the component mounts
    fetchIndexes(setWmsIndex, "wms");
    fetchIndexes(setGeojsonIndex, "geojson");
  }, []);

  const stateProviderValue = {
    geojsonLayers,
    wmsLayers,
  };

  return (
    <MapComponentizerProvider value={stateProviderValue}>
      {children}
    </MapComponentizerProvider>
  );
};

export { MapComponentizerContext, MapComponentizerContextProvider };
